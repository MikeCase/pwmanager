from cryptography.fernet import Fernet
import string
from random import randint, choice

class PWManager:

    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}

    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)

    def load_key(self, path):
        with open(path, 'rb') as f:
            self.key = f.read()

    def create_pwd_file(self, path, initial_vals=None):
        self.password_file = path

        if initial_vals is not None:
            for key, val in initial_vals.items():
                self.add_pwd(key, val)

    def load_pwd_file(self, path):
        self.password_file = path
        
        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.split(':')
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode('utf-8')

    def add_pwd(self, site, pwd):
        self.password_dict[site] = pwd
        
        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(pwd.encode())
                f.write(f'{site}:{encrypted.decode()}\n')
        
    def get_pwd(self, site):
        return self.password_dict[site]

    def generate_pwd(self, min_length, max_length, char_set):
        password_min = int(min_length)
        password_max = int(max_length)
        char_dict = {
            'letters': string.ascii_letters,
            'digits': string.digits,
            'special': string.punctuation,
        }
        all_chars = ""

        for char in char_set:
            all_chars += char_dict[char]

        password = "".join(choice(all_chars) for x in range(randint(password_min,password_max)))
        return password
        

def main():
    pwm = PWManager()
    
    print("""What do you want to do?
    (1) Create new key
    (2) Load existing key
    (3) Create new password file
    (4) Load existing password file
    (5) Add new password
    (6) Get a password
    (7) Generate password
    (q) Quit

    """)

    done = False
    while not done:
        opt = input("Enter your choice: ")
        if opt == "1":
            path = input("Enter path for key file (include filename): ")
            pwm.create_key(path)

        elif opt == "2":
            path = input("Enter path of key file: ")
            pwm.load_key(path)

        elif opt == "3":
            path = input("Enter Path: ")
            pwm.create_pwd_file(path)

        elif opt == "4":
            path = input("Enter Path: ")
            pwm.load_pwd_file(path)

        elif opt == "5":
            site = input("Enter the site: ")
            pwd = input("Enter password (or G for random password): ")
            if pwd == "g".upper() or "g".lower():
                pwd = pwm.generate_pwd(6,24, ["letters","digits","special"])
            pwm.add_pwd(site, pwd)

        elif opt == "6":
            site = input("Enter the site: ")
            print(f"Password for {site} is {pwm.get_pwd(site)}")

        elif opt == "7":
            min_pw_len = input("Minimum length of password: ")
            max_pw_len = input("Maximum password length: ")
            chars = input("""Please choose all characters you want to use. I.E. 1, 2, 3 or 1, 2 or 2,3 etc. 

            (1) All letters upper and lower case
            (2) All digits 0-9
            (3) All special characters
            """)

            chars = chars.strip(" ").split(",")
            char_set = []
            if '1' in chars:
                char_set.append('letters')
            if '2' in chars:
                char_set.append('digits')
            if '3' in chars:
                char_set.append('special')

            password = pwm.generate_pwd(min_pw_len, max_pw_len, char_set)
            print(f"Generated Password: {password}.")

        elif opt == "q":
            done = True

if __name__ == '__main__':
    main()