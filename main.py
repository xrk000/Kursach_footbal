import sys
import mysql.connector
from PyQt6.QtWidgets import QApplication, QWidget, QTabWidget, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, \
    QPushButton, QSpacerItem, QSizePolicy, QInputDialog, QDialogButtonBox, QDialog, QComboBox, QLineEdit, QDateEdit, \
    QTextEdit, QFormLayout
from PyQt6.QtCore import Qt, QSize, QDate
from PyQt6.QtGui import QIcon



class AddSekciiDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Добавить новую секцию')
        self.setMinimumWidth(300)

        # Основной layout для окна
        layout = QVBoxLayout()

        # Создаём метки и поля ввода
        self.name_label = QLabel('Название секции:')
        self.name_input = QLineEdit()

        self.trainer_label = QLabel('Тренер:')
        self.trainer_input = QLineEdit()

        self.group_label = QLabel('Группа:')
        self.group_input = QComboBox()
        self.group_input.addItems(['Группа 1', 'Группа 2', 'Группа 3'])  # Пример групп

        # Добавляем метки и поля ввода в layout
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.trainer_label)
        layout.addWidget(self.trainer_input)
        layout.addWidget(self.group_label)
        layout.addWidget(self.group_input)

        # Кнопки "Добавить" и "Отмена"
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)

        self.setLayout(layout)

    def get_data(self):
        """Возвращает данные из полей ввода"""
        return self.name_input.text(), self.trainer_input.text(), self.group_input.currentText()
class EditSekciiDialog(QDialog):
    def __init__(self, name='', trainer='', group=''):
        super().__init__()

        self.setWindowTitle('Редактировать секцию')
        self.setMinimumWidth(300)

        # Основной layout для окна
        layout = QVBoxLayout()

        # Создаём метки и поля ввода
        self.name_label = QLabel('Название секции:')
        self.name_input = QLineEdit(name)

        self.trainer_label = QLabel('Тренер:')
        self.trainer_input = QLineEdit(trainer)

        self.group_label = QLabel('Группа:')
        self.group_input = QComboBox()
        self.group_input.addItems(['Группа 1', 'Группа 2', 'Группа 3'])  # Пример групп
        self.group_input.setCurrentText(group)

        # Добавляем метки и поля ввода в layout
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.trainer_label)
        layout.addWidget(self.trainer_input)
        layout.addWidget(self.group_label)
        layout.addWidget(self.group_input)

        # Кнопки "Сохранить" и "Отмена"
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)

        self.setLayout(layout)

    def get_data(self):
        """Возвращает данные из полей ввода"""
        return self.name_input.text(), self.trainer_input.text(), self.group_input.currentText()
