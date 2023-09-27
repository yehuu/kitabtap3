import requests

ALININO_URL = "https://alinino.az/search.json?q="

class Alinino:
    def __init__(self):
        self.axtarilan_soz = ""
        self.parsed_html = ""
        self.price = ""

    def alinino(self, axtarilan_soz):
        self.axtarilan_soz = axtarilan_soz
        is_parsed = self.parse_alinino()
        if is_parsed:
            if not self.book_exists():
                return False
            else:
                return self.price
    def book_exists(self):
        # print(self.parsed_html)
        # print(self.parsed_html[0]['variants'][0]['quantity'])
        for single_book in self.parsed_html:
            similarity = self.similarity(self.axtarilan_soz, single_book['title'])
            if similarity > 79:
                if single_book['variants'][0]['quantity']  >   0:
                    self.price  =   single_book['variants'][0]['price']
                    return True
        return False

    def parse_alinino(self):
        alinino_url = f"{ALININO_URL}{self.axtarilan_soz}"
        alinino_response = requests.get(alinino_url)

        if alinino_response.ok:
            json_data = alinino_response.json()  # Parse the JSON data
            self.parsed_html = json_data  # Store the parsed JSON data
            return True
        return False


    def similarity(self, sentence1, sentence2):
        set_a = set(sentence1.lower())
        set_b = set(sentence2.lower())
        similarity = len(set_a.intersection(set_b)) / len(set_a.union(set_b)) * 100
        return similarity


