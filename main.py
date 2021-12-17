import requests
import json
import sys
import datetime
import argparse
from PyQt5.QtWidgets import *
from api.TMDBRest import TMDBRest
from view.main_window import MainWindown


def teste_api():
    api = TMDBRest()
    now1 = datetime.datetime.now()
    print(f'now1 [{now1}]')
    resp = api.search_tvshow(query='FBI')
    now2 = datetime.datetime.now()
    print(resp)
    print(f'now1 [{now1}] now2 [{now2}] diff [{now2 - now1}]')
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--maximized', action='store_true', help='Mostrar a tela principal maximizada')
    parser.add_argument('-a', '--api', action='store_true', help='Chamar função teste_api()')
    args = parser.parse_args()

    if args.api:
        teste_api()
        sys.exit()

    app = QApplication([])
    win = MainWindown()

    if args.maximized:
        win.showMaximized()
    else:
        win.show()

    sys.exit(app.exec())
