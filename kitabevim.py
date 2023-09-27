from urllib.parse import quote
import requests
from bs4 import BeautifulSoup
import json
import re



SEARCH_URL = "https://kitabevim.az/wp-admin/admin-ajax.php"
MAX_SIMILARITY = 80

class Kitabevim:
    def __init__(self):
        self.axtarilan_soz = ""
        self.parsed_html = ""
        self.price = ""

    def kitabevim(self, axtarilan_soz):
        self.axtarilan_soz = axtarilan_soz
        if self.book_parsed():
            if not self.book_exists():
                return False
            else:
                return self.price


    def book_exists(self):
        not_found = self.parsed_html.find('p')
        if not_found:
            if "tapılmadı" in not_found.text:
                print("Not found")
                return False
        all_books = self.parsed_html.find_all('li')
        for single_book in all_books:
            book_name = single_book.find('span', {'class':'hightlight'})
            if book_name:
                similarity = self.similarity(book_name.text, self.axtarilan_soz)
                if similarity > MAX_SIMILARITY:
                    all_prices = single_book.find_all('span', {'class':'woocommerce-Price-amount amount'})
                    cheap_price = ''
                    for single_price in all_prices:
                        single_price_pattern = f"\d+\.\d+"
                        filtered_price = re.findall(single_price_pattern, single_price.text)
                        if cheap_price:
                            if float(filtered_price[0]) < cheap_price:
                                self.price = filtered_price[0]
                            else:
                                self.price = cheap_price
                        else:
                            self.price = filtered_price[0]
                        return True
        return False


    def book_parsed(self):
        search_url = f"{SEARCH_URL}"
        data = {'action': 'mymedi_ajax_search', 'category': '', 'search_string': f'{self.axtarilan_soz}'}
        search_html = requests.post(search_url, data=data)
        search_html.encoding = 'utf-8'
        if search_html.ok:
            json_data = json.loads(search_html.text)
            pretty_json = json.dumps(json_data, indent=4)
            soup = BeautifulSoup(json_data["html"], 'html.parser')
            self.parsed_html = soup
            return True
        else:
            return False


    def similarity(self, sentence1, sentence2):
        print(sentence1)
        print(sentence2)
        if sentence1:
            set_a = set(sentence1.lower())
            set_b = set(sentence2.lower())

            similarity = len(set_a.intersection(set_b)) / len(set_a.union(set_b)) * 100
        else:
            similarity = 0
        return similarity


    def prepare_axtarilan_soz(self):
        # ancaq parsed funksiyasinda istifade olunur..URL uchun hazirlayir
        return quote(self.axtarilan_soz.lower()).replace("i%CC%87", "i")