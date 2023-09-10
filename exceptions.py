class reg_error_taken(Exception):
    def __init__(self):
        super(reg_error_taken, self).__init__('This email address is already taken.')

class log_error_empty(Exception):
    def __init__(self):
        super(log_error_empty, self).__init__('You did not fill all required fields.')

class reg_error_empty(Exception):
    def __init__(self):
        super(reg_error_empty, self).__init__('You did not fill all required fields.')

class log_error_wrong(Exception):
    def __init__(self):
        super(log_error_wrong, self).__init__('Email and password do not match.')

class reg_error_password_mismatch(Exception):
    def __init__(self):
        super(reg_error_password_mismatch, self).__init__('Passwords do not match.')

class reg_error_invalid_domain(Exception):
    def __init__(self, domain):
        super(reg_error_invalid_domain, self).__init__(f'Invalid email domain: {domain}')

class log_error_user_not_found(Exception):
    def __init__(self):
        super(log_error_user_not_found, self).__init__('User with this email does not exist.')

class log_error_wrong_password(Exception):
    def __init__(self):
        super(log_error_wrong_password, self).__init__('Incorrect password.')

class log_error(Exception):
    def __init__(self, message):
        super().__init__(message)
