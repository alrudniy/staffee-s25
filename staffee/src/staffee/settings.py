import os
import toga 
from toga.style import Pack
from toga.constants import *
from staffee.notif_settings import NotificationSettings

class SettingsView:
    def __init__(self, app):
        # Store the app instance
        self.app = app

    # Create view
    def create_settings_view(self):
        # Back button
        back_button = self.app.icon_manager.create_back_button(self.navigate_back)

        # Chat label
        title_label = toga.Label(
            "Settings", style=Pack(padding=(15, 35, 15, 0), font_size=15, 
            font_family = 'sans-serif', flex=8, background_color="#ffffff", text_align="center"))
        
        # Header box 
        header_box = toga.Box(
            children=[back_button, title_label],
            style=Pack(direction=ROW, alignment="center", background_color="#ffffff"))


        # Add notifications button
        notifications = toga.Button(
            "Notifications",
            on_press=self.open_notif_settings_view,
            style=Pack(height=40, padding=5, background_color="#ffffff",
            color="#364052")
        )

        # Personal information
        personal_info = toga.Button(
            "Personal Information",
            on_press=self.placeholder_action,
            style=Pack(height=40, padding=5, background_color="#ffffff", color="#364052")
        )

        # Change password
        change_password = toga.Button(
            "Change Password",
            on_press=self.placeholder_action,
            style=Pack(height=40, padding=5, background_color="#ffffff", color="#364052")
        )

        # Payment options
        payment_options = toga.Button(
            "Payment Options",
            on_press=self.placeholder_action,
            style=Pack(height=40, padding=5, background_color="#ffffff", color="#364052")
        )

        # Support
        support = toga.Button(
            "Support",
            on_press=self.placeholder_action,
            style=Pack(height=40, padding=5, background_color="#ffffff", color="#364052")
        )

        # Terms of Service
        tos = toga.Button(
            "Terms of Service",
            on_press=self.placeholder_action,
            style=Pack(height=40, padding=5, background_color="#ffffff", color="#364052")
        )

        # Contents box
        contents_box = toga.Box(
            children=[notifications, toga.Divider(),
                      personal_info, toga.Divider(),
                      change_password, toga.Divider(),
                      payment_options, toga.Divider(),
                      support, toga.Divider(),
                      tos, toga.Divider()],
            style=Pack(direction=COLUMN, padding=(20, 10, 10, 10), background_color="#ffffff")
        )
        
        main_box = toga.Box(
            children=[header_box, toga.Divider(), contents_box],
            style=Pack(direction=COLUMN, alignment="center", padding=10, background_color="#ffffff")
        )

        return main_box
    
    def placeholder_action(self, widget):  # Placeholder for action of the add job
        pass

    def open_notif_settings_view(self, widget):
        """
        Open the Notification Settings view in the same window.
        """
        notif_view = NotificationSettings(self.app)
        notif_content = notif_view.create_notif_settings_view()
        self.app.main_window.content = notif_content

    # Navigate back
    def navigate_back(self, widget):
        # Access the main app to switch back to the main view
        if hasattr(self.app, 'navigation_history') and hasattr(self.app, 'current_view'):
            if self.app.navigation_history:
                previous_view = self.app.navigation_history.pop()
                self.app.current_view = previous_view
                
                if previous_view == "account_view":
                    self.app.main_window.title = "Account View"
                    if hasattr(self.app, 'account_view'):
                        self.app.main_window.content = self.app.account_view.create_content() 