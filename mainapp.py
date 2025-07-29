import sys
from BlurWindow.blurWindow import GlobalBlur
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QFrame, QApplication, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QSize, QThread, pyqtSignal, QObject, QThreadPool
from detailbox import DetailBox
from Api_Orders import orders
import time

class Worker(QObject):
    # print('at Worker')
    finished = pyqtSignal()
    result = pyqtSignal(dict)

    def __init__(self, item_name, frame):
        super().__init__()
        self.item_name = item_name
        self.frame = frame

    def search_item(self):
        orders_dict: dict = orders(self.item_name)
        # print('done')
        self.result.emit(orders_dict)
        self.finished.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        GlobalBlur(self.winId(), Dark=True)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NativeWindow)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle('WF Prices')
        self.setWindowIcon(QIcon('Resources\\Warframe market logo crop (1).png'))

        shadow_main = QGraphicsDropShadowEffect(self)
        shadow_main.setColor(QColor(1, 1, 1, 255))
        shadow_main.setBlurRadius(15)
        shadow_main.setXOffset(1)
        shadow_main.setYOffset(1)
        # self.setGraphicsEffect(shadow_main)

        self.box_amount = 12
        self.frame_boxes = [DetailBox(6) for i in range(0, self.box_amount)]

        main_grid = QGridLayout()
        row: int = 0
        col: int = 0
        cols = 3
        for idi, i in enumerate(self.frame_boxes):
            self.frame_boxes[idi].search.clicked.connect(self.start_thread)

            if 9 <= self.box_amount <= 18:
                cols = self.box_amount/3
            if self.box_amount > 18:
                # cols = round(self.box_amount/3)-1
                cols = 5
            if self.box_amount > 30:
                cols = 6
            if self.box_amount <= 6:
                cols = 2
            main_grid.addWidget(i, row, col)
            row += 1
            if row == cols:
                col += 1
                row = 0


        # self.frame_boxes[0].search.clicked.connect(lambda: uh.search_item(self.frame_boxes[0].input.text()))
        self.threads = []


        main_frame = QFrame(self)
        main_frame.setLayout(main_grid)
        self.setCentralWidget(main_frame)


    def search_item(self, orders_dict):
        sent = self.sender()
        orders_dict: dict = orders_dict
        for i in range(0, self.frame_boxes[0].number_listed):
            sent.frame.names[i].setText(orders_dict['sell'][i]['ingame_name'])
            sent.frame.prices[i].setText(str(orders_dict['sell'][i]['platinum']))

    def start_thread(self):
        self.thread = QThread()
        frame = self.sender().parent().parent()
        self.worker = Worker(frame.input.text(), frame)

        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.search_item)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.worker.result.connect(self.search_item)

        self.thread.start()


if __name__ == "__main__":
    app = QApplication([])

    widget = MainWindow()
    widget.show()

    sys.exit(app.exec())
