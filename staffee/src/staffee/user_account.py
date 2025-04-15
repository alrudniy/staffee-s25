import os
import toga
from toga.style import Pack
from toga.constants import *
from staffee.settings import SettingsView

class UserAccount:
    def __init__(self, app):
        self.app = app
    
    
    def create_content(self):
        # Header
        title_label = toga.Label('Account', style=Pack(font_size=20, font_weight='bold', padding=(20, 20, 10, 20),
                                                       background_color="#ffffff"))
        
        back_button = self.app.icon_manager.create_back_button(self.navigate_back)

        header_box = toga.Box(style=Pack(direction=ROW, alignment=CENTER, padding=(0, 10), background_color="#ffffff"),
            children=[back_button, title_label])
        
        # Code for profile picture

        # Profile name and edit button
        profile_name = toga.Box(style=Pack(direction = COLUMN, padding=(5, 5, 5, 5), text_align="left",
                                           background_color="#ffffff", alignment=LEFT))
        profile_name.add(toga.Label('Profile Name', style=Pack(font_size=15, padding=(5, 5, 5, 5))))
        profile_name.add(toga.Label('Edit Staff Profile', style=Pack(font_size=12, padding=(5, 5, 5, 5), color=GREEN)))
        
        # Profile Box
        profile_box = toga.Box(style=Pack(direction=ROW, padding=(20, 20, 10, 20), alignment=LEFT), children=[profile_name])

        # Button select
        history_button = toga.Button("History", 
                                     on_press=self.placeholder_action,
                                     style=Pack(height=40, padding=5, background_color="#ffffff",
                                                color="#364052", font_size=10))
        
        invite_friends = toga.Button("Invite Friends",
                                     on_press=self.placeholder_action,
                                     style=Pack(height=40, padding=5, background_color="#ffffff",
                                                color="#364052", font_size=10))
        
        settings_button = toga.Button("Settings",
                                        on_press=self.open_settings_view,
                                        style=Pack(height=40, padding=5, background_color="#ffffff",
                                                    color="#364052", font_size=10))
        
        contact_us = toga.Button("Contact Us",
                                on_press=self.placeholder_action,
                                style=Pack(height=40, padding=5, background_color="#ffffff",
                                           color="#364052", font_size=10))
        
        logout_button = toga.Button("Logout",
                                    on_press=self.placeholder_action,
                                    style=Pack(height=40, padding=5, background_color="#ffffff",
                                               color="#364052", font_size=10))


        
        buttons_box = toga.Box(style=Pack(direction=COLUMN, padding=(20, 20, 10, 20), alignment=LEFT), children=[
            history_button, invite_friends, settings_button, contact_us, logout_button])

        # Main Box
        main_box = toga.Box(
            children=[header_box, profile_box, toga.Divider(), buttons_box],
            style=Pack(direction=COLUMN, alignment="center", padding=10, background_color="#ffffff")
        )

        return main_box
    
    def placeholder_action(self, widget):  # Placeholder for action of the add job
        pass

    def open_settings_view(self, widget):
        """
        Open the Settings view in the same window.
        """

        try:
            self.current_view = "settings_view"

            self.settings_view = SettingsView(self.app)

            settings_content = self.settings_view.create_settings_view()
            self.app.main_window.title = "Settings View"
            self.app.main_window.content = settings_content
        except Exception as e:
            print(f"Error in open_settings_view: {e}")
        
    # Navigate back
    def navigate_back(self, widget):
        # Access the main app to switch back to the main view
        if hasattr(self.app, 'navigation_history') and hasattr(self.app, 'current_view'):
            if self.app.navigation_history:
                previous_view = self.app.navigation_history.pop()
                self.app.current_view = previous_view
                
                if previous_view == "main":
                    self.app.main_window.title = self.app.formal_name
                    self.app.main_window.content = self.app.main_content
                elif previous_view == "staff_view":
                    self.app.main_window.title = "Staff View"
                    if hasattr(self.app, 'staff_view'):
                        self.app.main_window.content = self.app.staff_view.create_content() 

    
