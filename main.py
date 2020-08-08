from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.button import MDRectangleFlatButton
import pandas as pd


class Example(MDApp):
    def build(self):
        DATA = pd.read_excel("downloaded_medals.xls")
        DATA = DATA.iloc[:, 1:]
        cols = DATA.columns.values
        values = DATA.values
        
        self.data_tables = MDDataTable(
            size_hint=(0.9, 0.6),
            use_pagination=True,
            column_data=[
                (col, dp(30))
                for col in cols
            ],
            row_data=values
        )
        self.data_tables.bind(on_row_press=self.on_row_press)
        self.data_tables.bind(on_check_press=self.on_check_press)

        self.button = MDRectangleFlatButton(
            pos_hint={"center_x": .5, "center_y": .5},
            text="Abrir Tabla",
            on_release=self.open_table
        )
        
        return self.button

    def open_table(self, instance):
        self.data_tables.open()

    def on_row_press(self, instance_table, instance_row):
        '''Called when a table row is clicked.'''

        print(instance_table, instance_row)

    def on_check_press(self, instance_table, current_row):
        '''Called when the check box in the table row is checked.'''

        print(instance_table, current_row)


Example().run()