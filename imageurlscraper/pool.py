import urllib3
pool = urllib3.PoolManager()


def get_site_data(url, attempt=1):
    r = pool.request('GET', url)
    if r.status == 200:
        return str(r.data)
    else:
        print("ERROR: {} for {} - Attempt #{}").format(r.status, url, attempt)
        return None


def get_site_url(url):
    """Meant for getting the redirect url."""
    r = pool.request('GET', url)
    if r.status == 200:
        return r.geturl()
    else:
        print("ERROR: {} for {}").format(r.status, url)
        return None