class SekciiTab(QWidget):
    def __init__(self):
        super().__init__()

        # Основной layout
        tab_layout = QVBoxLayout()

        # Горизонтальный layout для кнопки "домик" и выравнивания справа
        home_button_layout = QHBoxLayout()
        home_button = QPushButton()
        home_button.setIcon(QIcon('img.png'))  # Путь к иконке домика
        home_button.setIconSize(QSize(30, 30))
        home_button.setStyleSheet(
            """QPushButton {background-color: #E0E0E0; border: none; border-radius: 8px; padding: 5px;}"""
        )
        home_button.clicked.connect(self.open_main_window)

        # Добавляем спейсер, чтобы кнопка выровнялась вправо
        home_button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        home_button_layout.addWidget(home_button)

        tab_layout.addLayout(home_button_layout)

        # Создаём горизонтальный layout для двух списков
        splitter_layout = QHBoxLayout()

        # Список слева
        self.sekcii_list_left = QListWidget()
        self.sekcii_list_left.addItems(['Секция 1', 'Секция 2', 'Секция 3'])
        self.sekcii_list_left.setMinimumHeight(600)  # Увеличиваем размер
        splitter_layout.addWidget(self.sekcii_list_left)

        # Список справа
        self.sekcii_list_right = QListWidget()
        self.sekcii_list_right.addItems(['Тренер 1', 'Тренер 2', 'Тренер 3'])
        self.sekcii_list_right.setMinimumHeight(600)
        splitter_layout.addWidget(self.sekcii_list_right)

        tab_layout.addLayout(splitter_layout)

        # Создаём горизонтальный layout для кнопок
        buttons_layout = QHBoxLayout()

        # Кнопки для добавления, редактирования и удаления записей (под левым списком)
        add_button = QPushButton('Добавить')
        add_button.setStyleSheet(
            """QPushButton {background-color: #E57373; color: white; border: none; border-radius: 8px; padding: 10px 20px;}"""
        )
        add_button.clicked.connect(self.show_add_sekcii_dialog)
        buttons_layout.addWidget(add_button)

        edit_button = QPushButton('Редактировать')
        edit_button.setStyleSheet(
            """QPushButton {background-color: #FF9800; color: white; border: none; border-radius: 8px; padding: 10px 20px;}"""
        )
        edit_button.clicked.connect(self.show_edit_sekcii_dialog)
        buttons_layout.addWidget(edit_button)

        delete_button = QPushButton('Удалить')
        delete_button.setStyleSheet(
            """QPushButton {background-color: #F44336; color: white; border: none; border-radius: 8px; padding: 10px 20px;}"""
        )
        delete_button.clicked.connect(self.delete_sekcii)
        buttons_layout.addWidget(delete_button)

        # Spacer для выравнивания кнопок слева
        spacer_left = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Добавляем левые спейсер элементы, чтобы кнопки не выходили за левую половину
        buttons_layout.addItem(spacer_left)

        # Ограничим ширину кнопок
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        tab_layout.addLayout(buttons_layout)

        # Кнопка выхода
        exit_button = QPushButton("Выход")
        exit_button.clicked.connect(self.exit_application)

        exit_button.setStyleSheet(
            """QPushButton {background-color: #E57373; color: white; border: none; border-radius: 8px; padding: 10px 20px;}"""
        )

        exit_layout = QHBoxLayout()
        exit_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        exit_layout.addWidget(exit_button)

        tab_layout.addLayout(exit_layout)

        self.setLayout(tab_layout)

    def show_add_sekcii_dialog(self):
        """Показать диалоговое окно для добавления секции"""
        dialog = AddSekciiDialog()

        if dialog.exec() == QDialog.DialogCode.Accepted:
            name, trainer, group = dialog.get_data()
            if name:  # Проверяем, что название секции не пустое
                self.sekcii_list_left.addItem(f'{name} ({trainer}, {group})')

    def show_edit_sekcii_dialog(self):
        """Показать диалоговое окно для редактирования секции"""
        current_item = self.sekcii_list_left.currentItem()
        if current_item:
            # Разделяем текст текущего элемента на составляющие (имя, тренер, группа)
            item_text = current_item.text()
            name, rest = item_text.split(' (', 1)
            trainer, group = rest.rstrip(')').split(', ')

            # Открываем диалог с предустановленными значениями
            dialog = EditSekciiDialog(name, trainer, group)

            if dialog.exec() == QDialog.DialogCode.Accepted:
                # Получаем новые данные из диалога
                name, trainer, group = dialog.get_data()

                # Обновляем текст элемента списка
                current_item.setText(f'{name} ({trainer}, {group})')

    def delete_sekcii(self):
        """Удалить выбранную секцию из левого списка"""
        current_item = self.sekcii_list_left.currentItem()
        if current_item:
            reply = QInputDialog.getItem(self, 'Удалить секцию', 'Вы уверены, что хотите удалить эту секцию?',
                                         ['Да', 'Нет'], 1, False)
            if reply[0] == 'Да':
                self.sekcii_list_left.takeItem(self.sekcii_list_left.row(current_item))

    def exit_application(self):
        """Завершаем работу приложения"""
        QApplication.quit()

    def open_main_window(self):
        """Открыть главное окно"""
        # Здесь нужно добавить логику для перехода в главное окно
        print("Открытие главного окна")


