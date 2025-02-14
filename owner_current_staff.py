'''
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
        async def action_fulfill_button(widget):
            """Handle fulfillment confirmation and remove job if confirmed."""
            if self.current_selection:
                confirm_question = await self.main_window.dialog(toga.ConfirmDialog(
                    "Confirm fulfillment",
                    "Has this job been completed?"
                ))
                if confirm_question:
                    self.remove_selected_job()

        async def action_cancel_button(widget):
            """Handle termination confirmation and remove job if confirmed."""
            if self.current_selection:
                confirm_question = await self.main_window.dialog(toga.ConfirmDialog(
                    "Confirm termination",
                    "Terminate this employee?"
                ))
                if confirm_question:
                    self.remove_selected_job()

        # Create buttons
        self.fulfill_button = toga.Button(
            "fulfill",
            on_press=action_fulfill_button,
            style=Pack(padding=5, width=100, background_color ='#228b22', color = '#FFFFFF')
        )
        self.cancel_button = toga.Button(
            "cancel",
            on_press=action_cancel_button,
            style=Pack(padding=5, width=100)
        )

        # Create button container
        self.button_container = toga.Box(
            children=[self.fulfill_button, self.cancel_button],
            style=Pack(direction=ROW, padding=5, alignment='center')
        )
        
        self.current_selection = None

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

        # Create content container that will hold both profile and buttons
        self.content_container = toga.Box(
            children=[self.profile_container, self.result_set, self.button_container],
            style=Pack(direction=COLUMN, padding=5)
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

        # Post label
        post_label = toga.Label('Active staff', style=Pack(padding=(10, 20)))
        
        # Add a prompt label
        self.prompt_label = toga.Label(
            'Select a job to view details',
            style=Pack(padding=20, text_align='center')
        )
        
        # Create dropdown menu for jobs
        self.job_selection = toga.Selection(
            items=['Select a job...'] + list(self.data.keys()),
            on_select=self.job_selection_change,
            style=Pack(padding=(15, 20), width=300)
        )
        
        # Create container for the dropdown
        job_container = toga.Box(
            children=[self.job_selection],
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

        # Create a container for dynamic content
        self.dynamic_content = toga.Box(
            children=[self.prompt_label],
            style=Pack(direction=COLUMN, padding=5)
        )

        # Main container with updated layout
        self.content_box = toga.Box(
            children=[
                header_box,
                toga.Box(children=[post_label], style=Pack(direction=ROW)),
                job_container,
                self.dynamic_content,
                toga.Box(style=Pack(flex=1)),  # Spacer
                nav_box
            ],
            style=Pack(direction=COLUMN)
        )
        
        self.main_window.content = self.content_box
    
    def clear_job_display(self):
        """Clear all job-related display elements"""
        # Remove all children from dynamic content
        self.dynamic_content.remove(*self.dynamic_content.children)
        
        # Add back the prompt label
        self.dynamic_content.add(self.prompt_label)
        
        # Clear current selection
        self.current_selection = None

    def job_selection_change(self, widget):
        """Handle job selection from dropdown menu"""
        job_key = widget.value
        
        # Clear the dynamic content
        self.dynamic_content.remove(*self.dynamic_content.children)
        
        if job_key and job_key != 'Select a job...' and job_key in self.data:
            self.current_selection = job_key
            job_details = self.data[job_key]
            
            # Create a new MultilineTextInput for this selection
            result_text = f"Details for {job_key}:\n\n"
            for key, value in job_details.items():
                result_text += f"{key}: {value}\n"
            
            result_display = toga.MultilineTextInput(
                readonly=True,
                value=result_text,
                style=Pack(padding=5, flex=1, height=200)
            )
            
            # Get the profile picture
            staff_id = job_details["ID"]
            if staff_id in self.profile_images:
                profile_pic = self.profile_images[staff_id]
            else:
                profile_pic = None
            
            # Create a new container for this selection's content
            selection_content = toga.Box(
                style=Pack(direction=COLUMN, padding=5)
            )
            
            if profile_pic:
                selection_content.add(profile_pic)
            
            selection_content.add(result_display)
            selection_content.add(self.button_container)
            
            # Add the selection content to dynamic content
            self.dynamic_content.add(selection_content)
        else:
            # Show the prompt if no valid selection
            self.dynamic_content.add(self.prompt_label)
            self.current_selection = None
    
    def remove_selected_job(self):
        """Remove the selected job from the dropdown and data dictionary."""
        if self.current_selection and self.current_selection in self.data:
            # Remove the job from the data dictionary
            del self.data[self.current_selection]
            
            # Update the dropdown items
            self.job_selection.items = ['Select a job...'] + list(self.data.keys())
            
            # Clear the display
            self.clear_job_display()

    def placeholder_action(self, widget):
        # Placeholder for action of the add job
        pass

def main():
    return TempApp("TempApp", "org.example.home")

if __name__ == "__main__":
    app = main()
    app.main_loop()