# from model.tvshow_search import TVShowSearch
import sqlite3
# import random


class TVShowDb:
    def __init__(self):
        self.db_name = 'tvshow_database.db'
        self.__conn = None
        self.__cursor = None
        self.main_table_name = 'tvshows'
        self.episode_table_name = 'episodes'
        # try:
        #     self.__connect()
        #     self.dump()
        #     self.__close_conn()
        #     self.dump()
        # except sqlite3.Error:
        #     print("Erro ao abrir banco")

    def dump(self):
        print(f'conn [{self.__conn}]')
        print(f'cursor [{self.__cursor}]')

    def __connect(self):
        self.__conn = sqlite3.connect(self.db_name)
        self.__cursor = self.__conn.cursor()

    def __commit(self):
        if self.__conn:
            self.__conn.commit()

    def __close_conn(self):
        if self.__conn:
            self.__conn.close()

    def list_all_tables(self):
        # listando as tabelas do bd
        self.__connect()
        self.__cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' ORDER BY name
        """)
        print('Tabelas:')
        for tabela in self.__cursor.fetchall():
            print('> [%s]' % tabela)
        self.__close_conn()

    def list_columns_from_table(self, table_name):
        self.__connect()
        self.__cursor.execute('PRAGMA table_info({})'.format(table_name))
        cols = [tupla[1] for tupla in self.__cursor.fetchall()]
        print(f'Colunas tabela {table_name}: {cols}')
        self.__close_conn()

    def create_main_table(self):
        self.__connect()
        self.__cursor.execute(f"""
        CREATE TABLE {self.main_table_name} (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                id_tmdb INTEGER NOT NULL,
                name TEXT NOT NULL,
                total_seasons INTEGER NOT NULL,
                eu BOOLEAN,
                pai BOOLEAN
        );
        """)
        self.__commit()
        self.__close_conn()

    def create_episode_table(self):
        self.__connect()
        self.__cursor.execute(f"""
        CREATE TABLE {self.episode_table_name} (
                id_tmdb INTEGER NOT NULL,
                season INTEGER NOT NULL,
                episode INTEGER NOT NULL,
                air_date DATE,
                watched BOOLEAN,
                PRIMARY KEY(id_tmdb,season,episode)
        );
        """)
        self.__commit()
        self.__close_conn()

    def reset_main_table(self):
        self.delete_all_tvshows()
        self.__connect()
        self.__cursor.execute(f"""
        UPDATE sqlite_sequence SET seq = 0 WHERE name = '{self.main_table_name}';
        """)
        self.__commit()
        self.__close_conn()

    def insert_tvshow(self, *args):
        # 1 - id_tmdb
        # 2 - name
        # 3 - season
        # 4 - eu
        # 5 - pai
        insert_list = [arg for arg in args]
        self.__connect()
        self.__cursor.execute(f"""
        INSERT INTO {self.main_table_name} (id_tmdb, name, total_seasons, eu, pai)
        VALUES (?,?,?,?,?)
        """, tuple(insert_list))
        self.__commit()
        self.__close_conn()

    def insert_tvshow_mock(self):
        rows = [
            # eu
            (79744, 'The Rookie', 4, True, False),
            (71728, 'Young Sheldon', 5, True, False),
            # pai
            (80748, 'FBI', 4, False, True),
            (94372, 'FBI: Most Wanted', 3, False, True),
            (4614, 'NCIS', 19, False, True),
            (17610, 'NCIS: Los Angeles', 13, False, True),
        ]
        self.__connect()
        self.__cursor.executemany(f"""
        INSERT INTO {self.main_table_name} (id_tmdb, name, total_seasons, eu, pai)
        VALUES (?,?,?,?,?)
        """, rows)
        self.__commit()
        self.__close_conn()

    def insert_episode(self, rows):
        self.__connect()
        self.__cursor.executemany(f"""
        INSERT INTO {self.episode_table_name} (id_tmdb, season, episode, air_date, watched)
        VALUES (?,?,?,?,?)
        """, rows)
        self.__commit()
        self.__close_conn()

    def insert_episode_mock(self, id_tmdb, season, episode_max, air_date=None, watched=False):
        rows = []
        for ep in range(1, episode_max + 1):
            # if not watched:
            #     watched = random.randint(0, 1)
            #     print(f'watched random [{watched}]')
            tup = (id_tmdb, season, ep, air_date, watched)
            rows.append(tup)

        self.__connect()
        self.__cursor.executemany(f"""
        INSERT INTO {self.episode_table_name} (id_tmdb, season, episode, air_date, watched)
        VALUES (?,?,?,?,?)
        """, rows)
        self.__commit()
        self.__close_conn()

    def insert_episodes_mock_example(self):
        # fbi
        self.insert_episode_mock(id_tmdb=80748, season=1, episode_max=22)
        self.insert_episode_mock(id_tmdb=80748, season=2, episode_max=19)
        self.insert_episode_mock(id_tmdb=80748, season=3, episode_max=15)
        self.insert_episode_mock(id_tmdb=80748, season=4, episode_max=7)

        # the rookie
        self.insert_episode_mock(id_tmdb=79744, season=1, episode_max=20)
        self.insert_episode_mock(id_tmdb=79744, season=2, episode_max=20)
        self.insert_episode_mock(id_tmdb=79744, season=3, episode_max=14)
        self.insert_episode_mock(id_tmdb=79744, season=4, episode_max=7)

    def select_all_tvshows(self, debug=False):
        self.__connect()
        self.__cursor.execute(f"""
        SELECT * FROM {self.main_table_name} ORDER BY name;
        """)
        lines = self.__cursor.fetchall()
        if debug:
            for line in lines:
                print(line)
        self.__close_conn()
        return lines

    def select_all_episodes(self, debug=False):
        self.__connect()
        self.__cursor.execute(f"""
        SELECT * FROM {self.episode_table_name} ORDER BY id_tmdb,season,episode;
        """)
        lines = self.__cursor.fetchall()
        if debug:
            for line in lines:
                print(line)
        self.__close_conn()
        return lines

    def select_all_episodes_by_tvshow(self, tvshow, debug=False):
        self.__connect()
        self.__cursor.execute(f"""
        SELECT * FROM {self.episode_table_name} WHERE id_tmdb = {tvshow.id_tmdb} ORDER BY season,episode;
        """)
        lines = self.__cursor.fetchall()
        if debug:
            for line in lines:
                print(line)
        self.__close_conn()
        return lines

    def delete_all_tvshows(self):
        self.__connect()
        self.__cursor.execute(f"""
        DELETE FROM {self.main_table_name};
        """)
        self.__commit()
        self.__close_conn()

    def delete_all_episodes(self):
        self.__connect()
        self.__cursor.execute(f"""
        DELETE FROM {self.episode_table_name};
        """)
        self.__commit()
        self.__close_conn()

    def delete_all_episodes_from_tvshow(self, id_tmdb):
        self.__connect()
        self.__cursor.execute(f"""
        DELETE FROM {self.episode_table_name} WHERE id_tmdb = {id_tmdb};
        """)
        self.__commit()
        self.__close_conn()

    def delete_tvshow_and_episodes(self, id_tmdb):
        self.__connect()
        self.__cursor.execute(f"""
        DELETE FROM {self.episode_table_name} WHERE id_tmdb = {id_tmdb};
        """)
        self.__cursor.execute(f"""
        DELETE FROM {self.main_table_name} WHERE id_tmdb = {id_tmdb};
        """)
        self.__commit()
        self.__close_conn()

    def mark_episode_seen(self, id_tmdb, season, episode):
        self.__connect()
        self.__cursor.execute(f"""
        UPDATE {self.episode_table_name}
        SET
        watched = 1
        WHERE
        id_tmdb = {id_tmdb} AND season = {season} AND episode = {episode};
        """)
        self.__commit()
        self.__close_conn()
