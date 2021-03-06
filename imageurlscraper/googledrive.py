from __future__ import print_function
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import imageurlscraper.errorhandling as err
import imageurlscraper.pool as pool
import os
verbose = err.verbose


def get_drive_connection():
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    drive_service = build('drive', 'v3', credentials=creds)
    return drive_service


class DriveScraper:
    def __init__(self, drive_service = None):
        self.drive_service = drive_service or get_drive_connection()
        self.image_already_exists = []
        self.folder_already_checked = []
        self.all_links = []
        self.pool = pool.pool

    def check_if_folder(self, url):
        return (self.pool.request('GET', url)).status == 200

    def get_links(self, link):
        if self.get_folders(link):
            if verbose:
                print("Added photos from {}.".format(link))
        else:
            if verbose:
                print("> Check page source for {}. It seems no images were found.".format(link))
        return self.all_links

    def get_folders(self, url):
        try:
            url_id = self.get_id_from_folder(url)
            image_ids = self.get_ids(url_id)
            for image_id in image_ids:
                folder_url = "https://drive.google.com/drive/folders/{}".format(image_id)
                image_url = "https://drive.google.com/uc?export=view&id={}".format(image_id)
                if self.check_if_folder(folder_url):
                    self.get_folders(folder_url)
                else:
                    self.all_links.append(image_url)
            return True
        except FileNotFoundError:
            raise err.CredentialsNeeded

    @staticmethod
    def get_id_from_folder(url):
        loc = url.find("folders/")
        end_loc = url.find("?")
        if end_loc == -1:
            end_loc = len(url)
        return url[loc + 8:end_loc]

    def get_ids(self, folder_id):
        try:
            q = "'{}'".format(folder_id)
            q = "{} in parents".format(q)
            response = self.drive_service.files().list(q=q,
                                                  spaces='',
                                                  fields='nextPageToken, files(id, name)',
                                                  pageSize=1000).execute()
            return [file.get('id') for file in response.get('files', [])]
        except Exception as e:
            if err.verbose:
                print("There was an error with a specific link. Folder ID: {} -{}".format(folder_id, e))
            return []  # returning an empty list instead of None




