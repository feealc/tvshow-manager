
class TVShowEpisodes:
    def __init__(self, from_db=None, from_json=None):
        if from_db is not None:
            self.__parse_from_tuple(from_db)
        if from_json is not None:
            self.__parse_from_json(from_json)

    def __str__(self) -> str:
        return f'Id TMDB [{self.id_tmdb}] temp [{self.season}] ep [{self.episode}] ' \
               f'air date [{self.air_date}] watched [{self.watched}]'

    def __parse_from_tuple(self, tuple_from_db):
        index = 0
        self.id_tmdb = tuple_from_db[index]

        index += 1
        self.season = tuple_from_db[index]

        index += 1
        self.episode = tuple_from_db[index]

        index += 1
        self.air_date = tuple_from_db[index]
        self.__treat_air_date()

        index += 1
        self.watched = tuple_from_db[index]
        self.__treat_watched()

    def __parse_from_json(self, json_from_api):
        self.id_tmdb = 0

        self.season = json_from_api['season_number']

        self.episode = json_from_api['episode_number']

        self.air_date = json_from_api['air_date']

        self.watched = False

    def set_id_tmdb(self, id_tmdb):
        self.id_tmdb = id_tmdb

    def to_tuple_table(self):
        array = [self.season, self.episode, self.air_date, self.watched]
        return tuple(array)

    def to_tuple(self):
        array = [self.id_tmdb, self.season, self.episode, self.air_date, self.watched]
        return tuple(array)

    def __treat_air_date(self):
        if self.air_date is None:
            self.air_date = ''

    def __treat_watched(self):
        if self.watched:
            self.watched = '✅'
        else:
            self.watched = ''
