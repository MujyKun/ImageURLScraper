# ImageURlScraper

ImageURLScraper is a multi-site image scraper. It automatically detects which site the image is coming from and scrapes it. Only relevant images are scraped from the site and shortened links are automatically unshortened. In the case that you have many links that need to be processed, these links can be distinguished by IDs when requesting the image links.

Currently Supported Sites:  
[Asiachan](https://kpop.asiachan.com/)  - Checks all previous and next pages from it's current location.  
[Google Drive](https://drive.google.com/) - Checks all folders and grabs the first 1000 images in each folder.  
[Imgur](https://imgur.com/) - Grabs all images in a gallery.  

## Installation

In a terminal, type ``pip install imageurlscraper``.

In order to scrape images from Google Drive, the credentials are needed.  
Steps to add Google Drive credentials:

Go to https://console.developers.google.com/apis/dashboard and at the top click `+ ENABLE APIS AND SERVICES`.  
Next, search for `Google Drive API`, click it, and then click Enable.  
Select a project and then you'll be on a page with your project.  
You will see a notice: "To use this API, you may need credentials. Click 'Create credentials' to get started.".  
Go ahead and click `Create Credentials`.  
You will be requested information on the type of credentials you need.  
For the API, select `Google Drive API`, and select `Other UI` for where the API will be called from.  
For the data you will be accessing, select Application data.  
After that, create a service account in the 2nd field. Have the role as `project owner` and make sure the Key type is `JSON`.  
Get your credentials and rename the JSON file to `credentials.JSON`
Go to the project source (if you installed by pip, go to a terminal and type `pip show imageurlscraper`)  
Put the `credentials.json` in the same folder as the `main.py`.



# Sample Code
```python
"""
This sample code links directly to the main function that automatically processes the links 
and returns back a dict with IDs and their image links. The original link will not be shown,
which is why IDs are useful.
IDs are REQUIRED input alongside their links, although they are only for classifying links.
Links can have several IDs if necessary to group them together.
"""
import imageurlscraper
import pprint
pp = pprint.PrettyPrinter(indent=4)

list_of_links = [
    # the list must contain an ID along with a link
    # This ID is helpful for distinguishing certain objects or people.
    # When the dict is returned.
    [0, "https://kpop.asiachan.com/222040"],
    [1, 'https://imgur.com/a/mEUURoG'],
    [2, 'https://bit.ly/xxxxxxx'],
    [3, 'http://imgur.com/a/jRcrF'],
    # [999, 'https://drive.google.com/drive/folders/1uWIObdgq65-TmBcA8oJIWOnbuuR_H5PB']
    # This google drive folder has a lot of media and will be skipped for testing purposes. but it can support
    # google drive links like these and will go through every folder in that folder.
]


scraper = imageurlscraper.main.Scraper()
all_images = scraper.run(list_of_links)  # a dict with all the links of the images.
pp.pprint(all_images)  
```

#### Sample Output (dict)
```
{   1: [   'https://i.imgur.com/RUb6Xwl.jpg',
           ...],
    3: [   'https://i.imgur.com/ILixI73.jpg',
           ...],
    4: [   'https://i.imgur.com/X8jZOc7.jpg',
           ...],
    5: [   'https://i.imgur.com/L4SFme0.jpg',
           ...],
    6: [   'https://i.imgur.com/G2ltCDf.jpg',
           ...],
    204: [   'https://static.asiachan.com/Lee.Jueun.full.222040.jpg',
             ...]
}
```

## More Samples
```Python
import imageurlscraper
scraper = imageurlscraper.main.Scraper()

shortened_link = "https://bit.ly/311n6vP"
unshortened_link = scraper.get_main_link(shortened_link)  # Expected Output -> http://google.com/


# Want to process links one by one or do not want to use IDs?
link = "https://imgur.com/a/mEUURoG"
image_links = scraper.process_source(link)  # Expected Output -> A LIST of image links.


# Want to run from the sources directly?
images = imageurlscraper.asiachan.AsiaChan().get_all_image_links(link)  # Asiachan, expected output -> A LIST of image links.
images = imageurlscraper.googledrive.DriveScraper().get_links(link)  # Google Drive, expected output -> A LIST of image links.
images = imageurlscraper.imgur.MediaScraper().start(link)  # Imgur, expected output -> A LIST of image links.

```


