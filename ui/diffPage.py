import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QMetaObject, Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QTableWidget, QVBoxLayout, QHBoxLayout, QApplication


class UiDiffPage(QWidget):
    def __init__(self, parent=None):
        super(UiDiffPage, self).__init__(parent)
        # 设置窗口标题
        self.setWindowTitle('table diff')
        # 设置窗口大小

        self.initUi()

        self.resize(800, 600)
        # self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

    # 界面初始化
    def initUi(self):
        # button
        pushButtonOldVersion = QPushButton("old version", self)
        pushButtonNewVersion = QPushButton("new version", self)
        pushButtonDiff = QPushButton("diff", self)
        pushButtonOldVersion.setObjectName("pushButtonOldVersion")
        pushButtonNewVersion.setObjectName("pushButtonNewVersion")
        pushButtonDiff.setObjectName("diff")

        # text label
        labelOldVersionDir = QLabel("old version directory", self)
        labelNewVersionDir = QLabel("new version directory", self)
        labelOldVersionDir.setObjectName("labelOldVersionDir")
        labelNewVersionDir.setObjectName("labelNewVersionDir")

        # table
        tableOldVersion = QTableWidget(self)
        tableNewVersion = QTableWidget(self)
        tableOldVersion.setObjectName("tableOldVersion")
        tableNewVersion.setObjectName("tableNewVersion")

        # layout
        oldVersionImport = QHBoxLayout()
        oldVersionImport.addWidget(pushButtonOldVersion,0)
        oldVersionImport.addWidget(labelOldVersionDir,1)
        newVersionImport = QHBoxLayout()
        newVersionImport.addWidget(pushButtonNewVersion, 0)
        newVersionImport.addWidget(labelNewVersionDir, 1)
        oldVersionShow = QVBoxLayout()
        oldVersionShow.addLayout(oldVersionImport)
        oldVersionShow.addWidget(tableOldVersion, 1)
        newVersionShow = QVBoxLayout()
        newVersionShow.addLayout(newVersionImport)
        newVersionShow.addWidget(tableNewVersion, 1)

        mainLayout = QHBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)  # 设置边距为0
        mainLayout.setSpacing(0)  # 设置间距为0
        mainLayout.addLayout(oldVersionShow)
        mainLayout.addWidget(pushButtonDiff)
        mainLayout.addLayout(newVersionShow)
        self.setLayout(mainLayout)

        # slot optimize
        QMetaObject.connectSlotsByName(self)

    #slots



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UiDiffPage()
    window.show()
    sys.exit(app.exec())
