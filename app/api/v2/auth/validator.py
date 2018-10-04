import re


def credentials_checker(username, password, email):
    """Checks the validity of credentials during signup"""

    num = re.compile(r'[0-9]')
    low = re.compile(r'[a-z]')
    upper = re.compile(r'[A-Z]')
    text = re.compile(r'[A-Za-z]')
    mail = re.compile(r'[\w\.-]+@[a-z]+\.[a-z]{2,4}')

    check_email = mail.findall(email)
    characters = text.findall(username)
    if len(characters) != len(username):
        return 'Enter only alphabetic characters for your username'
    if len(password) <= 6:
        return 'Enter a password longer than 6 characters'
    if not (upper.findall(password) and low.findall(password) and num.findall(password)):
        return 'Password must have atleast one lowercase one upper case and one digit'
    if not check_email or len(check_email[0]) != len(email):
        return 'Enter the correct format of the email e.g. johndoe@mail.com'
    return username, password
