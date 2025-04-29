import toga
import mysql.connector
import re
from toga.style import Pack
from toga.constants import COLUMN, ROW
from staffee.owner_view_staff import OwnerViewStaff
from staffee.profile_view import ProfileView
from staffee.icon_manager import IconManager
from staffee.chat import ChatView
from staffee.user_account import UserAccount
from staffee.settings import SettingsView
from staffee.edit_staff_profile import EditStaffProfile
from passlib.hash import pbkdf2_sha256  # Use passlib's pbkdf2_sha256 hasher (pure Python)
import os

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
        self.DB_CONFIG = DB_CONFIG
        # Create main window
        self.main_window = toga.MainWindow(title=self.formal_name)
        
        # Initialize icon manager - do this early so icons are available throughout the app
        self.icon_manager = IconManager(self)
        
        # Initialize view modules
        self.profile_view = ProfileView(self)

        self.user_account = UserAccount(self)
        self.settings_view = SettingsView(self)
        self.edit_staff_profile = EditStaffProfile(self)
        
        # Create main content
        self.main_content = self.create_main_content()

        # Store user information once logged in
        self.current_user = {
            "uid": None,
            "email": None,
            "first_name": None,
            "last_name": None,
            "type": None
        }

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

        first_name_label = toga.Label("First name", style=Pack(padding=(0, 0, 0, 8), font_weight="bold", font_size=10, background_color="white"))
        self.first_name_input = toga.TextInput(placeholder="i.e. John", style=Pack(padding=(10, 10, 20, 10), font_size=15))

        last_name_label = toga.Label("Last name", style=Pack(padding=(0, 0, 0, 8), font_weight="bold", font_size=10, background_color="white"))
        self.last_name_input = toga.TextInput(placeholder="i.e. Doe", style=Pack(padding=(10, 10, 20, 10), font_size=15))

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
            children=[title, email_label, self.email_input, first_name_label, self.first_name_input,
                    last_name_label, self.last_name_input, password_label, self.password_input, 
                    confirm_password_label, self.confirm_password_input, user_type_label, self.user_type_selection, create_button, account_box, self.message_label],
            style=Pack(direction=COLUMN, alignment="center", padding=10, background_color="white")
        )
        self.main_window.content = box

    def create_account(self, widget):
        """Handle account creation."""
        first_name = self.first_name_input.value
        last_name = self.last_name_input.value
        email = self.email_input.value
        password = self.password_input.value
        confirm_password = self.confirm_password_input.value
        usertype = self.user_type_selection.value

        # Default profile picture path
        default_img = "defaultpfp.png"
        # Validate all fields are filled
        if not first_name or not last_name or not email or not password or not confirm_password:
            self.message_label.text = "All fields are required."
            return

        # Check if passwords match
        if password != confirm_password:
            self.message_label.text = "Passwords do not match."
            return
        
        def is_valid_email(address):
            pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            return re.match(pattern, address) is not None

        if is_valid_email(email) == False:
            self.message_label.text = "Email is invalid."
            return
        
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()

            # Query to check if the email exists
            cursor.execute("SELECT COUNT(*) FROM Users WHERE email = %s", (email,))
            (count,) = cursor.fetchone()

            if count > 0:
                self.message_label.text = "Email is already in use."
                cursor.close()
                conn.close()
                return

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            self.message_label.text = f"Database error: {err}"
            return
        

        # Hash the password
        hashed_password = self.hash_password(password)

        # Attempt to insert user with default profile picture path
        if self.insert_user(email, hashed_password, usertype, first_name, last_name, default_img):
            self.message_label.text = "Account created successfully!"
            self.show_login_screen()
        else:
            self.message_label.text = "Error creating account. Try again."


    def hash_password(self, plain_text_password):
        """
        Hash the password securely using passlib's pbkdf2_sha256.
        This is a pure Python implementation that works on all platforms including mobile.
        
        Args:
            plain_text_password (str): The plain text password to hash
            
        Returns:
            str: A secure hash of the password
        """
        # Use passlib's pbkdf2_sha256 hasher (pure Python implementation)
        return pbkdf2_sha256.hash(plain_text_password)

    def insert_user(self, email, hashed_password, usertype, first_name, last_name, pfp_img):
        """Insert a new user into the database."""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            query = "INSERT INTO Users (email, password, type, first_name, last_name, pfp_path) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (email, hashed_password, usertype, first_name, last_name, pfp_img))
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

        user_info = self.authenticate_user(username, password)
        
        if user_info:
            # Store user information
            self.current_user = user_info
            
            if user_info["type"] == "Business Owner":
                connector = mysql.connector.connect(**DB_CONFIG)
                UID_cursor = connector.cursor(dictionary=True)

                # Query to fetch the UID of Owner
                query = "SELECT UID FROM Users WHERE email = %s"
                UID_cursor.execute(query, (username,))
                business_owner_uid = UID_cursor.fetchone()
            
                # Close cursor and connection to prevent resource leaks
                UID_cursor.close()
                connector.close()
                
                self.current_user["uid"] = business_owner_uid['UID']
                self.open_owner_view_staff(widget, business_owner_uid['UID'])
            else:
                self.show_main_content()
        else:
            self.message_label.text = "Invalid credentials. Please try again."

    def authenticate_user(self, email, password):
        """
        Check the database for user credentials and return the user info.
        
        Args:
            email: The user's email address
            password: The user's password
            
        Returns:
            Dictionary containing user information if authentication is successful, None otherwise
        """
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)

            # Query to fetch the user's password, type, and other information
            query = "SELECT UID, email, password, type, first_name, last_name FROM Users WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()

            if not user:
                print("No user found with that email.")
                return None

            print(f"Retrieved user: {user}")  # Debugging

            # Use passlib's verify method instead of bcrypt.checkpw
            if pbkdf2_sha256.verify(password, user['password']):
                # Return user information if credentials are correct
                return {
                    "uid": user['UID'],
                    "email": user['email'],
                    "first_name": user['first_name'],
                    "last_name": user['last_name'],
                    "type": user['type']
                }
            else:
                print("Password does not match.")  # Debugging
                return None
                
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    def show_main_content(self):
        """
        Replace login screen with main app content.
        Uses the main content created by create_main_content().
        """
        self.current_view = "main"
        self.main_window.title = "Main Application"
        self.main_window.content = self.main_content
    
    def create_main_content(self):
        """
        Create the main content layout including header, main area, and navigation bar.
        
        Returns:
            toga.Box: The main content container
        """
        # Button to open the Owner View Staff screen
        open_staff_view_button = toga.Button(
            'Open Owner View Staff',
            on_press=lambda widget: self.open_owner_view_staff(widget),  # Pass widget
            style=Pack(
                padding=(20, 5),
                width=200,
                height=40,
                background_color='#228b22',
                color='#FFFFFF',
                font_size=10
            )
        )

        # Header with title
        title_label = toga.Label(
            'Main Application', 
            style=Pack(
                font_size=18, 
                font_weight='bold', 
                padding=(20, 20, 10, 20)
            )
        )

        # Get action box (new job button and calendar button) from icon manager
        action_box = self.icon_manager.create_action_box(self.placeholder_action)

        # Combine title and action box into header
        header_box = toga.Box(
            children=[title_label, action_box],
            style=Pack(direction=ROW, alignment='center', padding=(0, 10))
        )

        # Navigation bar - use the icon manager to create it
        # Modified: removed chat_action parameter to match current method signature
        nav_box = self.icon_manager.create_nav_bar()
        
        # Main content layout
        main_content = toga.Box(
            children=[header_box, open_staff_view_button, toga.Box(style=Pack(flex=1)), nav_box],
            style=Pack(direction=COLUMN, padding=20)
        )

        return main_content

    def open_owner_view_staff(self, widget, business_owner_uid=None):
        """
        Navigate to the Owner View Staff screen.
        Adds current view to navigation history for back navigation.
        """
        try:
            self.navigation_history.append(self.current_view)
            self.current_view = "staff_view"

            self.staff_view = OwnerViewStaff(self, widget, business_owner_uid)

            staff_content = self.staff_view.create_content()
            self.main_window.title = "Staff View"
            self.main_window.content = staff_content
        except Exception as e:
            print(f"Error in open_owner_view_staff: {e}")

    def open_chat_view(self, widget):
        """
        Navigate to the Chat View screen.
        """
        try:
            # Check if user is logged in
            if not self.current_user["uid"]:
                print("User not logged in")
                return

            # Add current view to navigation history
            self.navigation_history.append(self.current_view)
            self.current_view = "chat_view"
            
            # Create new chat view
            chat_view = ChatView(self, DB_CONFIG)
            
            # Create the content
            chat_content = chat_view.create_content()
            
            # Initialize with current user data
            chat_view.initialize_user_data(
                self.current_user["uid"], 
                self.current_user["type"]
            )
            
            # Set as main window content
            self.main_window.title = "Chat"
            self.main_window.content = chat_content
            
        except Exception as e:
            print(f"Error in open_chat_view: {e}")

    def placeholder_action(self, widget):
        """
        Placeholder for button actions that are not yet implemented.
        Useful for testing and UI development.
        """
        print("Placeholder action triggered")

def main():
    """
    Main entry point for the application.
    Returns the application instance.
    """
    return MainApp("Staffee Demo", "org.example.demoApp")