class TrenerTab(QWidget):
    def __init__(self):
        super().__init__()

        tab_layout = QVBoxLayout()

        # Горизонтальный layout для кнопки "домик" и выравнивания справа
        home_button_layout = QHBoxLayout()
        home_button = QPushButton()
        home_button.setIcon(QIcon('img.png'))  # Путь к иконке домика
        home_button.setIconSize(QSize(30, 30))
        home_button.setStyleSheet(
            """QPushButton {background-color: #E0E0E0; border: none; border-radius: 8px; padding: 5px;}"""
        )
        home_button.clicked.connect(self.open_main_window)

        # Добавляем спейсер, чтобы кнопка выровнялась вправо
        home_button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        home_button_layout.addWidget(home_button)

        tab_layout.addLayout(home_button_layout)

        # Список для отображения тренеров (слева)
        self.trener_list = QListWidget()
        self.trener_list.addItems(['Тренер 1', 'Тренер 2', 'Тренер 3'])
        self.trener_list.setMinimumHeight(600)  # Увеличиваем размер
        tab_layout.addWidget(self.trener_list)

        # Создаем горизонтальный layout для кнопок
        buttons_layout = QHBoxLayout()

        # Кнопки для добавления, редактирования и удаления тренеров
        add_button = QPushButton('Добавить')
        add_button.setStyleSheet("""
                    QPushButton {
                        background-color: #E57373;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        padding: 10px 20px;
                    }
                    QPushButton:hover {
                        background-color: #D32F2F;
                    }
                    QPushButton:pressed {
                        background-color: #C62828;
                    }
                """)
        add_button.clicked.connect(self.add_trener)
        buttons_layout.addWidget(add_button)

        edit_button = QPushButton('Редактировать')
        edit_button.setStyleSheet("""
                    QPushButton {
                        background-color: #FF9800;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        padding: 10px 20px;
                    }
                    QPushButton:hover {
                        background-color: #F57C00;
                    }
                    QPushButton:pressed {
                        background-color: #E65100;
                    }
                """)
        edit_button.clicked.connect(self.edit_trener)
        buttons_layout.addWidget(edit_button)

        delete_button = QPushButton('Удалить')
        delete_button.setStyleSheet("""
                    QPushButton {
                        background-color: #F44336;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        padding: 10px 20px;
                    }
                    QPushButton:hover {
                        background-color: #D32F2F;
                    }
                    QPushButton:pressed {
                        background-color: #C62828;
                    }
                """)
        delete_button.clicked.connect(self.delete_trener)
        buttons_layout.addWidget(delete_button)

        # Spacer для выравнивания кнопок слева
        spacer_left = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Добавляем левые спейсер элементы, чтобы кнопки не выходили за левую половину
        buttons_layout.addItem(spacer_left)

        tab_layout.addLayout(buttons_layout)

        # Кнопка выхода
        exit_button = QPushButton("Выход")
        exit_button.clicked.connect(self.exit_application)

        exit_button.setStyleSheet(
            """QPushButton {background-color: #E57373; color: white; border: none; border-radius: 8px; padding: 10px 20px;}"""
        )

        exit_layout = QHBoxLayout()
        exit_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        exit_layout.addWidget(exit_button)

        tab_layout.addLayout(exit_layout)

        self.setLayout(tab_layout)

    def add_trener(self):
        """Открыть окно добавления нового тренера"""
        dialog = TrenerDialog(self)
        if dialog.exec():
            name = dialog.name_input.text()
            surname = dialog.surname_input.text()
            patronymic = dialog.patronymic_input.text()
            birth_date = dialog.birth_date_input.date().toString("yyyy-MM-dd")
            phone = dialog.phone_input.text()
            additional_info = dialog.additional_info_input.toPlainText()
            self.trener_list.addItem(f"{surname} {name} {patronymic} ({birth_date}, {phone})")

    def edit_trener(self):
        """Открыть окно редактирования тренера"""
        current_item = self.trener_list.currentItem()
        if current_item:
            dialog = TrenerDialog(self, current_item.text())
            if dialog.exec():
                name = dialog.name_input.text()
                surname = dialog.surname_input.text()
                patronymic = dialog.patronymic_input.text()
                birth_date = dialog.birth_date_input.date().toString("yyyy-MM-dd")
                phone = dialog.phone_input.text()
                additional_info = dialog.additional_info_input.toPlainText()
                current_item.setText(f"{surname} {name} {patronymic} ({birth_date}, {phone})")

    def delete_trener(self):
        """Удалить выбранного тренера"""
        current_item = self.trener_list.currentItem()
        if current_item:
            reply = QInputDialog.getItem(self, 'Удалить тренера', 'Вы уверены, что хотите удалить этого тренера?', ['Да', 'Нет'], 1, False)
            if reply[0] == 'Да':
                self.trener_list.takeItem(self.trener_list.row(current_item))

    def exit_application(self):
        """Завершаем работу приложения"""
        QApplication.quit()

    def open_main_window(self):
        """Открыть главное окно"""
        print("Открытие главного окна")
class TrenerDialog(QDialog):
    def __init__(self, parent, trainer_info=None):
        super().__init__(parent)

        self.setWindowTitle("Добавить/Редактировать тренера")
        self.setFixedSize(400, 400)

        layout = QVBoxLayout()

        # Лейблы и поля ввода
        self.surname_input = QLineEdit()
        self.name_input = QLineEdit()
        self.patronymic_input = QLineEdit()
        self.birth_date_input = QDateEdit(QDate.currentDate())
        self.phone_input = QLineEdit()
        self.additional_info_input = QTextEdit()

        # Если передано существующее имя, то редактируем
        if trainer_info:
            info_parts = trainer_info.split(" ")
            surname, name, patronymic = info_parts[0], info_parts[1], info_parts[2] if len(info_parts) > 2 else ""
            self.surname_input.setText(surname)
            self.name_input.setText(name)
            self.patronymic_input.setText(patronymic)

        # Добавляем элементы в layout
        layout.addWidget(QLabel("Фамилия"))
        layout.addWidget(self.surname_input)

        layout.addWidget(QLabel("Имя"))
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("Отчество"))
        layout.addWidget(self.patronymic_input)

        layout.addWidget(QLabel("Дата рождения"))
        layout.addWidget(self.birth_date_input)

        layout.addWidget(QLabel("Номер телефона"))
        layout.addWidget(self.phone_input)

        layout.addWidget(QLabel("Дополнительная информация"))
        layout.addWidget(self.additional_info_input)

        # Кнопки
        button_layout = QHBoxLayout()

        self.submit_button = QPushButton("Добавить" if trainer_info is None else "Изменить")
        self.submit_button.clicked.connect(self.accept)

        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)


