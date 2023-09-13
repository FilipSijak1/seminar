import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit, QCheckBox
from log import Ui_MainWindow
from reg import Ui_reg_window
from menu import Ui_menu
from db import db
from PyQt5.QtCore import Qt
from exceptions import (
    log_error_empty,
    reg_error_taken,
    log_error_wrong,
    reg_error_password_mismatch,
    reg_error_empty,
    reg_error_invalid_domain,
    log_error_user_not_found,
    log_error_wrong_password,
    log_error,
)
import sqlite3
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel

class LoginApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.Login.clicked.connect(self.login)
        self.ui.Register.clicked.connect(self.open_registration)
        self.current_user = None

        self.registration_window = RegistrationWindow()
        self.menu_window = MenuWindow()

        self.show_password_checkbox = QCheckBox("Show Password", self.ui.centralwidget)
        self.show_password_checkbox.setGeometry(670, 270, 15, 15)
        self.show_password_checkbox.setChecked(False)
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)
        self.ui.password.setEchoMode(QLineEdit.Password)

    def toggle_password_visibility(self, state):
        if state == Qt.Checked:
            self.ui.password.setEchoMode(QLineEdit.Normal)
        else:
            self.ui.password.setEchoMode(QLineEdit.Password)

    def show_message_box(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.exec_()

    def open_registration(self):
        self.hide()
        self.registration_window.show()

    def open_menu(self):
        self.hide()
        self.menu_window.open_menu(self.current_user)
        self.menu_window.show()

    def register(self):
        email = self.ui.email.text()
        username = self.ui.username.text()
        password = self.ui.password.text()
        confirm_password = self.ui.confirm_password.text()

        try:
            if not all([email, username, password, confirm_password]):
                raise reg_error_empty

            if password != confirm_password:
                raise reg_error_password_mismatch

            user = Korisnik(email, username, password)
            user.register()
            QMessageBox.information(self, "Success", "Registration successful.")
        except reg_error_taken:
            self.show_message_box("This email address is already taken.")
        except reg_error_empty:
            self.show_message_box("You did not fill all required fields.")
        except reg_error_password_mismatch:
            self.show_message_box("Passwords do not match.")
        except Exception as e:
            self.show_message_box(f"An error occurred: {str(e)}")

    def login(self):
        email = self.ui.email.text()
        password = self.ui.password.text()

        try:
            if not all([email, password]):
                raise log_error_empty

            if not self.is_user_in_db(email, password):
                raise log_error_user_not_found

            if not self.is_password_correct(email, password):
                raise log_error_wrong_password

            user = Auth.login(email, password)  # Dobijte korisnika nakon uspješne prijave
            if user:
                self.current_user = user  # Postavite trenutno prijavljenog korisnika
                QMessageBox.information(self, "Success", "Login successful.")
                self.open_menu()
            else:
                raise log_error_user_not_found

        except log_error_user_not_found:
            self.show_message_box("Incorrect password or email.")
        except log_error_wrong:
            self.show_message_box("Incorrect password.")
        except log_error_empty:
            self.show_message_box("You did not fill all required fields.")

    def is_user_in_db(self, email, password):
        cursor = db.conn.cursor()
        cursor.execute('SELECT * FROM korisnici WHERE email = ? AND password = ?', (email, password))
        user = cursor.fetchone()
        cursor.close()
        return user is not None

    def is_password_correct(self, email, password):
        cursor = db.conn.cursor()
        cursor.execute('SELECT * FROM korisnici WHERE email = ? AND password = ?', (email, password))
        user = cursor.fetchone()
        cursor.close()
        return user is not None

class RegistrationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_reg_window()
        self.ui.setupUi(self)

        self.ui.user_register.clicked.connect(self.register)
        self.ui.back.clicked.connect(self.back_main_window)

        # Dodajemo dva nova QLineEdit polja za unos lozinke i ponovljene lozinke
        self.password = self.ui.password
        self.confirm_password = self.ui.confirm_password

        # Dodajemo dva nova checkboxa za prikazivanje/skrivanje lozinke
        self.show_password_checkbox = QCheckBox("Show Password", self.ui.centralwidget)
        self.show_password_checkbox.setGeometry(670, 290, 15, 15)
        self.show_password_checkbox.setChecked(False)
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)

        self.show_confirm_password_checkbox = QCheckBox("Show Confirm Password", self.ui.centralwidget)
        self.show_confirm_password_checkbox.setGeometry(670, 340, 15, 15)
        self.show_confirm_password_checkbox.setChecked(False)
        self.show_confirm_password_checkbox.stateChanged.connect(self.toggle_confirm_password_visibility)

        # Postavljamo da se lozinka i ponovljena lozinka inicijalno prikazuju kao Password
        self.password.setEchoMode(QLineEdit.Password)
        self.confirm_password.setEchoMode(QLineEdit.Password)

    def toggle_password_visibility(self, state):
        if state == Qt.Checked:
            self.password.setEchoMode(QLineEdit.Normal)
        else:
            self.password.setEchoMode(QLineEdit.Password)

    def toggle_confirm_password_visibility(self, state):
        if state == Qt.Checked:
            self.confirm_password.setEchoMode(QLineEdit.Normal)
        else:
            self.confirm_password.setEchoMode(QLineEdit.Password)


    def back_main_window(self):
        self.hide()
        self.login_window = LoginApp()
        self.login_window.show()

    def show_message_box(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.exec_()

    def register(self):
        email = self.ui.email.text()
        username = self.ui.username.text()
        password = self.ui.password.text()
        confirm_password = self.ui.confirm_password.text()

        try:
            if not all([email, username, password, confirm_password]):
                raise reg_error_empty

            if password != confirm_password:
                raise reg_error_password_mismatch

            if not self.is_valid_email_domain(email):
                raise reg_error_invalid_domain(email.split('@')[1])

            user = Korisnik(email, username, password)
            user.register()
            QMessageBox.information(self, "Success", "Registration successful.")
        except reg_error_taken:
            self.show_message_box("This email address is already taken.")
        except reg_error_empty:
            self.show_message_box("You did not fill all required fields.")
        except reg_error_password_mismatch:
            self.show_message_box("Passwords do not match.")
        except reg_error_invalid_domain as e:
            self.show_message_box(str(e))
        except Exception as e:
            self.show_message_box(f"An error occurred: {str(e)}")

    def is_valid_email_domain(self, email):
        allowed_domains = ["tvz.hr"]
        domain = email.split('@')[1]
        return domain in allowed_domains

class Korisnik:
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password

    def register(self):
        try:
            cursor = db.conn.cursor()
            cursor.execute('''
                INSERT INTO korisnici (email, username, password)
                VALUES (?, ?, ?)
            ''', (self.email, self.username, self.password))
            db.conn.commit()
        except sqlite3.IntegrityError as e:
            raise reg_error_taken
        except sqlite3.Error as e:
            raise reg_error_empty
        finally:
            cursor.close()

class MenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_menu()
        self.ui.setupUi(self)
        self.ui.robot_registration.clicked.connect(self.show_first_page)
        self.ui.testing.clicked.connect(self.show_second_page)
        self.ui.analytics.clicked.connect(self.show_third_page)
        self.ui.logout.clicked.connect(self.logout)
        self.label_options = ['High priority bug', 'Bug', 'Info']
        self.ui.messgaes.currentIndexChanged.connect(self.handle_label_selection)
        self.ui.save_notation.clicked.connect(self.save_test_results)
        self.current_user = None
        self.ui.messgaes.setCurrentIndex(0)
        self.selected_entries = []
        self.ui.notation_number.display(0)
        self.ui.high_priority_bug.clicked.connect(self.show_high_priority_bug_data)
        self.ui.bug.clicked.connect(self.show_bug_data)
        self.ui.info.clicked.connect(self.show_info_data)

        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('shepherd.db')
        if not self.db.open():
            QMessageBox.critical(self, "Error", "Database Error: %s" % self.db.lastError().text())

    def show_first_page(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def show_second_page(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def show_third_page(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def show_high_priority_bug_data(self):
        print("Show High Priority Bug Data called")
        self.show_data('High priority bug')

    def show_bug_data(self):
        self.show_data('Bug')

    def show_info_data(self):
        self.show_data('Info')

    def logout(self):
        # Prikazivanje poruke za potvrdu odjave
        reply = QMessageBox.question(self, 'Logout', 'Are you sure you want to logout?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        # Ako korisnik odabere "Yes" za odjavu
        if reply == QMessageBox.Yes:
            self.close()
            self.login_window = LoginApp()
            self.login_window.show()

    def open_menu(self, user):
        self.current_user = user

    def update_entry_count(self):
        try:
            selected_label = self.ui.messgaes.currentText()
            # Ovdje dodajte logiku za dohvaćanje broja unosa za odabrani label iz baze podataka
            # i ažurirajte broj prikazan na QLCDNumber widgetu.
        except Exception as e:
            print("Error in update_entry_count:", str(e))

    def handle_label_selection(self, index):
        try:
            self.selected_label = self.ui.messgaes.currentText()
            self.update_entry_count()
        except Exception as e:
            print("Error in handle_label_selection:", str(e))

    def save_test_results(self):
        selected_label = self.selected_label
        print(f"Selected label: {selected_label}")
        description = self.ui.description.toPlainText()
        user = self.current_user[1]  # Zamijenite s trenutno prijavljenim korisnikom

        try:
            # Povezivanje s bazom podataka
            conn = sqlite3.connect('shepherd.db')
            cursor = conn.cursor()

            # Spremanje podataka u bazu
            cursor.execute('''
                INSERT INTO test_results (label, description, user, date, time)
                VALUES (?, ?, ?, date('now'), time('now'))
            ''', (selected_label, description, user))

            conn.commit()
            conn.close()

            QMessageBox.information(self, "Success", "Test results saved successfully.")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error saving test results: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def show_high_priority_bugs(self):
        high_priority_bugs = db.get_high_priority_bugs()
        self.selected_entries = high_priority_bugs
        # Ovdje ažurirate QTableView s pronađenim unesima.

    def show_bug_entries(self):
        bug_entries = db.get_bug_entries()
        self.selected_entries = bug_entries
        # Ovdje ažurirate QTableView s pronađenim unesima.

    def show_info_entries(self):
        info_entries = db.get_info_entries()
        self.selected_entries = info_entries
        # Ovdje ažurirate QTableView s pronađenim unesima

    def show_data(self, label):
        query = QSqlQuery()
        query.prepare('SELECT * FROM test_results WHERE label = :label')
        query.bindValue(':label', label)
        if query.exec_():
            model = QSqlQueryModel()
            model.setQuery(query)
            self.ui.tableView.setModel(model)

            # Ažurirajte QLCDNumber s brojem prikazanih unosa
            count_query = QSqlQuery()
            count_query.prepare('SELECT COUNT(*) FROM test_results WHERE label = :label')
            count_query.bindValue(':label', label)
            if count_query.exec_() and count_query.first():
                count = count_query.value(0)
                self.ui.notation_number.display(count)
        else:
            QMessageBox.critical(self, "Error", "Error fetching data: %s" % query.lastError().text())


class Auth:
    @staticmethod
    def login(email, password):
        try:
            cursor = db.conn.cursor()
            cursor.execute('SELECT * FROM korisnici WHERE email = ? AND password = ?', (email, password))
            user = cursor.fetchone()
            if user is None:
                raise log_error_wrong
            return user
        except sqlite3.Error as e:
            raise log_error("Greška prilikom prijave: " + str(e))
        finally:
            cursor.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginApp()
    registration_window = RegistrationWindow()
    login_window.show()
    sys.exit(app.exec_())