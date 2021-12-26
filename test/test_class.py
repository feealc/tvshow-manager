import unittest
from model.tvshow_base import TVShowBase

# RUN - python -m unittest -v
# RUN - python -m unittest -v tests.test_class


class MyTestClass(unittest.TestCase):

    # @classmethod
    # def setUpClass(cls) -> None:
    #     cls.api = TMDBRest()

    # @classmethod
    # def tearDownClass(cls) -> None:
    #     if os.path.isfile(cls.db_name):
    #         os.remove(cls.db_name)

    def test_cls_01_01_format_date_empty(self):
        tvs = TVShowBase()
        fmt = tvs.format_date(value='')
        self.assertEqual(fmt, '')

    def test_cls_01_02_format_date(self):
        date_str = '1991-03-27'
        date_str_expected = '27/mar/91'
        tvs = TVShowBase()
        fmt = tvs.format_date(value=date_str)
        self.assertEqual(fmt, date_str_expected)


if __name__ == '__main__':
    # unittest.main(failfast=True, exit=True)
    unittest.main()
