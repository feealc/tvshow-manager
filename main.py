import requests
import json
import sys
from PyQt5.QtWidgets import *
from api.TMDBRest import TMDBRest
from view.main_window import MainWindown


def teste_api():
    pass
    # api = TMDBRest()
    # api.url_add_path('tv', 4614)
    # api.url_add_param()
    # api.dump_url()
    #
    # # r = requests.get('https://api.themoviedb.org/3/tv/4614?api_key=c0d396029a40f08a4fb7a2102797c458&language=en-US')
    # r = requests.get(api.get_url())
    # # print(r.json())
    # print(json.dumps(r.json(), indent=4, ensure_ascii=False))
    # ncis = TVShow(r.json())
    # ncis.dump()


def teste_gui():
    # print('teste_gui()')
    app = QApplication([])
    win = MainWindown()
    # win.show()
    win.showMaximized()
    sys.exit(app.exec())


if __name__ == '__main__':
    # teste_api()
    teste_gui()
