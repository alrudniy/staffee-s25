import toga
import bcrypt
import mysql.connector
from toga.style import Pack
from toga.constants import COLUMN

# Database connection details
DB_CONFIG = {
    "host": "34.125.69.91",
    "user": "staffee_user",
    "password": "SmoothS@iling",
    "database": "staffee",
    "charset": "utf8mb4",  # Ensure this matches your database setup
    "collation": "utf8mb4_general_ci"  # Use a compatible collation
}

class BeeWareApp(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.show_login_screen()
        self.main_window.show()

    def show_login_screen(self, widget=None):
        """Display the login screen."""
        title = toga.Label("Sign In", style=Pack(padding=(40, 0, 30, 0), text_align="center", font_weight="bold", font_size=30, background_color="white"))
        email_label = toga.Label("Email", style=Pack(padding=(0, 0, 0, 8), font_weight="bold", font_size=10, background_color="white"))
        self.username_input = toga.TextInput(placeholder="georgia.young@example.com", style=Pack(padding=(10, 10, 20, 10), font_size=15))
        password_label = toga.Label("Password", style=Pack(padding=(0, 0, 0, 8), font_weight="bold", font_size=10, background_color="white"))
        self.password_input = toga.PasswordInput(placeholder="", style=Pack(padding=(10, 10, 20, 10), font_size=15))

        login_button = toga.Button("Sign In", on_press=self.login, style=Pack(padding=9, background_color="green", color="white", height=50, font_size=10, font_weight="bold"))

        donthaveacc = toga.Label("Don't have an account?", style=Pack(font_size=12, background_color="white", padding_right=5))
        create_account_label = toga.Button("Sign Up", on_press=self.show_create_account_screen, style=Pack(background_color="white", color="green", font_size=12))

        account_box = toga.Box(children=[donthaveacc, create_account_label], style=Pack(direction="row", alignment="center", padding=10, background_color="white"))

        self.message_label = toga.Label("", style=Pack(padding=5, color="red", background_color="white"))

        box = toga.Box(
            children=[title, email_label, self.username_input, password_label, self.password_input, login_button, account_box, self.message_label],
            style=Pack(direction=COLUMN, alignment="center", padding=10, background_color="white")
        )

        self.main_window.content = box

    def show_create_account_screen(self, widget=None):
        """Display the Create Account screen."""
        title = toga.Label("Create a free account", style=Pack(padding=(40, 0, 30, 0), text_align="center", font_weight="bold", font_size=30, background_color="white"))
        email_label = toga.Label("Email", style=Pack(padding=(0, 0, 0, 8), font_weight="bold", font_size=10, background_color="white"))
        self.email_input = toga.TextInput(placeholder="your.email@example.com", style=Pack(padding=(10, 10, 20, 10), font_size=15))

        password_label = toga.Label("Password", style=Pack(padding=(0, 0, 0, 8), font_weight="bold", font_size=10, background_color="white"))
        self.password_input = toga.PasswordInput(style=Pack(padding=(10, 10, 20, 10), font_size=15))

        confirm_password_label = toga.Label("Confirm Password", style=Pack(padding=(0, 0, 0, 8), font_weight="bold", font_size=10, background_color="white"))
        self.confirm_password_input = toga.PasswordInput(style=Pack(padding=(10, 10, 20, 10), font_size=15))

        create_button = toga.Button("Create Account", on_press=self.create_account, style=Pack(padding=9, background_color="green", color="white", height=50, font_size=10, font_weight="bold"))
        back_button = toga.Button("Back to Login", on_press=self.show_login_screen, style=Pack(padding=9, background_color="gray", color="white", height=50, font_size=10, font_weight="bold"))

        self.message_label = toga.Label("", style=Pack(padding=5, color="red", background_color="white"))

        box = toga.Box(
            children=[title, email_label, self.email_input, password_label, self.password_input, confirm_password_label, self.confirm_password_input, create_button, back_button, self.message_label],
            style=Pack(direction=COLUMN, alignment="center", padding=10, background_color="white")
        )
        self.main_window.content = box

    def create_account(self, widget):
        """Handle account creation."""
        email = self.email_input.value
        password = self.password_input.value
        confirm_password = self.confirm_password_input.value

        if not email or not password or not confirm_password:
            self.message_label.text = "All fields are required."
            return

        if password != confirm_password:
            self.message_label.text = "Passwords do not match."
            return

        hashed_password = self.hash_password(password)

        if self.insert_user(email, hashed_password):
            self.message_label.text = "Account created successfully!"
            self.show_login_screen()
        else:
            self.message_label.text = "Error creating account. Try again."

    def hash_password(self, plain_text_password):
        """Hash the password securely."""
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(plain_text_password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    def insert_user(self, email, hashed_password):
        """Insert a new user into the database."""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            query = "INSERT INTO Users (email, password) VALUES (%s, %s)"
            cursor.execute(query, (email, hashed_password))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            self.message_label.text = f"Database error: {err}"
            return False

    def login(self, widget):
        """Handle user login."""
        username = self.username_input.value
        password = self.password_input.value

        if self.authenticate_user(username, password):
            self.show_screen_a()
        else:
            self.message_label.text = "Invalid credentials. Please try again."

    def authenticate_user(self, email, password):
        """Authenticate user against the database using hashed passwords."""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)

            query = "SELECT password FROM Users WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()

            cursor.close()
            conn.close()

            if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                return True
            else:
                return False
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return False

    def show_screen_a(self, widget=None):
        """Placeholder screen after login."""
        label = toga.Label("Welcome!", style=Pack(padding=5))
        logout_button = toga.Button("Log Out", on_press=self.show_login_screen, style=Pack(padding=5))

        box = toga.Box(children=[label, logout_button], style=Pack(direction=COLUMN, alignment="center", padding=10))
        self.main_window.content = box

def main():
    return BeeWareApp("BeeWare Navigation App", "org.example.bewareapp")

if __name__ == "__main__":
    app = main()
    app.main_loop()