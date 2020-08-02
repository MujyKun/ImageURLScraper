verbose = False


class WrongType(Exception):
    """Input was the wrong type."""
    def __init__(self, error_type):
        super(WrongType, self).__init__("Type should be a List or Dictionary, not {}".format(error_type))


class InvalidLink(Exception):
    """Link provided was invalid. (Specifically for Imgur)"""
    def __init__(self, link):
        super(InvalidLink, self).__init__("{} is not supported by the imgur scraper. Try a gallery instead.".format(link))


class StatusError(Exception):
    """Status Codes"""
    def __init__(self, link, status_code):
        super(StatusError, self).__init__("{} returned {} when connecting to it.".format(link, status_code))


class CredentialsNeeded(Exception):
    def __init__(self):
        github_link = "https://github.com/MujyKun/ImageURLScraper#installation"
        super(CredentialsNeeded, self).__init__("credentials.json was not found. Please refer to {}".format(github_link))
