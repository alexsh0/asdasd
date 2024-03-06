import os
import flet as ft
import pandas as pd
from flet import(ElevatedButton,
                  FilePicker,
                  FilePickerResultEvent,
                  Page,
                  Row,
                  Text,
                  RadioGroup,
                  Radio,
                  DataTable,
                  ControlEvent)


def main(page: Page):

    def setTable(e : ControlEvent):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'таблицы')
        files = [f for f in os.listdir(filename) if f.endswith('.xlsx')]

        data = pd.DataFrame()

        for file in files:
            df = pd.read_excel(os.path.join(filename, file))[1:]
            df = df.drop(columns = ['Unnamed: 3','Unnamed: 4','Unnamed: 5'])
            df.columns = ['Date','Class','FIO']
            df = df.dropna()
            data = pd.concat([data, df])

        data = data.reset_index(drop=True)
        data_columns=df.columns

    
        
        page.add(DataTable(columns=ft.DataColumn(Text(data_columns))))

        
    def setDates(path : str):
        files_buttons = []
        
        for file in os.listdir(path):
            if file.endswith(".xlsx"):
                file_path = os.path.join(path, file)
                file_name = os.path.splitext(file)[0]
                

                
                files_buttons.append(Radio(value=file_path, label=file_name))
                
        dates.content = Row(files_buttons)
        dates.on_change = setTable
        dates.update()
        
    def get_directory_result(e: FilePickerResultEvent):        
        directory_path.value = e.path
        directory_path.update()
        
        if e.path:
            setDates(e.path)
        else:
            dates.content.clean()
            dates.value = ""
            dates.update()
            
            table.rows.clear()
            table.columns.clear()
            table.update()

    get_directory_dialog = FilePicker(on_result=get_directory_result)
    directory_path = Text()
    dates=RadioGroup(content=Row())
    table=DataTable()


    page.add(get_directory_dialog)
    page.add(Row([ElevatedButton("Обновить таблицу", on_click=setTable)]))
    page.add(dates)
    page.add(table)

    page.scroll = "auto"
    page.update()
ft.app(target=main)
