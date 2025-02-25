import os
import toga
from toga.style import Pack
from toga.constants import *
from staffee.owner_view_staff import OwnerViewStaffWindow

class MainApp(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)
        
        # Create main content
        main_content = self.create_main_content()
        self.main_window.content = main_content
        self.main_window.show()
    
    def create_main_content(self):
        # Load icons - fix the double assignment and don't try to create directories
        images_dir = self.paths.app / "resources" / "images"
    
        # Add debug print to see if the directory exists
        print(f"Looking for images in: {images_dir}")
        print(f"Directory exists: {os.path.exists(images_dir)}")
    
        try:
            cal_icon = toga.Icon(os.path.join(images_dir, "calendar.png"))
            home_icon = toga.Icon(os.path.join(images_dir, "home.png"))
            chat_icon = toga.Icon(os.path.join(images_dir, "chat.png"))
            noti_icon = toga.Icon(os.path.join(images_dir, "notification.png"))
            user_icon = toga.Icon(os.path.join(images_dir, "user.png"))
            print("Icons loaded successfully")
        except Exception as e:
            print(f"Error loading icons: {e}")
            cal_icon = home_icon = chat_icon = noti_icon = user_icon = None
        
        
        # Button to open the Owner View Staff window
        open_staff_view_button = toga.Button(
            'Open Owner View Staff',
            on_press=self.open_owner_view_staff,
            style=Pack(
                padding=(20, 5),
                width=200,
                height=40,
                background_color='#228b22',
                color='#FFFFFF',
            )
        )

        # Header
        title_label = toga.Label('Main Application', style=Pack(font_size=18, font_weight='bold', padding=(20, 20, 10, 20)))

        # Navigation bar
        nav_items = [
            ('Home', home_icon, '🏠'),
            ('Chat', chat_icon, '💬'),
            ('Notifications', noti_icon, '🔔'),
            ('Account', user_icon, '👤')
        ]

        new_job_button = toga.Button(
            '+ New job',
            on_press=self.placeholder_action,
            style=Pack(
                padding=(20, 5),
                width=100,
                height=30,
                background_color='#FFFFFF',
                color='#228b22',
            )
        )

        # Calendar button with icon handling
        if cal_icon:
            calendar_button = toga.Button(
                icon=cal_icon,
                on_press=self.placeholder_action,
                style=Pack(padding=(20, 5), width=50, height=50)
            )
        else:
            calendar_button = toga.Button(
                '📅',
                on_press=self.placeholder_action,
                style=Pack(padding=(20, 5), width=50, height=50)
            )

        header_box = toga.Box(
            children=[title_label, new_job_button, calendar_button],
            style=Pack(direction=ROW, alignment='center', padding=(0, 10))
        )

        ############ END OF CODE INVOLVING HEADER STUFF ############

        # Navigation bar
        nav_items = [
            ('Home', home_icon, '🏠'),
            ('Chat', chat_icon, '💬'),
            ('Notifications', noti_icon, '🔔'),
            ('Account', user_icon, '👤')
        ]
        
        nav_box = toga.Box(
            style=Pack(direction=ROW, alignment='center', padding=5)
        )
        
        for label, icon, fallback in nav_items:
            if icon:
                nav_button = toga.Button(
                    icon=icon,
                    on_press=self.placeholder_action,
                    style=Pack(width=50, height=50)
                )
            else:
                nav_button = toga.Button(
                    fallback,
                    on_press=self.placeholder_action,
                    style=Pack(width=50, height=50)
                )

            label_widget = toga.Label(
                label, 
                style=Pack(
                    font_size=12,
                    padding=(5, 0, 0, 0),
                    text_align='center'
                )
            )

            nav_item = toga.Box(
                children=[nav_button, label_widget],
                style=Pack(
                    direction=COLUMN,
                    alignment='center',
                    flex=1,
                    padding=(5, 10)
                )
            )
            nav_box.add(nav_item)
        
        # Main content layout
        main_content = toga.Box(
            children=[
                header_box,
                open_staff_view_button,
                toga.Box(style=Pack(flex=1)),  # Spacer
                nav_box
            ],
            style=Pack(direction=COLUMN, padding=20)
        )
        
        return main_content
    
    def open_owner_view_staff(self, widget):
        """Open the Owner View Staff window"""
        staff_window = OwnerViewStaffWindow() 
        self.windows.add(staff_window) # adding the window to the app's window collecction
        staff_window.show() # showing the window 
    
    def placeholder_action(self, widget):
        """Placeholder for button actions"""
        pass

def main():
    return MainApp("Staffee Demo", "org.example.demoApp")
