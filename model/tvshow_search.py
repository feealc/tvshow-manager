from .tvshow_base import TVShowBase


class TVShowSearch(TVShowBase):
    def __init__(self, json):
        super().__init__()
        self.__json = json
        self.__parse()

    def __str__(self) -> str:
        return f'Id TMDB [{self.id}] Nome [{self.name}] First Air Date [{self.first_air_date}]'

    def __parse(self):
        self.id = self.__json['id']

        self.name = self.__json['name']

        self.first_air_date = ''
        if 'first_air_date' in self.__json:
            self.first_air_date = self.__json['first_air_date']

    def to_tuple(self):
        array = [self.name, self.get_first_air_date()]
        return tuple(array)

    def get_first_air_date(self):
        return self.format_date(value=self.first_air_date)
