from .tvshow_base import TVShowBase


class TVShow(TVShowBase):
    def __init__(self, tuple_from_db):
        super().__init__()
        # init var
        self.id = ''
        self.name = ''
        self.eu = ''
        self.pai = ''
        self.first_air_date = ''
        self.homepage = ''
        self.last_episode_air_date = ''
        self.last_episode_episode_number = ''
        self.last_episode_season_number = ''
        self.next_episode_air_date = ''
        self.next_episode_episode_number = ''
        self.next_episode_season_number = ''
        self.number_of_seasons = ''
        self.number_of_episodes = ''
        self.network = ''
        self.status = ''

        self.__parse(tuple_from_db)

    def __str__(self) -> str:
        return f'id [{self.id}] Temp [{self.number_of_seasons}] ' \
               f'Nome [{self.name}] Eu [{self.eu}] Pai [{self.pai}]'

    def __parse(self, tuple_from_db):
        index = 0
        self.id = tuple_from_db[index]

        index += 1
        self.name = tuple_from_db[index]

        index += 1
        self.number_of_seasons = tuple_from_db[index]

        index += 1
        self.eu = bool(tuple_from_db[index])
        self.eu_desc = ''
        if self.eu:
            self.eu_desc = 'Sim'

        index += 1
        self.pai = bool(tuple_from_db[index])
        self.pai_desc = ''
        if self.pai:
            self.pai_desc = 'Sim'

    def parse_from_json_api(self, json):
        key = 'first_air_date'
        if key in json:
            self.first_air_date = json[key]

        key = 'homepage'
        if key in json:
            self.homepage = json[key]

        key = 'last_episode_to_air'
        if key in json:
            aux = json[key]
            if aux is not None:
                key2 = 'air_date'
                if key2 in aux:
                    self.last_episode_air_date = aux[key2]
                key2 = 'episode_number'
                if key2 in aux:
                    self.last_episode_episode_number = aux[key2]
                key2 = 'season_number'
                if key2 in aux:
                    self.last_episode_season_number = aux[key2]

        key = 'next_episode_to_air'
        if key in json:
            aux = json[key]
            if aux is not None:
                key2 = 'air_date'
                if key2 in aux:
                    self.next_episode_air_date = aux[key2]
                key2 = 'episode_number'
                if key2 in aux:
                    self.next_episode_episode_number = aux[key2]
                key2 = 'season_number'
                if key2 in aux:
                    self.next_episode_season_number = aux[key2]

        key = 'number_of_seasons'
        if key in json:
            self.number_of_seasons = json[key]

        key = 'number_of_episodes'
        if key in json:
            self.number_of_episodes = json[key]

        key = 'networks'
        if key in json:
            self.network = json[key][0]['name']

        key = 'status'
        if key in json:
            self.status = json[key]

    def get_last_episode(self):
        if self.last_episode_season_number != '' and self.last_episode_episode_number != '':
            return f'{self.last_episode_season_number}x{self.last_episode_episode_number}'
        else:
            return ''

    def get_next_episode(self):
        if self.next_episode_season_number != '' and self.next_episode_episode_number != '':
            return f'{self.next_episode_season_number}x{self.next_episode_episode_number}'
        else:
            return ''

    def get_last_episode_air_date(self):
        return self.format_date(value=self.last_episode_air_date)

    def get_next_episode_air_date(self):
        return self.format_date(value=self.next_episode_air_date)

    def get_first_air_date(self):
        return self.format_date(value=self.first_air_date)

    def dump(self):
        msg = (
            f'first_air_date [{self.first_air_date}]' + '\n'
            f'homepage [{self.homepage}]' + '\n'
            f'last_episode_air_date [{self.last_episode_air_date}] '
            f'last_episode_season_number [{self.last_episode_season_number}] '
            f'last_episode_episode_number [{self.last_episode_episode_number}]' + '\n'
            f'next_episode_air_date [{self.next_episode_air_date}] '
            f'next_episode_season_number [{self.next_episode_season_number}] '
            f'next_episode_episode_number [{self.next_episode_episode_number}]' + '\n'
            f'number_of_episodes [{self.number_of_episodes}] number_of_seasons [{self.number_of_seasons}]' + '\n'
            f'network [{self.network}]' + '\n'
            f'status [{self.status}]' + '\n'
        )
        print(msg)

    def to_tuple(self):
        array = [self.id, self.name, self.number_of_seasons, self.eu_desc, self.pai_desc]
        return tuple(array)

    def get_url_tmdb(self):
        return f'https://www.themoviedb.org/tv/{self.id}'
