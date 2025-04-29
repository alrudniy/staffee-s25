import os
import toga
from toga.style import Pack
from toga.constants import *

class EditStaffProfile:
    def __init__(self, app):
        self.app = app
    
    def create_content(self):
        # Header - title and back button
        title_label = toga.Label('Edit Staff Profile', style=Pack(font_size=20, font_weight='bold', padding=(20, 20, 10, 20),
                                                       background_color="#ffffff"))
        
        back_button = self.app.icon_manager.create_back_button(self.navigate_back)

        header_box = toga.Box(style=Pack(direction=ROW, alignment=CENTER, padding=(0, 10), background_color="#ffffff"),
            children=[back_button, title_label])
        
        # Entry content of page
        p1 = toga.Label("Job position", style=Pack(padding=(15, 5), font_weight='bold'))

        pos_select = toga.Selection(
            items=["Technician"],
            on_select=self.placeholder_action,
            style=Pack(padding=(15, 5), font_weight='bold')
        )

        pos_select.value = "Technician"

        p2 = toga.Label("QPR License (if applicable)", style=Pack(padding=(15, 5), font_weight='bold'))

        license_input = toga.TextInput(
            placeholder="License Number",
            on_change=self.placeholder_action,
            style=Pack(padding=(15, 5), font_weight='bold')
        )

        city_input = toga.TextInput(
            placeholder="City",
            on_change=self.placeholder_action,
            style=Pack(padding=(15, 5), font_weight='bold')
        )

        year_input = toga.TextInput(
            placeholder="Year",     # not sure if meant to be year of issue or year of expiry
            on_change=self.placeholder_action,
            style=Pack(padding=(15, 5), font_weight='bold')
        )

        p2_text_input = toga.Box(
            children=[license_input, city_input, year_input],
            style=Pack(direction=ROW, padding=(15, 5), font_weight='bold')
        )

        p3 = toga.Label("Softwares", style=Pack(padding=(15, 5), font_weight='bold'))

        software_input = toga.TextInput(
            placeholder="",
            on_change=self.placeholder_action,
            style=Pack(padding=(15, 5), font_weight='bold')
        )

        p4 = toga.Label("Details", style=Pack(padding=(15, 5), font_weight='bold'))

        details_input = toga.MultilineTextInput(
            placeholder="",
            on_change=self.placeholder_action,
            style=Pack(padding=(15, 5), font_weight='bold')
        )

        entry_box = toga.Box(
            children=[p1, pos_select, p2, p2_text_input, p3, software_input, p4, details_input],
            style=Pack(direction=COLUMN, padding=(15, 5), font_weight='bold')
        )

        # Save button
        save_button = toga.Button(
            "Save",
            on_press=self.placeholder_action,
            style=Pack(padding=5, width=100, background_color ='#228b22', color = '#FFFFFF')
        )

        main_box = toga.Box(
            children=[header_box, entry_box, save_button],
            style=Pack(direction=COLUMN, alignment="center", padding=10, background_color="#ffffff")
        )
        return main_box
    
    def placeholder_action(self, widget):  # Placeholder for action of the add job
        pass

    # Navigate back
    def navigate_back(self, widget):
        # Access the main app to switch back to the main view
        if hasattr(self.app, 'navigation_history') and hasattr(self.app, 'current_view'):
            if self.app.navigation_history:
                previous_view = self.app.navigation_history.pop()
                self.app.current_view = previous_view
                
                if previous_view == "account_view":
                    self.app.main_window.title = "Account View"
                    if hasattr(self.app, 'user_account'):
                        user_account = self.app.user_account
                        self.app.main_window.content = user_account.create_content()