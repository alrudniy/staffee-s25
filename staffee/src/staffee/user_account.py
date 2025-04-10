import os
import toga
from toga.style import Pack
from toga.constants import *
from settings import SettingsView

class UserAccount(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)

        # Initialize view modules
        self.settings_view = SettingsView(self)

        self.create_content()
        self.main_window.show()
    
    '''
    def _init__(self, app):
        self.app = app
    '''
    
    
    def create_content(self):
        # Header
        title_label = toga.Label('Account', style=Pack(font_size=20, font_weight='bold', padding=(20, 20, 10, 20),
                                                       background_color="#ffffff"))

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
            children=[title_label, profile_box, toga.Divider(), buttons_box],
            style=Pack(direction=COLUMN, alignment="center", padding=10, background_color="#ffffff")
        )

        self.main_window.content = main_box
    
    def placeholder_action(self, widget):  # Placeholder for action of the add job
        pass

    def open_settings_view(self, widget):
        """
        Open the Settings view in the same window.
        """
        settings_content = self.settings_view.create_settings_view()
        self.main_window.content = settings_content

def main():
    return UserAccount("UserAccount", "org.example.home")

if __name__ == "__main__":
    app = main()
    app.main_loop()
