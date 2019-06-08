# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'JansenWidget.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1120, 610)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.screen = QJansenScreen(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.screen.sizePolicy().hasHeightForWidth())
        self.screen.setSizePolicy(sizePolicy)
        self.screen.setMinimumSize(QtCore.QSize(640, 480))
        self.screen.setObjectName("screen")
        self.horizontalLayout_2.addWidget(self.screen)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(280, 0))
        self.tabWidget.setMaximumSize(QtCore.QSize(300, 16777215))
        self.tabWidget.setAccessibleName("")
        self.tabWidget.setObjectName("tabWidget")
        self.tabVideo = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabVideo.sizePolicy().hasHeightForWidth())
        self.tabVideo.setSizePolicy(sizePolicy)
        self.tabVideo.setMinimumSize(QtCore.QSize(0, 0))
        self.tabVideo.setAccessibleName("")
        self.tabVideo.setAccessibleDescription("")
        self.tabVideo.setObjectName("tabVideo")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tabVideo)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupSource = QtWidgets.QGroupBox(self.tabVideo)
        self.groupSource.setObjectName("groupSource")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupSource)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.bcamera = QtWidgets.QRadioButton(self.groupSource)
        self.bcamera.setChecked(True)
        self.bcamera.setObjectName("bcamera")
        self.horizontalLayout.addWidget(self.bcamera)
        self.bfilters = QtWidgets.QRadioButton(self.groupSource)
        self.bfilters.setObjectName("bfilters")
        self.horizontalLayout.addWidget(self.bfilters)
        spacerItem = QtWidgets.QSpacerItem(283, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addWidget(self.groupSource)
        self.groupDvr = QtWidgets.QGroupBox(self.tabVideo)
        self.groupDvr.setMinimumSize(QtCore.QSize(0, 0))
        self.groupDvr.setObjectName("groupDvr")
        self.dvrLayout = QtWidgets.QVBoxLayout(self.groupDvr)
        self.dvrLayout.setContentsMargins(2, 2, 2, 2)
        self.dvrLayout.setSpacing(1)
        self.dvrLayout.setObjectName("dvrLayout")
        self.dvr = QDVR(self.groupDvr)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dvr.sizePolicy().hasHeightForWidth())
        self.dvr.setSizePolicy(sizePolicy)
        self.dvr.setMinimumSize(QtCore.QSize(0, 0))
        self.dvr.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.dvr.setFrameShadow(QtWidgets.QFrame.Raised)
        self.dvr.setObjectName("dvr")
        self.dvrLayout.addWidget(self.dvr)
        self.verticalLayout.addWidget(self.groupDvr)
        self.groupCamera = QtWidgets.QGroupBox(self.tabVideo)
        self.groupCamera.setMinimumSize(QtCore.QSize(0, 0))
        self.groupCamera.setObjectName("groupCamera")
        self.cameraLayout = QtWidgets.QVBoxLayout(self.groupCamera)
        self.cameraLayout.setContentsMargins(2, 2, 2, 2)
        self.cameraLayout.setSpacing(1)
        self.cameraLayout.setObjectName("cameraLayout")
        self.camera = QtWidgets.QFrame(self.groupCamera)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.camera.sizePolicy().hasHeightForWidth())
        self.camera.setSizePolicy(sizePolicy)
        self.camera.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.camera.setFrameShadow(QtWidgets.QFrame.Raised)
        self.camera.setObjectName("camera")
        self.cameraLayout.addWidget(self.camera)
        self.verticalLayout.addWidget(self.groupCamera)
        self.groupFilters = QtWidgets.QGroupBox(self.tabVideo)
        self.groupFilters.setMinimumSize(QtCore.QSize(0, 0))
        self.groupFilters.setObjectName("groupFilters")
        self.filterLayout = QtWidgets.QVBoxLayout(self.groupFilters)
        self.filterLayout.setContentsMargins(2, 2, 2, 2)
        self.filterLayout.setSpacing(1)
        self.filterLayout.setObjectName("filterLayout")
        self.filters = QVideoFilter(self.groupFilters)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filters.sizePolicy().hasHeightForWidth())
        self.filters.setSizePolicy(sizePolicy)
        self.filters.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.filters.setFrameShadow(QtWidgets.QFrame.Raised)
        self.filters.setObjectName("filters")
        self.filterLayout.addWidget(self.filters)
        self.verticalLayout.addWidget(self.groupFilters)
        spacerItem1 = QtWidgets.QSpacerItem(20, 338, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.tabWidget.addTab(self.tabVideo, "")
        self.tabHistogram = QtWidgets.QWidget()
        self.tabHistogram.setObjectName("tabHistogram")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tabHistogram)
        self.verticalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.histogram = QHistogramTab(self.tabHistogram)
        self.histogram.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.histogram.setFrameShadow(QtWidgets.QFrame.Raised)
        self.histogram.setObjectName("histogram")
        self.verticalLayout_3.addWidget(self.histogram)
        self.tabWidget.addTab(self.tabHistogram, "")
        self.tabHelp = QtWidgets.QWidget()
        self.tabHelp.setObjectName("tabHelp")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tabHelp)
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.bback = QtWidgets.QPushButton(self.tabHelp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bback.sizePolicy().hasHeightForWidth())
        self.bback.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/go-previous.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bback.setIcon(icon)
        self.bback.setObjectName("bback")
        self.verticalLayout_2.addWidget(self.bback)
        self.browser = QtWebKitWidgets.QWebView(self.tabHelp)
        self.browser.setUrl(QtCore.QUrl("qrc:/help/help/jansen.html"))
        self.browser.setObjectName("browser")
        self.verticalLayout_2.addWidget(self.browser)
        self.tabWidget.addTab(self.tabHelp, "")
        self.horizontalLayout_2.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1120, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSavePhoto = QtWidgets.QAction(MainWindow)
        self.actionSavePhoto.setObjectName("actionSavePhoto")
        self.actionSavePhotoAs = QtWidgets.QAction(MainWindow)
        self.actionSavePhotoAs.setObjectName("actionSavePhotoAs")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.menuFile.addAction(self.actionSavePhoto)
        self.menuFile.addAction(self.actionSavePhotoAs)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.actionQuit.triggered.connect(MainWindow.close)
        self.bback.clicked.connect(self.browser.back)
        self.tabWidget.currentChanged['int'].connect(self.histogram.expose)
        self.dvr.recording['bool'].connect(self.camera.setDisabled)
        self.dvr.recording['bool'].connect(self.filters.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tabWidget.setStatusTip(_translate("MainWindow", "Record from video camera directly"))
        self.groupSource.setTitle(_translate("MainWindow", "Recording Source"))
        self.bcamera.setStatusTip(_translate("MainWindow", "Record raw video from camera"))
        self.bcamera.setText(_translate("MainWindow", "Camera"))
        self.bfilters.setStatusTip(_translate("MainWindow", "Record filtered video stream"))
        self.bfilters.setText(_translate("MainWindow", "Filters"))
        self.groupDvr.setTitle(_translate("MainWindow", "Video Recorder"))
        self.groupCamera.setTitle(_translate("MainWindow", "Video Camera"))
        self.groupFilters.setTitle(_translate("MainWindow", "Video Filters"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabVideo), _translate("MainWindow", "Video"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabHistogram), _translate("MainWindow", "Histogram"))
        self.bback.setText(_translate("MainWindow", "Back"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabHelp), _translate("MainWindow", "Help"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionSavePhoto.setText(_translate("MainWindow", "Save Photo"))
        self.actionSavePhoto.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionSavePhotoAs.setText(_translate("MainWindow", "Save Photo As ..."))
        self.actionSavePhotoAs.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))


from PyQt5 import QtWebKitWidgets
from jansenlib.QDVR.QDVR import QDVR
from jansenlib.QHistogramTab import QHistogramTab
from jansenlib.QJansenScreen import QJansenScreen
from jansenlib.video.QVideoFilter.QVideoFilter import QVideoFilter
import help_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
