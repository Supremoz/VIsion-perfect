import sys
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from visionperfect_ui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.home_btn_1.clicked.connect(self.show_home_page)
        self.ui.home_btn_2.clicked.connect(self.show_home_page)
        self.ui.gallery_btn_1.clicked.connect(self.show_gallery_page)
        self.ui.gallery_btn_2.clicked.connect(self.show_gallery_page)
        self.ui.info_btn_1.clicked.connect(self.show_info_page)
        self.ui.info_btn_2.clicked.connect(self.show_info_page)
        self.ui.btn_origbg.clicked.connect(self.show_originalbg)
        self.ui.btn_resultbg.clicked.connect(self.show_resultbg)
        self.ui.pushButton_15.clicked.connect(self.select_image)

        # Hide widget_4 when the program starts
        self.ui.widget_4.hide()

        # Connect exit_btn_1 and exit_btn_2 to close the program
        self.ui.exit_btn_1.clicked.connect(QApplication.instance().quit)
        self.ui.exit_btn_2.clicked.connect(QApplication.instance().quit)

    def show_home_page(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def show_gallery_page(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def show_info_page(self):
        self.ui.stackedWidget.setCurrentIndex(2)
    def show_originalbg(self):
        self.ui.stackedWidget_3.setCurrentIndex(1)
    def show_resultbg(self):
        self.ui.stackedWidget_3.setCurrentIndex(0)


    def select_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")

        if file_path:
            pixmap = QPixmap(file_path)
            pixmap = pixmap.scaled(self.ui.lbl_imgbg_result.size(), Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.ui.lbl_imgbg_result.setPixmap(pixmap)
            self.ui.lbl_imgbg_result.setScaledContents(True)
            self.ui.lbl_imgbg_result.adjustSize()
            self.ui.pushButton_15.setText("Remove Bg")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load the style.qss file
    style_file = QFile("style.qss")
    style_file.open(QFile.ReadOnly | QFile.Text)
    style_stream = QTextStream(style_file)
    app.setStyleSheet(style_stream.readAll())

    window = MainWindow()
    window.setCentralWidget(window.ui.centralwidget)
    window.show()
    sys.exit(app.exec_())