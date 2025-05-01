import os
import toga
from toga.style.pack import ROW, COLUMN
from staffee.user_account import UserAccount
from staffee.chat import ChatView  # Import the ChatView class for handling the chat screen
import mysql.connector

class IconManager:
    def __init__(self, app):
        """
        Initialize the IconManager with the application instance.
        
        Args:
            app: The main application instance
        """
        self.app = app
        self.account_view = UserAccount(app)

        self.icons = {}
        self.fallback_icons = {
            'cal-24': '📅',
            'home-24': '🏠',
            'chat-24': '💬',
            'noti-24': '🔔',
            'acc-24': '👤'
        }
        self._load_icons()

    def _load_icons(self):
        """Load all icons from the resources directory and store them for reuse."""
        try:
            images_dir = self.app.paths.app / "resources" / "navi_icons"
            icon_names = ['cal-24', 'home-24', 'chat-24', 'noti-24', 'acc-24']
            
            for name in icon_names:
                icon_path = os.path.join(images_dir, f"{name}.png")
                try:
                    self.icons[name] = toga.Icon(icon_path)
                    print(f"Loaded icon: {name}")
                except Exception as e:
                    print(f"Error loading icon {name}: {e}")
                    self.icons[name] = None
                    
            print("Icons loaded successfully")
        except Exception as e:
            print(f"Error initializing icons: {e}")

    def get_icon(self, name):
        """Get an icon by name."""
        return self.icons.get(name)

    def get_fallback(self, name):
        """Get a fallback text icon by name."""
        return self.fallback_icons.get(name, '•')

    def create_action_box(self, on_press_handler):
        """Create an action box with new job button and calendar button."""
        new_job_button = toga.Button(
            '+ New job',
            on_press=on_press_handler,
            style=toga.style.Pack(
                padding = 0,
                width=100,
                height=40,
                background_color='#FFFFFF',
                color='#228b22',
                font_size=10,
                text_align="center",
            )
        )
        
        cal_icon = self.get_icon('cal-24')
        if cal_icon:
            calendar_button = toga.Button(
                icon=cal_icon,
                on_press=on_press_handler,
                style=toga.style.Pack(
                    width=70,
                    height=70,
                    padding=0,
                    alignment="center"
                )
            )
        else:
            calendar_button = toga.Button(
                self.get_fallback('cal-24'),
                on_press=on_press_handler,
                style=toga.style.Pack(
                    width=70,
                    height=70,
                    padding=0
                )
            )
        
        action_box = toga.Box(
            children=[new_job_button, calendar_button],
            style=toga.style.Pack(
                direction=ROW, 
                alignment='center'
            )
        )
        
        return action_box
        
    def create_new_job_button(self, on_press_handler):
        """Create a new job button with standardized styling."""
        new_job_button = toga.Button(
            '+ New job',
            on_press=on_press_handler,
            style=toga.style.Pack(
                padding=0,
                width=100,
                height=40,
                background_color='#FFFFFF',
                color='#228b22',
                font_size=10,
                alignment="center",
                flex = 1,
                text_align = "center"
            )
        )
        
        return new_job_button

    def create_back_button(self, on_press_handler):
        """Create a back button with standardized styling."""
        back_button = toga.Button(
            '← Back',
            on_press=on_press_handler,
            style=toga.style.Pack(
                padding=0,
                width=80,
                height=40,
                background_color='#228b22',
                color='#FFFFFF',
                font_size=7,
                text_align="center"
            )
        )
        
        return back_button

    def create_calendar_button(self, on_press_handler):
        """Create a calendar button with the calendar icon - Android optimized."""
        cal_icon = self.get_icon('cal-24')
        
        if cal_icon:
            calendar_button = toga.Button(
                icon=cal_icon,
                on_press=on_press_handler,
                style=toga.style.Pack(
                    width=70,      
                    height=70,     
                    padding=0,     
                    alignment = "center"
                )
            )
        else:
            calendar_button = toga.Button(
                self.get_fallback('cal-24'),
                on_press=on_press_handler,
                style=toga.style.Pack(
                    width=70,
                    height=70,
                    padding=0
                )
            )
            
        return calendar_button

    def create_nav_bar(self):
        """Create a navigation bar with Android-optimized button sizes."""
        nav_items = [
            ('Home', 'home-24', self.home_action),
            ('Chat', 'chat-24', self.chat_action),
            ('Notifications', 'noti-24', self.noti_action),
            ('Account', 'acc-24', self.acc_action)
        ]
        
        nav_box = toga.Box(
            style=toga.style.Pack(
                direction=ROW, 
                alignment='center',
                padding=0
            )
        )
        
        for label, icon_name, button_action in nav_items:
            icon = self.get_icon(icon_name)
            
            if icon:
                nav_button = toga.Button(
                    icon=icon,
                    on_press=button_action,
                    style=toga.style.Pack(
                        width=70,
                        height=70,
                        padding=0,
                        alignment="center"
                    )
                )
            else:
                nav_button = toga.Button(
                    self.get_fallback(icon_name),
                    on_press=button_action,
                    style=toga.style.Pack(
                        width=70,
                        height=70,
                        padding=0,
                        alignment="center"
                    )
                )
            
            label_widget = toga.Label(
                label, 
                style=toga.style.Pack(
                    font_size=10,
                    text_align='center'
                )
            )
            
            nav_item = toga.Box(
                children=[nav_button, label_widget],
                style=toga.style.Pack(
                    direction=COLUMN,
                    alignment='center',
                    flex=1,
                    padding=0
                )
            )
            
            nav_box.add(nav_item)
        
        return nav_box
    
    def home_action(self, widget):
        print("Go home")

    def chat_action(self, widget):
        """Open the Chat view in the same window."""
        try:
            self.app.navigation_history.append(self.app.current_view)
            self.app.current_view = "chat_view"
            self.app.main_window.title = "Chat View"

            # Correctly pass db_config now
            chat_view = ChatView(self.app, self.app.DB_CONFIG)
            chat_content = chat_view.create_content()

            # Initialize chat view with current user data
            chat_view.initialize_user_data(
                self.app.current_user["uid"],
                self.app.current_user["type"]
            )

            self.app.main_window.content = chat_content

        except Exception as e:
            print(f"Error in chat_action: {e}")

    def noti_action(self, widget):
        print("Go notifications")

    def acc_action(self, widget=None):
        if self.app.current_user["type"] == "Applicant":
                                
            """Open the Account view in the same window."""
            try:
                self.app.navigation_history.append(self.app.current_view)
                self.app.current_view = "account_view"
                self.app.main_window.title = "Account View"

                account_content = self.account_view.create_content()
                self.app.main_window.content = account_content
            except Exception as e:
                print(f"Error in acc_action: {e}")

        else: print("hello")