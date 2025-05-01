import os
import toga
from toga.style import Pack
from toga.constants import *
from staffee.settings import SettingsView
from staffee.edit_staff_profile import EditStaffProfile

class BusinessProfile:
    def __init__(self, app):
        self.app = app
        self.resource_path = os.path.join(os.path.dirname(__file__), 'resources')
        self.settings_view = SettingsView(self.app)
        self.edit_staff_profile = EditStaffProfile(self.app)
    
    def create_content(self):
        # Header
        title_label = toga.Label('Account', style=Pack(font_size=20, font_weight='bold', padding=(20, 20, 10, 20),
                                                       background_color="#ffffff"))
        
        back_button = self.app.icon_manager.create_back_button(self.navigate_back)

        header_box = toga.Box(style=Pack(direction=ROW, alignment=CENTER, padding=(0, 10), background_color="#ffffff"),
            children=[back_button, title_label])
        
        # Code for profile picture
        # Profile Box
        profile_box = toga.Box(style=Pack(direction=ROW, padding=(20, 20, 10, 20), alignment=LEFT))

        company_name = toga.Label("Comp Name 1", style=Pack(padding=10))
        tel_label = toga.Label("123-456-7890")
        Location_label = toga.Label("36 Madison Ave")

        profile_box.add(company_name)
        profile_box.add(tel_label)
        profile_box.add(Location_label)

               
        # Use the icon manager to create the navigation bar
        nav_box = self.app.icon_manager.create_nav_bar()

        # Main Box
        main_box = toga.Box(
            children=[header_box, profile_box, toga.Divider(), nav_box],
            style=Pack(direction=COLUMN, alignment="center", padding=10, background_color="#ffffff")
        )

        return main_box
    
    def placeholder_action(self, widget):  # Placeholder for action of the add job
        pass

    def open_edit_staff_view(self, widget):
        """
        Open the Edit Staff view in the same window.
        """

        try:
            self.app.navigation_history.append(self.app.current_view)
            self.app.current_view = "edit_staff_profile_view"

            staff_view_content = self.edit_staff_profile.create_content()
            self.app.main_window.title = "Edit Staff View"
            self.app.main_window.content = staff_view_content
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
                    if hasattr(self.app, "staff_view"):
                        self.app.main_window.content = self.app.staff_view.create_content() 