from urllib.parse import quote
import requests
from bs4 import BeautifulSoup


SEARCH_URL = "https://www.bookzone.az/arama?filter_name="
MAX_SIMILARITY = 80

class Bookzone:
    def __init__(self):
        self.axtarilan_soz = ""
        self.parsed_html = ""
        self.price = ""

    def bookzone(self, axtarilan_soz):
        self.axtarilan_soz = axtarilan_soz
        if self.book_parsed():
            if not self.book_exists():
                return False
            else:
                return self.price


    def book_exists(self):
        not_found = self.parsed_html.find_all('div', {'class': 'emptytext uk-alert'})
        if not_found:
            return False
        all_books = self.parsed_html.find_all('div', {'class':'uk-panel uk-panel-box'})
        for single_book in all_books:
            # print(single_book)
            book_name = single_book.find_all('a', {'class':'prd-name'})
            for single_book_name in book_name:
                book_name = single_book_name.text.strip()
                pass
            if book_name:
                if self.similarity(book_name, self.axtarilan_soz) > MAX_SIMILARITY:
                    pure_price = single_book.find_all('span', {'class':'pure-price'})
                    if pure_price:
                        self.price = pure_price[0].text.split(' ')[0]
                        return True
                    else:
                        new_price = single_book.find_all('span', {'class': 'price-new'})
                        self.price = new_price[0].text.split(' ')[0]
                        return True
        return False


    def book_parsed(self):
        search_url = f"{SEARCH_URL}{self.prepare_axtarilan_soz()}"
        search_html = requests.get(search_url)
        search_html.encoding = 'utf-8'
        if search_html.ok:
            soup = BeautifulSoup(search_html.text, 'html.parser')
            self.parsed_html = soup
            # print(self.parsed_html)
            return True
        else:
            return False


    def similarity(self, sentence1, sentence2):

        set_a = set(sentence1.lower())
        set_b = set(sentence2.lower())

        similarity = len(set_a.intersection(set_b)) / len(set_a.union(set_b)) * 100
        return similarity
        return 5

    def prepare_axtarilan_soz(self):
        # ancaq parsed funksiyasinda istifade olunur..URL uchun hazirlayir
        return quote(self.axtarilan_soz.lower()).replace("i%CC%87", "i")