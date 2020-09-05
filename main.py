import json
import threading

import requests
from kivy.clock import mainthread
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.floatlayout import MDFloatLayout


Builder.load_string("""
<RootLayout>:
    table_box: table_box

    MDLabel:
        pos_hint: {"center_x": .5, "top": 1}
        size_hint: .9, .1
        color: 0, 0, 0, 1
        text: "Viajes Disponibles"
        halign: "center"
        font_style: "H3"

    MDBoxLayout:
        id: table_box
        pos_hint: {"center_x": .5, "top": .8}
        size_hint: .9, .6
        
    MDFillRoundFlatButton:
        text: "Actualizar Tabla"
        pos_hint: {"center_x": .5, "top": .1}
        on_release: root.start_second_thread()


"""
)

TRIPS_SELECTED = []

class RootLayout(MDFloatLayout):
    stop = threading.Event()

    def start_second_thread(self):
        threading.Thread(target=self.load_data).start()

    def load_data(self, *args):
        if TRIPS_SELECTED:
            for n_trip in TRIPS_SELECTED:
                post_request = requests.delete(f'https://remasterautostop-fc4ec.firebaseio.com/trips_available/{n_trip}.json')

        get_request = requests.get(f'https://remasterautostop-fc4ec.firebaseio.com/trips_available.json')
        trips_data = json.loads(get_request.content.decode())

        count = 0
        cols = ["Viaje"]
        values = []

        for trip, data in trips_data.items():
            lista = []
            lista.append(trip)
            for key, info in data.items():
                lista.append(info)
                
                if count == 0:
                    cols.append(key)
            count += 1
            values.append(lista)

        self.update_table(cols, values)

    def on_check_press(self, instance_table, current_row):
        '''Called when the check box in the table row is checked.'''
        if current_row[0] in TRIPS_SELECTED:
            TRIPS_SELECTED.remove(current_row[0])
        else:
            TRIPS_SELECTED.append(current_row[0])


    @mainthread
    def update_table(self, cols, values):
        self.table_box.clear_widgets()

        self.data_table = MDDataTable(
                column_data=[(col, dp(40)) for col in cols],
                row_data=values,
                check=True
                )

        self.data_table.bind(on_check_press=self.on_check_press)

        self.table_box.add_widget(self.data_table)


class Example(MDApp):
    def on_stop(self):
        self.root.stop.set()

    def on_start(self):
        self.root.start_second_thread()

    def build(self):
        return RootLayout()


Example().run()
