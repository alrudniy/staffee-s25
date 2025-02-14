''''
This program holds the window that will be used to display the activate staff members 
via a drop down menu with a description that will include:
1. hourly rate 
2. date and time slot they are scheduled
3. number of clients 'recommending' individual 
4. 'fulfilled' button : allows owner to indicate completion and recommend (optional)
5. 'cancel' button : allows owner to terminate current employee for any reason (i.e. improper conduct)
. Will include a confirmation pop up to confirm this action.
'''

import os
import toga 
from toga.style import Pack
from toga.constants import *

'''1. In order to create a window that would be standalone, I had to create a temp application with it's
own main window in order to properly demonstrate the window I am working on. 
'''

class TempApp(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.create_owner_view_staff()
        self.main_window.show()

    def create_owner_view_staff(self):
        def action_fulfill_button(fulfill_button):
            toga.ConfirmDialog()
            pass
        def action_cancel_button(cancel_button):
            # event 
            pass
         
        # creating the 'fulfill' and 'cancel' buttons
        fulfill_button = toga.Button("fulfill",on_press=action_fulfill_button)
        cancel_button = toga.Button("cancel",on_press=action_cancel_button)

        # Get the current directory and set up image path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(current_dir, "images")
        os.makedirs(images_dir, exist_ok=True)
        default_profile_path = os.path.join(images_dir, "defaultpfp.png")
        
        # Create paths for the icons with error handling
        try:
            cal_icon = toga.Icon(os.path.join(images_dir, "calendar.png"))
            chat_icon = toga.Icon(os.path.join(images_dir, "chat.png"))
            home_icon = toga.Icon(os.path.join(images_dir, "home.png"))
            noti_icon = toga.Icon(os.path.join(images_dir, "notification.png"))
            user_icon = toga.Icon(os.path.join(images_dir, "user.png"))
        except Exception as e:
            print(f"Error loading icons: {e}")
            cal_icon = chat_icon = home_icon = noti_icon = user_icon = None
        
        # Create image dictionary mapping IDs to profile pictures
        self.profile_images = {}
        try:
            default_image = toga.ImageView(default_profile_path)
            default_image.style.update(width=200, height=100, padding=7)
            # Map each ID to the default profile picture
            self.profile_images = {1: default_image, 2: default_image, 3: default_image}
        except Exception:
            self.profile_images = {}

        # Initialize data
        self.data = {
            "job 1 at pharmacy 1": {
                "ID": 1, "name": "Arthur Smith", "recommended": 0,
                "hourly rate": f"${25:.2f}/h", "date": None,
                "start time": None, "end time": None
            },
            "job 1 at pharmacy 2": {
                "ID": 2, "name": "Vincent Doom", "recommended": 5.4,
                "hourly rate": f"${75:.2f}/h", "date": None,
                "start time": None, "end time": None
            },
            "job 1 at pharmacy 3": {
                "ID": 3, "name": "Frank Castle", "recommended": 4,
                "hourly rate": f"${55:.2f}/h", "date": None,
                "start time": None, "end time": None
            }
        }

        # Create dedicated container for profile pictures
        self.profile_container = toga.Box(
            style=Pack(direction=COLUMN, alignment='center', padding=5)
        )

        # Create result set for job details
        self.result_set = toga.MultilineTextInput(
            readonly=True,
            style=Pack(padding=5, flex=1, height=200)
        )

        # Header
        title_label = toga.Label('Home', style=Pack(font_size=24, font_weight='bold', padding=(20, 20, 10, 20)))
        
        new_job_button = toga.Button(
            '+ New job',
            on_press=self.placeholder_action,
            style=Pack(
                padding=(20, 5),
                width=100,
                height=30,
                background_color='#FFFFFF',  # White text'
                color='#228b22', # Forest green
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

        # Post label
        post_label = toga.Label('Active staff', style=Pack(padding=(10, 20)))
        
        # Create dropdown menu for jobs
        job_selection = toga.Selection(
            items=list(self.data.keys()),
            on_select=self.job_selection_change,
            style=Pack(padding=(15, 20), width=300)
        )
        
        # Create container for the dropdown
        job_container = toga.Box(
            children=[job_selection],
            style=Pack(direction=COLUMN, padding=10, alignment='center')
        )

        # Navigation bar with vertically aligned icons and labels
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
                    padding=(5, 0, 0, 0),  # Add padding above the label
                    text_align='center'
                )
            )

            nav_item = toga.Box(
                children=[nav_button, label_widget],
                style=Pack(
                    direction=COLUMN,
                    alignment='center',
                    flex=1,
                    padding=(5, 10)  # Reduced vertical padding
                )
            )
            nav_box.add(nav_item)

        # Main container with updated layout
        self.content_box = toga.Box(
            children=[
                header_box,
                toga.Box(children=[post_label], style=Pack(direction=ROW)),
                job_container,  # Changed from job_list to job_container
                self.profile_container,
                self.result_set,
                toga.Box(style=Pack(flex=1)),  # Spacer
                nav_box
            ],
            style=Pack(direction=COLUMN)
        )
        
        self.main_window.content = self.content_box

    def job_selection_change(self, widget):
        """Handle job selection from dropdown menu"""
        job_key = widget.value
        if job_key in self.data:
            job_details = self.data[job_key]
            
            # Format and display the results
            result_text = f"Details for {job_key}:\n\n"
            for key, value in job_details.items():
                result_text += f"{key}: {value}\n"
            
            self.result_set.value = result_text
            
            # Update profile picture in the dedicated container
            staff_id = job_details["ID"]
            if staff_id in self.profile_images:
                # Clear the profile container
                for child in self.profile_container.children:
                    self.profile_container.remove(child)
                
                # Add the new profile picture
                self.profile_container.add(self.profile_images[staff_id])

    def placeholder_action(self, widget):
        # Placeholder for button actions
        pass

def main():
    return TempApp("Home", "org.example.home")

if __name__ == "__main__":
    app = main()
    app.main_loop()