from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from database.tvshow_db import TVShowDb
from model.tvshow import TVShow
from view.add_tvshow import AddTvShowWindow
from view.tvshow_info import TvShowInfoWindow


class MainWindown(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.main_layout = QVBoxLayout()
        self.centralWidget.setLayout(self.main_layout)

        self.__db = TVShowDb()
        self.tvshows_list = []

        self.__init_interface()
        self.__load_tbshows()
        self.__select_row_test()

    def __select_row_test(self):
        for index, tvs in enumerate(self.tvshows_list):
            # print(f'index [{index}] nome [{tvs.name}]')
            if tvs.name == 'FBI Most Wanted':
                self.main_table.selectRow(index)

    def __init_interface(self):
        # window
        self.setWindowTitle('Séries')
        self.resize(700, 500)

        # add button
        self.bt_add_tvshow = QPushButton("Adicionar")
        self.bt_add_tvshow.clicked.connect(self.__add_tvshow)

        # table
        self.main_table = QTableWidget()
        self.main_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        header_labels = ['Id', 'Id TMDb', 'Nome', 'Temporadas', 'Eu', 'Pai']
        self.main_table.setColumnCount(len(header_labels))
        self.main_table.setHorizontalHeaderLabels(header_labels)

        # episodes button
        self.bt_episodes = QPushButton('Episódios')
        self.bt_episodes.clicked.connect(self.__show_episodes)

        # all
        self.main_layout.addWidget(self.bt_add_tvshow)
        self.main_layout.addWidget(self.main_table)
        self.main_layout.addWidget(self.bt_episodes)
        self.__create_test_buttons()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def __add_tvshow(self):
        self.add_win = AddTvShowWindow()
        self.add_win.window_closed.connect(self.add_win_close_event)
        self.add_win.show()

    def __show_episodes(self):
        index = self.main_table.currentRow()
        # print(f'index [{index}]')
        if index >= 0:
            tvs = self.tvshows_list[index]
            # print(f'name [{tvs.name}]')
            self.info_win = TvShowInfoWindow(tvshow=tvs)
            self.info_win.show()
        # else:
        #     print('nada sera feito...')

    def add_win_close_event(self):
        self.__load_tbshows()

    def __load_tbshows(self):
        self.main_table.clearContents()
        self.main_table.setRowCount(0)

        lines = self.__db.select_all_tvshows()
        self.tvshows_list = []
        for line in lines:
            tvs = TVShow(line)
            self.tvshows_list.append(tvs)
            self.__add_table_row(tvs)
        self.__ajust_table_columns()

    def __ajust_table_columns(self):
        header = self.main_table.horizontalHeader()
        # id
        index = 0
        header.setSectionResizeMode(index, QHeaderView.ResizeToContents)
        # id tmdb
        index += 1
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

    def __add_table_row(self, tvshow):
        row = self.main_table.rowCount()
        self.main_table.setRowCount(row + 1)
        col = 0
        for item in tvshow.to_tuple():
            cell = QTableWidgetItem(str(item))
            self.main_table.setItem(row, col, cell)
            col += 1

    def __create_test_buttons(self):
        gb_test = QGroupBox('Test')
        gb_test_layout = QVBoxLayout()

        row_tvshow = QHBoxLayout()
        row_episodes = QHBoxLayout()

        bt_reload = QPushButton('Reload')
        bt_reload.clicked.connect(self.__create_test_buttons_reload)
        bt_reset = QPushButton('Reset')
        bt_reset.clicked.connect(self.__create_test_buttons_reset)
        row_tvshow.addWidget(bt_reload)
        row_tvshow.addWidget(bt_reset)

        bt_clear_episodes = QPushButton('Apagar todos episódios')
        bt_clear_episodes.clicked.connect(self.__create_test_buttons_clear_episodes)
        bt_reset_episodes = QPushButton('Reset episódios')
        bt_reset_episodes.clicked.connect(self.__create_test_buttons_reset_episodes)
        row_episodes.addWidget(bt_clear_episodes)
        row_episodes.addWidget(bt_reset_episodes)

        gb_test_layout.addLayout(row_tvshow)
        gb_test_layout.addLayout(row_episodes)

        gb_test.setLayout(gb_test_layout)
        self.main_layout.addWidget(gb_test)

    def __create_test_buttons_reload(self):
        self.__load_tbshows()

    def __create_test_buttons_reset(self):
        self.__db.reset_main_table()
        self.__db.insert_tvshow_mock()
        self.__load_tbshows()

    def __create_test_buttons_clear_episodes(self):
        self.__db.delete_all_episodes()
        QMessageBox.information(self, ' ', 'Todos os episódios foram apagados.', QMessageBox.Ok)

    def __create_test_buttons_reset_episodes(self):
        self.__db.delete_all_episodes()
        self.__db.insert_episodes_mock_example()
        QMessageBox.information(self, ' ', 'Reset dos episódios realizado com sucesso.', QMessageBox.Ok)