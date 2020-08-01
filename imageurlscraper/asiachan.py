import imageurlscraper


class AsiaChan:
    def __init__(self):
        self.original_url = ""
        self.first_run = 1
        self.current_post = ""
        self.post_number = 0
        self.current_image = ""
        self.all_image_links = []

    def get_all_image_links(self, link):
        self.start(link)
        return self.all_image_links

    def start(self, url, mode=0):  # 0 for previous, 1 for next
        if self.first_run == 1:
            self.original_url = url
            self.first_run = 0
        html = imageurlscraper.pool.get_site_data(url)
        if mode == 0:
            previous = self.get_previous_page(html)
            current_link = self.get_static_image(html)
            self.all_image_links.append(current_link)
            if previous is not None:
                self.start(previous)
            else:
                self.start(self.original_url, 1)
        else:
            next = self.get_next_page(html)
            current_link = self.get_static_image(html)
            if current_link is not None:
                self.all_image_links.append(current_link)
            if next is not None:
                self.start(next, 1)

    def get_previous_page(self, html):
        start_pos = html.find('rel="prev"')
        if start_pos == -1:
            return None
        else:
            end_pos = start_pos - 2
            self.check_if_post_number(html, end_pos, 1, 0)
            # print("https://kpop.asiachan.com/{} - previous".format(self.post_number))
            return "https://kpop.asiachan.com/{}".format(self.post_number)

    def get_next_page(self, html):
        start_pos = html.find('rel="next"')
        if start_pos == -1:
            return None
        else:

            end_pos = start_pos - 2
            self.check_if_post_number(html, end_pos, 9, 1)
            # print("https://kpop.asiachan.com/{} - next".format(self.post_number))
            return "https://kpop.asiachan.com/{}".format(self.post_number)

    def get_static_image(self, html):
        base_url = "https://static.asiachan.com/"
        start_pos = html.find('"contentUrl":')
        if start_pos == -1:
            return None
        else:
            self.check_if_image(html, start_pos+43, 10)
            return "{}{}".format(base_url, self.current_image)

    def check_if_image(self, html, start_pos, counter):
        link = (html[start_pos:start_pos+counter])
        if link[len(link)-1] == '"':
            self.current_image = link[0:len(link)-1]
        else:
            self.check_if_image(html, start_pos, counter+1)

    def check_if_post_number(self, html, end_pos, counter, mode): # mode at 1 = next, mode at 0 = previous
        if mode == 0:
            perfect_sixth = (html[end_pos-counter:end_pos])
            if perfect_sixth[0] == '/':
                self.post_number = perfect_sixth[1:end_pos]
            else:
                self.check_if_post_number(html, end_pos, counter+1, 0)
        if mode == 1:
            perfect_sixth = (html[end_pos-counter:end_pos])
            if perfect_sixth[0] == '/':
                self.post_number = perfect_sixth[1:end_pos]
            else:
                self.check_if_post_number(html, end_pos, counter-1, 1)


"""
Once having next page, only check for next page.
Once having previous page, only check for previous page.
"""

