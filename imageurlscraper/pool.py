import urllib3
import imageurlscraper.errorhandling as err
verbose = err.verbose
pool = urllib3.PoolManager()


def get_site_data(url, attempt=1):
    r = pool.request('GET', url)
    if r.status == 200:
        return str(r.data)
    elif r.status == 429:
        return err.StatusError(url, r.status)
    else:
        return None


def get_site_url(url):
    """Meant for getting the redirect url."""
    r = pool.request('GET', url)
    if r.status == 200:
        return r.geturl()
    elif r.status == 429 or r.status == 400:
        return err.StatusError(url, r.status)
    else:
        if verbose:
            print("ERROR: {} for {}".format(r.status, url))
        return None
