import sys
import subprocess
import mysql.connector
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPalette, QBrush
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QVBoxLayout, \
    QHBoxLayout, QMessageBox


class Register(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        # Устанавливаем фон
        background_pixmap = QPixmap("bg_login.jpg")  # Укажите путь к изображению
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setBrush(QPalette.ColorRole.Window, QBrush(background_pixmap))
        self.setPalette(p)

        # Создаем белый блок
        white_block = QWidget(self)
        white_block.setStyleSheet("""
            background-color: rgba(255, 255, 255, 255);  /* Прозрачный белый */
            border-radius: 13px;
        """)
        white_block.setGeometry(250, 150, 500, 400)  # Задаем положение и размеры блока

        # Создаем элементы внутри белого блока
        lb_login = QLabel("Логин:", white_block)
        lb_password = QLabel("Пароль:", white_block)

        lb_login.setStyleSheet("font-weight: bold; "
                               "font-size: 35px;")
        lb_password.setStyleSheet("font-weight: bold; "
                                  "font-size: 35px;")

        in_login = QLineEdit(white_block)
        in_password = QLineEdit(white_block)
        in_login.setStyleSheet("""
            QLineEdit {
                background-color: #f0f0f0;
                border: 2px solid #4CAF50;
                border-radius: 5px;
                padding: 5px;
                font-size: 25px;
            }
            QLineEdit:focus {
                border: 2px solid #45a049;
                background-color: #e8f5e9;
            }
        """)
        in_password.setStyleSheet(in_login.styleSheet())
        in_login.setFixedWidth(300)
        in_password.setFixedWidth(300)

        btn_login = QPushButton("Войти")
        btn_login.clicked.connect(lambda: self.check_credentials(in_login.text(), in_password.text()))
        btn_login.setStyleSheet("""
            QPushButton {
                background-color: #282EDB;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 40px;
                width: 190px;
                border: 5px solid #212595;

            }
            QPushButton:hover {
                background-color: #1118EB;
            }
            QPushButton:pressed {
                background-color: #1318A8;
            }
        """)

        # Макет для белого блока
        white_layout = QVBoxLayout(white_block)
        grid_layout = QGridLayout()
        grid_layout.addWidget(lb_login, 0, 0, alignment=Qt.AlignmentFlag.AlignRight)
        grid_layout.addWidget(in_login, 0, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        grid_layout.addWidget(lb_password, 1, 0, alignment=Qt.AlignmentFlag.AlignRight)
        grid_layout.addWidget(in_password, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        white_layout.addLayout(grid_layout)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(btn_login)
        button_layout.addStretch()
        white_layout.addLayout(button_layout)

        # Основной макет окна
        main_layout = QVBoxLayout(self)
        main_layout.addStretch()
        main_layout.addWidget(white_block, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch()

        self.setWindowTitle("Футбол")
        self.resize(1000, 700)

    def check_credentials(self, login, password):
        if not login or not password:
            self.show_message("Ошибка", "Логин и пароль не могут быть пустыми.")
            return

        # Подключение к базе данных и проверка введенных данных
        try:
            conn = mysql.connector.connect(
                host="150.241.90.210",
                user="korv",
                password="rjHdbr54@3",
                database="korvtestdb"
            )
            cursor = conn.cursor()

            query = "SELECT * FROM users WHERE login = %s AND pass = %s"
            cursor.execute(query, (login, password))

            result = cursor.fetchone()

            if result is None:
                self.show_message("Ошибка", "Неверный логин или пароль.")
            else:
                self.close()  # Закрыть окно регистрации
                subprocess.Popen(["python", "main.py"])  # Запуск main.py

            cursor.close()
            conn.close()

        except mysql.connector.Error as e:
            self.show_message("Ошибка базы данных", f"Ошибка базы данных: {e}")

    def show_message(self, title, message):
        """Отображение сообщения в message box"""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Information if "Ошибка" not in title else QMessageBox.Icon.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()


if __name__ == "__main__":
    app = QApplication([])
    window = Register()
    window.show()
    app.exec()
