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
            style=Pack(padding=5, width=30, height=30, flex=2)
        )

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
            on_press=self.create_notif_settings_view,
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

        self.main_window.content = main_box

    def create_notif_settings_view(self, widget):
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
            on_press=self.create_settings_view,
            style=Pack(padding=(20, 5), width=30, height=30, flex=1)
        )

        # Chat label
        title_label = toga.Label(
            "Notification Settings", style=Pack(padding=(15, 5), font_size=15, 
            font_family = 'sans-serif', flex=8))
        
        # Header box 
        header_box = toga.Box(
            children=[back_button, title_label],
            style=Pack(direction=ROW, alignment="center"))
        
        
        # Description paragraphs
        par1 = toga.Label("Choose what notifications you want to receive"
        "below and we will update the settings.", style=Pack(padding=(15, 5), font_size=5))

        sub1 = toga.Label("Push Notifications", style=Pack(padding=(15, 5), font_size=15))

        par2 = toga.Label("Send me push notifications for contracts on these days only")

        switches = toga.Box(
            children=[toga.Switch("All", id=0, on_change=self.push_notification, value=False),
                      toga.Switch("Monday", id=1, on_change=self.placeholder_action, value=False),
                      toga.Switch("Tuesday", id=2, on_change=self.placeholder_action, value=False),
                      toga.Switch("Wednesday", id=3, on_change=self.placeholder_action, value=False),
                      toga.Switch("Thursday", id=4, on_change=self.placeholder_action, value=False),
                      toga.Switch("Friday", id=5, on_change=self.placeholder_action, value=False),
                      toga.Switch("Saturday", id=6, on_change=self.placeholder_action, value=False),
                      toga.Switch("Sunday", id=7, on_change=self.placeholder_action, value=False)],
            style=Pack(direction=COLUMN)
        )

        # Scroll box
        scroll_box = toga.ScrollContainer(
            content=toga.Box(
                children=[par1, sub1,
                          par2, switches],
                style=Pack(direction=COLUMN, padding=10)
            )
        )

        main_box = toga.Box(
            children=[header_box, scroll_box],
            style=Pack(direction=COLUMN))
        
        self.main_window.content = main_box
    
    def placeholder_action(self, widget):  # Placeholder for action of the add job
        pass
    
    
    def push_notification(self, widget, value):
        if value==True:
            for i in range(1, 8):
                widget = self.main_window.content.children[1].children[3].children[i]
                widget.value = True
                widget.enabled = False
        else:
            for i in range(1, 8):
                widget = self.main_window.content.children[1].children[3].children[i]
                widget.value = False
                widget.enabled = True




def main():
    return SettingsApp("SettingsApp", "org.example.home")

if __name__ == "__main__":
    app = main()
    app.main_loop()