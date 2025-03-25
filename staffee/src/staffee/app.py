import os
import bcrypt
import toga
import mysql.connector
from toga.style import Pack
from toga.constants import COLUMN, ROW
from staffee.owner_view_staff import OwnerViewStaff
from staffee.profile_view import ProfileView
from staffee.icon_manager import IconManager

# Database connection details
DB_CONFIG = {
    "host": "34.125.69.91",
    "user": "staffee_user",
    "password": "SmoothS@iling",
    "database": "staffee",
    "charset": "utf8mb4",
    "collation": "utf8mb4_general_ci"
}

class MainApp(toga.App):
    def startup(self):
        # Create main window
        self.main_window = toga.MainWindow(title=self.formal_name)
        

        # Initialize icon manager
        self.icon_manager = IconManager(self)
        
        # Create main content
        self.main_content = self.create_main_content()
        
        # Initialize view modules
        self.staff_view = OwnerViewStaff(self)
        self.profile_view = ProfileView(self)

        # Show login screen first
        self.show_login_screen()
        self.main_window.show()
        
        # Track navigation
        self.navigation_history = []
        self.current_view = "login"
    
    def show_login_screen(self):
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

    def show_create_account_screen(self, widget):
        """Display the Create Account screen."""
        title = toga.Label("Create a\nfree account", style=Pack(padding=(40, 0, 30, 0), text_align="center", font_weight="bold", font_size=30, background_color="white"))
        email_label = toga.Label("Email", style=Pack(padding=(0, 0, 0, 8), font_weight="bold", font_size=10, background_color="white"))
        self.email_input = toga.TextInput(placeholder="your.email@example.com", style=Pack(padding=(10, 10, 20, 10), font_size=15))

        password_label = toga.Label("Password", style=Pack(padding=(0, 0, 0, 8), font_weight="bold", font_size=10, background_color="white"))
        self.password_input = toga.PasswordInput(style=Pack(padding=(10, 10, 20, 10), font_size=15))

        confirm_password_label = toga.Label("Confirm Password", style=Pack(padding=(0, 0, 0, 8), font_weight="bold", font_size=10, background_color="white"))
        self.confirm_password_input = toga.PasswordInput(style=Pack(padding=(10, 10, 20, 10), font_size=15))
        
        user_type_label = toga.Label(
            "I am a:",
            style=Pack(padding=(0, 0, 0, 8), font_weight="bold", font_size=10, background_color="white")
        )
        self.user_type_selection = toga.Selection(
            items=["Business Owner", "Applicant"],
            style=Pack(padding=(10, 10, 20, 10), font_size=15)
        )

        create_button = toga.Button("Create Account", on_press=self.create_account, style=Pack(padding=9, background_color="green", color="white", height=50, font_size=10, font_weight="bold"))
        alreadyhaveacc = toga.Label("Already have an account?", style=Pack(font_size=12, background_color="white", padding_right=5))

        back_button = toga.Button("Sign In",  on_press=lambda widget: self.show_login_screen(), style=Pack(background_color="white", color="green", font_size=12))
        account_box = toga.Box(children=[alreadyhaveacc, back_button], style=Pack(direction="row", alignment="center", padding=10, background_color="white"))

        self.message_label = toga.Label("", style=Pack(padding=5, color="red", background_color="white"))

        box = toga.Box(
            children=[title, email_label, self.email_input, password_label, self.password_input, confirm_password_label, self.confirm_password_input, user_type_label, self.user_type_selection, create_button, account_box, self.message_label],
            style=Pack(direction=COLUMN, alignment="center", padding=10, background_color="white")
        )
        self.main_window.content = box

    def create_account(self, widget):
        """Handle account creation."""
        email = self.email_input.value
        password = self.password_input.value
        confirm_password = self.confirm_password_input.value
        usertype = self.user_type_selection.value

        if not email or not password or not confirm_password:
            self.message_label.text = "All fields are required."
            return

        if password != confirm_password:
            self.message_label.text = "Passwords do not match."
            return

        hashed_password = self.hash_password(password)

        if self.insert_user(email, hashed_password, usertype):
            self.message_label.text = "Account created successfully!"
            self.show_login_screen()
        else:
            self.message_label.text = "Error creating account. Try again."

    def hash_password(self, plain_text_password):
        """Hash the password securely."""
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(plain_text_password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    def insert_user(self, email, hashed_password, usertype):
        """Insert a new user into the database."""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            query = "INSERT INTO Users (email, password, type) VALUES (%s, %s, %s)"
            cursor.execute(query, (email, hashed_password, usertype))
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

        usertype = self.authenticate_user(username, password)
        
        if usertype:
            if usertype == "Business Owner":
                self.open_owner_view_staff(widget)
            else:
                self.create_main_content()
        else:
            self.message_label.text = "Invalid credentials. Please try again."

    def authenticate_user(self, email, password):
        """Check the database for user credentials and return the user type."""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)

            # Modified query to also fetch the user type
            query = "SELECT password, type FROM Users WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()

            if not user:
                print("No user found with that email.")
                return None

            print(f"Retrieved user: {user}")  # Debugging

            if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                return user['type']  # Return the user type if credentials are correct
            else:
                print("Password does not match.")  # Debugging
                return None
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return None
    
    def show_main_content(self):
        """Replace login screen with main app content."""
        self.current_view = "main"
        self.main_window.title = "Main Application"

        # Load icons
        images_dir = self.paths.app / "resources" / "images"
        try:
            cal_icon = toga.Icon(os.path.join(images_dir, "calendar.png"))
            home_icon = toga.Icon(os.path.join(images_dir, "home.png"))
            chat_icon = toga.Icon(os.path.join(images_dir, "chat.png"))
            noti_icon = toga.Icon(os.path.join(images_dir, "notification.png"))
            user_icon = toga.Icon(os.path.join(images_dir, "user.png"))
        except Exception:
            cal_icon = home_icon = chat_icon = noti_icon = user_icon = None
        
        # Button to open staff view
        open_staff_view_button = toga.Button(
            'Open Owner View Staff',
            on_press=self.open_owner_view_staff,
            style=Pack(padding=(20, 5), width=200, height=40, background_color='#228b22', color='#FFFFFF')
        )
    
    def create_main_content(self):
        # Load icons
        self.current_view = "main"
        self.main_window.title = "Main Application"

        images_dir = self.paths.app / "resources" / "images"
        try:
            cal_icon = toga.Icon(os.path.join(images_dir, "calendar.png"))
            home_icon = toga.Icon(os.path.join(images_dir, "home.png"))
            chat_icon = toga.Icon(os.path.join(images_dir, "chat.png"))
            noti_icon = toga.Icon(os.path.join(images_dir, "notification.png"))
            user_icon = toga.Icon(os.path.join(images_dir, "user.png"))
        except Exception:
            cal_icon = home_icon = chat_icon = noti_icon = user_icon = None

        # Button to open the Owner View Staff screen
        open_staff_view_button = toga.Button(
            'Open Owner View Staff',
            on_press=self.open_owner_view_staff,
            style=Pack(
                padding=(20, 5),
                width=200,
                height=40,
                background_color='#228b22',
                color='#FFFFFF',
                font_size=10
            )
        )

        # Header
        title_label = toga.Label('Main Application', style=Pack(font_size=18, font_weight='bold', padding=(20, 20, 10, 20)))
        new_job_button = toga.Button('+ New job', on_press=self.placeholder_action, style=Pack(padding=(20, 5), width=100, height=30))
        
        # Calendar button now correctly references cal_icon
        calendar_button = toga.Button(icon=cal_icon if cal_icon else '📅', on_press=self.placeholder_action, style=Pack(padding=(20, 5), width=30, height=30))

        header_box = toga.Box(children=[title_label, new_job_button, calendar_button], style=Pack(direction=ROW, alignment='center', padding=(0, 10)))

        # Navigation bar
        nav_items = [
            ('Home', home_icon, '🏠'),
            ('Chat', chat_icon, '💬'),
            ('Notifications', noti_icon, '🔔'),
            ('Account', user_icon, '👤')
        ]

        nav_box = toga.Box(style=Pack(direction=ROW, alignment='center', padding=5))

        for label, icon, fallback in nav_items:
            nav_button = toga.Button(icon=icon if icon else fallback, on_press=self.placeholder_action, style=Pack(width=30, height=30))
            label_widget = toga.Label(label, style=Pack(font_size=12, padding=(5, 0, 0, 0), text_align='center'))

            nav_item = toga.Box(children=[nav_button, label_widget], style=Pack(direction=COLUMN, alignment='center', flex=1, padding=(5, 10)))
            nav_box.add(nav_item)

        # Main content layout
        main_content = toga.Box(
            children=[header_box, open_staff_view_button, toga.Box(style=Pack(flex=1)), nav_box],
            style=Pack(direction=COLUMN, padding=20)
        )

        self.main_window.content = main_content

        # Header
        title_label = toga.Label('Main Application', style=Pack(font_size=18, font_weight='bold', padding=(20, 20, 10, 20)))
        new_job_button = toga.Button('+ New job', on_press=self.placeholder_action, style=Pack(padding=(20, 5), width=100, height=30))

        # Calendar button
        calendar_button = toga.Button(icon=cal_icon if cal_icon else '📅', on_press=self.placeholder_action, style=Pack(padding=(20, 5), width=30, height=30))

        header_box = toga.Box(children=[title_label, new_job_button, calendar_button], style=Pack(direction=ROW, alignment='center', padding=(0, 10)))

        # Navigation bar
        nav_items = [
            ('Home', home_icon, '🏠'),
            ('Chat', chat_icon, '💬'),
            ('Notifications', noti_icon, '🔔'),
            ('Account', user_icon, '👤')
        ]

        nav_box = toga.Box(style=Pack(direction=ROW, alignment='center', padding=5))
        
        for label, icon, fallback in nav_items:
            nav_button = toga.Button(icon=icon if icon else fallback, on_press=self.placeholder_action, style=Pack(width=30, height=30))
            label_widget = toga.Label(label, style=Pack(font_size=12, padding=(5, 0, 0, 0), text_align='center'))

            nav_item = toga.Box(children=[nav_button, label_widget], style=Pack(direction=COLUMN, alignment='center', flex=1, padding=(5, 10)))
            nav_box.add(nav_item)

        # Get action box (new job button and calendar button) from icon manager
        action_box = self.icon_manager.create_action_box(self.placeholder_action)

        header_box = toga.Box(
            children=[title_label, action_box],
            style=Pack(direction=ROW, alignment='center', padding=(0, 10))
        )

        ############ END OF CODE INVOLVING HEADER ############

        ############ NAVIGATION BAR CODE HERE ################ 

        # Navigation bar - use the icon manager to create it
        nav_box = self.icon_manager.create_nav_bar(self.placeholder_action)
        
        # Main content layout
        main_content = toga.Box(
            children=[header_box, open_staff_view_button, toga.Box(style=Pack(flex=1)), nav_box],
            style=Pack(direction=COLUMN, padding=20)
        )

        self.main_window.content = main_content

    def open_owner_view_staff(self, widget):
        """Navigate to the Owner View Staff screen."""
        try:
            self.navigation_history.append(self.current_view)
            self.current_view = "staff_view"
            staff_content = self.staff_view.create_content()
            self.main_window.title = "Staff View"
            self.main_window.content = staff_content
        except Exception as e:
            print(f"Error in open_owner_view_staff: {e}")

    def placeholder_action(self, widget):
        """Placeholder for button actions."""
        print("Placeholder action triggered")

def main():
    return MainApp("Staffee Demo", "org.example.demoApp")