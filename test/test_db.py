from database.tvshow_db import TVShowDb
from model.tvshow import TVShow
from model.tvshow_episodes import TVShowEpisodes
import unittest
import os

# RUN - python -m unittest -v
# RUN - python -m unittest -v tests.test_db


class MyTestDb(unittest.TestCase):
    db_name = 'database_test.db'
    # data for testing
    tvs1_id = 123
    tvs1 = (tvs1_id, 'Teste 1', 1, True, False)
    tvs2_id = 456
    tvs2 = (tvs2_id, 'Teste 2', 2, False, True)

    @classmethod
    def setUpClass(cls) -> None:
        cls.db = TVShowDb(db_name=cls.db_name)
        cls.main_table_name = 'tvshows'
        cls.episode_table_name = 'episodes'

    @classmethod
    def tearDownClass(cls) -> None:
        if os.path.isfile(cls.db_name):
            os.remove(cls.db_name)

    def check_episode_seen(self, line, value):
        self.assertIsInstance(line, tuple)
        ep = TVShowEpisodes(from_db=line)
        self.assertIsInstance(ep.watched, bool)
        self.assertIsInstance(line[4], int)
        if value:  # seen
            self.assertTrue(ep.watched)
            self.assertEqual(ep.watched_table, '✅')
            self.assertTrue(line[4])
            self.assertEqual(line[4], 1)
        else:  # not seen
            self.assertFalse(ep.watched)
            self.assertEqual(ep.watched_table, '')
            self.assertFalse(line[4])
            self.assertEqual(line[4], 0)

    def check_season_seen(self, lines, value):
        self.assertIsInstance(lines, list)
        for line in lines:
            self.check_episode_seen(line=line, value=value)

    def test_db_00_create_db_file(self):
        if os.path.isfile(self.db_name):
            os.remove(self.db_name)
        self.db.create_db_file()
        self.assertTrue(os.path.isfile(self.db_name))

    def test_db_01_01_create_main_table(self):
        cols = ['id', 'name', 'total_seasons', 'eu', 'pai']
        self.db.create_main_table()
        cols_ret = self.db.list_columns_from_table(table_name=self.main_table_name)
        self.assertEqual(cols_ret, cols)

    def test_db_01_02_create_episodes_table(self):
        cols = ['id', 'season', 'episode', 'air_date', 'watched']
        self.db.create_episode_table()
        cols_ret = self.db.list_columns_from_table(table_name=self.episode_table_name)
        self.assertEqual(cols_ret, cols)

    def test_db_01_03_all_tables(self):
        all_tables = [(self.episode_table_name,), (self.main_table_name,)]
        all_tables_ret = self.db.list_all_tables()
        self.assertEqual(all_tables_ret, all_tables)

    def test_db_02_01_insert_tvshow(self):
        self.db.insert_tvshow(*self.tvs1)
        self.db.insert_tvshow(*self.tvs2)
        lines = self.db.select_all_tvshows()
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0], self.tvs1)
        self.assertEqual(lines[1], self.tvs2)

    def test_db_02_02_insert_episode(self):
        self.db.insert_episode_mock(id=self.tvs1_id, season=1, episode_max=3, air_date=None, watched=False)
        self.db.insert_episode_mock(id=self.tvs2_id, season=1, episode_max=2, air_date=None, watched=False)
        lines = self.db.select_all_episodes()
        self.assertEqual(len(lines), 5)

    def test_db_03_01_select_all_tvshows(self):
        lines = self.db.select_all_tvshows()
        self.assertEqual(len(lines), 2)
        # eu
        tvs_eu = TVShow(tuple_from_db=lines[0])
        self.assertEqual(tvs_eu.id, self.tvs1[0])
        self.assertEqual(tvs_eu.name, self.tvs1[1])
        self.assertEqual(tvs_eu.number_of_seasons, self.tvs1[2])
        self.assertEqual(tvs_eu.eu, self.tvs1[3])
        self.assertEqual(tvs_eu.eu_desc, 'Sim')
        self.assertEqual(tvs_eu.pai, self.tvs1[4])
        self.assertEqual(tvs_eu.pai_desc, '')
        # pai
        tvs_pai = TVShow(tuple_from_db=lines[1])
        self.assertEqual(tvs_pai.id, self.tvs2[0])
        self.assertEqual(tvs_pai.name, self.tvs2[1])
        self.assertEqual(tvs_pai.number_of_seasons, self.tvs2[2])
        self.assertEqual(tvs_pai.eu, self.tvs2[3])
        self.assertEqual(tvs_pai.eu_desc, '')
        self.assertEqual(tvs_pai.pai, self.tvs2[4])
        self.assertEqual(tvs_pai.pai_desc, 'Sim')

    def test_db_03_02_select_all_tvshows(self):
        lines = self.db.select_all_episodes()
        self.assertEqual(len(lines), 5)

    def test_db_03_03_select_episode_by_tvshow(self):
        lines = self.db.select_all_episodes_by_tvshow(id=self.tvs1_id)
        self.assertEqual(len(lines), 3)
        ep_cls = TVShowEpisodes(from_db=lines[0])
        self.assertEqual(ep_cls.id, self.tvs1_id)
        self.assertEqual(ep_cls.season, 1)
        self.assertEqual(ep_cls.episode, 1)
        self.assertEqual(ep_cls.air_date, '')
        self.assertFalse(ep_cls.watched)

    def test_db_04_01_mark_episode_seen(self):
        line = self.db.select_episode(id=self.tvs1_id, season=1, episode=1)
        self.check_episode_seen(line=line, value=False)
        self.db.mark_reset_episode_seen(id=self.tvs1_id, season=1, episode=1, value=True)
        self.assertEqual(self.db.get_row_count(), 1)
        line2 = self.db.select_episode(id=self.tvs1_id, season=1, episode=1)
        self.check_episode_seen(line=line2, value=True)

    def test_db_04_02_reset_episode_seen(self):
        line = self.db.select_episode(id=self.tvs1_id, season=1, episode=1)
        self.check_episode_seen(line=line, value=True)
        self.db.mark_reset_episode_seen(id=self.tvs1_id, season=1, episode=1, value=False)
        self.assertEqual(self.db.get_row_count(), 1)
        line2 = self.db.select_episode(id=self.tvs1_id, season=1, episode=1)
        self.check_episode_seen(line=line2, value=False)

    def test_db_04_03_mark_season_seen(self):
        lines = self.db.select_episodes_from_season(id=self.tvs2_id, season=1)
        self.check_season_seen(lines=lines, value=False)
        self.db.mark_reset_season_seen(id=self.tvs2_id, season=1, value=True)
        self.assertEqual(self.db.get_row_count(), 2)
        lines2 = self.db.select_episodes_from_season(id=self.tvs2_id, season=1)
        self.check_season_seen(lines=lines2, value=True)

    def test_db_04_04_reset_season_seen(self):
        lines = self.db.select_episodes_from_season(id=self.tvs2_id, season=1)
        self.check_season_seen(lines=lines, value=True)
        self.db.mark_reset_season_seen(id=self.tvs2_id, season=1, value=False)
        self.assertEqual(self.db.get_row_count(), 2)
        lines2 = self.db.select_episodes_from_season(id=self.tvs2_id, season=1)
        self.check_season_seen(lines=lines2, value=False)

    def test_db_05_01_delete_episode_by_tvshow(self):
        lines = self.db.select_all_episodes_by_tvshow(id=self.tvs2_id)
        self.assertEqual(len(lines), 2)
        self.db.delete_all_episodes_from_tvshow(id=self.tvs2_id)
        lines = self.db.select_all_episodes_by_tvshow(id=self.tvs2_id)
        self.assertEqual(len(lines), 0)

    def test_db_05_02_delete_all_episodes(self):
        lines = self.db.select_all_episodes()
        self.assertEqual(len(lines), 3)
        self.db.delete_all_episodes()
        lines = self.db.select_all_episodes()
        self.assertEqual(len(lines), 0)

    def test_db_05_03_delete_all_tvshow(self):
        lines = self.db.select_all_tvshows()
        self.assertEqual(len(lines), 2)
        self.db.delete_all_tvshows()
        lines = self.db.select_all_tvshows()
        self.assertEqual(len(lines), 0)


if __name__ == '__main__':
    # unittest.main(failfast=True, exit=True)
    unittest.main()
