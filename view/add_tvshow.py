from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from api.TMDBRest import TMDBRest
from model.tvshow_search import TVShowSearch
from database.tvshow_db import TVShowDb
import json
import traceback


class AddTvShowWindow(QMainWindow):
    window_closed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.main_layout = QVBoxLayout()
        self.centralWidget.setLayout(self.main_layout)

        self.__init_interface()
        #
        self.__api = TMDBRest()
        self.__db = TVShowDb()
        self.tvshow_search_list = []

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()
        # event.ignore() # if you want the window to never be closed

    def __init_interface(self):
        # window
        self.setWindowTitle('Adicionar série')
        self.resize(500, 400)

        self.label_name = QLabel()
        self.label_name.setText("Nome série: ")
        self.textbox_name = QLineEdit()
        self.textbox_name.setText('NCIS')
        self.button_search = QPushButton('Buscar')
        self.button_search.clicked.connect(self.search_tvshow)

        self.layout_row = QHBoxLayout()
        self.layout_row.addWidget(self.label_name)
        self.layout_row.addWidget(self.textbox_name)
        self.layout_row.addWidget(self.button_search)

        self.table_result = QTableWidget()
        self.table_result.setSelectionBehavior(QAbstractItemView.SelectRows)

        header_labels = ['Nome', 'Data 1º episódio']
        self.table_result.setColumnCount(len(header_labels))
        self.table_result.setHorizontalHeaderLabels(header_labels)
        self.table_result.horizontalHeader().setStretchLastSection(True)

        self.rb_eu = QRadioButton("Eu")
        self.rb_pai = QRadioButton("Pai")
        self.rb_eu.setChecked(True)
        self.layout_rb = QHBoxLayout()
        self.layout_rb.setAlignment(QtCore.Qt.AlignCenter)
        self.layout_rb.addWidget(self.rb_eu)
        self.layout_rb.addWidget(self.rb_pai)
        self.groupbox_rb = QGroupBox()
        self.groupbox_rb.setLayout(self.layout_rb)

        self.bt_save = QPushButton('Salvar')
        self.bt_save.clicked.connect(self.save_add_tvshow)

        # 

        self.main_layout.addLayout(self.layout_row)
        self.main_layout.addWidget(self.table_result)
        # self.main_layout.addLayout(self.layout_rb)
        self.main_layout.addWidget(self.groupbox_rb)
        self.main_layout.addWidget(self.bt_save)
        # self.setLayout(self.layout_main)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def search_tvshow(self):
        tvshow_name_search = self.textbox_name.text()

        if len(tvshow_name_search) == 0:
            QMessageBox.information(self, ' ', 'Nenhuma série foi preenchida para busca.', QMessageBox.Ok)
            self.textbox_name.setFocus()
            return

        try:
            resp = self.__api.search_tvshow(query=tvshow_name_search)
            # print(json.dumps(resp, indent=4, ensure_ascii=False))

            if resp['status_code'] == 200:
                r = resp['resp_json']
                # print(json.dumps(r, indent=4, ensure_ascii=False))
                result_list = r['results']
                # print(json.dumps(result_list, indent=4, ensure_ascii=False))

                self.tvshow_search_list = []
                for result in result_list:
                    # print(json.dumps(result, indent=4, ensure_ascii=False))
                    tvs = TVShowSearch(result)
                    # print(tvs)
                    self.tvshow_search_list.append(tvs)
            else:
                QMessageBox.critical(self, ' ', 'Erro ao consultar api.', QMessageBox.Ok)
                return
        except:
            QMessageBox.critical(self, ' ', 'Erro ao pesquisar série.', QMessageBox.Ok)
            print(traceback.format_exc())
            return

        self.table_result.clearContents()
        self.table_result.setRowCount(0)

        self.tvshow_search_list.sort(key=lambda x: x.name)
        for tvs in self.tvshow_search_list:
            # print(tvs)
            self.__add_table_row(tvs)
        self.__ajust_table_columns()

    def __add_table_row(self, tvshow):
        row = self.table_result.rowCount()
        self.table_result.setRowCount(row + 1)
        col = 0
        for item in tvshow.to_tuple():
            cell = QTableWidgetItem(str(item))
            # cell.setFlags(QtCore.Qt.ItemIsEditable)
            # cell.setFlags(QtCore.Qt.ItemIsEnabled)
            # cell.setFlags(QtCore.Qt.ItemIsEditable)
            self.table_result.setItem(row, col, cell)
            col += 1

    def __ajust_table_columns(self):
        header = self.table_result.horizontalHeader()
        # name
        index = 0
        header.setSectionResizeMode(index, QHeaderView.ResizeToContents)
        # first air date
        index += 1
        header.setSectionResizeMode(index, QHeaderView.ResizeToContents)

    def save_add_tvshow(self):
        index = self.table_result.currentRow()
        # print(f'table row [{index}]')
        if index >= 0:
            tvs = self.tvshow_search_list[index]
            show_to_add = tvs.name
            op_eu = self.rb_eu.isChecked()
            op_pai = self.rb_pai.isChecked()
            # print(f'serie [{show_to_add}] eu [{op_eu}] pai [{op_pai}]')

            msg = (
                f'Deseja adicionar a série?' + '\n'
                f'\n'
                f'{show_to_add}' + '\n'
                f'{"Eu" if op_eu else "Pai"}'
            )
            q = QMessageBox.question(self, ' ', msg, QMessageBox.Yes | QMessageBox.No)
            if q == QMessageBox.Yes:
                try:
                    ret = self.__api.get_tvshow_info(tvs.id_tmdb)
                    # print(json.dumps(ret, indent=4, ensure_ascii=False))
                    total_seasons = ret['resp_json']['number_of_seasons']
                    # print(f'number_of_seasons [{total_seasons}]')

                    self.__db.insert_tvshow(tvs.id_tmdb, tvs.name, total_seasons, op_eu, op_pai)
                    QMessageBox.information(self, ' ', f'Série {show_to_add} adicionada com sucesso.', QMessageBox.Ok)
                    self.close()
                except:
                    pass
        else:
            row_count = self.table_result.rowCount()
            if row_count == 0:
                QMessageBox.information(self, ' ', 'Precisa buscar uma série antes de adicionar.', QMessageBox.Ok)
                self.textbox_name.setFocus()
                return
            else:
                QMessageBox.information(self, ' ', 'Selecione uma série para adicionar.', QMessageBox.Ok)
                self.table_result.setFocus()
                return