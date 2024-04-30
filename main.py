import sys
import rembg
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from visionperfect_ui import Ui_MainWindow
from PIL import Image

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
        self.selected_file_path = None
        self.ui.btn_downloadbg.clicked.connect(self.download_result_image)

        # Hide btn when the program starts
        self.ui.widget_4.hide()
        self.ui.btn_rbg.hide()
        self.ui.btn_origbg.hide()
        self.ui.btn_downloadbg.hide()
        self.ui.btn_resultbg.hide()
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
        self.ui.stackedWidget_3.setCurrentIndex(2)

    def show_resultbg(self):
        self.ui.stackedWidget_3.setCurrentIndex(0)

    def select_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")

        if file_path:
            self.selected_file_path = file_path
            pixmap = QPixmap(file_path)
            pixmap = pixmap.scaled(self.ui.lbl_imgbg_result.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.ui.lbl_imgbg_result.setPixmap(pixmap)
            self.ui.lbl_imgbg_result.setScaledContents(True)
            self.ui.lbl_imgbg_result.adjustSize()
            self.ui.pushButton_15.hide()
            self.ui.btn_rbg.show()
            self.ui.btn_rbg.clicked.connect(self.remove_background)
            self.show_originalbg()

    def remove_background(self):
        if self.selected_file_path is None:
            return
    
        with open(self.selected_file_path, "rb") as f:
            input_image = Image.open(f)
            output_image = rembg.remove(input_image)
    
        # Create a new image with a transparent background
        transparent_background = Image.new('RGBA', input_image.size, (0, 0, 0, 0))
    
        # Paste the output image onto the transparent background
        transparent_background.paste(output_image, mask=output_image)
    
        # Convert the output image to a QPixmap
        output_pixmap = QPixmap.fromImage(QImage(transparent_background.tobytes(), transparent_background.size[0], transparent_background.size[1], QImage.Format_RGBA8888))
        output_pixmap = output_pixmap.scaled(self.ui.lbl_imgbg.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    
        # Set the output image as the pixmap for lbl_imgbg
        self.ui.lbl_imgbg.setPixmap(output_pixmap)
        self.ui.lbl_imgbg.setScaledContents(True)
        self.ui.lbl_imgbg.adjustSize()
        self.ui.btn_downloadbg.show()
        self.ui.btn_origbg.show()
        self.ui.btn_resultbg.show()
        self.ui.btn_rbg.hide()
        self.show_resultbg()

    def download_result_image(self):
        file_dialog = QFileDialog()
        file_name, _ = file_dialog.getSaveFileName(self, "Save Image", "result.png", "Image Files (*.png)")

        if file_name:
            # Convert the output image to a QImage
            output_image = QImage(self.ui.lbl_imgbg.pixmap().toImage())

            # Save the output image
            output_image.save(file_name)

            # Show a message box to confirm the save
            QMessageBox.information(self, "Image Saved",f"Image saved as {file_name}")

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