from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from database.tvshow_db import TVShowDb
from model.tvshow import TVShow
from view.add_tvshow import AddTvShowWindow
from view.dashboard_window import DashboardWindow
from custom.BTableWidget import BTableWidget


class MainWindown(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.main_layout = QVBoxLayout()
        self.centralWidget.setLayout(self.main_layout)

        self.__db = TVShowDb()
        self.tvshows_list = []
        self.tvshows_list_filter = []

        self.__init_interface()
        self.__load_tbshows()
        self.__select_row_test()

    def __select_row_test(self):
        for index, tvs in enumerate(self.tvshows_list):
            # print(f'index [{index}] nome [{tvs.name}]')
            if tvs.name == 'FBI: Most Wanted':
                self.main_table.selectRow(index)

    def __init_interface(self):
        # window
        self.setWindowTitle('Séries')
        self.resize(800, 700)

        # filter
        self.gb_filter = QGroupBox('Filtro')
        self.gb_filter_layout = QHBoxLayout()
        self.rb_all = QRadioButton("Todas")
        self.rb_all.toggled.connect(self.__action_rb_all)
        self.rb_eu = QRadioButton("Eu")
        self.rb_eu.toggled.connect(self.__action_rb_eu)
        self.rb_pai = QRadioButton("Pai")
        self.rb_pai.toggled.connect(self.__action_rb_pai)
        self.gb_filter_layout.setAlignment(Qt.AlignCenter)
        self.gb_filter_layout.addWidget(self.rb_all)
        self.gb_filter_layout.addSpacing(30)
        self.gb_filter_layout.addWidget(self.rb_eu)
        self.gb_filter_layout.addSpacing(30)
        self.gb_filter_layout.addWidget(self.rb_pai)
        self.gb_filter.setLayout(self.gb_filter_layout)

        # table
        self.main_table = BTableWidget()
        self.main_table.b_hide_vertical_headers()
        self.main_table.b_set_select_row()
        header_labels = ['Id', 'Nome', 'Temporadas', 'Eu', 'Pai']
        self.main_table.b_set_column_header(header_labels=header_labels)
        self.main_table.doubleClicked.connect(self.__show_dashboard_doubleclick)

        # buttons
        self.bt_add_tvshow = QPushButton("Adicionar")
        self.bt_add_tvshow.clicked.connect(self.__add_tvshow)
        # self.bt_add_tvshow.setShortcut('Ctrl+D')
        self.bt_delete_tvshow = QPushButton("Apagar")
        self.bt_delete_tvshow.clicked.connect(self.__delete_tvshow)
        self.bt_dashboard = QPushButton('Dashboard')
        self.bt_dashboard.clicked.connect(self.__show_dashboard)
        self.row_layout1 = QHBoxLayout()
        self.row_layout1.addWidget(self.bt_add_tvshow)
        self.row_layout1.addWidget(self.bt_delete_tvshow)
        self.row_layout2 = QHBoxLayout()
        self.row_layout2.addWidget(self.bt_dashboard)

        # all
        self.main_layout.addWidget(self.gb_filter)
        self.main_layout.addWidget(self.main_table)
        self.main_layout.addLayout(self.row_layout1)
        self.main_layout.addLayout(self.row_layout2)
        self.__create_test_buttons()
        self.rb_all.setChecked(True)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def __add_tvshow(self):
        self.add_win = AddTvShowWindow()
        self.add_win.window_closed.connect(self.add_win_close_event)
        self.add_win.show()

    def __delete_tvshow(self):
        index = self.main_table.currentRow()
        # print(f'index [{index}]')
        if index >= 0:
            tvs = self.tvshows_list[index]
            q = QMessageBox.question(self, 'Apagar série', f'Tem certeza que deseja apagar a série {tvs.name}?',
                                     QMessageBox.Yes | QMessageBox.No)
            if q == QMessageBox.Yes:
                self.__db.delete_tvshow_and_episodes(id=tvs.id)
                QMessageBox.information(self, 'Apagar série', f'Série {tvs.name} apagada com sucesso.', QMessageBox.Ok)
                self.__load_tbshows()
        else:
            QMessageBox.information(self, 'Apagar série', 'Escolha uma série para apagar.', QMessageBox.Ok)
            self.main_table.setFocus()

    def __show_dashboard(self):
        index = self.main_table.currentRow()
        # print(f'index [{index}]')
        if index >= 0:
            tvs = self.tvshows_list[index]
            # print(tvs)
            self.dashboard_win = DashboardWindow(tvshow=tvs)
            self.dashboard_win.show()
        # else:
        #     print('nada sera feito...')

    def __show_dashboard_doubleclick(self, mi):
        index = mi.row()
        if index >= 0:
            tvs = self.tvshows_list[index]
            # print(tvs)
            self.dashboard_win = DashboardWindow(tvshow=tvs)
            self.dashboard_win.show()

    def add_win_close_event(self):
        self.__load_tbshows()

    def __load_tbshows(self):
        self.main_table.b_clear_content()

        lines = self.__db.select_all_tvshows()
        self.tvshows_list = []
        for line in lines:
            tvs = TVShow(line)
            self.tvshows_list.append(tvs)

        self.tvshows_list_filter = []
        for tvs in self.tvshows_list:
            if self.rb_eu.isChecked():
                if tvs.eu:
                    self.tvshows_list_filter.append(tvs)
            elif self.rb_pai.isChecked():
                if tvs.pai:
                    self.tvshows_list_filter.append(tvs)
            else:
                self.tvshows_list_filter.append(tvs)

        for tvs in self.tvshows_list_filter:
            self.main_table.b_add_row(from_tuple=tvs.to_tuple())

        self.__ajust_table_columns()

    def __ajust_table_columns(self):
        header = self.main_table.horizontalHeader()
        # id
        index = 0
        header.setSectionResizeMode(index, QHeaderView.ResizeToContents)
        # name
        index += 1
        header.setSectionResizeMode(index, QHeaderView.Stretch)
        # seasons
        index += 1
        header.setSectionResizeMode(index, QHeaderView.ResizeToContents)
        # eu
        index += 1
        header.setSectionResizeMode(index, QHeaderView.ResizeToContents)
        # pai
        index += 1
        header.setSectionResizeMode(index, QHeaderView.ResizeToContents)

    def __create_test_buttons(self):
        gb_test = QGroupBox('Test')
        gb_test_layout = QVBoxLayout()

        row_tvshow = QHBoxLayout()
        bt_reload = QPushButton('Reload')
        bt_reload.clicked.connect(self.__create_test_buttons_reload)
        bt_reset = QPushButton('Reset')
        bt_reset.clicked.connect(self.__create_test_buttons_reset)
        row_tvshow.addWidget(bt_reload)
        row_tvshow.addWidget(bt_reset)

        row_episodes = QHBoxLayout()
        bt_clear_episodes = QPushButton('Apagar todos episódios')
        bt_clear_episodes.clicked.connect(self.__create_test_buttons_clear_episodes)
        bt_reset_episodes = QPushButton('Reset episódios')
        bt_reset_episodes.clicked.connect(self.__create_test_buttons_reset_episodes)
        row_episodes.addWidget(bt_clear_episodes)
        row_episodes.addWidget(bt_reset_episodes)

        row_select = QHBoxLayout()
        bt_select_tvshow = QPushButton('Select séries')
        bt_select_tvshow.clicked.connect(self.__create_test_buttons_select_tvshows)
        bt_select_episodes = QPushButton('Select episódios')
        bt_select_episodes.clicked.connect(self.__create_test_buttons_select_episodes)
        row_select.addWidget(bt_select_tvshow)
        row_select.addWidget(bt_select_episodes)

        gb_test_layout.addLayout(row_tvshow)
        gb_test_layout.addLayout(row_episodes)
        gb_test_layout.addLayout(row_select)

        gb_test.setLayout(gb_test_layout)
        self.main_layout.addWidget(gb_test)

    def __create_test_buttons_reload(self):
        self.__load_tbshows()

    def __create_test_buttons_reset(self):
        self.__db.insert_tvshow_mock()
        self.__load_tbshows()
        QMessageBox.information(self, ' ', 'Reset das séries realizado com sucesso.', QMessageBox.Ok)

    def __create_test_buttons_clear_episodes(self):
        self.__db.delete_all_episodes()
        QMessageBox.information(self, ' ', 'Todos os episódios foram apagados.', QMessageBox.Ok)

    def __create_test_buttons_reset_episodes(self):
        self.__db.delete_all_episodes()
        self.__db.insert_episodes_mock_example()
        QMessageBox.information(self, ' ', 'Reset dos episódios realizado com sucesso.', QMessageBox.Ok)

    def __create_test_buttons_select_tvshows(self):
        self.__db.select_all_tvshows(debug=True)

    def __create_test_buttons_select_episodes(self):
        self.__db.select_all_episodes(debug=True)

    def __action_rb_all(self):
        self.__load_tbshows()

    def __action_rb_eu(self):
        self.__load_tbshows()

    def __action_rb_pai(self):
        self.__load_tbshows()
