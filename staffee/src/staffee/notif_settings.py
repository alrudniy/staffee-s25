import os
import toga 
from toga.style import Pack
from toga.constants import *

class NotificationSettings:
    def __init__(self, app):
        # Store the app instance
        self.app = app
    
    def create_notif_settings_view(self):
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
            "Notification Settings", style=Pack(padding=(15, 5), font_size=15, 
            font_family = 'sans-serif', flex=8))
            
        # Header box 
        header_box = toga.Box(
            children=[back_button, title_label],
            style=Pack(direction=ROW, alignment="center"))
            
            
        # Description paragraphs
        par1 = toga.Label("Choose what notifications you want to receive"
        "below and we will update the settings.", style=Pack(padding=(15, 5), font_size=5))

        sub1 = toga.Label("Push Notifications", style=Pack(padding=(15, 5), font_size=15, font_weight="bold"))

        par2 = toga.Label("Send me push notifications for contracts on these days only")

        notifSwitches = toga.Box(
            children=[toga.Switch("All", id=1, on_change=self.push_notification, value=False),
                        toga.Switch("Monday", id=2, on_change=self.placeholder_action, value=False),
                        toga.Switch("Tuesday", id=3, on_change=self.placeholder_action, value=False),
                        toga.Switch("Wednesday", id=4, on_change=self.placeholder_action, value=False),
                        toga.Switch("Thursday", id=5, on_change=self.placeholder_action, value=False),
                        toga.Switch("Friday", id=6, on_change=self.placeholder_action, value=False),
                        toga.Switch("Saturday", id=7, on_change=self.placeholder_action, value=False),
                        toga.Switch("Sunday", id=8, on_change=self.placeholder_action, value=False)],
            style=Pack(direction=COLUMN)
        )

        sub2 = toga.Label("Software", style=Pack(padding=(15, 5), font_size=15, font_weight="bold"))

        softwareSwitch = toga.Switch("Notify me for new contracts only if I know their software", on_change=self.placeholder_action, value=False)

        sub3 = toga.Label("Chat Notification", style=Pack(padding=(15, 5), font_size=15, font_weight="bold"))

        chatSwitch = toga.Switch("Notify me when I receive a new message in the chat", on_change=self.placeholder_action, value=False)

        sub4 = toga.Label("SMS Notification", style=Pack(padding=(15, 5), font_size=15, font_weight="bold"))

        smsSwitch = toga.Switch("Receive SMS notifications", on_change=self.placeholder_action, value=False)

        sub5 = toga.Label("Call Notification", style=Pack(padding=(15, 5), font_size=15, font_weight="bold"))

        callSwitch = toga.Switch("Receive call notifications", on_change=self.placeholder_action, value=False)

        sub6 = toga.Label("Distance", style=Pack(padding=(15, 5), font_size=15, font_weight="bold"))

        par6 = toga.Label("Notify me for new contracts based on the maximal distance I am willing to travel",
                            style=Pack(padding=(15, 5), font_size=5))

        distanceInput = toga.NumberInput("km", min=0, step=5, value=0, style=Pack(padding=(15, 5)))

        sub7 = toga.Button("Two-Factor Authentification", on_press=self.placeholder_action, style=Pack(padding=(15, 5), font_size=15, font_weight="bold"))

        # Scroll box
        scroll_box = toga.ScrollContainer(
            content=toga.Box(
                children=[par1, sub1,
                            par2, notifSwitches,
                            sub2, softwareSwitch,
                            sub3, chatSwitch,
                            sub4, smsSwitch,
                            sub5, callSwitch,
                            sub6, par6, distanceInput,
                            sub7],
                style=Pack(direction=COLUMN, padding=10, height=500, width=300)
            )
        )

        main_box = toga.Box(
            children=[header_box, scroll_box],
            style=Pack(direction=COLUMN))
            
        return main_box
        
    def placeholder_action(self, widget):  # Placeholder for action of the add job
        pass
        
        
    def push_notification(self, widget):
        toggle_value = widget.value

        switches_box = self.app.main_window.content.children[1].content.children[3]
        for child in switches_box.children:
            if child.id != "1":
                child.value = toggle_value
                child.enabled = not toggle_value
