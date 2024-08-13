import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QMetaObject, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QTableWidget, QVBoxLayout, QHBoxLayout, QApplication, \
    QFileDialog, QTabWidget, QTableWidgetItem
from uitl.type import load_table,print_color


class UiDiffPage(QWidget):
    def __init__(self, parent=None):
        super(UiDiffPage, self).__init__(parent)
        # 设置窗口标题
        self.setWindowTitle('table diff')
        # 设置窗口大小
        self.initUi()
        self.resize(800, 600)
        #self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

    # 界面初始化
    def initUi(self):
        # button
        self.pushButtonOldVersion = QPushButton("old version", self)
        self.pushButtonNewVersion = QPushButton("new version", self)
        self.pushButtonDiff = QPushButton("diff", self)
        self.pushButtonOldVersion.setObjectName("pushButtonOldVersion")
        self.pushButtonNewVersion.setObjectName("pushButtonNewVersion")
        self.pushButtonDiff.setObjectName("pushButtonDiff")

        # text label
        self.labelOldVersionDir = QLabel("old version directory", self)
        self.labelNewVersionDir = QLabel("new version directory", self)
        self.labelOldVersionDir.setObjectName("labelOldVersionDir")
        self.labelNewVersionDir.setObjectName("labelNewVersionDir")

        # table
        self.tableOldVersion = QTabWidget(self)
        self.tableNewVersion = QTabWidget(self)
        self.tableOldVersion.setObjectName("tableOldVersion")
        self.tableNewVersion.setObjectName("tableNewVersion")

        # layout
        self.oldVersionImport = QHBoxLayout()
        self.oldVersionImport.addWidget(self.pushButtonOldVersion,0)
        self.oldVersionImport.addWidget(self.labelOldVersionDir,1)
        self.newVersionImport = QHBoxLayout()
        self.newVersionImport.addWidget(self.pushButtonNewVersion, 0)
        self.newVersionImport.addWidget(self.labelNewVersionDir, 1)
        self.oldVersionShow = QVBoxLayout()
        self.oldVersionShow.addLayout(self.oldVersionImport)
        self.oldVersionShow.addWidget(self.tableOldVersion, 1)
        self.newVersionShow = QVBoxLayout()
        self.newVersionShow.addLayout(self.newVersionImport)
        self.newVersionShow.addWidget(self.tableNewVersion, 1)

        self.mainLayout = QHBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)  # 设置边距为0
        self.mainLayout.setSpacing(0)  # 设置间距为0
        self.mainLayout.addLayout(self.oldVersionShow)
        self.mainLayout.addWidget(self.pushButtonDiff)
        self.mainLayout.addLayout(self.newVersionShow)
        self.setLayout(self.mainLayout)

        # slot optimize
        QMetaObject.connectSlotsByName(self)

    #slots
    @QtCore.pyqtSlot()
    def on_pushButtonOldVersion_clicked(self):
        folder_path = QFileDialog.getOpenFileName(self, "选择旧版表格", "/", "Files(*.xlsx)")
        dir = folder_path.__getitem__(0)
        self.labelOldVersionDir.clear()
        self.labelOldVersionDir.setText(dir)
        print(self.labelOldVersionDir.text())
        self.tableOldVersion.clear()
        load_table(self.labelOldVersionDir.text(), self.tableOldVersion)

    @QtCore.pyqtSlot()
    def on_pushButtonNewVersion_clicked(self):
        folder_path = QFileDialog.getOpenFileName(self, "选择新版表格", "/", "Files(*.xlsx)")
        dir = folder_path.__getitem__(0)
        self.labelNewVersionDir.clear()
        self.labelNewVersionDir.setText(dir)
        print(self.labelNewVersionDir.text())
        self.tableNewVersion.clear()
        load_table(dir, self.tableNewVersion)

    @QtCore.pyqtSlot()
    def on_pushButtonDiff_clicked(self):
        all_differences = print_color(self.labelOldVersionDir.text(), self.labelNewVersionDir.text())
        print(all_differences)
        for sheet_index, differences in all_differences.items():
            # 获取对应的 QTableWidget
            table_widget1 = self.tableOldVersion.widget(sheet_index)  # 根据索引获取对应的 tab
            table_widget2 = self.tableNewVersion.widget(sheet_index)

            # 遍历差异并上色
            for (i, j, color) in differences:
                item1 = table_widget1.item(i, j)  # 获取当前单元格项
                item2 = table_widget2.item(i, j)
                if item1 is None:
                    item1 = QTableWidgetItem()  # 如果没有项，则创建一个新的
                    table_widget1.setItem(i, j, item1)  # 设置单元格项
                if item2 is None:
                    item2 = QTableWidgetItem()  # 如果没有项，则创建一个新的
                    table_widget2.setItem(i, j, item2)  # 设置单元格项

                # 根据颜色设置背景
                if color == 'green':
                    item1.setBackground(QColor(0, 255, 0))  # 绿色
                    item2.setBackground(QColor(0, 255, 0))  # 绿色
                elif color == 'red':
                    item1.setBackground(QColor(255, 0, 0))  # 红色
                    item2.setBackground(QColor(255, 0, 0))  # 绿色
                elif color == 'yellow':
                    item1.setBackground(QColor(255, 255, 0))  # 黄色
                    item2.setBackground(QColor(255, 255, 0))  # 黄色

        print("diff")




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UiDiffPage()
    window.show()
    sys.exit(app.exec())
