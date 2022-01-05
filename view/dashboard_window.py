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
import webbrowser


class DashboardWindow(QMainWindow):
    window_closed = pyqtSignal()

    def __init__(self, parent=None, tvshow=None):
        super().__init__(parent)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.main_layout = QVBoxLayout()
        self.centralWidget.setLayout(self.main_layout)
        self.tab2_is_filtered = False

        if tvshow is None:
            return
        else:
            self.tvshow = tvshow

        self.__db = TVShowDb()
        self.__api = TMDBRest()
        self.__spacing = 30
        self.tab2_episodes_list = []
        self.tab2_episodes_list_filter = []

        self.__init_interface()

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()
        # event.ignore() # if you want the window to never be closed

    def __init_interface(self):
        self.setWindowTitle('Dashboard')
        self.resize(1200, 800)

        # label title
        self.lbl_tvshow_name = QLabel()
        self.lbl_tvshow_name.setText(self.tvshow.name)
        self.lbl_tvshow_name.setFont(QFont('Arial', 16))
        self.lbl_tvshow_name.setAlignment(QtCore.Qt.AlignCenter)

        # tabs
        self.tabbar = QTabWidget()
        self.__create_tabbar()

        #

        self.main_layout.addWidget(self.lbl_tvshow_name)
        self.main_layout.addWidget(self.tabbar)

    def __create_tabbar(self):
        self.__create_tabbar_tab1()
        self.tabbar.addTab(self.tab1, 'Informações')
        self.__create_tabbar_tab2()
        self.tabbar.addTab(self.tab2, 'Episódios')
        # self.tabbar.setCurrentIndex(1)

    def __create_tabbar_tab1(self):
        self.tab1 = QWidget()
        self.tab1_layout = QVBoxLayout()
        self.tab1_layout.setAlignment(QtCore.Qt.AlignTop)

        # update button
        row1 = QHBoxLayout()
        self.tab1_bt_update = QPushButton('Atualizar')
        self.tab1_bt_update.clicked.connect(self.__tab1_action_update)
        self.tab1_bt_open_tmdb = QPushButton('Abrir TMDB site')
        self.tab1_bt_open_tmdb.clicked.connect(self.__tab1_action_open_tmdb_site)
        row1.addWidget(self.tab1_bt_update)
        row1.addWidget(self.tab1_bt_open_tmdb)

        # labels
        self.tab1_lbl_id = QLabel()
        self.tab1_lbl_id.setFont(QFont('Arial', 12))
        self.tab1_lbl_status = QLabel()
        self.tab1_lbl_status.setFont(QFont('Arial', 12))
        self.tab1_lbl_network = QLabel()
        self.tab1_lbl_network.setFont(QFont('Arial', 12))
        self.tab1_lbl_first_air_date = QLabel()
        self.tab1_lbl_first_air_date.setFont(QFont('Arial', 12))
        self.tab1_lbl_number_of_seasons = QLabel()
        self.tab1_lbl_number_of_seasons.setFont(QFont('Arial', 12))
        self.tab1_lbl_number_of_episodes = QLabel()
        self.tab1_lbl_number_of_episodes.setFont(QFont('Arial', 12))

        # last and next episode
        row_last_next_episode = QHBoxLayout()
        self.tab1_gb_last_episode = QGroupBox('Último episódio')
        self.tab1_gb_last_episode_layout = QVBoxLayout()
        self.tab1_lbl_last_episode_air_date = QLabel()
        self.tab1_lbl_last_episode_air_date.setFont(QFont('Arial', 12))
        self.tab1_lbl_last_episode_season_episode = QLabel()
        self.tab1_lbl_last_episode_season_episode.setFont(QFont('Arial', 12))
        self.tab1_gb_last_episode_layout.addWidget(self.tab1_lbl_last_episode_air_date)
        self.tab1_gb_last_episode_layout.addWidget(self.tab1_lbl_last_episode_season_episode)
        self.tab1_gb_last_episode.setLayout(self.tab1_gb_last_episode_layout)
        row_last_next_episode.addWidget(self.tab1_gb_last_episode)
        #
        self.tab1_gb_next_episode = QGroupBox('Próximo episódio')
        self.tab1_gb_next_episode_layout = QVBoxLayout()
        self.tab1_lbl_next_episode_air_date = QLabel()
        self.tab1_lbl_next_episode_air_date.setFont(QFont('Arial', 12))
        self.tab1_lbl_next_episode_season_episode = QLabel()
        self.tab1_lbl_next_episode_season_episode.setFont(QFont('Arial', 12))
        self.tab1_gb_next_episode_layout.addWidget(self.tab1_lbl_next_episode_air_date)
        self.tab1_gb_next_episode_layout.addWidget(self.tab1_lbl_next_episode_season_episode)
        self.tab1_gb_next_episode.setLayout(self.tab1_gb_next_episode_layout)
        row_last_next_episode.addWidget(self.tab1_gb_next_episode)
        #
        self.__tab1_labels_set_text()

        # ---

        self.tab1_layout.addLayout(row1)
        self.tab1_layout.addSpacing(self.__spacing)
        self.tab1_layout.addWidget(self.tab1_lbl_id)
        self.tab1_layout.addSpacing(self.__spacing)
        self.tab1_layout.addWidget(self.tab1_lbl_status)
        self.tab1_layout.addSpacing(self.__spacing)
        self.tab1_layout.addWidget(self.tab1_lbl_network)
        self.tab1_layout.addSpacing(self.__spacing)
        self.tab1_layout.addWidget(self.tab1_lbl_first_air_date)
        self.tab1_layout.addSpacing(self.__spacing)
        self.tab1_layout.addWidget(self.tab1_lbl_number_of_seasons)
        self.tab1_layout.addWidget(self.tab1_lbl_number_of_episodes)
        self.tab1_layout.addSpacing(self.__spacing)
        self.tab1_layout.addLayout(row_last_next_episode)
        self.tab1.setLayout(self.tab1_layout)

    def __tab1_labels_set_text(self):
        self.tab1_lbl_id.setText(f'ID: {self.tvshow.id}')
        self.tab1_lbl_status.setText(f'Status: {self.tvshow.status}')
        self.tab1_lbl_network.setText(f'Emissora: {self.tvshow.network}')
        self.tab1_lbl_first_air_date.setText(f'Exibição 1º episódio: {self.tvshow.get_first_air_date()}')
        self.tab1_lbl_number_of_seasons.setText(f'Temporadas: {self.tvshow.number_of_seasons}')
        self.tab1_lbl_number_of_episodes.setText(f'Episódios: {self.tvshow.number_of_episodes}')

        self.tab1_lbl_last_episode_air_date.setText(f'Data exibição: {self.tvshow.get_last_episode_air_date()}')
        self.tab1_lbl_last_episode_season_episode.setText(f'Episódio: {self.tvshow.get_last_episode()}')

        self.tab1_lbl_next_episode_air_date.setText(f'Data exibição: {self.tvshow.get_next_episode_air_date()}')
        self.tab1_lbl_next_episode_season_episode.setText(f'Episódio: {self.tvshow.get_next_episode()}')

    def __create_tabbar_tab2(self):
        self.tab2 = QWidget()
        self.tab2_layout = QVBoxLayout()
        self.tab2_layout.setAlignment(QtCore.Qt.AlignTop)

        # init episodes button
        row_init_upd_epsodes = QHBoxLayout()
        self.tab2_bt_init_from_tmdb = QPushButton('Inicializar episódios')
        self.tab2_bt_init_from_tmdb.clicked.connect(self.__tab2_action_init_from_tmdb)
        self.tab2_bt_update_from_tmdb = QPushButton('Atualizar últimos episódios')
        self.tab2_bt_update_from_tmdb.clicked.connect(self.__tab2_action_update_episodes)
        row_init_upd_epsodes.addWidget(self.tab2_bt_init_from_tmdb)
        row_init_upd_epsodes.addWidget(self.tab2_bt_update_from_tmdb)

        # filter options
        self.tab2_gb_filter = QGroupBox('Filtro')
        self.tab2_gb_filter_layout = QVBoxLayout()
        self.tab2_bt_clear_filter = QPushButton('Limpar')
        self.tab2_bt_clear_filter.clicked.connect(self.__tab2_action_clear_filter)
        self.tab2_gb_filter_layout.addWidget(self.tab2_bt_clear_filter)
        self.tab2_label_filter_cb = QLabel("Temporadas:")
        self.tab2_cb_seasons_filter = QComboBox()
        self.tab2_cb_seasons_filter.activated.connect(self.__tab2_action_cb_filter_changed)
        # self.tab2_cb_seasons_filter.currentIndexChanged.connect(self.__tab2_action_cb_filter_changed)
        self.tab2_label_filter_cb.setBuddy(self.tab2_cb_seasons_filter)
        self.tab2_layout_filter_row_cb = QHBoxLayout()
        self.tab2_layout_filter_row_cb.addWidget(self.tab2_label_filter_cb)
        self.tab2_layout_filter_row_cb.addWidget(self.tab2_cb_seasons_filter)
        self.tab2_gb_filter_layout.addLayout(self.tab2_layout_filter_row_cb)
        self.tab2_gb_filter.setLayout(self.tab2_gb_filter_layout)

        # progress bar
        self.tab2_pbar = QProgressBar()
        self.tab2_pbar.setValue(0)

        # table
        row_table = QHBoxLayout()
        self.tab2_main_table = BTableWidget()
        self.tab2_main_table.b_set_select_row()
        self.tab2_main_table.b_hide_vertical_headers()
        header_labels = ['Temp', 'Ep', 'Exibido', 'Visto']
        self.tab2_main_table.b_set_column_header(header_labels=header_labels)
        self.tab2_main_table.horizontalHeader().setStretchLastSection(True)
        self.tab2_main_table.setMaximumWidth(550)
        self.tab2_main_table.b_set_center_content()
        row_table.addWidget(self.tab2_main_table)
        row_table.setAlignment(QtCore.Qt.AlignCenter)

        # mark as seen
        self.tab2_gb_seen = QGroupBox('Visto')
        self.tab2_gb_seen_layout = QVBoxLayout()
        row_gb_seen_1 = QHBoxLayout()
        self.tab2_bt_mark_episode_as_seen = QPushButton('Marcar episódio como visto')
        self.tab2_bt_mark_episode_as_seen.clicked.connect(self.__tab2_action_mark_episode_as_seen)
        self.tab2_bt_mark_season_as_seen = QPushButton('Marcar temporada como vista')
        self.tab2_bt_mark_season_as_seen.clicked.connect(self.__tab2_action_mark_season_as_seen)
        row_gb_seen_1.addWidget(self.tab2_bt_mark_episode_as_seen)
        row_gb_seen_1.addWidget(self.tab2_bt_mark_season_as_seen)
        row_gb_seen_2 = QHBoxLayout()
        self.tab2_bt_reset_episode_as_seen = QPushButton('Reset episódio')
        self.tab2_bt_reset_episode_as_seen.clicked.connect(self.__tab2_action_reset_episode_as_seen)
        self.tab2_bt_reset_season_as_seen = QPushButton('Reset temporada')
        self.tab2_bt_reset_season_as_seen.clicked.connect(self.__tab2_action_reset_season_as_seen)
        row_gb_seen_2.addWidget(self.tab2_bt_reset_episode_as_seen)
        row_gb_seen_2.addWidget(self.tab2_bt_reset_season_as_seen)

        self.tab2_gb_seen_layout.addLayout(row_gb_seen_1)
        self.tab2_gb_seen_layout.addLayout(row_gb_seen_2)
        self.tab2_gb_seen.setLayout(self.tab2_gb_seen_layout)

        # ---

        self.tab2_layout.addLayout(row_init_upd_epsodes)
        self.tab2_layout.addWidget(self.tab2_gb_filter)
        self.tab2_layout.addWidget(self.tab2_pbar)
        self.tab2_layout.addLayout(row_table)
        self.tab2_layout.addWidget(self.tab2_gb_seen)
        self.tab2.setLayout(self.tab2_layout)

        self.__tab2_load_episodes()

    def __tab2_load_episodes(self):
        # print('__tab2_load_episodes()')
        self.tab2_main_table.b_clear_content()

        index = self.tab2_cb_seasons_filter.currentIndex()
        val = self.tab2_cb_seasons_filter.currentText()
        self.tab2_is_filtered = True if index >= 0 else False

        lines = self.__db.select_all_episodes_by_tvshow(id=self.tvshow.id, debug=False)
        self.tab2_episodes_list = []
        seasons_list = []
        for line in lines:
            tvs = TVShowEpisodes(from_db=line)
            self.tab2_episodes_list.append(tvs)
            if tvs.season not in seasons_list:
                seasons_list.append(tvs.season)
        if not self.tab2_is_filtered:
            self.tab2_cb_seasons_filter.clear()
            self.tab2_cb_seasons_filter.addItems(map(str, seasons_list))
            self.tab2_cb_seasons_filter.setCurrentIndex(-1)

        self.tab2_episodes_list_filter = []
        if self.tab2_is_filtered:
            self.tab2_episodes_list_filter = [tvs for tvs in self.tab2_episodes_list if int(tvs.season) == int(val)]
        else:
            self.tab2_episodes_list_filter = self.tab2_episodes_list

        for tvs in self.tab2_episodes_list_filter:
            self.tab2_main_table.b_add_row(from_tuple=tvs.to_tuple_table())

        episodes_count = len(self.tab2_episodes_list_filter)
        self.tab2_pbar.setMinimum(0)
        if episodes_count != 0:
            self.tab2_pbar.setMaximum(episodes_count)
        eps_watched = 0
        for ep in self.tab2_episodes_list_filter:
            if ep.watched:
                eps_watched += 1
        self.tab2_pbar.setValue(eps_watched)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def __tab1_action_update(self):
        # print('__action_update()')
        try:
            ret = self.__api.get_tvshow_info(id=self.tvshow.id)
            # print(json.dumps(ret, indent=4, ensure_ascii=False))
            if ret['status_code'] == 200:
                self.tvshow.parse_from_json_api(json=ret['resp_json'])
                # self.tvshow.dump()
                self.__tab1_labels_set_text()
            else:
                QMessageBox.critical(self, ' ', 'Erro ao consultar série.', QMessageBox.Ok)
                return
        except:
            QMessageBox.critical(self, ' ', 'Erro ao atualizar série.', QMessageBox.Ok)
            print(traceback.format_exc())

    def __tab1_action_open_tmdb_site(self):
        # print('__action_open_tmdb_site()')
        webbrowser.open(self.tvshow.get_url_tmdb())

    def __tab2_action_init_from_tmdb(self):
        # print('__tab2_action_init_from_tmdb()')
        msg = (
            f'Deseja inicializar os episódios dessa série?' + '\n'
            f'\n'
            f'Todas as informações atuais serão perdidas.'
        )
        q = QMessageBox.question(self, ' ', msg, QMessageBox.Yes | QMessageBox.No)
        if q == QMessageBox.Yes:
            # print('yes')
            # print(self.tvshow)
            self.__db.delete_all_episodes_from_tvshow(id=self.tvshow.id)
            # self.tvshow.total_seasons = 2  # forçando pra testar
            for temp in range(1, self.tvshow.number_of_seasons + 1):
                # print(f'temp [{temp}]')
                ret = self.__api.get_tvshow_season_episodes(id=self.tvshow.id, season=temp)
                episodes_json = ret['resp_json']['episodes']
                # print(json.dumps(episodes_json, indent=4, ensure_ascii=False))

                self.episodes_list = []
                episodes_list_tuple = []
                for ep_json in episodes_json:
                    ep = TVShowEpisodes(from_json=ep_json)
                    ep.set_id(id=self.tvshow.id)
                    # print(ep)
                    if ep.air_date != '':
                        if ep.is_episode_air_date_valid(value=ep.air_date):
                            self.episodes_list.append(ep)
                            episodes_list_tuple.append(ep.to_tuple())

                self.__db.insert_episode(episodes_list_tuple)

            self.__tab2_load_episodes()
            QMessageBox.information(self, ' ', 'Inicialização realizada com sucesso.', QMessageBox.Ok)

    def __tab2_action_update_episodes(self):
        line = self.__db.select_last_episode(id=self.tvshow.id, debug=True)
        if line is None:
            msg = 'Não há episódios da série. É necessário inicializar.'
            QMessageBox.information(self, ' ', msg, QMessageBox.Ok)
            return
        tvs_db = TVShowEpisodes(from_db=line)
        ret = self.__api.get_tvshow_info(id=self.tvshow.id)
        if ret['status_code'] == 200:
            self.tvshow.parse_from_json_api(json=ret['resp_json'])
            self.tvshow.dump()
            if tvs_db.season == self.tvshow.last_episode_season_number:  # same season
                if tvs_db.episode == self.tvshow.last_episode_episode_number:
                    QMessageBox.information(self, ' ', 'Não há episódios para atualizar.', QMessageBox.Ok)
                    return
                temp = tvs_db.season
                diff_ep = self.tvshow.last_episode_episode_number - tvs_db.episode
                if diff_ep > 0:
                    print(f'diff_ep [{diff_ep}] last ep [{tvs_db.episode}]')
                    ret = self.__api.get_tvshow_season_episodes(id=self.tvshow.id, season=temp)
                    episodes_json = ret['resp_json']['episodes']
                    episodes_update = []
                    for ep_json in episodes_json:
                        ep = TVShowEpisodes(from_json=ep_json)
                        ep.set_id(id=self.tvshow.id)
                        if ep.episode > tvs_db.episode:
                            if ep.is_episode_air_date_valid(value=ep.air_date):
                                # print(ep)
                                episodes_update.append(ep.to_tuple())

                    self.__db.insert_episode(rows=episodes_update)

                    self.__tab2_load_episodes()
                    QMessageBox.information(self, ' ', 'Episódios atualizados com sucesso.', QMessageBox.Ok)
            elif self.tvshow.last_episode_season_number > tvs_db.season:  # next season
                temp = self.tvshow.last_episode_season_number
                ret = self.__api.get_tvshow_season_episodes(id=self.tvshow.id, season=temp)
                episodes_json = ret['resp_json']['episodes']
                episodes_update = []
                for ep_json in episodes_json:
                    ep = TVShowEpisodes(from_json=ep_json)
                    ep.set_id(id=self.tvshow.id)
                    if ep.is_episode_air_date_valid(value=ep.air_date):
                        # print(ep)
                        episodes_update.append(ep.to_tuple())

                self.__db.insert_episode(rows=episodes_update)

                self.__tab2_load_episodes()
                QMessageBox.information(self, ' ', 'Episódios atualizados com sucesso.', QMessageBox.Ok)

    def __tab2_action_cb_filter_changed(self):
        self.__tab2_load_episodes()

    def __tab2_action_clear_filter(self):
        self.tab2_cb_seasons_filter.setCurrentIndex(-1)
        self.__tab2_load_episodes()

    def __tab2_mark_reset_episode(self, value):
        index = self.tab2_main_table.currentRow()
        # print(f'index [{index}]')
        if index >= 0:
            if self.tab2_is_filtered:
                ep = self.tab2_episodes_list_filter[index]
            else:
                ep = self.tab2_episodes_list[index]
            # print(ep)
            self.__db.mark_reset_episode_seen(id=ep.id, season=ep.season, episode=ep.episode, value=value)
            self.__tab2_load_episodes()
        else:
            QMessageBox.information(self, ' ', 'Escolha um episódio.', QMessageBox.Ok)
            self.tab2_main_table.setFocus()

    def __tab2_action_mark_episode_as_seen(self):
        self.__tab2_mark_reset_episode(value=True)

    def __tab2_action_reset_episode_as_seen(self):
        self.__tab2_mark_reset_episode(value=False)

    def __tab2_mark_reset_season(self, value):
        index = self.tab2_cb_seasons_filter.currentIndex()
        # print(f'index [{index}]')
        if index >= 0:
            val = self.tab2_cb_seasons_filter.currentText()
            self.__db.mark_reset_season_seen(id=self.tvshow.id, season=val, value=value)
            self.__tab2_load_episodes()
        else:
            QMessageBox.information(self, ' ', 'Selecione o filtro por uma temporada.', QMessageBox.Ok)
            self.tab2_cb_seasons_filter.setFocus()

    def __tab2_action_mark_season_as_seen(self):
        self.__tab2_mark_reset_season(value=True)

    def __tab2_action_reset_season_as_seen(self):
        self.__tab2_mark_reset_season(value=False)
