import mysql.connector
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QSpacerItem, QSizePolicy, \
    QMessageBox, QDialog, QFormLayout, QComboBox, QLineEdit, QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize


class GruppiTab(QWidget):
    def __init__(self,main_window):
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

        # Разделитель с двумя списками
        splitter_layout = QHBoxLayout()

        self.gruppi_list_left = QListWidget()
        self.gruppi_list_left.setMinimumHeight(600)
        self.gruppi_list_left.setStyleSheet("""
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
        self.gruppi_list_left.itemClicked.connect(self.on_group_selected)
        splitter_layout.addWidget(self.gruppi_list_left)

        self.gruppi_list_right = QListWidget()
        self.gruppi_list_right.setMinimumHeight(600)
        self.gruppi_list_right.setStyleSheet("""
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
                background-color: #FF9800;
                color: white;
            }
            QListWidget::item:selected {
                background-color: #FF5722;
                color: white;
            }
        """)
        splitter_layout.addWidget(self.gruppi_list_right)

        tab_layout.addLayout(splitter_layout)

        # Горизонтальный layout для кнопок
        buttons_layout = QHBoxLayout()

        add_button = QPushButton('Добавить')
        add_button.setStyleSheet("""
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
        add_button.clicked.connect(self.add_gruppi)

        edit_button = QPushButton('Редактировать')
        edit_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
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
                background-color: #F57C00;
                transform: scale(1.05);
            }
        """)
        edit_button.clicked.connect(self.edit_gruppi)

        delete_button = QPushButton('Удалить')
        delete_button.setStyleSheet("""
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
        delete_button.clicked.connect(self.delete_gruppi)

        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(edit_button)
        buttons_layout.addWidget(delete_button)
        buttons_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        tab_layout.addLayout(buttons_layout)

        # Кнопка выхода
        exit_button = QPushButton("Выход")
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: #D32F2F;
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
                background-color: #B71C1C;
                transform: scale(1.05);
            }
        """)
        exit_button.clicked.connect(self.exit_application)
        exit_layout = QHBoxLayout()
        exit_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        exit_layout.addWidget(exit_button)
        tab_layout.addLayout(exit_layout)

        self.setLayout(tab_layout)

        self.load_groups_from_db()


    def on_group_selected(self):
        """Обрабатываем выбор группы в левом списке и загружаем спортсменов"""
        current_item = self.gruppi_list_left.currentItem()
        if current_item:
            group_id = current_item.text().split(":")[0]
            self.load_athletes_for_group(group_id)

    def load_athletes_for_group(self, group_id):
        """Загружаем список спортсменов для выбранной группы"""
        self.gruppi_list_right.clear()
        try:
            query = """
                   SELECT a.Athlete_ID, a.LastName, a.FirstName, a.MiddleName
                   FROM athletes a
                   WHERE a.Group_ID = %s
               """
            self.cursor.execute(query, (group_id,))
            athletes = self.cursor.fetchall()
            for athlete_id, last_name, first_name, middle_name in athletes:
                self.gruppi_list_right.addItem(f"{athlete_id}: {last_name} {first_name} {middle_name}")
        except Exception as e:
            print(f"Error loading athletes: {e}")

    def connect_to_db(self):
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

    def load_groups_from_db(self):
        self.gruppi_list_left.clear()
        self.gruppi_list_right.clear()  # правая таблица всё равно остаётся пустой
        try:
            query = """
                SELECT g.Group_ID, g.Name, 
                       CONCAT(c.LastName, ' ', c.FirstName) AS CoachName, 
                       s.Nameee AS SectionName
                FROM groupsp g
                LEFT JOIN coaches c ON g.Coach_ID = c.Coach_ID
                LEFT JOIN sections s ON g.Section_ID = s.Section_ID
            """
            self.cursor.execute(query)
            groups = self.cursor.fetchall()
            for row in groups:
                group_id, group_name, coach_name, section_name = row
                self.gruppi_list_left.addItem(f"{group_id}: {group_name} | {section_name} | {coach_name}")
        except Exception as e:
            print(f"Error executing query: {e}")

    def add_gruppi(self):
        dialog = GruppiDialog(self, self.cursor)
        if dialog.exec():
            group_name, section_id, coach_id = dialog.get_data()
            query = "INSERT INTO groupsp (Name, Section_ID, Coach_ID) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (group_name, section_id, coach_id))
            self.conn.commit()
            self.load_groups_from_db()  # Обновляем список групп

    def edit_gruppi(self):
        current_item = self.gruppi_list_left.currentItem()
        if current_item:
            group_id = current_item.text().split(":")[0]
            dialog = GruppiDialog(self, self.cursor, group_id)
            if dialog.exec():
                group_name, section_id, coach_id = dialog.get_data()
                query = "UPDATE groupsp SET Name=%s, Section_ID=%s, Coach_ID=%s WHERE Group_ID=%s"
                self.cursor.execute(query, (group_name, section_id, coach_id, group_id))
                self.conn.commit()
                self.load_groups_from_db()  # Обновляем список групп

    def delete_gruppi(self):
        """Обработчик кнопки удаления группы с подтверждением"""
        current_item = self.gruppi_list_left.currentItem()
        if current_item:
            group_id = current_item.text().split(":")[0]
            reply = QMessageBox.question(self, "Удаление группы", "Вы уверены, что хотите удалить эту группу?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                query = "DELETE FROM groupsp WHERE Group_ID=%s"
                self.cursor.execute(query, (group_id,))
                self.conn.commit()
                self.load_groups_from_db()  # Обновляем список групп

    def exit_application(self):
        """Обработчик кнопки выхода с подтверждением"""
        reply = QMessageBox.question(self, "Выход", "Вы уверены, что хотите выйти?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            QApplication.quit()

    def open_main_window(self):
        self.main_window.show_glavnoe_menu()

class GruppiDialog(QDialog):
    def __init__(self, parent, cursor, group_id=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить/Редактировать группу")
        self.setFixedSize(400, 300)

        self.cursor = cursor
        self.group_id = group_id

        layout = QVBoxLayout()

        # Основной layout для формы
        form_layout = QFormLayout()

        # Поля ввода
        self.group_name_input = QLineEdit()
        self.group_name_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #388E3C;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                font-family: 'Arial', sans-serif;
                background-color: #F9F9F9;
            }
            QLineEdit:focus {
                border-color: #FF9800;
            }
        """)

        self.section_combobox = QComboBox()
        self.section_combobox.setStyleSheet("""
            QComboBox {
                border: 2px solid #388E3C;
                border-radius: 8px;
                padding: 8px;
                font-size: 16px;
                font-family: 'Arial', sans-serif;
                background-color: #F9F9F9;
            }
            QComboBox:focus {
                border-color: #FF9800;
            }
        """)

        self.trainer_combobox = QComboBox()
        self.trainer_combobox.setStyleSheet("""
            QComboBox {
                border: 2px solid #388E3C;
                border-radius: 8px;
                padding: 8px;
                font-size: 16px;
                font-family: 'Arial', sans-serif;
                background-color: #F9F9F9;
            }
            QComboBox:focus {
                border-color: #FF9800;
            }
        """)

        # Заполнение комбобоксов
        self.load_sections()
        self.load_trainers()

        if group_id:
            self.load_group_data(group_id)

        # Добавление полей в форму
        form_layout.addRow("Название группы", self.group_name_input)
        form_layout.addRow("Секция", self.section_combobox)
        form_layout.addRow("Тренер", self.trainer_combobox)

        layout.addLayout(form_layout)

        # Кнопки
        button_layout = QHBoxLayout()
        submit_button = QPushButton("Сохранить")
        submit_button.setStyleSheet("""
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
        submit_button.clicked.connect(self.accept)

        cancel_button = QPushButton("Отмена")
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #D32F2F;
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
                background-color: #B71C1C;
                transform: scale(1.05);
            }
        """)
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(submit_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def load_sections(self):
        """Загружает данные секций из базы данных"""
        self.cursor.execute("SELECT Section_ID, Nameee FROM sections")
        for section_id, name in self.cursor.fetchall():
            self.section_combobox.addItem(name, section_id)

    def load_trainers(self):
        """Загружает данные тренеров из базы данных"""
        self.cursor.execute("SELECT Coach_ID, LastName, FirstName FROM coaches")
        for coach_id, lastname, firstname in self.cursor.fetchall():
            display_name = f"{lastname} {firstname}"
            self.trainer_combobox.addItem(display_name, coach_id)

    def load_group_data(self, group_id):
        """Загружает данные группы из базы данных для редактирования"""
        query = "SELECT Name, Section_ID, Coach_ID FROM groupsp WHERE Group_ID=%s"
        self.cursor.execute(query, (group_id,))
        name, section_id, coach_id = self.cursor.fetchone()
        self.group_name_input.setText(name)
        self.section_combobox.setCurrentIndex(self.section_combobox.findData(section_id))
        self.trainer_combobox.setCurrentIndex(self.trainer_combobox.findData(coach_id))

    def get_data(self):
        """Возвращает данные введенные в форму"""
        group_name = self.group_name_input.text()
        section_id = self.section_combobox.currentData()
        coach_id = self.trainer_combobox.currentData()
        return group_name, section_id, coach_id
