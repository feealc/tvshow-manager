
class TVShowSearch:
    def __init__(self, json):
        self.__json = json
        self.__parse()

    def __str__(self) -> str:
        return f'Id TMDB [{self.id_tmdb}] Nome [{self.name}] First Air Date [{self.first_air_date}]'

    def __parse(self):
        self.id_tmdb = self.__json['id']

        self.name = self.__json['name']

        self.first_air_date = ''
        if 'first_air_date' in self.__json:
            self.first_air_date = self.__json['first_air_date']

    def to_tuple(self):
        array = [self.name, self.first_air_date]
        return tuple(array)
