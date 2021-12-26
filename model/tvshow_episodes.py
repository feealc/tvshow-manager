from .tvshow_base import TVShowBase


class TVShowEpisodes(TVShowBase):
    def __init__(self, from_db=None, from_json=None):
        super().__init__()
        if from_db is not None:
            self.__parse_from_tuple(from_db)
        if from_json is not None:
            self.__parse_from_json(from_json)

    def __str__(self) -> str:
        return f'id [{self.id}] season [{self.season}] episode [{self.episode}] ' \
               f'air_date [{self.air_date}] watched [{self.watched}]'

    def __parse_from_tuple(self, tuple_from_db):
        index = 0
        self.id = tuple_from_db[index]

        index += 1
        self.season = int(tuple_from_db[index])

        index += 1
        self.episode = int(tuple_from_db[index])

        index += 1
        self.air_date = tuple_from_db[index]
        self.__treat_air_date()

        index += 1
        self.watched = bool(tuple_from_db[index])
        self.__treat_watched()

    def __parse_from_json(self, json_from_api):
        self.id = 0

        self.season = json_from_api['season_number']

        self.episode = json_from_api['episode_number']

        self.air_date = json_from_api['air_date']

        self.watched = False

    def set_id(self, id):
        self.id = id

    def to_tuple_table(self):
        array = [self.season, self.episode, self.get_air_date(), self.watched_table]
        return tuple(array)

    def to_tuple(self):
        array = [self.id, self.season, self.episode, self.air_date, self.watched]
        return tuple(array)

    def get_air_date(self):
        return self.format_date(value=self.air_date)

    def __treat_air_date(self):
        if self.air_date is None:
            self.air_date = ''

    def __treat_watched(self):
        if self.watched:
            self.watched_table = '✅'
        else:
            self.watched_table = ''
