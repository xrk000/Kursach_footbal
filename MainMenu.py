from PyQt6.QtCore import Qt, QTimer, QDateTime, QTime
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QHBoxLayout, QApplication, QPushButton
import datetime


class GlavnoeMenuTab(QWidget):
    def __init__(self, cursor):
        super().__init__()

        self.cursor = cursor  # Курсор базы данных

        # Основной layout
        main_layout = QVBoxLayout()

        # Заголовок "Тренировки"
        title_label = QLabel("Тренировки")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: white;
            text-align: center;
            text-shadow: 2px 2px 4px black;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

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

        # Список текущих тренировок
        self.current_trainings_list = QListWidget()
        self.current_trainings_list.setStyleSheet("""
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

        # Метка для текущих тренировок
        current_trainings_label = QLabel("Текущие тренировки")
        current_trainings_label.setStyleSheet("font-size: 18px; color: white; text-shadow: 2px 2px 5px black;")

        # Список прошедших и будущих тренировок
        self.past_trainings_list = QListWidget()
        self.past_trainings_list.setStyleSheet("""
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
        self.future_trainings_list = QListWidget()
        self.future_trainings_list.setStyleSheet("""
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

        # Нижняя область с двумя списками
        bottom_layout = QHBoxLayout()

        # Создаем layout для списка прошедших тренировок
        past_layout = QVBoxLayout()
        past_layout.addWidget(past_trainings_label := QLabel("Прошедшие тренировки"))
        past_layout.addWidget(self.past_trainings_list)
        past_trainings_label.setStyleSheet("font-size: 18px; color: white; text-shadow: 2px 2px 5px black;")

        # Создаем layout для списка будущих тренировок
        future_layout = QVBoxLayout()
        future_layout.addWidget(future_trainings_label := QLabel("Будущие тренировки"))
        future_layout.addWidget(self.future_trainings_list)
        future_trainings_label.setStyleSheet("font-size: 18px; color: white; text-shadow: 2px 2px 5px black;")

        bottom_layout.addLayout(past_layout)
        bottom_layout.addLayout(future_layout)

        # Добавляем все элементы в основной layout
        main_layout.addWidget(current_trainings_label)
        main_layout.addWidget(self.current_trainings_list)
        main_layout.addLayout(bottom_layout)

        # Нижняя область для времени и кнопки выхода
        bottom_left_layout = QHBoxLayout()

        # Метка времени (слева)
        self.time_label = QLabel()
        self.time_label.setStyleSheet("font-size: 18px; color: white; text-shadow: 2px 2px 5px black;")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        bottom_left_layout.addWidget(self.time_label)

        # Кнопка выхода (справа)
        bottom_left_layout.addWidget(exit_button, alignment=Qt.AlignmentFlag.AlignRight)

        # Добавляем layout для нижней области
        main_layout.addLayout(bottom_left_layout)

        # Устанавливаем основной layout
        self.setLayout(main_layout)

        # Таймер для обновления времени и списка тренировок
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_date_time)
        self.timer.timeout.connect(self.update_training_list)
        self.timer.start(1000)  # Обновление каждую секунду

        # Инициализация времени и списка тренировок
        self.update_date_time()
        self.update_training_list()

    def exit_application(self):
        """Выход из приложения"""
        QApplication.quit()

    def update_date_time(self):
        """Обновляет дату и время."""
        current_date_time = QDateTime.currentDateTime()
        self.time_label.setText(current_date_time.toString("dd.MM.yyyy HH:mm"))

    def update_training_list(self):
        """Обновляет список тренировок на сегодняшний день, разделяя их на текущие, прошедшие и будущие."""
        self.current_trainings_list.clear()
        self.past_trainings_list.clear()
        self.future_trainings_list.clear()

        current_datetime = QDateTime.currentDateTime()
        current_date = current_datetime.date().toString("yyyy-MM-dd")

        # Получаем все тренировки на текущую дату
        self.cursor.execute("""
            SELECT EventDate, EventTime, Group_ID
            FROM schedules
            WHERE EventDate = %s
        """, (current_date,))

        trainings = self.cursor.fetchall()

        if not trainings:
            self.current_trainings_list.addItem("Нет тренировок на сегодняшний день.")
            return

        current_trainings = []
        past_trainings = []
        future_trainings = []

        for training in trainings:
            event_date, event_time, group_id = training
            group_name = self.get_group_name(group_id)

            if isinstance(event_time, datetime.timedelta):
                start_hour = event_time.seconds // 3600
                start_minute = (event_time.seconds % 3600) // 60
            else:
                start_hour = int(event_time // 100)
                start_minute = int(event_time % 100)

            start_time = QTime(start_hour, start_minute)
            item_text = f"Группа: {group_name}, Начало: {start_time.toString('HH:mm')}"
            end_time = start_time.addSecs(3600)
            current_time = current_datetime.time()

            if start_time <= current_time <= end_time:
                current_trainings.append(item_text)
            elif end_time < current_time:
                past_trainings.append(item_text)
            else:
                future_trainings.append(item_text)

        if current_trainings:
            for item in current_trainings:
                self.current_trainings_list.addItem(item)
        else:
            self.current_trainings_list.addItem("Нет текущих тренировок.")

        if past_trainings:
            for item in past_trainings:
                self.past_trainings_list.addItem(item)
        else:
            self.past_trainings_list.addItem("Нет прошедших тренировок.")

        if future_trainings:
            for item in future_trainings:
                self.future_trainings_list.addItem(item)
        else:
            self.future_trainings_list.addItem("Нет будущих тренировок.")

    def get_group_name(self, group_id):
        """Получает имя группы по ID."""
        self.cursor.execute("SELECT Name FROM groupsp WHERE Group_ID = %s", (group_id,))
        result = self.cursor.fetchone()
        return result[0] if result else "Неизвестная группа"
