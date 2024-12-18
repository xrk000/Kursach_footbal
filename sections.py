import mysql.connector
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QSpacerItem, QSizePolicy, \
    QMessageBox, QDialog, QFormLayout, QComboBox, QLineEdit, QDialogButtonBox, QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, Qt

class AddSectionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить секцию")
        self.setFixedSize(300, 200)

        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.year_input = QLineEdit()
        self.gender_input = QComboBox()
        self.gender_input.addItems(["Мужской", "Женский"])

        form_layout.addRow("Название:", self.name_input)
        form_layout.addRow("Год рождения:", self.year_input)
        form_layout.addRow("Пол:", self.gender_input)

        buttons = QHBoxLayout()
        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)
        buttons.addWidget(save_button)
        buttons.addWidget(cancel_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(buttons)

        self.setLayout(main_layout)

    def get_data(self):
        return self.name_input.text(), self.year_input.text(), self.gender_input.currentText()

class EditSectionDialog(QDialog):
    def __init__(self, name, year, gender):
        super().__init__()
        self.setWindowTitle("Редактировать секцию")
        self.setFixedSize(300, 200)

        form_layout = QFormLayout()

        self.name_input = QLineEdit(name)
        self.year_input = QLineEdit(year)
        self.gender_input = QComboBox()
        self.gender_input.addItems(["Мужской", "Женский"])
        self.gender_input.setCurrentText(gender)

        form_layout.addRow("Название:", self.name_input)
        form_layout.addRow("Год рождения:", self.year_input)
        form_layout.addRow("Пол:", self.gender_input)

        buttons = QHBoxLayout()
        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)
        buttons.addWidget(save_button)
        buttons.addWidget(cancel_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(buttons)

        self.setLayout(main_layout)

    def get_data(self):
        return self.name_input.text(), self.year_input.text(), self.gender_input.currentText()

class SekciiTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        home_button_layout = QHBoxLayout()
        home_button = QPushButton()
        home_button.setIcon(QIcon('img.png'))
        home_button.setIconSize(QSize(30, 30))
        home_button.setStyleSheet("""QPushButton {background-color: #E0E0E0; border: none; border-radius: 8px; padding: 5px;}""")
        home_button.clicked.connect(self.open_main_window)
        home_button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        home_button_layout.addWidget(home_button)
        layout.addLayout(home_button_layout)

        splitter_layout = QHBoxLayout()

        self.sekcii_list_left = QListWidget()
        self.sekcii_list_left.setMinimumHeight(600)
        splitter_layout.addWidget(self.sekcii_list_left)

        self.sekcii_list_right = QListWidget()
        self.sekcii_list_right.setMinimumHeight(600)
        splitter_layout.addWidget(self.sekcii_list_right)

        layout.addLayout(splitter_layout)

        buttons_layout = QHBoxLayout()
        add_button = QPushButton('Добавить')
        add_button.setStyleSheet("""QPushButton {background-color: #E57373; color: white; border: none; border-radius: 8px; padding: 10px 20px;}""")
        add_button.clicked.connect(self.show_add_sekcii_dialog)
        buttons_layout.addWidget(add_button)

        edit_button = QPushButton('Редактировать')
        edit_button.setStyleSheet("""QPushButton {background-color: #FF9800; color: white; border: none; border-radius: 8px; padding: 10px 20px;}""")
        edit_button.clicked.connect(self.show_edit_sekcii_dialog)
        buttons_layout.addWidget(edit_button)

        delete_button = QPushButton('Удалить')
        delete_button.setStyleSheet("""QPushButton {background-color: #F44336; color: white; border: none; border-radius: 8px; padding: 10px 20px;}""")
        delete_button.clicked.connect(self.delete_sekcii)
        buttons_layout.addWidget(delete_button)

        layout.addLayout(buttons_layout)

        exit_button = QPushButton("Выход")
        exit_button.clicked.connect(self.exit_application)
        exit_button.setStyleSheet("""QPushButton {background-color: #E57373; color: white; border: none; border-radius: 8px; padding: 10px 20px;}""")
        exit_layout = QHBoxLayout()
        exit_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        exit_layout.addWidget(exit_button)
        layout.addLayout(exit_layout)

        self.setLayout(layout)

        self.connect_to_db()
        self.load_sections_from_db()

    def connect_to_db(self):
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

    def load_sections_from_db(self):
        self.sekcii_list_left.clear()
        try:
            self.cursor.execute("SELECT Nameee, BirthYear, Gender FROM sections")
            rows = self.cursor.fetchall()
            for row in rows:
                name, year, gender = row
                self.sekcii_list_left.addItem(f"{name} ({year}, {gender})")
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Ошибка загрузки данных", str(e))

    def add_section_to_db(self, name, year, gender):
        try:
            query = "INSERT INTO sections (Nameee, BirthYear, Gender) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (name, year, gender))
            self.conn.commit()
            self.load_sections_from_db()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Ошибка добавления данных", str(e))

    def edit_section_in_db(self, name, year, gender):
        current_item = self.sekcii_list_left.currentItem()
        if current_item:
            old_name = current_item.text().split(' (')[0]
            try:
                query = "UPDATE sections SET Nameee = %s, BirthYear = %s, Gender = %s WHERE Nameee = %s"
                self.cursor.execute(query, (name, year, gender, old_name))
                self.conn.commit()
                self.load_sections_from_db()
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка редактирования данных", str(e))

    def delete_sekcii(self):
        current_item = self.sekcii_list_left.currentItem()
        if current_item:
            name = current_item.text().split(' (')[0]
            try:
                reply = QMessageBox.question(self, "Удаление секции", f"Вы уверены, что хотите удалить секцию '{name}'?",
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if reply == QMessageBox.StandardButton.Yes:
                    query = "DELETE FROM sections WHERE Nameee = %s"
                    self.cursor.execute(query, (name,))
                    self.conn.commit()
                    self.load_sections_from_db()
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка удаления данных", str(e))

    def show_add_sekcii_dialog(self):
        dialog = AddSectionDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name, year, gender = dialog.get_data()
            try:
                year = int(year)
                self.add_section_to_db(name, year, gender)
            except ValueError:
                QMessageBox.critical(self, "Ошибка", "Год рождения должен быть числом!")

    def show_edit_sekcii_dialog(self):
        current_item = self.sekcii_list_left.currentItem()
        if current_item:
            name, rest = current_item.text().split(" (", 1)
            year, gender = rest.rstrip(")").split(", ")
            dialog = EditSectionDialog(name, year, gender)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                new_name, new_year, new_gender = dialog.get_data()
                try:
                    new_year = int(new_year)
                    self.edit_section_in_db(new_name, new_year, new_gender)
                except ValueError:
                    QMessageBox.critical(self, "Ошибка", "Год рождения должен быть числом!")

    def exit_application(self):
        QApplication.quit()

    def open_main_window(self):
        print("Открытие главного окна")
