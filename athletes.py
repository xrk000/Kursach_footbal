import mysql.connector
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QSpacerItem, QSizePolicy, \
    QMessageBox, QDialog, QFormLayout, QComboBox, QLineEdit, QDialogButtonBox, QApplication, QListWidgetItem, QDateEdit, \
    QTextEdit, QLabel
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, Qt, QDate


class SportsmeniTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window  # Получаем доступ к основному окну

        self.conn = None
        self.cursor = None
        self.connect_to_db()

        tab_layout = QVBoxLayout()

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
        tab_layout.addLayout(home_button_layout)

        # Список спортсменов
        self.sportsmeni_list = QListWidget()
        self.sportsmeni_list.setMinimumHeight(600)
        self.sportsmeni_list.setStyleSheet("""
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
        tab_layout.addWidget(self.sportsmeni_list)

        # Загрузка данных спортсменов
        self.load_sportsmeni_from_db()

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
        add_button.clicked.connect(self.add_sportsmeni)
        buttons_layout.addWidget(add_button)

        edit_button = QPushButton("Редактировать")
        edit_button.setStyleSheet(button_style.replace("#388E3C", "#FF9800").replace("#2C6B3D", "#F57C00"))
        edit_button.clicked.connect(self.edit_sportsmeni)
        buttons_layout.addWidget(edit_button)

        delete_button = QPushButton("Удалить")
        delete_button.setStyleSheet(button_style.replace("#388E3C", "#F44336").replace("#2C6B3D", "#D32F2F"))
        delete_button.clicked.connect(self.delete_sportsmeni)
        buttons_layout.addWidget(delete_button)

        # Добавляем пространство для выравнивания кнопок слева до середины
        buttons_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        tab_layout.addLayout(buttons_layout)

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
        tab_layout.addLayout(exit_layout)

        self.setLayout(tab_layout)

    def connect_to_db(self):
        """Подключение к базе данных"""
        try:
            self.conn = mysql.connector.connect(
                host="",
                user="",
                password="",
                database=""
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Ошибка подключения к базе данных", str(e))

    def load_sportsmeni_from_db(self):
        """Загружаем список спортсменов из базы данных"""
        self.sportsmeni_list.clear()
        try:
            query = """
                SELECT a.Athlete_ID, a.LastName, a.FirstName, a.MiddleName, a.BirthDate, a.Phone, g.Name 
                FROM athletes a
                JOIN groupsp g ON a.Group_ID = g.Group_ID
            """
            self.cursor.execute(query)
            athletes = self.cursor.fetchall()
            for row in athletes:
                athlete_id, surname, name, patronymic, birth_date, phone, group_name = row
                self.sportsmeni_list.addItem(f"{athlete_id}: {surname} {name} {patronymic} | {birth_date} | {phone} | Группа: {group_name}")
        except Exception as e:
            print(f"Error executing query: {e}")

    def add_sportsmeni(self):
        """Добавление спортсмена в базу данных"""
        dialog = SportsmeniDialog(self)
        if dialog.exec():
            surname, name, patronymic, birth_date, phone, group = dialog.get_data()
            query = """
                INSERT INTO athletes (LastName, FirstName, MiddleName, BirthDate, Phone, Group_ID) 
                VALUES (%s, %s, %s, %s, %s, (SELECT Group_ID FROM groupsp WHERE Name = %s))
            """
            self.cursor.execute(query, (surname, name, patronymic, birth_date, phone, group))
            self.conn.commit()
            self.load_sportsmeni_from_db()  # Обновляем список спортсменов

    def edit_sportsmeni(self):
        """Редактирование спортсмена"""
        try:
            current_item = self.sportsmeni_list.currentItem()
            if current_item:
                athlete_id = current_item.text().split(":")[0]
                print(athlete_id)
                dialog = SportsmeniDialog(self, athlete_id)
                if dialog.exec():
                    surname, name, patronymic, birth_date, phone, group = dialog.get_data()
                    query = """
                        UPDATE athletes 
                        SET LastName=%s, FirstName=%s, MiddleName=%s, BirthDate=%s, Phone=%s, 
                            Group_ID=(SELECT Group_ID FROM groupsp WHERE Name=%s)
                        WHERE Athlete_ID=%s
                    """
                    self.cursor.execute(query, (surname, name, patronymic, birth_date, phone, group, athlete_id))
                    self.conn.commit()
                    self.load_sportsmeni_from_db()  # Обновляем список спортсменов
        except Exception as e:
            print(f"Ошибка: {e}")
    def delete_sportsmeni(self):
        """Удаление спортсмена"""
        current_item = self.sportsmeni_list.currentItem()
        if current_item:
            athlete_id = current_item.text().split(":")[0]
            reply = QMessageBox.question(self, "Удаление спортсмена", "Вы уверены, что хотите удалить этого спортсмена?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                query = "DELETE FROM athletes WHERE Athlete_ID=%s"
                self.cursor.execute(query, (athlete_id,))
                self.conn.commit()
                self.load_sportsmeni_from_db()  # Обновляем список спортсменов

    def exit_application(self):
        """Выход из приложения"""
        reply = QMessageBox.question(self, "Выход", "Вы уверены, что хотите выйти?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            QApplication.quit()

    def open_main_window(self):
        self.main_window.show_glavnoe_menu()


class SportsmeniDialog(QDialog):
    def __init__(self, parent, athlete_id=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить/Редактировать спортсмена")
        self.setFixedSize(400, 500)
        self.setStyleSheet("background-color: #f5f5f5; font-family: Arial, sans-serif;")

        self.cursor = parent.cursor
        self.athlete_id = athlete_id

        layout = QFormLayout()

        # Поля ввода с улучшенным стилем
        self.surname_input = QLineEdit()
        self.surname_input.setPlaceholderText("Введите фамилию")
        self.surname_input.setStyleSheet("""
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

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите имя")
        self.name_input.setStyleSheet(self.surname_input.styleSheet())

        self.patronymic_input = QLineEdit()
        self.patronymic_input.setPlaceholderText("Введите отчество")
        self.patronymic_input.setStyleSheet(self.surname_input.styleSheet())

        self.birth_date_input = QDateEdit()
        self.birth_date_input.setDisplayFormat("dd.MM.yyyy")  # Устанавливаем формат даты
        self.birth_date_input.setDate(QDate.currentDate())  # Устанавливаем текущую дату по умолчанию
        self.birth_date_input.setStyleSheet("""
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

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Введите номер телефона")
        self.phone_input.setStyleSheet(self.surname_input.styleSheet())

        self.group_combobox = QComboBox()
        self.group_combobox.setStyleSheet("""
            QComboBox {
                border: 2px solid #388E3C;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                font-family: 'Arial', sans-serif;
            }
        """)

        self.load_groups()

        if athlete_id:
            self.load_athlete_data(athlete_id)

        # Размещение Фамилии и Имени в одной строке
        name_layout = QHBoxLayout()
        name_layout.addWidget(self.surname_input)
        name_layout.addWidget(self.name_input)

        layout.addRow(QLabel("Фамилия Имя:"), name_layout)  # Фамилия и Имя в одной строке
        layout.addRow(QLabel("Отчество:"), self.patronymic_input)
        layout.addRow(QLabel("Дата рождения:"), self.birth_date_input)
        layout.addRow(QLabel("Номер телефона:"), self.phone_input)
        layout.addRow(QLabel("Группа:"), self.group_combobox)

        # Кнопки с улучшенным стилем
        button_layout = QHBoxLayout()

        self.submit_button = QPushButton("Сохранить")
        self.submit_button.setStyleSheet("""
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
        self.submit_button.clicked.connect(self.accept)

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

        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(cancel_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def load_groups(self):
        """Загрузка списка групп"""
        self.cursor.execute("SELECT Name FROM groupsp")
        for row in self.cursor.fetchall():
            self.group_combobox.addItem(row[0])

    def load_athlete_data(self, athlete_id):
        """Загрузка данных спортсмена для редактирования"""
        query = "SELECT LastName, FirstName, MiddleName, BirthDate, Phone, Group_ID FROM athletes WHERE Athlete_ID=%s"
        self.cursor.execute(query, (athlete_id,))
        result = self.cursor.fetchone()
        if result:
            surname, name, patronymic, birth_date, phone, group_id = result
            self.surname_input.setText(surname)
            self.name_input.setText(name)
            self.patronymic_input.setText(patronymic)
            self.birth_date_input.setDate(birth_date)
            self.phone_input.setText(phone)
            self.set_group_combobox(group_id)

    def set_group_combobox(self, group_id):
        """Установить группу в комбобокс на основе ID"""
        for index in range(self.group_combobox.count()):
            if self.group_combobox.itemData(index) == group_id:
                self.group_combobox.setCurrentIndex(index)
                break

    def get_data(self):
        """Получить данные из формы"""
        surname = self.surname_input.text()
        name = self.name_input.text()
        patronymic = self.patronymic_input.text()
        birth_date = self.birth_date_input.date().toString("yyyy-MM-dd")
        phone = self.phone_input.text()
        group = self.group_combobox.currentText()
        return surname, name, patronymic, birth_date, phone, group

