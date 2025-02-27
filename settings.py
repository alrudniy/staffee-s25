import os
import toga 
from toga.style import Pack
from toga.constants import *

'''1. In order to create a window that would be standalone, I had to create a temp application with it's
own main window in order to properly demonstrate the window I am working on. 
'''

class SettingsApp(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.create_settings_view()
        self.main_window.show()


    def create_settings_view(self):
        # Get the current directory and set up image path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(current_dir, "images")
        os.makedirs(images_dir, exist_ok=True)

        # Create paths for icons with error handling
        try:
            back_icon_path = os.path.join(images_dir, "back_arrow.png")

            back_icon = toga.Icon(back_icon_path)
        except Exception as e:
            print(f"Error loading icons: {e}")
            back_icon = None

        # Back arrow button 
        back_button = toga.Button(
            icon=back_icon,
            on_press=self.placeholder_action,
            style=Pack(padding=(20, 5), width=30, height=30, flex=1)
        )

        # Chat label
        title_label = toga.Label(
            "Settings", style=Pack(padding=(15, 5), font_size=15, 
            font_family = 'sans-serif', flex=8))
        
        # Header box 
        header_box = toga.Box(
            children=[back_button, title_label],
            style=Pack(direction=ROW, alignment="center"))
        
        main_box = toga.Box(
            children=[header_box],
            style=Pack(direction=COLUMN, alignment="center", padding=10)
        )

        self.main_window.content = main_box
    
    def placeholder_action(self, widget):
        # Placeholder for action of the add job
            pass