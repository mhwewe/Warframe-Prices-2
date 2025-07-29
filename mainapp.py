import sys
from BlurWindow.blurWindow import GlobalBlur
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QFrame, QApplication, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QSize, QThread, pyqtSignal
from detailbox import DetailBox
from Api_Orders import orders

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
        for i in self.frame_boxes:
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

        self.frame_boxes[0].search.clicked.connect(lambda: self.search_item(self.frame_boxes[0].input.text()))

        main_frame = QFrame(self)
        main_frame.setLayout(main_grid)
        self.setCentralWidget(main_frame)


    def search_item(self, item_name):
        orders_dict: dict = orders(item_name)
        for i in range(0, self.frame_boxes[0].number_listed):
            self.frame_boxes[0].names[i].setText(orders_dict['sell'][i]['ingame_name'])
            self.frame_boxes[0].prices[i].setText(str(orders_dict['sell'][i]['platinum']))


if __name__ == "__main__":
    app = QApplication([])

    widget = MainWindow()
    widget.show()

    sys.exit(app.exec())