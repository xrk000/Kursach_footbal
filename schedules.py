import mysql.connector
import re
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QSpacerItem, QSizePolicy, \
    QMessageBox, QDialog, QFormLayout, QComboBox, QLineEdit, QDialogButtonBox, QApplication, QListWidgetItem, QDateEdit, \
    QTextEdit, QLabel
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, Qt, QDate, QTime

class RaspisanieTab(QWidget):
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
        home_button.clicked.connect(self.go_home)
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
        home_button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        home_button_layout.addWidget(home_button)
        tab_layout.addLayout(home_button_layout)

        # Горизонтальный layout для выбора даты
        date_layout = QHBoxLayout()
        self.date_picker = QDateEdit(QDate.currentDate())
        self.date_picker.setDisplayFormat("dd.MM.yyyy")
        self.date_picker.setCalendarPopup(True)
        self.date_picker.dateChanged.connect(self.load_schedules_for_selected_date)

        # Стиль для QDateEdit с увеличенной стрелочкой
        self.date_picker.setStyleSheet("""
            QDateEdit {
                background-color: #F5F5F5;
                border: 2px solid #388E3C;
                border-radius: 12px;
                padding: 5px 10px;
                font-family: 'Arial', sans-serif;
                font-size: 16px;
                position: relative;
            }

            QDateEdit::down-arrow {
                width: 20px; /* Подгоняем размеры */
                height: 20px; 
                border: none;
                background: transparent;
                image: url('arrow_down.png');
                background-repeat: no-repeat;
                background-position: center;
                margin-top: -10px; /* Мелкая настройка для выравнивания */
            }


            /* Это оставляет стандартную стрелочку видимой, но сверху будет картинка */
            QDateEdit::drop-down {
                width: 40px; /* Увеличиваем размер кнопки */
                height: 40px;
                background: transparent;
                border: none;
            }

            /* Если нужно подправить отображение всплывающего календаря */
            QDateEdit::calendar-popup {
                border-radius: 8px;
                background-color: #F5F5F5;
                border: 2px solid #388E3C;
            }
        """)

        # Добавляем текстовый лейбл и комбобокс в layout
        date_layout.addWidget(QLabel("Выберите дату:"))
        date_layout.addWidget(self.date_picker)
        tab_layout.addLayout(date_layout)

        # Список расписания
        self.schedule_list = QListWidget()
        self.schedule_list.setMinimumHeight(300)
        self.schedule_list.setStyleSheet("""
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
        tab_layout.addWidget(self.schedule_list)

        # Горизонтальный layout для кнопок (Добавить, Редактировать, Удалить)
        buttons_layout = QHBoxLayout()

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
        add_button.clicked.connect(self.add_schedule)
        buttons_layout.addWidget(add_button)

        edit_button = QPushButton("Редактировать")
        edit_button.setStyleSheet(button_style.replace("#388E3C", "#FF9800").replace("#2C6B3D", "#F57C00"))
        edit_button.clicked.connect(self.edit_schedule)
        buttons_layout.addWidget(edit_button)

        delete_button = QPushButton("Удалить")
        delete_button.setStyleSheet(button_style.replace("#388E3C", "#F44336").replace("#2C6B3D", "#D32F2F"))
        delete_button.clicked.connect(self.delete_schedule)
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

        self.load_schedules_from_db()  # Загружаем расписания при старте

    def go_home(self):
        self.main_window.show_glavnoe_menu()
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

    def load_schedules_from_db(self):
        """Загружаем список расписаний из базы данных"""
        self.schedule_list.clear()
        try:
            query = """
                SELECT s.Schedule_ID, s.EventDate, s.EventTime, g.Name, s.Venue
                FROM schedules s
                JOIN groupsp g ON s.Group_ID = g.Group_ID
            """
            self.cursor.execute(query)
            schedules = self.cursor.fetchall()
            for row in schedules:
                schedule_id, event_date, event_time, group_name, venue = row
                self.schedule_list.addItem(f"{schedule_id} | {event_date} | {event_time} | {group_name} | {venue}")
        except Exception as e:
            print(f"Error executing query: {e}")

    def load_schedules_for_selected_date(self):
        """Загружаем расписания для выбранной даты"""
        selected_date = self.date_picker.date().toString("yyyy-MM-dd")
        self.schedule_list.clear()  # Очищаем текущий список
        try:
            query = """
                SELECT s.Schedule_ID, s.EventDate, s.EventTime, g.Name, s.Venue
                FROM schedules s
                JOIN groupsp g ON s.Group_ID = g.Group_ID
                WHERE s.EventDate = %s
            """
            self.cursor.execute(query, (selected_date,))
            schedules = self.cursor.fetchall()
            for row in schedules:
                schedule_id, event_date, event_time, group_name, venue = row
                self.schedule_list.addItem(f"{schedule_id} | {event_date} | {event_time} | {group_name} | {venue}")
        except Exception as e:
            print(f"Error executing query: {e}")

    def add_schedule(self):
        """Добавить новое расписание"""
        dialog = ScheduleDialog(self)
        if dialog.exec():
            event_date, event_time, group, venue = dialog.get_data()
            query = """
                INSERT INTO schedules (EventDate, EventTime, Group_ID, Venue) 
                VALUES (%s, %s, (SELECT Group_ID FROM groupsp WHERE Name = %s), %s)
            """
            self.cursor.execute(query, (event_date, event_time, group, venue))
            self.conn.commit()
            self.load_schedules_for_selected_date()  # Обновляем список на выбранную дату

    def edit_schedule(self):
        """Редактировать выбранное расписание"""
        current_item = self.schedule_list.currentItem()
        if current_item:
            schedule_id = current_item.text()[0]
            dialog = ScheduleDialog(self, schedule_id)
            if dialog.exec():
                event_date, event_time, group, venue = dialog.get_data()

                # Преобразование QDate в строку формата YYYY-MM-DD
                if isinstance(event_date, QDate):
                    event_date = event_date.toString("yyyy-MM-dd")

                # Преобразование QTime в строку формата HH:MM:SS
                if isinstance(event_time, QTime):
                    event_time = event_time.toString("HH:mm:ss")

                try:
                    query = """
                        UPDATE schedules
                        SET EventDate=%s, EventTime=%s, Group_ID=(SELECT Group_ID FROM groupsp WHERE Name=%s), Venue=%s
                        WHERE Schedule_ID=%s
                    """
                    schedule_id = schedule_id[0]
                    print(schedule_id)
                    self.cursor.execute(query, (event_date, event_time, group, venue, schedule_id))
                    self.conn.commit()

                    # Обновляем список расписаний
                    self.load_schedules_for_selected_date()
                except mysql.connector.Error as e:
                    QMessageBox.critical(self, "Ошибка базы данных",
                                         f"Произошла ошибка при обновлении расписания:\n{e}")
                except Exception as e:
                    QMessageBox.critical(self, "Неизвестная ошибка", f"Произошла ошибка:\n{e}")


    def delete_schedule(self):
        """Удалить выбранное расписание"""
        current_item = self.schedule_list.currentItem()
        if current_item:
            try:
                # Получение текста элемента
                item_text = current_item.text()
                print(f"Текст текущего элемента: {item_text}")

                # Попытка извлечь идентификатор с помощью регулярных выражений
                match = re.match(r'^\d+', item_text)  # Ищем число в начале строки
                if not match:
                    raise ValueError("Не удалось найти идентификатор расписания.")

                schedule_id = match.group()  # Получаем найденный идентификатор
                print(f"Извлеченный Schedule_ID: {schedule_id}")

                # Проверка, что schedule_id является числом
                if not schedule_id.isdigit():
                    raise ValueError("Неверный формат идентификатора расписания. Ожидалось число.")

                # Выполнение запроса
                query = "DELETE FROM schedules WHERE Schedule_ID = %s"
                self.cursor.execute(query, (schedule_id,))
                self.conn.commit()

                QMessageBox.information(self, "Успех", f"Расписание с ID {schedule_id} успешно удалено.")
                self.load_schedules_for_selected_date()  # Обновляем список на выбранную дату
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при удалении расписания: {e}")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {e}")
        else:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, выберите расписание для удаления.")

    def exit_application(self):
        """Обработчик кнопки выхода с подтверждением"""
        reply = QMessageBox.question(self, "Выход", "Вы уверены, что хотите выйти?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            QApplication.quit()


class ScheduleDialog(QDialog):
    def __init__(self, parent, schedule_id=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить/Редактировать занятие")
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: #f5f5f5; font-family: Arial, sans-serif;")

        self.cursor = parent.cursor
        self.schedule_id = schedule_id

        layout = QFormLayout()

        # Поле для выбора даты
        self.date_picker = QDateEdit(QDate.currentDate())
        self.date_picker.setDisplayFormat("dd.MM.yyyy")
        self.date_picker.setCalendarPopup(True)
        self.date_picker.setStyleSheet("""
            QDateEdit {
                border: 2px solid #388E3C;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                font-family: 'Arial', sans-serif;
            }
        """)

        # Поле для ввода времени с маской
        self.time_input = QLineEdit()
        self.time_input.setInputMask("00:00")  # Устанавливаем маску формата HH:MM
        self.time_input.setPlaceholderText("Введите время (например, 14:30)")
        self.time_input.setStyleSheet("""
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

        self.group_combobox = QComboBox()
        self.group_combobox.setStyleSheet("""
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
        self.load_groups()

        self.place_input = QLineEdit()
        self.place_input.setPlaceholderText("Введите место проведения")
        self.place_input.setStyleSheet(self.time_input.styleSheet())

        if schedule_id:
            self.load_schedule_data(schedule_id)

        layout.addRow(QLabel("Дата:"), self.date_picker)
        layout.addRow(QLabel("Время:"), self.time_input)
        layout.addRow(QLabel("Группа:"), self.group_combobox)
        layout.addRow(QLabel("Место проведения:"), self.place_input)

        # Кнопки с улучшенным стилем
        button_layout = QHBoxLayout()
        self.submit_button = self.create_button("Сохранить", "#4CAF50", "#388E3C", self.accept)
        cancel_button = self.create_button("Отмена", "#F44336", "#D32F2F", self.reject)

        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(cancel_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def create_button(self, text, bg_color, hover_color, handler):
        """Создает кнопку с заданным стилем"""
        button = QPushButton(text)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: bold;
                text-align: center;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
            }}
            QPushButton:hover {{
                background-color: {hover_color};
                transform: scale(1.05);
            }}
        """)
        button.clicked.connect(handler)
        return button

    def load_groups(self):
        """Загрузка списка групп"""
        self.cursor.execute("SELECT Name FROM groupsp")
        for row in self.cursor.fetchall():
            self.group_combobox.addItem(row[0])

    def load_schedule_data(self, schedule_id):
        """Загрузка данных занятия для редактирования"""
        query = "SELECT EventDate, EventTime, Group_ID, Venue FROM schedules WHERE Schedule_ID=%s"
        self.cursor.execute(query, (schedule_id,))
        result = self.cursor.fetchone()
        if result:
            event_date, event_time, group_id, venue = result
            self.date_picker.setDate(QDate.fromString(event_date, "yyyy-MM-dd"))
            self.time_input.setText(event_time)
            self.set_group_combobox(group_id)
            self.place_input.setText(venue)

    def set_group_combobox(self, group_id):
        """Установить группу в комбобокс на основе ID"""
        for index in range(self.group_combobox.count()):
            if self.group_combobox.itemData(index) == group_id:
                self.group_combobox.setCurrentIndex(index)
                break

    def get_data(self):
        """Получить данные из формы"""
        event_date = self.date_picker.date().toString("yyyy-MM-dd")
        event_time = self.time_input.text()
        group = self.group_combobox.currentText()
        venue = self.place_input.text()
        return event_date, event_time, group, venue
