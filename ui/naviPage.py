import ast
from functools import partial

import numpy
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QTabWidget, QLabel, QHBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox
from uitl.type import create_dataframe

class UiNaviPage(QWidget):
    def __init__(self,ui_diff_page):
        super().__init__()
        self.setWindowTitle('navigation')
        self.initUi(ui_diff_page)
        self.resize(400, 300)

    def initUi(self, ui_diff_page):

        self.tableNavi = QTabWidget(self)
        self.tableNavi.setObjectName("tableNavi")
        sheets = create_dataframe(ui_diff_page.all_differences)
        self.mainlayout = QHBoxLayout()
        self.mainlayout.addWidget(self.tableNavi)

        for i, df in enumerate(sheets):
            table_widget = QTableWidget(df.shape[0], df.shape[1])  # 创建 QTableWidget
            table_widget.setHorizontalHeaderLabels(df.columns)  # 设置表头
            table_widget.setObjectName(str(df.sheet_key))
            print (i,table_widget.objectName())

            for row in range(df.shape[0]):
                for col in range(df.shape[1]):
                    item = QTableWidgetItem(str(df.iat[row, col]))
                    table_widget.setItem(row, col, item)
            # 连接信号，传递行和列信息
            table_widget.itemClicked.connect(
                partial(self.on_tableNavi_itemClicked, sheet_name=table_widget.objectName(), item=item, ui_diff_page=ui_diff_page,))
            self.tableNavi.addTab(table_widget, table_widget.objectName())  # 将 QTableWidget 添加到标签页

        self.setLayout(self.mainlayout)


    def on_tableNavi_itemClicked(self, sheet_name, item ,ui_diff_page):
        print("clicked")
        mes = item.text()
        tuple_values = ast.literal_eval(mes)
        row,col = tuple_values
        print(f"Cell clicked: Tab {sheet_name},row {row}, col {col}")
        if (row is None) or (col is None):
            QMessageBox.about(self,"maybe","here is picture or other things not digital")
            return
        ui_diff_page.navigate_to_row(int(sheet_name), row, col)
