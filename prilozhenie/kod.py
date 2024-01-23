import os
import flet
import pandas as pd
from flet import (ElevatedButton,
                  FilePicker,
                  FilePickerResultEvent,
                  Page,
                  Row,
                  Text,
                  RadioGroup,
                  Radio,
                  DataTable,
                  ControlEvent)
from simpledt import DataFrame


def main(page: Page):

    def setTable(e : ControlEvent):
        data = pd.read_excel(e.data)
        data_frame = DataFrame(data)  
        table.rows = data_frame.datatable.rows
        table.columns = data_frame.datatable.columns
        table.update()
        
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
    dates = RadioGroup(content=Row())
    table = DataTable()



    page.add(get_directory_dialog)
    page.add(Row([ElevatedButton("Открыть папку с файлами", on_click=lambda _: get_directory_dialog.get_directory_path()), directory_path]))
    page.add(dates)
    page.add(table)

    
    page.update()
flet.app(target=main)