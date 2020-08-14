import imageurlscraper
import sys
err = imageurlscraper.errorhandling
sys.setrecursionlimit(15000)


class Scraper:
    def __init__(self):
        self.all_images = {}  # dict containing all image links.

    def run(self, links):
        """Main Process"""
        try:
            dic = self.check_type(links)
            for info in links:
                if dic:
                    member_links = links[info]
                    for member_link in member_links:
                        self.add_source(info, member_link)
                else:
                    member_id, link = self.get_member_and_link(info)
                    self.add_source(member_id, link)
            return self.all_images
        except Exception as e:
            if err.verbose:
                print("There was an error. Returning current list. -{}".format(e))
            return self.all_images

    def add_source(self, member_id, link):
        """Updates list of image links."""
        image_links = self.process_source(link)
        if image_links is not None:
            for image in image_links:
                if member_id not in self.all_images:
                    self.all_images[member_id] = [image]
                else:
                    self.all_images[member_id].append(image)

    @staticmethod
    def check_type(obj):
        obj_type = type(obj)
        if obj_type is dict:
            return True
        elif obj_type is list:
            return False
        else:
            raise err.WrongType(obj_type)

    @staticmethod
    def get_member_and_link(info):
        if type(info[0]) is int:
            return info[0], info[1]
        else:
            return info[1], info[0]

    @staticmethod
    def process_source(link):
        """Checks which site the link comes from and processes it."""
        link = Scraper.get_main_link(link)
        if link is not None:
            if 'kpop.asiachan.com' in link:
                return imageurlscraper.asiachan.AsiaChan().get_all_image_links(link)
            elif 'drive.google.com' in link:
                return imageurlscraper.googledrive.DriveScraper().get_links(link)
            elif 'imgur.com' in link:
                return imageurlscraper.imgur.MediaScraper().start(link)
            pass

    @staticmethod
    def get_main_link(link):
        """Transforms shortened links into their original link."""
        return imageurlscraper.pool.get_site_url(link)

