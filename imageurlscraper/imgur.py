import imageurlscraper
from bs4 import BeautifulSoup as soup
import json
err = imageurlscraper.errorhandling
verbose = err.verbose


class MediaScraper:
    def __init__(self):
        self.pool = imageurlscraper.pool.pool
        self.base_url = "https://i.imgur.com/"
        self.all_links = []

    @staticmethod
    def convert_string_to_json(string):
        return json.loads(string)

    def start(self, link):
        page_html = imageurlscraper.pool.get_site_data(link)
        if page_html is not None:
            try:
                page_soup = soup(page_html, "html.parser")
                gallery_script = str((page_soup.findAll("script"))[9])
                gallery = gallery_script[gallery_script.find("image"):gallery_script.find("}}")+2]
                gallery = gallery[gallery.find("{"):len(gallery)]
                gallery = self.convert_string_to_json(gallery)
                for image in gallery['album_images']['images']:
                    image_type = image['ext']
                    image_hash = image['hash']
                    image_url = self.base_url + image_hash + image_type
                    self.all_links.append(image_url)
            except IndexError:
                if verbose:
                    raise err.InvalidLink(link)
            except json.decoder.JSONDecodeError:
                if verbose:
                    print("{} should not be processed because it does not belong to this domain.".format(link))
        return self.all_links
