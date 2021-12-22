import os
import sys
from database.tvshow_db import TVShowDb


def apaga_arquivo_bd(file_name):
    if os.path.isfile(file_name):
        os.remove(file_name)


if __name__ == '__main__':
    # ep_max = 1
    # for ep in range(1,ep_max + 1):
    #     print(f'ep [{ep}]')
    # sys.exit()

    NAME_DB = 'tvshow_database.db'
    apaga_arquivo_bd(NAME_DB)

    db = TVShowDb()
    db.create_main_table()
    db.create_episode_table()
    db.list_all_tables()
    db.list_columns_from_table('tvshows')
    db.list_columns_from_table('episodes')

    db.insert_tvshow_mock()
    db.select_all_tvshows(debug=True)

    db.insert_episodes_mock_example()
    db.select_all_episodes(debug=True)

    db.delete_all()
    db.insert_tvshow_mock()
    db.insert_episodes_mock_example()
    db.select_all(debug=True)
