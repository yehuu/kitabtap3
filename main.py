from kivy.app import App
from axtar import Kitab
from Custom_Layouts import BgBoxLayout
from alinino import Alinino
from kitabal import Kitabal
from bookzone import Bookzone
from kitabevim import Kitabevim

# global_axtarilan_soz = ""

kitab = Kitab()
alinino = Alinino()
kitabal = Kitabal()
bookzone = Bookzone()
kitabevim = Kitabevim()

class Interface(BgBoxLayout):
    def axtar(self):
        # global global_axtarilan_soz
        axtarilan_soz = self.ids.kitab_adi.text


        # Libraffda axtarilir..
        result = kitab.libraff(axtarilan_soz)
        if result:
            self.ids.libraff.text = f"{result} azn"
        else:
            self.ids.libraff.text = "tapılmadı"

        if self.ids.libraff.text:
            # Alininoda axtarilir..
            result_ali = alinino.alinino(axtarilan_soz)
            if result_ali:
                self.ids.alinino.text = f"{result_ali} azn"
            else:
                self.ids.alinino.text = "tapılmadı"

        if self.ids.alinino.text:
            # Kitabalda axtarilir..
            result_kitabal = kitabal.kitabal(axtarilan_soz)
            if result_kitabal:
                self.ids.kitabal.text = f"{result_kitabal} azn"
            else:
                self.ids.kitabal.text = "tapılmadı"


        if self.ids.kitabal.text:
            # Bookzone axtarilir..
            result_bookzone = bookzone.bookzone(axtarilan_soz)
            if result_bookzone:
                self.ids.bookzone.text = f"{result_bookzone} azn"
            else:
                self.ids.bookzone.text = "tapılmadı"

        if self.ids.bookzone.text:
            # Kitabevim axtarilir..
            result_kitabevim = kitabevim.kitabevim(axtarilan_soz)
            if result_kitabevim:
                self.ids.kitabevim.text = f"{result_kitabevim} azn"
            else:
                self.ids.kitabevim.text = "tapılmadı"


class LayoutsApp(App):
    pass

LayoutsApp().run()