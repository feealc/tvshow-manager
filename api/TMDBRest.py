import requests


class TMDBRest:
    def __init__(self) -> None:
        self.__base_url = 'https://api.themoviedb.org/3'
        self.__url = ''
        self.__api_key = 'c0d396029a40f08a4fb7a2102797c458'
        #
        self.__headers = {}
        self.__response = None
        self.__timeout = 0.2

    def __clean(self):
        self.__url = ''
        self.__headers = {}
        self.__response = None

    def __create_headers(self):
        self.__headers = {
            'Accept': 'application/json'
        }

    def dump_url(self):
        print(f'url [{self.__url}]')

    def get_url(self):
        return self.__url

    def __handle_response(self):
        resp_dict = {
            'status_code': self.__response.status_code,
            'resp_json': self.__response.json()
        }
        return resp_dict

    def url_add_path(self, *args):
        if self.__url == '':
            self.__url = self.__base_url

        for arg in args:
            self.__url += '/' + str(arg)

    def url_add_param(self, **kwargs):
        self.__url += '?' + 'api_key' + '=' + self.__api_key
        self.__url += '&' + 'language' + '=' + 'en-US'

        for key, value in kwargs.items():
            self.__url += '&' + key + '=' + value

    def search_tvshow(self, query):
        # print('search_tvshow()...')
        self.__clean()
        self.__create_headers()
        self.url_add_path('search')
        self.url_add_path('tv')
        self.url_add_param(include_adult='false', query=query)
        # self.dump_url()

        self.__response = requests.get(self.__url, timeout=self.__timeout)
        return self.__handle_response()

    def get_tvshow_info(self, id_tmdb):
        # print('get_tvshow_info()...')
        self.__clean()
        self.__create_headers()
        self.url_add_path('tv')
        self.url_add_path(id_tmdb)
        self.url_add_param()
        # self.dump_url()

        self.__response = requests.get(self.__url, timeout=self.__timeout)
        return self.__handle_response()

    def get_tvshow_season_episodes(self, id_tmdb, season):
        # print('get_tvshow_season_episodes()...')
        self.__clean()
        self.__create_headers()
        self.url_add_path('tv')
        self.url_add_path(id_tmdb)
        self.url_add_path('season')
        self.url_add_path(season)
        self.url_add_param()
        # self.dump_url()

        self.__response = requests.get(self.__url, timeout=self.__timeout)
        return self.__handle_response()
