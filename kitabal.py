import requests
import re
from bs4 import BeautifulSoup

SEARCH_URL = "http://kitabal.az/search.php?search="
MAX_SIMILARITY = 80

class Kitabal:
    def __init__(self):
        self.axtarilan_soz = ""
        self.parsed_html = ""
        self.price = ""

    def kitabal(self, axtarilan_soz):
        self.axtarilan_soz = axtarilan_soz
        if self.book_parsed():
            if not self.book_exists():
                return False
            else:
                return self.price


    def book_exists(self):
        all_books = self.parsed_html.find_all('div', {'class': 'col-sm-4 col-md-3'})
        for single_book in all_books:
            # bura kitab adini goturmek uchundur..
            all_h6 = single_book.find_all('h6')
            for single_h6 in all_h6:
                anchor = single_h6.find('a')
                if anchor:
                    href = anchor.get('href')
                    if  href[:8] == 'book.php':
                        book_name = anchor.get('title')
                        if self.similarity(book_name, self.axtarilan_soz) > 79:
                            # eger kitabi adi uygunluyu yuksekdirse o zaman qiymetini gotur
                            # bura kitabin qiymetini goturmek uchundur..
                            all_span = single_book.find_all('span', {'class':'amount text-primary'})
                            for single_span in all_span:
                                style = single_span.get('style','')
                                if 'text-decoration: line-through;' not in style:
                                    book_price = single_span.text
                                    search_price = r"\d+\.\d+"
                                    matches = re.findall(search_price, book_price)
                                    if matches:
                                        self.price = matches[0]
                                        return True
        return False


    def book_parsed(self):
        search_url = f"{SEARCH_URL}{self.axtarilan_soz}"
        search_html = requests.get(search_url)
        search_html.encoding = 'utf-8'
        if search_html.ok:
            # decoded_html = search_html.text.encode('utf-8').decode('utf-8')
            soup = BeautifulSoup(search_html.text, 'html.parser')
            self.parsed_html = soup
            return True
        else:
            return False


    def similarity(self, sentence1, sentence2):

        set_a = set(sentence1.lower())
        set_b = set(sentence2.lower())

        similarity = len(set_a.intersection(set_b)) / len(set_a.union(set_b)) * 100
        return similarity

    def prepare_axtarilan_soz(self, axtarilan_soz):
        return quote(axtarilan_soz.lower()).replace("i%CC%87", "i")