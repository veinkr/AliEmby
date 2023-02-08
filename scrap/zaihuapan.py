import requests
from aligo import Aligo
from bs4 import BeautifulSoup

from base import BaseScraper


class ZaihuaScraper(BaseScraper):
    base_search_url = "https://www.zaihuapan.com/?s="

    def search(self, search_key):
        results = []
        response = requests.get(self.base_search_url + search_key)
        bs_rets = BeautifulSoup(response.text, features="lxml").find_all("div", {"class": "post"})
        for bs_ret in bs_rets:
            ret = bs_ret.find("span", {"class": "post-title"}).a
            if ret.text:
                results.append(self.aligo.share_link_extract_code(ret["title"]))
        return results


if __name__ == '__main__':
    aligo = Aligo()
    for result in ZaihuaScraper(aligo).search("斗罗大陆"):
        share_token = aligo.get_share_token(result.share_id)
        aligo.share_file_save_all_to_drive(share_token = share_token)
        break