class GruppiTab(QWidget):
    def __init__(self):
        super().__init__()

        tab_layout = QVBoxLayout()

        # Горизонтальный layout для кнопки "домик" и выравнивания справа
        home_button_layout = QHBoxLayout()
        home_button = QPushButton()
        home_button.setIcon(QIcon('img.png'))  # Путь к иконке домика
        home_button.setIconSize(QSize(30, 30))
        home_button.setStyleSheet(
            """QPushButton {background-color: #E0E0E0; border: none; border-radius: 8px; padding: 5px;}"""
        )
        home_button.clicked.connect(self.open_main_window)

        # Добавляем спейсер, чтобы кнопка выровнялась вправо
        home_button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        home_button_layout.addWidget(home_button)

        tab_layout.addLayout(home_button_layout)

        # Список для отображения групп (левый)
        self.gruppi_list_left = QListWidget()
        self.gruppi_list_left.addItems(['Группа 1', 'Группа 2', 'Группа 3'])
        self.gruppi_list_left.setMinimumHeight(600)

        # Список для отображения групп (правый)
        self.gruppi_list_right = QListWidget()
        self.gruppi_list_right.addItems(['Секция 1', 'Секция 2', 'Секция 3'])
        self.gruppi_list_right.setMinimumHeight(600)

        # Добавляем оба списка в горизонтальный layout
        splitter_layout = QHBoxLayout()
        splitter_layout.addWidget(self.gruppi_list_left)
        splitter_layout.addWidget(self.gruppi_list_right)
        tab_layout.addLayout(splitter_layout)

        # Создаем горизонтальный layout для кнопок
        buttons_layout = QHBoxLayout()

        # Кнопки для добавления, редактирования и удаления групп
        add_button = QPushButton('Добавить')
        add_button.setStyleSheet("""
                    QPushButton {
                        background-color: #E57373;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        padding: 10px 20px;
                    }
                    QPushButton:hover {
                        background-color: #D32F2F;
                    }
                    QPushButton:pressed {
                        background-color: #C62828;
                    }
                """)
        add_button.clicked.connect(self.add_gruppi)
        buttons_layout.addWidget(add_button)

        edit_button = QPushButton('Редактировать')
        edit_button.setStyleSheet("""
                    QPushButton {
                        background-color: #FF9800;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        padding: 10px 20px;
                    }
                    QPushButton:hover {
                        background-color: #F57C00;
                    }
                    QPushButton:pressed {
                        background-color: #E65100;
                    }
                """)
        edit_button.clicked.connect(self.edit_gruppi)
        buttons_layout.addWidget(edit_button)

        delete_button = QPushButton('Удалить')
        delete_button.setStyleSheet("""
                    QPushButton {
                        background-color: #F44336;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        padding: 10px 20px;
                    }
                    QPushButton:hover {
                        background-color: #D32F2F;
                    }
                    QPushButton:pressed {
                        background-color: #C62828;
                    }
                """)
        delete_button.clicked.connect(self.delete_gruppi)
        buttons_layout.addWidget(delete_button)

        # Spacer для выравнивания кнопок слева
        spacer_left = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        buttons_layout.addItem(spacer_left)

        tab_layout.addLayout(buttons_layout)

        # Кнопка выхода
        exit_button = QPushButton("Выход")
        exit_button.clicked.connect(self.exit_application)

        exit_button.setStyleSheet(
            """QPushButton {background-color: #E57373; color: white; border: none; border-radius: 8px; padding: 10px 20px;}"""
        )

        exit_layout = QHBoxLayout()
        exit_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        exit_layout.addWidget(exit_button)

        tab_layout.addLayout(exit_layout)

        self.setLayout(tab_layout)

    def add_gruppi(self):
        """Открыть окно добавления новой группы"""
        dialog = GruppiDialog(self)
        if dialog.exec():
            group_name = dialog.group_name_input.text()
            section_name = dialog.section_combobox.currentText()
            trainer_name = dialog.trainer_combobox.currentText()
            self.gruppi_list_left.addItem(f"{group_name} - {section_name} - {trainer_name}")

    def edit_gruppi(self):
        """Открыть окно редактирования группы"""
        current_item = self.gruppi_list_left.currentItem()
        if current_item:
            dialog = GruppiDialog(self, current_item.text())
            if dialog.exec():
                group_name = dialog.group_name_input.text()
                section_name = dialog.section_combobox.currentText()
                trainer_name = dialog.trainer_combobox.currentText()
                current_item.setText(f"{group_name} - {section_name} - {trainer_name}")

    def delete_gruppi(self):
        """Удалить выбранную группу"""
        current_item = self.gruppi_list_left.currentItem()
        if current_item:
            reply = QInputDialog.getItem(self, 'Удалить группу', 'Вы уверены, что хотите удалить эту группу?',
                                         ['Да', 'Нет'], 1, False)
            if reply[0] == 'Да':
                self.gruppi_list_left.takeItem(self.gruppi_list_left.row(current_item))

    def exit_application(self):
        """Завершаем работу приложения"""
        QApplication.quit()

    def open_main_window(self):
        """Открыть главное окно"""
        print("Открытие главного окна")
