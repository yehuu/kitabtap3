import requests
from bs4 import BeautifulSoup

LIBRAFF_URL = "https://www.libraff.az/?match=all&subcats=Y&pcode_from_q=Y&pshort=Y&pfull=Y&pname=Y&pkeywords=Y&search_performed=Y&dispatch=products.search&sl=az&q="
MAX_SIMILARITY = 80

class Kitab:
    def __init__(self):
        self.axtarilan_soz = ""
        self.parsed_html = ""
        self.price = ""

    def libraff(self, axtarilan_soz):
        self.axtarilan_soz = axtarilan_soz
        if self.libraff_parsed():
            if not self.book_exists():
                return False
            else:
                return self.price


    def book_exists(self):
        axtarishda = self.parsed_html.find('div', {'class': 'ty-no-items cm-pagination-container'})
        if axtarishda != None:
            return False
        stokda = self.parsed_html.find_all("div", {'class': 'ty-column4'})
        for element in stokda:
            stock_is_empty = element.find_all('span', {'class': 'ty-qty-out-of-stock ty-control-group__item'})

            find_book_name = element.find_all('a', {'class': 'product-title'})
            find_book_price = element.find_all('span', {'class': 'ty-price-num'})
            if find_book_name:
                book_name = find_book_name[0].text.lower()
            else:
                return False
            if find_book_price:
                book_price = find_book_price[0].text
            if not stock_is_empty:
                print(book_name)
                similarity = self.similarity(book_name, self.axtarilan_soz)
                if similarity > MAX_SIMILARITY:
                    self.price = book_price
                    return True
        return False


    def libraff_parsed(self):
        libraff_url = f"{LIBRAFF_URL}{self.axtarilan_soz}"
        libraff_html = requests.get(libraff_url)
        libraff_html.encoding = 'utf-8'
        if libraff_html.ok:
            soup = BeautifulSoup(libraff_html.text, 'html.parser')
            self.parsed_html = soup
            return True
        else:
            return False





    def similarity(self, sentence1, sentence2):
        print("calculate_cosine_similarity funksiyasinin ichindeyem")
        set_a = set(sentence1.lower())
        set_b = set(sentence2.lower())

        similarity = len(set_a.intersection(set_b)) / len(set_a.union(set_b)) * 100
        return similarity


# https://alinino.az/search.json?q=kimyag%C9%99r