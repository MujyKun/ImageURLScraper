import imageurlscraper
import sys


class Scraper:
    def __init__(self):
        self.all_images = {}  # dict containing all image links.

    def run(self, links):
        """Main Process"""
        for info in links:
            member_id = info[0]
            link = info[1]
            try:
                image_links = self.process_source(link)
                for image in image_links:
                    if member_id not in self.all_images:
                        self.all_images[member_id] = [image]
                    else:
                        self.all_images[member_id].append(image)
            except Exception as e:
                pass
        return self.all_images

    @staticmethod
    def process_source(link):
        """Checks which site the link comes from and processes it."""
        link = Scraper.get_main_link(link)
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


# Instead of going straight to a database, it should have the photo link to member id in a dict and then later moved.


list_of_links = [
    # [287, 'https://drive.google.com/drive/folders/1uWIObdgq65-TmBcA8oJIWOnbuuR_H5PB'],
    [204, "https://kpop.asiachan.com/222040"],
    [1, 'https://imgur.com/a/mEUURoG'],
    [2, 'https://bit.ly/36GWd2A'],
    [3, 'http://imgur.com/a/jRcrF'],
    [4, "http://imgur.com/a/8GPIv"],
    [5, "http://imgur.com/a/nU4oI"],
    [6, "http://imgur.com/a/HwLwe"]
]
sys.setrecursionlimit(15000)
