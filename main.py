import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from log import Ui_MainWindow
from reg import Ui_reg_window
from menu import Ui_menu
from db import db
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

class LoginApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.Login.clicked.connect(self.login)
        self.ui.Register.clicked.connect(self.open_registration)

        self.registration_window = RegistrationWindow()
        self.menu_window = MenuWindow()

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

            Auth.login(email, password)
            QMessageBox.information(self, "Success", "Login successful.")
            self.open_menu()

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

    def show_first_page(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def show_second_page(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def show_third_page(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def logout(self):
        # Prikazivanje poruke za potvrdu odjave
        reply = QMessageBox.question(self, 'Logout', 'Are you sure you want to logout?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        # Ako korisnik odabere "Yes" za odjavu
        if reply == QMessageBox.Yes:
            self.close()
            self.login_window = LoginApp()
            self.login_window.show()

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