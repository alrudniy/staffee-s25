import toga
from toga.style import Pack
from toga.constants import COLUMN

class BeeWareApp(toga.App):
    def startup(self):
        # Create a main window for the application
        self.main_window = toga.MainWindow(title=self.formal_name)
        # Start with the login screen
        self.show_login_screen()
        self.main_window.show()

    def show_login_screen(self):
        # --- Login Screen ---
        title = toga.Label("Login", style=Pack(padding=(0, 0, 20, 0)))
        self.username_input = toga.TextInput(placeholder="Username", style=Pack(padding=5))
        self.password_input = toga.PasswordInput(placeholder="Password", style=Pack(padding=5))
        login_button = toga.Button("Login", on_press=self.login, style=Pack(padding=5))
        # Label to show error messages
        self.message_label = toga.Label("", style=Pack(padding=5, color="red"))

        # Arrange login widgets in a vertical box
        box = toga.Box(
            children=[title, self.username_input, self.password_input, login_button, self.message_label],
            style=Pack(direction=COLUMN, alignment="center", padding=10)
        )
        self.main_window.content = box

    def login(self, widget):
        username = self.username_input.value
        password = self.password_input.value
        print(f"Attempting login with Username: {username}, Password: {password}")

        # Check if the credentials are correct
        if username == "user" and password == "testing":
            self.show_screen_a()
        else:
            self.message_label.text = "Invalid credentials. Please try again."

    def logout(self, widget):
        # Return to the login screen.
        self.show_login_screen()

    def show_screen_a(self, widget=None):
        # --- Screen A ---
        label = toga.Label("Screen A", style=Pack(padding=5))
        button_to_b = toga.Button("Go to Screen B", on_press=self.show_screen_b, style=Pack(padding=5))
        button_to_c = toga.Button("Go to Screen C", on_press=self.show_screen_c, style=Pack(padding=5))
        logout_button = toga.Button("Log Out", on_press=self.logout, style=Pack(padding=5))

        box = toga.Box(
            children=[label, button_to_b, button_to_c, logout_button],
            style=Pack(direction=COLUMN, alignment="center", padding=10)
        )
        self.main_window.content = box

    def show_screen_b(self, widget=None):
        # --- Screen B ---
        label = toga.Label("Screen B", style=Pack(padding=5))
        button_to_a = toga.Button("Go to Screen A", on_press=self.show_screen_a, style=Pack(padding=5))
        button_to_c = toga.Button("Go to Screen C", on_press=self.show_screen_c, style=Pack(padding=5))
        logout_button = toga.Button("Log Out", on_press=self.logout, style=Pack(padding=5))

        box = toga.Box(
            children=[label, button_to_a, button_to_c, logout_button],
            style=Pack(direction=COLUMN, alignment="center", padding=10)
        )
        self.main_window.content = box

    def show_screen_c(self, widget=None):
        # --- Screen C ---
        label = toga.Label("Screen C", style=Pack(padding=5))
        button_to_a = toga.Button("Go to Screen A", on_press=self.show_screen_a, style=Pack(padding=5))
        button_to_b = toga.Button("Go to Screen B", on_press=self.show_screen_b, style=Pack(padding=5))
        logout_button = toga.Button("Log Out", on_press=self.logout, style=Pack(padding=5))

        box = toga.Box(
            children=[label, button_to_a, button_to_b, logout_button],
            style=Pack(direction=COLUMN, alignment="center", padding=10)
        )
        self.main_window.content = box

def main():
    return BeeWareApp("BeeWare Navigation App", "org.example.bewareapp")

if __name__ == "__main__":
    app = main()
    app.main_loop()

