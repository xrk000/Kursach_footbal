import mysql.connector
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QListWidget, QLabel, QTableWidget, \
    QTableWidgetItem, QCheckBox, QPushButton, QSpacerItem, QSizePolicy, QApplication, QMessageBox
from PyQt6.QtCore import QDate, QSize


class PoseshhenieTab(QWidget):
    def __init__(self,main_window):
        super().__init__()
        self.main_window = main_window  # Получаем доступ к основному окну

        self.conn = None
        self.cursor = None
        self.connect_to_db()

        # Устанавливаем общий стиль для виджета
        self.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
            }

            QLabel {
                background-color: #FFFFFF;
                font-size: 20px;
                font-weight: bold;
                color: #000000;
                padding: 5px;
                border-radius: 10px;
                margin: 5px;
            }

            QComboBox {
                background-color: #FFFFFF;
                border: 2px solid #388E3C;
                border-radius: 8px;
                padding: 5px;
                color: black;
                font-size: 16px;
            }
            QComboBox QAbstractItemView {
                background-color: #EDF2F4;
                selection-background-color: #EF233C;
                selection-color: white;
            }

            QListWidget {
                border: 2px solid #388E3C;
                border-radius: 10px;
                background-color: #FFFFFF;
                color: black;
                padding: 5px;
                font-size: 14px;
            }

            QListWidget::item {
                padding: 8px;
                border-radius: 6px;
            }
            QListWidget::item:hover {
                background-color: #4CAF50;
                color: white;
            }
            QListWidget::item:selected {
                background-color: #FF9800;
                color: white;
            }

            QTableWidget {
                border: 2px solid #388E3C;
                border-radius: 10px;
                background-color: #EDF2F4;
                gridline-color: #388E3C;
                font-size: 14px;
                color: black;
            }
            QHeaderView::section {
                background-color: #C8CED7;
                font-weight: bold;
                color: white;
                padding: 5px;
                border: none;
                border-bottom: 2px solid #388E3C;
            }

            QPushButton {
                background-color: #EF233C;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
                text-align: center;
                transition: background-color 0.3s ease;
            }
            QPushButton:hover {
                background-color: #D90429;
            }
            QPushButton:pressed {
                background-color: #8D99AE;
            }
        """)

        # Основной вертикальный layout
        main_layout = QVBoxLayout()

        # Верхний layout с кнопкой "домик"
        top_buttons_layout = QHBoxLayout()
        top_buttons_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        home_button = QPushButton()
        home_button.setIcon(QIcon('home.png'))  # Путь к иконке "домик"
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
        top_buttons_layout.addWidget(home_button)

        main_layout.addLayout(top_buttons_layout)

        # Основное содержимое
        tab_layout = QHBoxLayout()

        # Левая часть
        left_layout = QVBoxLayout()

        # Комбобокс для выбора группы
        group_layout = QVBoxLayout()
        self.group_combo = QComboBox()
        self.group_combo.addItem("")
        self.load_groups()
        self.group_combo.currentTextChanged.connect(self.update_group_selection)
        group_layout.addWidget(QLabel('Выберите группу:'))
        group_layout.addWidget(self.group_combo)
        left_layout.addLayout(group_layout)

        # Список спортсменов
        athlete_layout = QVBoxLayout()
        self.athlete_list = QListWidget()
        self.athlete_list.itemSelectionChanged.connect(self.update_athlete_selection)
        athlete_layout.addWidget(QLabel('Спортсмены:'))
        athlete_layout.addWidget(self.athlete_list)
        left_layout.addLayout(athlete_layout)

        tab_layout.addLayout(left_layout)

        # Правая часть
        right_layout = QVBoxLayout()

        # Создаем горизонтальный layout для "Процент посещения" и значения
        attendance_layout = QHBoxLayout()

        # Лейбл для процента посещения
        self.attendance_label = QLabel("Процент посещения:")
        self.attendance_label.setStyleSheet("font-size: 18px; color: black; text-shadow: 2px 2px 5px black;")

        # Лейбл с процентом посещения
        self.attendance_percentage = QLabel("0%")
        self.attendance_percentage.setStyleSheet("""
                background-color: white;
                font-size: 24px;
                font-weight: bold;
                color: black;
                padding: 5px;
                border-radius: 8px;
        """)

        # Добавляем элементы в горизонтальный layout
        attendance_layout.addWidget(self.attendance_label)
        attendance_layout.addWidget(self.attendance_percentage)

        # Добавляем горизонтальный layout в правую часть
        right_layout.addLayout(attendance_layout)

        # Таблица
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Дата", "Время", "Место", "Присутствие"])
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        right_layout.addWidget(self.table_widget)

        tab_layout.addLayout(right_layout)
        main_layout.addLayout(tab_layout)

        # Нижняя кнопка "выход"
        bottom_buttons_layout = QHBoxLayout()
        bottom_buttons_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        exit_button = QPushButton("Выход")
        exit_button.clicked.connect(self.exit_application)
        bottom_buttons_layout.addWidget(exit_button)

        main_layout.addLayout(bottom_buttons_layout)

        self.setLayout(main_layout)

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
            print(f"Ошибка подключения к базе данных: {e}")

    def load_groups(self):
        """Загрузка списка групп из базы данных в комбобокс"""
        query = "SELECT Group_ID, Name FROM groupsp"
        self.cursor.execute(query)
        groups = self.cursor.fetchall()
        for group in groups:
            group_id, group_name = group
            self.group_combo.addItem(group_name, group_id)  # Добавляем название группы и её ID

    def update_group_selection(self):
        """Обновить данные при выборе группы"""
        self.load_athletes_for_group()

    def load_athletes_for_group(self):
        """Загрузка спортсменов для выбранной группы"""
        selected_group_name = self.group_combo.currentText()

        if selected_group_name == "Выберите группу":
            self.athlete_list.clear()
            return  # Если не выбрана группа, не загружать спортсменов.

        self.athlete_list.clear()  # Очищаем список спортсменов

        # Загружаем спортсменов из выбранной группы
        query = """
            SELECT a.Athlete_ID, a.LastName, a.FirstName
            FROM athletes a
            JOIN groupsp g ON a.Group_ID = g.Group_ID
            WHERE g.Name = %s
        """
        self.cursor.execute(query, (selected_group_name,))
        athletes = self.cursor.fetchall()

        # Добавляем спортсменов в список
        for athlete in athletes:
            athlete_id, last_name, first_name = athlete
            self.athlete_list.addItem(f"{last_name} {first_name} (ID: {athlete_id})")

    def update_athlete_selection(self):
        """Обновить список тренировок при выборе спортсмена"""
        selected_item = self.athlete_list.currentItem()
        if not selected_item:
            self.table_widget.setRowCount(0)
            self.attendance_percentage.setText("0%")
            return

        athlete_name = selected_item.text()
        athlete_id = int(athlete_name.split("(ID: ")[1].strip(")"))

        # Загрузить тренировки группы, к которой относится спортсмен
        self.load_schedule_for_athlete(athlete_id)

        # Рассчитать процент посещения
        self.calculate_attendance_percentage(athlete_id)

    def load_schedule_for_athlete(self, athlete_id):
        """Загрузка расписания тренировок для группы выбранного спортсмена"""
        selected_group_name = self.group_combo.currentText()

        if selected_group_name == "Выберите группу":
            self.table_widget.setRowCount(0)
            return

        # Вычисляем дату недели назад
        one_week_ago = QDate.currentDate().addDays(-7).toString("yyyy-MM-dd")

        # Очищаем таблицу
        self.table_widget.setRowCount(0)

        query = """
            SELECT s.EventDate, s.EventTime, s.Venue, s.Schedule_ID,
                   IFNULL(a.Presence, 0) AS Presence
            FROM schedules s
            LEFT JOIN attendance a ON s.Schedule_ID = a.Schedule_ID AND a.Athlete_ID = %s
            WHERE s.Group_ID = (SELECT Group_ID FROM athletes WHERE Athlete_ID = %s)
              AND s.EventDate >= %s
        """
        try:
            self.cursor.execute(query, (athlete_id, athlete_id, one_week_ago))
            schedules = self.cursor.fetchall()

            # Заполняем таблицу
            for row_num, schedule in enumerate(schedules):
                event_date, event_time, venue, schedule_id, presence = schedule
                self.table_widget.insertRow(row_num)
                self.table_widget.setItem(row_num, 0, QTableWidgetItem(str(event_date)))
                self.table_widget.setItem(row_num, 1, QTableWidgetItem(str(event_time)))
                self.table_widget.setItem(row_num, 2, QTableWidgetItem(str(venue)))

                # Добавляем чекбокс для отметки присутствия
                presence_checkbox = QCheckBox()
                presence_checkbox.setChecked(presence == 1)
                presence_checkbox.stateChanged.connect(
                    lambda state, row=row_num, schedule_id=schedule_id: self.save_attendance(state, row, schedule_id,
                                                                                            athlete_id))
                self.table_widget.setCellWidget(row_num, 3, presence_checkbox)

        except Exception as e:
            print(f"Error loading schedule for athlete: {e}")

    def calculate_attendance_percentage(self, athlete_id):
        """Вычисление процента посещения спортсмена за последнюю неделю."""
        selected_group_name = self.group_combo.currentText()

        if selected_group_name == "Выберите группу":
            self.attendance_percentage.setText("0%")
            return

        # Вычисляем дату недели назад
        one_week_ago = QDate.currentDate().addDays(-7).toString("yyyy-MM-dd")

        try:
            # Считаем общее количество тренировок
            query_total = """
                SELECT COUNT(*)
                FROM schedules
                WHERE Group_ID = (SELECT Group_ID FROM athletes WHERE Athlete_ID = %s)
                  AND EventDate >= %s
            """
            self.cursor.execute(query_total, (athlete_id, one_week_ago))
            total_sessions = self.cursor.fetchone()[0]

            # Считаем количество посещений
            query_attended = """
                SELECT COUNT(*)
                FROM attendance
                WHERE Athlete_ID = %s
                  AND AttendanceDate >= %s
                  AND Presence = 1
            """
            self.cursor.execute(query_attended, (athlete_id, one_week_ago))
            attended_sessions = self.cursor.fetchone()[0]

            # Вычисляем процент посещения
            if total_sessions > 0:
                percentage = (attended_sessions / total_sessions) * 100
            else:
                percentage = 0

            # Обновляем лейбл с процентом
            self.attendance_percentage.setText(f"{int(percentage)}%")
        except Exception as e:
            print(f"Ошибка при расчете процента посещения: {e}")
            self.attendance_percentage.setText("Ошибка")

    def save_attendance(self, state, row, schedule_id, athlete_id):
        """Сохранение данных о посещаемости в базу данных"""
        attendance_date = self.table_widget.item(row, 0).text()  # Берём дату из таблицы
        presence = 1 if state == 2 else 0  # Если чекбокс установлен, сохраняем 1 (присутствует)

        try:
            # Проверяем, есть ли запись о посещаемости
            query_check = """
                SELECT COUNT(*) FROM attendance
                WHERE AttendanceDate = %s AND Athlete_ID = %s AND Schedule_ID = %s
            """
            self.cursor.execute(query_check, (attendance_date, athlete_id, schedule_id))
            exists = self.cursor.fetchone()[0]

            if exists:
                # Обновляем запись
                query_update = """
                    UPDATE attendance
                    SET Presence = %s
                    WHERE AttendanceDate = %s AND Athlete_ID = %s AND Schedule_ID = %s
                """
                self.cursor.execute(query_update, (presence, attendance_date, athlete_id, schedule_id))
            else:
                # Добавляем новую запись
                query_insert = """
                    INSERT INTO attendance (AttendanceDate, Athlete_ID, Presence, Schedule_ID)
                    VALUES (%s, %s, %s, %s)
                """
                self.cursor.execute(query_insert, (attendance_date, athlete_id, presence, schedule_id))

            self.conn.commit()
            print(f"Данные о посещаемости для спортсмена ID {athlete_id} на тренировке ID {schedule_id} сохранены.")
        except Exception as e:
            print(f"Ошибка при сохранении данных о посещаемости: {e}")

    def exit_application(self):
        """Обработчик кнопки выхода с подтверждением"""
        reply = QMessageBox.question(self, "Выход", "Вы уверены, что хотите выйти?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            QApplication.quit()

    def open_main_window(self):
        self.main_window.show_glavnoe_menu()

