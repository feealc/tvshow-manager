import unittest
# import os
from api.TMDBRest import TMDBRest
from model.tvshow_search import TVShowSearch
from model.tvshow import TVShow
from datetime import datetime

# RUN - python -m unittest -v
# RUN - python -m unittest -v tests.test_api


class MyTestApi(unittest.TestCase):
    key_status_code = 'status_code'
    key_resp_json = 'resp_json'
    id_castle = 1419
    tvs1 = (id_castle, 'Castle', 8, True, False)

    @classmethod
    def setUpClass(cls) -> None:
        cls.api = TMDBRest()

    # @classmethod
    # def tearDownClass(cls) -> None:
    #     if os.path.isfile(cls.db_name):
    #         os.remove(cls.db_name)

    @staticmethod
    def get_current_date_int():
        return int(datetime.now().strftime('%Y%m%d'))

    def check_resp_dict(self, resp):
        self.assertIsInstance(resp, dict)
        self.assertTrue(self.key_status_code in resp)
        self.assertTrue(self.key_resp_json in resp)
        self.assertEqual(resp[self.key_status_code], 200)
        self.assertIsInstance(resp[self.key_resp_json], dict)

    def test_api_01_search(self):
        resp = self.api.search_tvshow(query='NCIS')
        self.check_resp_dict(resp=resp)
        result_list = resp[self.key_resp_json]['results']
        for result in result_list:
            tvs = TVShowSearch(result)
            self.assertEqual(tvs.id, result['id'])
            self.assertEqual(tvs.name, result['name'])
            self.assertEqual(tvs.first_air_date, result['first_air_date'])

    def test_api_02_update(self):
        resp = self.api.get_tvshow_info(id=self.id_castle)
        self.check_resp_dict(resp=resp)
        tvs_json = resp[self.key_resp_json]
        tvs = TVShow(tuple_from_db=self.tvs1)
        tvs.parse_from_json_api(json=tvs_json)
        self.assertEqual(tvs.first_air_date, tvs_json['first_air_date'])
        self.assertEqual(tvs.homepage, tvs_json['homepage'])
        self.assertEqual(tvs.number_of_seasons, tvs_json['number_of_seasons'])
        self.assertEqual(tvs.number_of_episodes, tvs_json['number_of_episodes'])
        self.assertEqual(tvs.network, tvs_json['networks'][0]['name'])
        self.assertEqual(tvs.status, tvs_json['status'])


if __name__ == '__main__':
    # unittest.main(failfast=True, exit=True)
    unittest.main()