class GruppiDialog(QDialog):
    def __init__(self, parent, group_info=None):
        super().__init__(parent)

        self.setWindowTitle("Добавить/Редактировать группу")
        self.setFixedSize(400, 400)

        layout = QVBoxLayout()

        # Лейблы и поля ввода
        self.group_name_input = QLineEdit()
        self.section_combobox = QComboBox()
        self.trainer_combobox = QComboBox()

        # Заполняем комбобоксы секциями и тренерами
        self.section_combobox.addItems(['Секция 1', 'Секция 2', 'Секция 3'])
        self.trainer_combobox.addItems(['Тренер 1', 'Тренер 2', 'Тренер 3'])

        # Если передано существующее название группы, то редактируем
        if group_info:
            info_parts = group_info.split(" - ")
            group_name, section_name, trainer_name = info_parts[0], info_parts[1], info_parts[2]
            self.group_name_input.setText(group_name)
            self.section_combobox.setCurrentText(section_name)
            self.trainer_combobox.setCurrentText(trainer_name)

        # Добавляем элементы в layout
        layout.addWidget(QLabel("Название группы"))
        layout.addWidget(self.group_name_input)

        layout.addWidget(QLabel("Секция"))
        layout.addWidget(self.section_combobox)

        layout.addWidget(QLabel("Тренер"))
        layout.addWidget(self.trainer_combobox)

        # Кнопки
        button_layout = QHBoxLayout()

        self.submit_button = QPushButton("Добавить" if group_info is None else "Изменить")
        self.submit_button.clicked.connect(self.accept)

        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)


