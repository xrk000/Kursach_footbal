import mysql.connector
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QSpacerItem, QSizePolicy, \
    QMessageBox, QDialog, QFormLayout, QComboBox, QLineEdit, QDialogButtonBox, QApplication, QListWidgetItem, QDateEdit, \
    QTextEdit
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, Qt, QDate


class TrenerTab(QWidget):
    def __init__(self):
        super().__init__()

        # Подключение к базе данных
        self.connect_to_db()

        layout = QVBoxLayout()

        # Кнопка "домик"
        home_button_layout = QHBoxLayout()
        home_button = QPushButton()
        home_button.setIcon(QIcon('home.png'))
        home_button.setIconSize(QSize(30, 30))
        home_button.setStyleSheet("""
            QPushButton {
                background-color: #2C6B3D; 
                border: none; 
                border-radius: 12px; 
                padding: 10px;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3);
            }
            QPushButton:hover {
                background-color: #1C4B2D;
                transform: scale(1.1);
            }
        """)
        home_button.clicked.connect(self.open_main_window)
        home_button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        home_button_layout.addWidget(home_button)
        layout.addLayout(home_button_layout)

        # Список тренеров
        self.trener_list = QListWidget()
        self.trener_list.setMinimumHeight(600)
        self.trener_list.setStyleSheet("""
            QListWidget {
                background-color: #F5F5F5; 
                border-radius: 12px; 
                padding: 10px;
                border: 2px solid #388E3C;
                font-family: 'Arial', sans-serif;
                font-size: 16px;
            }
            QListWidget::item {
                padding: 12px;
                background-color: #F9F9F9;
                margin-bottom: 6px;
                border-radius: 8px;
            }
            QListWidget::item:hover {
                background-color: #4CAF50;
                color: white;
            }
            QListWidget::item:selected {
                background-color: #FF9800;
                color: white;
                outline: none;
                border: none;
            }
        """)
        layout.addWidget(self.trener_list)

        # Загрузка данных тренеров
        self.load_coaches()

        # Горизонтальный layout для кнопок
        buttons_layout = QHBoxLayout()

        # Стилизация кнопок
        button_style = """
            QPushButton {
                background-color: #388E3C;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: bold;
                text-align: center;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
            }
            QPushButton:hover {
                background-color: #2C6B3D;
                transform: scale(1.05);
            }
        """

        add_button = QPushButton("Добавить")
        add_button.setStyleSheet(button_style)
        add_button.clicked.connect(self.add_trener)
        buttons_layout.addWidget(add_button)

        edit_button = QPushButton("Редактировать")
        edit_button.setStyleSheet(button_style.replace("#388E3C", "#FF9800").replace("#2C6B3D", "#F57C00"))
        edit_button.clicked.connect(self.edit_trener)
        buttons_layout.addWidget(edit_button)

        delete_button = QPushButton("Удалить")
        delete_button.setStyleSheet(button_style.replace("#388E3C", "#F44336").replace("#2C6B3D", "#D32F2F"))
        delete_button.clicked.connect(self.delete_trener)
        buttons_layout.addWidget(delete_button)

        # Добавляем пространство для выравнивания кнопок слева до середины
        buttons_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        layout.addLayout(buttons_layout)

        # Кнопка выхода
        exit_button = QPushButton("Выход")
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: #D32F2F; /* Красный цвет */
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: bold;
                text-align: center;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
            }
            QPushButton:hover {
                background-color: #B71C1C; /* Более темный красный */
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background-color: #F44336; /* Светлый красный при нажатии */
            }
        """)
        exit_button.clicked.connect(self.exit_application)
        exit_layout = QHBoxLayout()
        exit_layout.addWidget(exit_button, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addLayout(exit_layout)

        self.setLayout(layout)

    def connect_to_db(self):
        """Подключаемся к базе данных."""
        try:
            self.conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="123456qwerty",
                database="cursovaya"
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Ошибка подключения к базе данных", str(e))

    def load_coaches(self):
        """Загружает тренеров из базы данных."""
        self.trener_list.clear()
        try:
            self.cursor.execute("SELECT Coach_ID, Lastname, FirstName, MiddleName, BirthDate, Phone, Email FROM coaches")
            for row in self.cursor.fetchall():
                coach_id, lastname, firstname, middlename, birthdate, phone, email = row
                display_text = f"{lastname} {firstname} {middlename} | {birthdate} | {phone} | {email}"
                item = QListWidgetItem(display_text)
                item.setData(Qt.ItemDataRole.UserRole, coach_id)
                self.trener_list.addItem(item)
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Ошибка загрузки данных", str(e))

    def add_trener(self):
        dialog = TrenerDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            lastname, firstname, middlename, birthdate, phone, email = dialog.get_data()
            try:
                query = """INSERT INTO coaches (Lastname, FirstName, MiddleName, BirthDate, Phone, Email)
                           VALUES (%s, %s, %s, %s, %s, %s)"""
                self.cursor.execute(query, (lastname, firstname, middlename, birthdate, phone, email))
                self.conn.commit()
                self.load_coaches()
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка добавления данных", str(e))

    def edit_trener(self):
            current_item = self.trener_list.currentItem()
            if current_item:
                coach_id = current_item.data(Qt.ItemDataRole.UserRole)
                try:
                    self.cursor.execute(
                        "SELECT Lastname, FirstName, MiddleName, BirthDate, Phone, Email FROM coaches WHERE Coach_ID=%s",
                        (coach_id,)
                    )
                    data = self.cursor.fetchone()
                    if data:
                        lastname, firstname, middlename, birthdate, phone, email = data

                        birthdate_qdate = QDate(birthdate)

                        dialog = TrenerDialog((lastname, firstname, middlename, birthdate_qdate, phone, email))
                        if dialog.exec() == QDialog.DialogCode.Accepted:
                            lastname, firstname, middlename, birthdate, phone, email = dialog.get_data()

                            try:
                                birthdate_qdate = QDate(birthdate)
                                if not birthdate_qdate.isValid():
                                    raise ValueError("Некорректная дата рождения!")

                                query = """
                                    UPDATE coaches 
                                    SET Lastname=%s, FirstName=%s, MiddleName=%s, BirthDate=%s, Phone=%s, Email=%s 
                                    WHERE Coach_ID=%s
                                """
                                self.cursor.execute(query,
                                                    (lastname, firstname, middlename, birthdate, phone, email, coach_id))
                                self.conn.commit()
                                self.load_coaches()
                            except ValueError as e:
                                QMessageBox.critical(self, "Ошибка", str(e))
                            except mysql.connector.Error as e:
                                QMessageBox.critical(self, "Ошибка редактирования данных", str(e))
                    else:
                        QMessageBox.warning(self, "Ошибка", "Тренер не найден.")
                except mysql.connector.Error as e:
                    QMessageBox.critical(self, "Ошибка загрузки данных", str(e))

    def delete_trener(self):
        current_item = self.trener_list.currentItem()
        if current_item:
            coach_id = current_item.data(Qt.ItemDataRole.UserRole)
            message_box = QMessageBox(self)
            message_box.setWindowTitle("Удаление тренера")
            message_box.setText("Вы уверены, что хотите удалить этого тренера?")
            message_box.setIcon(QMessageBox.Icon.Warning)

            yes_button = message_box.addButton("Удалить", QMessageBox.ButtonRole.AcceptRole)
            no_button = message_box.addButton("Отмена", QMessageBox.ButtonRole.RejectRole)

            # Применяем стили для сообщения
            message_box.setStyleSheet("""
                QMessageBox {
                    font-family: 'Arial', sans-serif;
                    font-size: 14px;
                    background-color: #f5f5f5;
                    border-radius: 8px;
                    border: 1px solid #F44336; /* Красная рамка */
                }
                QMessageBox QLabel {
                    color: #333;
                }
                QPushButton {
                    background-color: #F44336;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #D32F2F;
                }
                QPushButton:pressed {
                    background-color: #B71C1C;
                }
                QPushButton:disabled {
                    background-color: #ccc;
                    color: #666;
                }
            """)

            message_box.setDefaultButton(no_button)
            message_box.exec()

            if message_box.clickedButton() == yes_button:
                try:
                    self.cursor.execute("DELETE FROM coaches WHERE Coach_ID=%s", (coach_id,))
                    self.conn.commit()
                    self.load_coaches()
                except mysql.connector.Error as e:
                    QMessageBox.critical(self, "Ошибка удаления данных", str(e))

    def exit_application(self):
        message_box = QMessageBox(self)
        message_box.setWindowTitle("Выход")
        message_box.setText("Вы уверены, что хотите выйти?")
        message_box.setIcon(QMessageBox.Icon.Warning)

        yes_button = message_box.addButton("Да", QMessageBox.ButtonRole.AcceptRole)
        no_button = message_box.addButton("Нет", QMessageBox.ButtonRole.RejectRole)

        # Применяем стили для сообщения
        message_box.setStyleSheet("""
            QMessageBox {
                font-family: 'Arial', sans-serif;
                font-size: 14px;
                background-color: #f5f5f5;
                border-radius: 8px;
                border: 1px solid #D32F2F; /* Красная рамка */
            }
            QMessageBox QLabel {
                color: #333;
            }
            QPushButton {
                background-color: #D32F2F;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #B71C1C;
            }
            QPushButton:pressed {
                background-color: #F44336;
            }
            QPushButton:disabled {
                background-color: #ccc;
                color: #666;
            }
        """)

        message_box.setDefaultButton(no_button)
        message_box.exec()

        if message_box.clickedButton() == yes_button:
            QApplication.quit()

    def open_main_window(self):
        from main import GlavnoeMenuTab  # Импортируем внутри функции
        self.glavnoe_menu_tab = GlavnoeMenuTab()  # Создаём экземпляр GlavnoeMenuTab
        self.glavnoe_menu_tab.show()  # Показываем GlavnoeMenuTab
        self.close()  # Закрываем текущий виджет TrenerTab

class TrenerDialog(QDialog):
    def __init__(self, data=None):
        super().__init__()

        self.setWindowTitle("Добавить/Редактировать тренера")
        self.setFixedSize(400, 400)

        # Основной layout для формы
        layout = QVBoxLayout()

        # Создаем форму с лейблами и полями ввода
        form_layout = QFormLayout()

        # Поля для ввода данных с улучшенным стилем
        self.lastname_edit = QLineEdit()
        self.lastname_edit.setPlaceholderText("Фамилия")
        self.lastname_edit.setStyleSheet("""
            QLineEdit {
                border: 2px solid #388E3C;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                font-family: 'Arial', sans-serif;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
        """)

        self.firstname_edit = QLineEdit()
        self.firstname_edit.setPlaceholderText("Имя")
        self.firstname_edit.setStyleSheet("""
            QLineEdit {
                border: 2px solid #388E3C;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                font-family: 'Arial', sans-serif;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
        """)

        self.middlename_edit = QLineEdit()
        self.middlename_edit.setPlaceholderText("Отчество")
        self.middlename_edit.setStyleSheet("""
            QLineEdit {
                border: 2px solid #388E3C;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                font-family: 'Arial', sans-serif;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
        """)

        self.birthdate_edit = QDateEdit()
        self.birthdate_edit.setDisplayFormat("dd.MM.yyyy")
        self.birthdate_edit.setDate(QDate.currentDate())
        self.birthdate_edit.setStyleSheet("""
            QDateEdit {
                border: 2px solid #388E3C;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                font-family: 'Arial', sans-serif;
            }
            QDateEdit:focus {
                border-color: #4CAF50;
            }

            /* Скрытие стрелочек */
            QDateEdit::down-button, QDateEdit::up-button {
                width: 0px;
                height: 0px;
                border: none;
                background: transparent;
            }

            /* Убираем кнопку календаря */
            QDateEdit::calendar-button {
                width: 0px;
                height: 0px;
                border: none;
                background: transparent;
            }
        """)

        self.phone_edit = QLineEdit()
        self.phone_edit.setPlaceholderText("Телефон")
        self.phone_edit.setStyleSheet("""
            QLineEdit {
                border: 2px solid #388E3C;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                font-family: 'Arial', sans-serif;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
        """)

        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("Доп. информация")
        self.email_edit.setStyleSheet("""
            QLineEdit {
                border: 2px solid #388E3C;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                font-family: 'Arial', sans-serif;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
        """)

        # Заполнение данных, если они переданы (редактирование)
        if data:
            lastname, firstname, middlename, birthdate, phone, email = data
            self.lastname_edit.setText(lastname)
            self.firstname_edit.setText(firstname)
            self.middlename_edit.setText(middlename)
            self.birthdate_edit.setDate(birthdate)
            self.phone_edit.setText(phone)
            self.email_edit.setText(email)

        # Размещение Фамилии и Имени в одной строке
        name_layout = QHBoxLayout()
        name_layout.addWidget(self.lastname_edit)
        name_layout.addWidget(self.firstname_edit)

        # Добавляем элементы на форму
        form_layout.addRow("Фамилия Имя:", name_layout)
        form_layout.addRow("Отчество:", self.middlename_edit)
        form_layout.addRow("Дата рождения:", self.birthdate_edit)
        form_layout.addRow("Телефон:", self.phone_edit)
        form_layout.addRow("Доп. информация:", self.email_edit)

        layout.addLayout(form_layout)

        # Кнопки ОК и Отмена с улучшенным стилем
        button_layout = QHBoxLayout()

        ok_button = QPushButton("ОК")
        ok_button.setStyleSheet("""
            QPushButton {
                background-color: #388E3C;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: bold;
                text-align: center;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
            }
            QPushButton:hover {
                background-color: #2C6B3D;
                transform: scale(1.05);
            }
        """)
        ok_button.clicked.connect(self.accept)

        cancel_button = QPushButton("Отмена")
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: bold;
                text-align: center;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
            }
            QPushButton:hover {
                background-color: #D32F2F;
                transform: scale(1.05);
            }
        """)
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        # Устанавливаем основной layout в окно
        self.setLayout(layout)

    def get_data(self):
        """Возвращает данные, введенные в форму."""
        return (
            self.lastname_edit.text(),
            self.firstname_edit.text(),
            self.middlename_edit.text(),
            self.birthdate_edit.text(),
            self.phone_edit.text(),
            self.email_edit.text()
        )






