import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider


class Map(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ps/map2.ui", self)
        self.z = 0
        self.setWindowTitle("Yandex Map")
        self.slider.valueChanged.connect(self.change_text)
        self.btn.clicked.connect(self.generate)

    def change_text(self):
        self.scale.setText(str(self.slider.value()))
        self.z = self.slider.value()

    def generate(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.yline.text()},{self.xline.text()}&z={self.z}&size=490,315&l=map"
        response = requests.get(map_request)

        if not response:
            print(map_request)
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

        self.pixmap = QPixmap(self.map_file)
        self.picture.setPixmap(self.pixmap)

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = Map()
    m.show()
    sys.exit(app.exec())