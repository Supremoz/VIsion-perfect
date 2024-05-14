import sys
import rembg
from PyQt5.QtCore import QFile, QTextStream, QRunnable, QThreadPool, Qt, pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from visionperfect_ui import Ui_MainWindow
from PIL import Image
from gradio_client import Client, file

class ImageEnhanceRunnable(QRunnable):
    def __init__(self, client, image, size, api_name):
        super(ImageEnhanceRunnable, self).__init__()
        self.client = client
        self.image = image
        self.size = size
        self.api_name = api_name
        self.signals = EnhanceSignals()

    def run(self):
        try:
            result = self.client.predict(image=self.image, size=self.size, api_name=self.api_name)
            self.signals.result.emit(result)
        except Exception as e:
            self.signals.error.emit(str(e))

class EnhanceSignals(QObject):
    result = pyqtSignal(str)
    error = pyqtSignal(str)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
    
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.is_notif_visible = False
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
        self.ui.btn_closebg.clicked.connect(self.show_introbg)
        self.ui.btn_uploaden.clicked.connect(self.enhance_image)
        self.ui.btn_resen.clicked.connect(self.show_output_enhance)
        self.ui.btn_origen.clicked.connect(self.input_enhance_image)
        self.ui.pushButton.clicked.connect(self.select_enhance_image)
        self.ui.btn_downloaden.clicked.connect(self.download_enhance_image)
        self.ui.btn_notif.clicked.connect(self.show_notif)
        # Hide btn when the program starts
        self.ui.widget_4.hide()
        self.ui.btn_rbg.hide()
        self.ui.btn_origbg.hide()
        self.ui.btn_downloadbg.hide()
        self.ui.btn_resultbg.hide()
        self.ui.comboBox.hide()
        self.ui.btn_closebg.hide()
        self.ui.btn_origen.hide()
        self.ui.btn_uploaden.hide()
        self.ui.btn_resen.hide()
        self.ui.btn_downloaden.hide()
        self.ui.progressBar.hide()
        self.ui.lbl_notifMessage.hide()
        # Connect exit_btn_1 and exit_btn_2 to close the program
        self.ui.exit_btn_1.clicked.connect(QApplication.instance().quit)
        self.ui.exit_btn_2.clicked.connect(QApplication.instance().quit)

        self.threadpool = QThreadPool()

    def show_output_enhance(self):
        self.ui.stackedWidget_2.setCurrentIndex(0)
    def input_enhance_image(self):
        self.ui.stackedWidget_2.setCurrentIndex(1)
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
        
    def show_introbg(self):
        self.ui.stackedWidget_3.setCurrentIndex(1)
        self.ui.btn_closebg.show()
        self.ui.pushButton_15.show()
        self.ui.btn_rbg.hide()
        self.ui.comboBox.hide()
        self.ui.btn_downloadbg.hide()
        self.ui.btn_origbg.hide()
        self.ui.btn_resultbg.hide()
    
    def show_notif(self):

        if not self.is_notif_visible:
            self.ui.progressBar.show()
            self.ui.lbl_notifMessage.show()
            self.is_notif_visible = True
        else:
            self.ui.progressBar.hide()
            self.ui.lbl_notifMessage.hide()
            self.is_notif_visible = False
        
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
            self.ui.btn_closebg.show()
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
        self.ui.comboBox.show()
        self.show_resultbg()
    def select_enhance_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")

        if file_path:
            self.selected_file_path = file_path
            pixmap = QPixmap(file_path)
            pixmap = pixmap.scaled(self.ui.lbl_imgen_result.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.ui.lbl_imgen_result.setPixmap(pixmap)
            self.ui.lbl_imgen_result.setScaledContents(True)
            self.ui.lbl_imgen_result.adjustSize()
            self.ui.btn_origen.show()
            self.ui.btn_uploaden.show()
            self.ui.btn_resen.show()
            self.ui.btn_downloaden.show()
            #self.ui.pushButton_15.hide()
            #self.ui.btn_closebg.show()
            #self.ui.btn_rbg.show()
            #self.ui.btn_rbg.clicked.connect(self.remove_background)
            #self.show_originalbg()

    def download_result_image(self):
        file_dialog = QFileDialog()
        file_name, _ = file_dialog.getSaveFileName(self, "Save Image", "result.png", "Image Files (*.png)")

        if file_name:
            # Convert the output image to a QImage
            output_image = QImage(self.ui.lbl_imgbg.pixmap().toImage())

            # Save the output image
            output_image.save(file_name)

            # Show a message box to confirm the save
            #QMessageBox.information(self, "Image Saved",f"Image saved as {file_name}")
    
    def enhance_image(self):
        if self.selected_file_path is None:
            return

        client = Client("doevent/Face-Real-ESRGAN")
        image = file(self.selected_file_path)
        size = "2x"
        api_name = "/predict"

        runnable = ImageEnhanceRunnable(client, image, size, api_name)
        runnable.signals.result.connect(self.display_enhanced_image)
        runnable.signals.error.connect(self.display_enhance_error)
        self.threadpool.start(runnable)
        

    def display_enhanced_image(self, result):
        pixmap = QPixmap.fromImage(QImage(result))
        pixmap = pixmap.scaled(self.ui.lbl_imgen.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.ui.lbl_imgen.setPixmap(pixmap)
        self.ui.lbl_imgen.setScaledContents(True)
        self.ui.lbl_imgen.adjustSize()

    def display_enhance_error(self, error):
        print(f"Enhance Error: {error}")

    def download_enhance_image(self):
        file_dialog = QFileDialog()
        file_name, _ = file_dialog.getSaveFileName(self, "Save Image", "result.png", "Image Files (*.png)")

        if file_name:
            # Convert the output image to a QImage
            output_image = QImage(self.ui.lbl_imgen.pixmap().toImage())

            # Save the output image
            output_image.save(file_name)

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