class SportsmeniTab(QWidget):
    def __init__(self):
        super().__init__()

        tab_layout = QVBoxLayout()

        # Горизонтальный layout для кнопки "домик" и выравнивания справа
        home_button_layout = QHBoxLayout()
        home_button = QPushButton()
        home_button.setIcon(QIcon('img.png'))  # Укажите путь к иконке
        home_button.setIconSize(QSize(30, 30))
        home_button.setStyleSheet(
            """QPushButton {background-color: #E0E0E0; border: none; border-radius: 8px; padding: 5px;}"""
        )
        home_button.clicked.connect(self.open_main_window)

        # Добавляем спейсер, чтобы кнопка выровнялась вправо
        home_button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        home_button_layout.addWidget(home_button)

        tab_layout.addLayout(home_button_layout)

        # Список для отображения спортсменов
        self.sportsmeni_list = QListWidget()
        self.sportsmeni_list.addItems(['Спортсмен 1', 'Спортсмен 2', 'Спортсмен 3'])
        self.sportsmeni_list.setMinimumHeight(600)
        tab_layout.addWidget(self.sportsmeni_list)

        # Список для групп (для выбора группы спортсменом)
        self.groups_list = ['Группа 1', 'Группа 2', 'Группа 3']

        # Создаем горизонтальный layout для кнопок
        buttons_layout = QVBoxLayout()

        # Кнопки для добавления, редактирования и удаления спортсменов
        button_layout = QHBoxLayout()

        add_button = QPushButton('Добавить')
        add_button.setStyleSheet("""
                    QPushButton {
                        background-color: #E57373;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        padding: 10px 20px;
                        font-size: 16px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #D32F2F;
                    }
                    QPushButton:pressed {
                        background-color: #C62828;
                    }
                """)
        add_button.clicked.connect(self.add_sportsmeni)
        button_layout.addWidget(add_button)

        edit_button = QPushButton('Редактировать')
        edit_button.setStyleSheet("""
                    QPushButton {
                        background-color: #FF9800;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        padding: 10px 20px;
                        font-size: 16px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #F57C00;
                    }
                    QPushButton:pressed {
                        background-color: #E65100;
                    }
                """)
        edit_button.clicked.connect(self.edit_sportsmeni)
        button_layout.addWidget(edit_button)

        delete_button = QPushButton('Удалить')
        delete_button.setStyleSheet("""
                    QPushButton {
                        background-color: #F44336;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        padding: 10px 20px;
                        font-size: 16px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #D32F2F;
                    }
                    QPushButton:pressed {
                        background-color: #C62828;
                    }
                """)
        delete_button.clicked.connect(self.delete_sportsmeni)
        button_layout.addWidget(delete_button)

        buttons_layout.addLayout(button_layout)

        # Кнопка выхода
        exit_button = QPushButton("Выход")
        exit_button.clicked.connect(self.exit_application)

        exit_button.setStyleSheet(
            """QPushButton {background-color: #E57373; color: white; border: none; border-radius: 8px; padding: 10px 20px;}"""
        )

        exit_layout = QHBoxLayout()
        exit_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        exit_layout.addWidget(exit_button)

        buttons_layout.addLayout(exit_layout)

        tab_layout.addLayout(buttons_layout)

        self.setLayout(tab_layout)

    def add_sportsmeni(self):
        """Открыть окно добавления нового спортсмена"""
        dialog = SportsmeniDialog(self)
        if dialog.exec():
            surname = dialog.surname_input.text()
            name = dialog.name_input.text()
            patronymic = dialog.patronymic_input.text()
            birth_date = dialog.birth_date_input.date().toString("yyyy-MM-dd")
            phone = dialog.phone_input.text()
            group = dialog.group_combobox.currentText()

            # Добавляем спортсмена в список
            self.sportsmeni_list.addItem(f"{surname} {name} {patronymic}, ДР: {birth_date}, Тел: {phone}, Группа: {group}")

    def edit_sportsmeni(self):
        """Открыть окно редактирования спортсмена"""
        current_item = self.sportsmeni_list.currentItem()
        if current_item:
            dialog = SportsmeniDialog(self, current_item.text())
            if dialog.exec():
                surname = dialog.surname_input.text()
                name = dialog.name_input.text()
                patronymic = dialog.patronymic_input.text()
                birth_date = dialog.birth_date_input.date().toString("yyyy-MM-dd")
                phone = dialog.phone_input.text()
                group = dialog.group_combobox.currentText()

                current_item.setText(f"{surname} {name} {patronymic}, ДР: {birth_date}, Тел: {phone}, Группа: {group}")

    def delete_sportsmeni(self):
        """Удалить выбранного спортсмена"""
        current_item = self.sportsmeni_list.currentItem()
        if current_item:
            reply = QInputDialog.getItem(self, 'Удалить спортсмена', 'Вы уверены, что хотите удалить этого спортсмена?', ['Да', 'Нет'], 1, False)
            if reply[0] == 'Да':
                self.sportsmeni_list.takeItem(self.sportsmeni_list.row(current_item))

    def exit_application(self):
        """Завершаем работу приложения"""
        QApplication.quit()

    def open_main_window(self):
        """Открыть главное окно"""
        print("Открытие главного окна")
class SportsmeniDialog(QDialog):
    def __init__(self, parent, sportsmeni_info=None):
        super().__init__(parent)

        self.setWindowTitle("Добавить/Редактировать спортсмена")
        self.setFixedSize(400, 500)

        layout = QFormLayout()

        # Лейблы и поля ввода
        self.surname_input = QLineEdit()
        self.name_input = QLineEdit()
        self.patronymic_input = QLineEdit()
        self.birth_date_input = QDateEdit(QDate.currentDate())
        self.phone_input = QLineEdit()
        self.group_combobox = QComboBox()
        self.group_combobox.addItems(parent.groups_list)

        # Если переданы данные спортсмена, заполняем поля
        if sportsmeni_info:
            info_parts = sportsmeni_info.split(", ")
            name_parts = info_parts[0].split(" ")
            surname, name, patronymic = name_parts[0], name_parts[1], name_parts[2]
            birth_date, phone, group = info_parts[1], info_parts[2], info_parts[3]

            self.surname_input.setText(surname)
            self.name_input.setText(name)
            self.patronymic_input.setText(patronymic)
            self.birth_date_input.setDate(QDate.fromString(birth_date, "yyyy-MM-dd"))
            self.phone_input.setText(phone)
            self.group_combobox.setCurrentText(group)

        # Добавляем элементы в layout
        layout.addRow("Фамилия", self.surname_input)
        layout.addRow("Имя", self.name_input)
        layout.addRow("Отчество", self.patronymic_input)
        layout.addRow("Дата рождения", self.birth_date_input)
        layout.addRow("Номер телефона", self.phone_input)
        layout.addRow("Группа", self.group_combobox)

        # Кнопки
        button_layout = QHBoxLayout()

        self.submit_button = QPushButton("Добавить" if sportsmeni_info is None else "Изменить")
        self.submit_button.clicked.connect(self.accept)

        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(cancel_button)

        layout.addRow(button_layout)

        self.setLayout(layout)


