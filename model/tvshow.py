
class TVShow:
    def __init__(self, tuple_from_db):
        self.__parse(tuple_from_db)

    def __str__(self) -> str:
        return f'id [{self.id}] Id TMDB [{self.id_tmdb}] Temp [{self.total_seasons}] ' \
               f'Nome [{self.name}] Eu [{self.eu}] Pai [{self.pai}]'

    def __parse(self, tuple_from_db):
        index = 0
        self.id = tuple_from_db[index]

        index += 1
        self.id_tmdb = tuple_from_db[index]

        index += 1
        self.name = tuple_from_db[index]

        index += 1
        self.total_seasons = tuple_from_db[index]

        index += 1
        self.eu = ''
        if tuple_from_db[index]:
            self.eu = 'Sim'

        index += 1
        self.pai = ''
        if tuple_from_db[index]:
            self.pai = 'Sim'

    def to_tuple(self):
        array = [self.id, self.id_tmdb, self.name, self.total_seasons, self.eu, self.pai]
        return tuple(array)
