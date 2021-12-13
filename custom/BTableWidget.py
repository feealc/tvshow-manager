from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *


class BTableWidget(QTableWidget):
    def __init__(self, parent=None):
        # super(BTableWidget, self).__init__()
        super().__init__(parent=parent)
        # print('BTableWidget init')

    def b_clear_content(self):
        self.clearContents()
        self.setRowCount(0)

    def b_add_row(self, from_tuple=None):
        row = self.rowCount()
        self.setRowCount(row + 1)
        col = 0
        for item in from_tuple:
            cell = QTableWidgetItem(str(item))
            # cell.setFlags(QtCore.Qt.ItemIsEditable)
            # cell.setFlags(QtCore.Qt.ItemIsEnabled)
            # cell.setFlags(QtCore.Qt.ItemIsEditable)
            self.setItem(row, col, cell)
            col += 1

    def b_set_column_header(self, header_labels):
        self.setColumnCount(len(header_labels))
        self.setHorizontalHeaderLabels(header_labels)

    def b_hide_vertical_headers(self):
        self.verticalHeader().setVisible(False)

    def b_show_vertical_headers(self):
        self.verticalHeader().setVisible(True)

    def b_set_select_row(self):
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
