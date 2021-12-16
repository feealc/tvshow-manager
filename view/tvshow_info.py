from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from api.TMDBRest import TMDBRest
from model.tvshow_episodes import TVShowEpisodes
from database.tvshow_db import TVShowDb
from custom.BTableWidget import BTableWidget
import json
import traceback


class TvShowInfoWindow(QMainWindow):
    window_closed = pyqtSignal()

    def __init__(self, parent=None, tvshow=None):
        super().__init__(parent)
        # print('TvShowInfoWindow class')
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.main_layout = QVBoxLayout()
        self.centralWidget.setLayout(self.main_layout)
        self.is_filtered = False

        if tvshow is None:
            return
        self.tvshow = tvshow
        self.__db = TVShowDb()
        self.__api = TMDBRest()
        # print(self.tvshow)

        self.episodes_list = []
        self.episodes_list_filter = []
        self.__init_interface()
        self.__load_episodes()

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()
        # event.ignore() # if you want the window to never be closed

    def __init_interface(self):
        self.setWindowTitle('Série Info')
        self.resize(800, 800)

        self.label_name_tvshow = QLabel()
        self.label_name_tvshow.setText(self.tvshow.name)
        self.label_name_tvshow.setFont(QFont('Arial', 16))
        self.label_name_tvshow.setAlignment(QtCore.Qt.AlignCenter)

        self.bt_init_from_tmdb = QPushButton('Inicializar episódios')
        self.bt_init_from_tmdb.clicked.connect(self.init_from_tmdb)
        self.layout_bts = QHBoxLayout()
        self.layout_bts.addWidget(self.bt_init_from_tmdb)
        self.gb_bts = QGroupBox()
        self.gb_bts.setLayout(self.layout_bts)

        # filter
        self.gb_filter = QGroupBox('Filtro')
        self.layout_filter_main = QVBoxLayout()
        self.bt_clear_filter = QPushButton('Limpar')
        self.bt_clear_filter.clicked.connect(self.clear_filter)
        self.layout_filter_main.addWidget(self.bt_clear_filter)
        self.label_filter_cb = QLabel("Temporadas:")
        self.cb_seasons_filter = QComboBox()
        self.cb_seasons_filter.activated.connect(self.cb_filter_changed)
        # self.cb_seasons_filter.currentIndexChanged.connect(self.cb_filter_changed)
        self.label_filter_cb.setBuddy(self.cb_seasons_filter)
        self.layout_filter_row_cb = QHBoxLayout()
        self.layout_filter_row_cb.addWidget(self.label_filter_cb)
        self.layout_filter_row_cb.addWidget(self.cb_seasons_filter)
        self.layout_filter_main.addLayout(self.layout_filter_row_cb)
        self.gb_filter.setLayout(self.layout_filter_main)

        # table
        self.main_table = BTableWidget()
        self.main_table.b_set_select_row()
        self.main_table.b_hide_vertical_headers()
        header_labels = ['Temp', 'Ep', 'Exibido', 'Visto']
        self.main_table.b_set_column_header(header_labels=header_labels)
        self.main_table.horizontalHeader().setStretchLastSection(True)

        # mark as seen
        self.gb_seen = QGroupBox('Visto')
        self.gb_seen_layout = QHBoxLayout()
        self.bt_mark_episode_as_seen = QPushButton('Marcar como visto')
        self.bt_mark_episode_as_seen.clicked.connect(self.mark_episode_as_seen)
        self.bt_mark_season_as_seen = QPushButton('Marcar temporada como vista')
        self.bt_mark_season_as_seen.clicked.connect(self.mark_season_as_seen)
        self.gb_seen_layout.addWidget(self.bt_mark_episode_as_seen)
        self.gb_seen_layout.addWidget(self.bt_mark_season_as_seen)
        self.gb_seen.setLayout(self.gb_seen_layout)

        # self.bt_save = QPushButton('Salvar')
        # self.bt_save.clicked.connect(self.save_add_tvshow)

        #

        self.main_layout.addWidget(self.label_name_tvshow)
        self.main_layout.addWidget(self.gb_bts)
        self.main_layout.addWidget(self.gb_filter)
        self.main_layout.addWidget(self.main_table)
        self.main_layout.addWidget(self.gb_seen)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def __load_episodes(self):
        self.main_table.b_clear_content()

        index = self.cb_seasons_filter.currentIndex()
        val = self.cb_seasons_filter.currentText()
        self.is_filtered = True if index >= 0 else False
        print(f'__load_episodes() - cbox temp - index [{index}] val [{val}] is_filtered [{self.is_filtered}]')

        lines = self.__db.select_all_episodes_by_tvshow(tvshow=self.tvshow, debug=False)
        self.episodes_list = []
        seasons_list = []
        for line in lines:
            tvs = TVShowEpisodes(from_db=line)
            self.episodes_list.append(tvs)
            if tvs.season not in seasons_list:
                seasons_list.append(tvs.season)
        if not self.is_filtered:
            self.cb_seasons_filter.clear()
            self.cb_seasons_filter.addItems(map(str, seasons_list))
            self.cb_seasons_filter.setCurrentIndex(-1)

        self.episodes_list_filter = []
        if self.is_filtered:
            self.episodes_list_filter = [tvs for tvs in self.episodes_list if int(tvs.season) == int(val)]
        else:
            self.episodes_list_filter = self.episodes_list

        for tvs in self.episodes_list_filter:
            self.main_table.b_add_row(from_tuple=tvs.to_tuple_table())

    def init_from_tmdb(self):
        # print('init_from_tmdb()')
        msg = (
            f'Deseja inicializar os episódios dessa série?' + '\n'
            f'\n'
            f'Todas as informações atuais serão perdidas.'
        )
        q = QMessageBox.question(self, ' ', msg, QMessageBox.Yes | QMessageBox.No)
        if q == QMessageBox.Yes:
            # print('yes')
            # print(self.tvshow)
            self.__db.delete_all_episodes_from_tvshow(self.tvshow.id_tmdb)
            # self.tvshow.total_seasons = 2  # forçando pra testar
            for temp in range(1, self.tvshow.total_seasons + 1):
                # print(f'temp [{temp}]')
                ret = self.__api.get_tvshow_season_episodes(id_tmdb=self.tvshow.id_tmdb, season=temp)
                episodes_json = ret['resp_json']['episodes']
                # print(json.dumps(episodes_json, indent=4, ensure_ascii=False))

                self.episodes_list = []
                episodes_list_tuple = []
                for ep_json in episodes_json:
                    ep = TVShowEpisodes(from_json=ep_json)
                    ep.set_id_tmdb(self.tvshow.id_tmdb)
                    # print(ep)
                    if ep.air_date != '':
                        # adicionar apenas episodio com data menor/igual a corrente
                        self.episodes_list.append(ep)
                        episodes_list_tuple.append(ep.to_tuple())

                self.__db.insert_episode(episodes_list_tuple)

            self.__load_episodes()

            QMessageBox.information(self, ' ', 'Inicialização realizada com sucesso.', QMessageBox.Ok)

    def cb_filter_changed(self):
        self.__load_episodes()

    def clear_filter(self):
        self.cb_seasons_filter.setCurrentIndex(-1)
        self.__load_episodes()

    def mark_episode_as_seen(self):
        # print('mark_as_seen()')
        index = self.main_table.currentRow()
        # print(f'index [{index}]')
        if index >= 0:
            ep = self.episodes_list[index]
            # print(ep)
            self.__db.mark_episode_seen(id_tmdb=ep.id_tmdb, season=ep.season, episode=ep.episode)
            self.__load_episodes()
        else:
            QMessageBox.information(self, ' ', 'Escolha um episódio.', QMessageBox.Ok)
            self.main_table.setFocus()

    def mark_season_as_seen(self):
        print('mark_season_as_seen()')
        index = self.cb_seasons_filter.currentIndex()
        print(f'index [{index}]')
        if index >= 0:
            val = self.cb_seasons_filter.currentText()
            self.__db.mark_season_seen(id_tmdb=self.tvshow.id_tmdb, season=val)
            self.__load_episodes()
        else:
            QMessageBox.information(self, ' ', 'Selecione o filtro por uma temporada.', QMessageBox.Ok)
            self.cb_seasons_filter.setFocus()