class RaspisanieTab(QWidget):
    def __init__(self):
        super().__init__()

        tab_layout = QVBoxLayout()

        # Список групп (например, как в разделе "Спортсмены")
        self.groups_list = ['Группа 1', 'Группа 2', 'Группа 3']

        # Горизонтальный layout для выбора даты
        date_layout = QHBoxLayout()

        # Поле для выбора даты
        self.date_picker = QDateEdit(QDate.currentDate())
        self.date_picker.setDisplayFormat("dd.MM.yyyy")
        self.date_picker.setCalendarPopup(True)
        self.date_picker.setStyleSheet(
            """QDateEdit {padding: 5px; font-size: 16px; border: 1px solid #ccc; border-radius: 5px;}"""
        )
        date_layout.addWidget(QLabel("Выберите дату:"))
        date_layout.addWidget(self.date_picker)

        # Добавляем дату в верхнюю часть
        tab_layout.addLayout(date_layout)

        # Список с расписанием
        self.schedule_list = QListWidget()
        self.schedule_list.addItems(['Занятие 1: 10:00', 'Занятие 2: 12:00', 'Занятие 3: 14:00'])
        self.schedule_list.setMinimumWidth(350)
        self.schedule_list.setMinimumHeight(300)
        tab_layout.addWidget(self.schedule_list)

        # Кнопки для работы с расписанием (Добавить, Редактировать, Удалить)
        buttons_layout = QVBoxLayout()

        button_layout = QHBoxLayout()

        # Кнопка "Добавить"
        add_button = QPushButton('Добавить')
        add_button.setStyleSheet("""
                    QPushButton {
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        padding: 10px 20px;
                        font-size: 16px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #45A049;
                    }
                    QPushButton:pressed {
                        background-color: #388E3C;
                    }
                """)
        add_button.clicked.connect(self.add_schedule)
        button_layout.addWidget(add_button)

        # Кнопка "Редактировать"
        edit_button = QPushButton('Редактировать')
        edit_button.setStyleSheet("""
                    QPushButton {
                        background-color: #FF9800;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        padding: 10px 20px;
                        font-size: 16px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #F57C00;
                    }
                    QPushButton:pressed {
                        background-color: #E65100;
                    }
                """)
        edit_button.clicked.connect(self.edit_schedule)
        button_layout.addWidget(edit_button)

        # Кнопка "Удалить"
        delete_button = QPushButton('Удалить')
        delete_button.setStyleSheet("""
                    QPushButton {
                        background-color: #F44336;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        padding: 10px 20px;
                        font-size: 16px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #D32F2F;
                    }
                    QPushButton:pressed {
                        background-color: #C62828;
                    }
                """)
        delete_button.clicked.connect(self.delete_schedule)
        button_layout.addWidget(delete_button)

        buttons_layout.addLayout(button_layout)

        # Кнопка выхода
        exit_button = QPushButton("Выход")
        exit_button.clicked.connect(self.exit_application)
        exit_button.setStyleSheet(
            """QPushButton {background-color: #E57373; color: white; border: none; border-radius: 8px; padding: 10px 20px;}"""
        )

        exit_layout = QHBoxLayout()
        exit_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        exit_layout.addWidget(exit_button)

        buttons_layout.addLayout(exit_layout)

        tab_layout.addLayout(buttons_layout)

        self.setLayout(tab_layout)

    def add_schedule(self):
        """Открыть окно добавления нового занятия"""
        dialog = ScheduleDialog(self, self.groups_list)  # Передаем список групп
        if dialog.exec():
            date = dialog.date_picker.date().toString("yyyy-MM-dd")
            time = dialog.time_combobox.currentText()
            group = dialog.group_combobox.currentText()
            place = dialog.place_input.text()

            # Добавляем занятие в список
            self.schedule_list.addItem(f"{date} | {time} | {group} | {place}")

    def edit_schedule(self):
        """Открыть окно редактирования выбранного занятия"""
        current_item = self.schedule_list.currentItem()
        if current_item:
            dialog = ScheduleDialog(self, self.groups_list, current_item.text())  # Передаем список групп
            if dialog.exec():
                date = dialog.date_picker.date().toString("yyyy-MM-dd")
                time = dialog.time_combobox.currentText()
                group = dialog.group_combobox.currentText()
                place = dialog.place_input.text()

                current_item.setText(f"{date} | {time} | {group} | {place}")

    def delete_schedule(self):
        """Удалить выбранное занятие"""
        current_item = self.schedule_list.currentItem()
        if current_item:
            reply = QInputDialog.getItem(self, 'Удалить занятие', 'Вы уверены, что хотите удалить это занятие?', ['Да', 'Нет'], 1, False)
            if reply[0] == 'Да':
                self.schedule_list.takeItem(self.schedule_list.row(current_item))

    def exit_application(self):
        """Завершаем работу приложения"""
        QApplication.quit()
