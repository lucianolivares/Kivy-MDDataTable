from kivy.metrics import dp
from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDRectangleFlatButton
import pandas as pd

import threading
from kivy.clock import Clock, mainthread

Builder.load_string("""
<RootLayout>:

    MDLabel:
        pos_hint: {"center_x": .5, "top": .9}
        size_hint: .9, .1
        color: 0, 0, 0, 1
        text: "MDDataTable"
    
    MDFlatButton:
        text: "Actualizar Tabla"
        pos_hint: {"center_x": .5, "top": .2}
        on_release: root.start_second_thread()


"""
)

class RootLayout(MDFloatLayout):
    stop = threading.Event()

    def start_second_thread(self):
        threading.Thread(target=self.charge_data).start()

    def charge_data(self):
        Clock.schedule_once(self.start_test, 5)

    def start_test(self, *args):
        DATA = pd.read_excel("downloaded_medals.xls")
        DATA = DATA.iloc[:, 1:]
        cols = DATA.columns.values
        values = DATA.values
        self.update_table(cols, values)

    @mainthread
    def update_table(self, cols, values):
        self.data_table = None

        self.data_table = MDDataTable(
            size_hint=(0.9, 0.6),
            use_pagination=True,
            column_data=[(col, dp(30)) for col in cols],
            row_data=values
        )
        self.data_table.open()




class Example(MDApp):
    def on_stop(self):
        self.root.stop.set()

    def build(self):
        return RootLayout()


Example().run()