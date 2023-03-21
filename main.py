import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt


class Map(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ps/map3.ui", self)
        self.z = 0
        self.setWindowTitle("Yandex Map")
        self.slider.valueChanged.connect(self.change_text)
        self.btn.clicked.connect(self.generate)

    def change_text(self):
        self.scale.setText(str(self.slider.value()))

    def z_change(self, up_or_down):
        if up_or_down == "down":
            self.slider.setValue(self.slider.value() - 1)
        else:
            self.slider.setValue(self.slider.value() + 1)
        self.generate()

    def change_coords(self, direction):
        if direction == "up":
            self.xline.setText(str(float(self.xline.text()) + 0.06))
        elif direction == "down":
            self.xline.setText(str(float(self.xline.text()) - 0.06))
        elif direction == "left":
            self.yline.setText(str(float(self.yline.text()) - 0.06))
        elif direction == "right":
            self.yline.setText(str(float(self.yline.text()) + 0.06))
        self.generate()

    def generate(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.yline.text()}," \
                      f"{self.xline.text()}&z={self.slider.value()}&size=490,315&l=map"
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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageDown:
            self.z_change("down")
        elif event.key() == Qt.Key.Key_PageUp:
            self.z_change("up")
        elif event.key() == Qt.Key.Key_W:
            self.change_coords("up")
        elif event.key() == Qt.Key.Key_S:
            self.change_coords("down")
        elif event.key() == Qt.Key.Key_A:
            self.change_coords("left")
        elif event.key() == Qt.Key.Key_D:
            self.change_coords("right")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = Map()
    m.show()
    sys.exit(app.exec())
