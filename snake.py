import random
import sys

from PyQt5.QtCore import QPoint, QRectF, Qt, QTimer
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget


class VimSnake(QWidget):
    def __init__(self):
        super(VimSnake, self).__init__()

        self.game_over = False
        self.start_game = True
        self.score = 0
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Vim Snake')
        self.setGeometry(100, 100, 400, 300)
        self.snake = [QPoint(100, 100), QPoint(90, 100), QPoint(80, 100)]
        self.direction = Qt.Key_Right
        self.food = self.generate_food()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)
        self.show()

    def keyPressEvent(self, event):
        key = event.key()

        if key in [Qt.Key_H, Qt.Key_J, Qt.Key_K, Qt.Key_L]:
            if not self.game_over:
                if key == Qt.Key_L and self.direction != Qt.Key_Left:
                    self.direction = Qt.Key_Right
                elif key == Qt.Key_H and self.direction != Qt.Key_Right:
                    self.direction = Qt.Key_Left
                elif key == Qt.Key_J and self.direction != Qt.Key_Up:
                    self.direction = Qt.Key_Down
                elif key == Qt.Key_K and self.direction != Qt.Key_Down:
                    self.direction = Qt.Key_Up

    def update_game(self):
        if not self.game_over:
            new_head = self.snake[0]
            if self.direction == Qt.Key_Left:
                new_head = QPoint(new_head.x() - 10, new_head.y())
            elif self.direction == Qt.Key_Right:
                new_head = QPoint(new_head.x() + 10, new_head.y())
            elif self.direction == Qt.Key_Up:
                new_head = QPoint(new_head.x(), new_head.y() - 10)
            elif self.direction == Qt.Key_Down:
                new_head = QPoint(new_head.x(), new_head.y() + 10)
            self.snake.insert(0, new_head)
            if new_head == self.food:
                self.food = self.generate_food()
                self.score += 10
            else:
                self.snake.pop()
            if self.check_collision():
                self.game_over = True
            self.update()

    def generate_food(self):
        x = random.randint(0, (self.width() - 10) // 10) * 10
        y = random.randint(0, (self.height() - 10) // 10) * 10
        return QPoint(x, y)

    def check_collision(self):
        head = self.snake[0]
        return head.x() < 0 or head.x() >= self.width() or head.y() < 0 or head.y() >= self.height() or head in self.snake[1:]

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#282a36"))

        for part in self.snake:
            painter.fillRect(QRectF(part.x(), part.y(), 10, 10),
                             QColor("#bd93f9"))

        painter.fillRect(QRectF(self.food.x(), self.food.y(), 10, 10), QColor(
            "#50fa7b"))

        if self.start_game:
            painter.setPen(QColor("#50fa7b"))
            painter.setFont(self.font())
            painter.drawText(self.rect(), Qt.AlignCenter,
                             f"Click để chơi")
        elif self.game_over:
            painter.setPen(QColor("#ff5555"))
            painter.setFont(self.font())
            painter.drawText(self.rect(), Qt.AlignCenter,
                             f"Thua cuộc - Điểm: {self.score}")
        else:
            painter.setPen(QColor("#f2f2f2"))
            painter.setFont(self.font())
            painter.drawText(self.rect().bottomLeft() +
                             QPoint(10, -10), f"Điểm: {self.score}")

    def mousePressEvent(self, event):
        if self.start_game:
            self.reset_game()
            self.start_game = False
            self.timer.start(100)
        elif self.game_over:
            self.reset_game()
            self.game_over = False
            self.timer.start()

    def reset_game(self):
        self.snake = [QPoint(100, 100), QPoint(90, 100), QPoint(80, 100)]
        self.direction = Qt.Key_Right
        self.food = self.generate_food()
        self.score = 0
        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VimSnake()
    sys.exit(app.exec_())