class ScheduleDialog(QDialog):
    def __init__(self, parent, groups_list, schedule_info=None):
        super().__init__(parent)

        self.setWindowTitle("Добавить/Редактировать занятие")
        self.setFixedSize(400, 300)

        layout = QFormLayout()

        # Лейблы и поля ввода
        self.date_picker = QDateEdit(QDate.currentDate())
        self.date_picker.setDisplayFormat("dd.MM.yyyy")
        self.date_picker.setCalendarPopup(True)
        self.time_combobox = QComboBox()
        self.time_combobox.addItems(["10:00", "12:00", "14:00", "16:00", "18:00"])  # Примерное время
        self.group_combobox = QComboBox()
        self.group_combobox.addItems(groups_list)  # Группы передаются из основного окна
        self.place_input = QLineEdit()

        # Если переданы данные занятия, заполняем поля
        if schedule_info:
            info_parts = schedule_info.split(" | ")
            date, time, group, place = info_parts[0], info_parts[1], info_parts[2], info_parts[3]

            self.date_picker.setDate(QDate.fromString(date, "yyyy-MM-dd"))
            self.time_combobox.setCurrentText(time)
            self.group_combobox.setCurrentText(group)
            self.place_input.setText(place)

        # Добавляем элементы в layout
        layout.addRow("Дата", self.date_picker)
        layout.addRow("Время", self.time_combobox)
        layout.addRow("Группа", self.group_combobox)
        layout.addRow("Место проведения", self.place_input)

        # Кнопки
        button_layout = QHBoxLayout()

        self.submit_button = QPushButton("Добавить" if schedule_info is None else "Изменить")
        self.submit_button.clicked.connect(self.accept)

        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(cancel_button)

        layout.addRow(button_layout)

        self.setLayout(layout)



class PoseshhenieTab(QWidget):
    def __init__(self):
        super().__init__()

        tab_layout = QVBoxLayout()

        # Содержимое вкладки
        tab_layout.addWidget(QLabel('Посещение'))

        self.setLayout(tab_layout)


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Окно с вкладками')

        # Делаем окно полноэкранным
        self.showFullScreen()

        # Создаём основной layout
        layout = QVBoxLayout()

        # Создаём QTabWidget
        tabs = QTabWidget()

        # Настроим внешний вид вкладок
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
            }
            QTabBar::tab {
                background: #3E8E41;
                color: white;
                padding: 18px;
                border-radius: 15px;
                font-size: 18px;
                width: 200px;
                text-align: center;
                border: none;
            }
            QTabBar::tab:selected {
                background: #2E6E31;
                font-weight: bold;
            }
            QTabWidget {
                background-color: #f0f0f0;
            }
        """)

        # Создаём экземпляры вкладок
        sekcii = SekciiTab()
        trener = TrenerTab()
        gruppi = GruppiTab()
        sportsmeni = SportsmeniTab()
        raspisanie = RaspisanieTab()
        poseshenie = PoseshhenieTab()

        # Добавляем вкладки в QTabWidget
        tabs.addTab(sekcii, "Секции")
        tabs.addTab(trener, "Тренеры")
        tabs.addTab(gruppi, "Группы")
        tabs.addTab(sportsmeni, "Спортсмены")
        tabs.addTab(raspisanie, "Расписание")
        tabs.addTab(poseshenie, "Посещение")

        # Добавляем QTabWidget в layout
        layout.addWidget(tabs)

        # Устанавливаем layout для основного окна
        self.setLayout(layout)
        self.check_credentials()

    def check_credentials(self):
        # Подключение к базе данных и проверка введенных данных
        try:
            conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="123456qwerty",
                database="cursovaya"
            )
            cursor = conn.cursor()
        except mysql.connector.Error as e:
            print(f"Ошибка базы данных: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())

