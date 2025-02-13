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
from toga.constants import COLUMN

'''1. In order to create a window that would be standalone, I had to create a temp application with it's
own main window in order to properly demonstrate the window I am working on. 
'''

class TempApp(toga.App):
    def startup(self):
        # Create a main window for the application
        self.main_window = toga.MainWindow(title=self.formal_name)
        # Start with owner_accepted_page
        self.direct_to_page()
        self.main_window.show()

    def direct_to_page(self):
        button = toga.Button("press", on_press=self.owner_accepted_page, style=Pack(padding=10))
        box = toga.Box(
            children=[button],
            style=Pack(direction=COLUMN, alignment="center", padding=10)
        )
        self.main_window.content = box

    def owner_accepted_page(self, widget):
        # Get the current directory and set up image path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(current_dir, "images")
        os.makedirs(images_dir, exist_ok=True)
        default_profile_path = os.path.join(images_dir, "defaultpfp.png")
        
        # Create image dictionary mapping IDs to profile pictures
        self.profile_images = {}
        try:
            default_image = toga.ImageView(default_profile_path)
            default_image.style.update(width=200, height=100, padding=7)
            # Map each ID to the default profile picture
            self.profile_images = {
                1: default_image,
                2: default_image,
                3: default_image
            }
        except Exception:
            self.profile_images = {}

        # Initialize data
        self.data = {
            "job 1 at pharmacy 3": {
                "ID": 1,
                "name": "Arthur Smith",
                "recommended": 0,
                "hourly rate": f"${25:.2f}/h",
                "date": None,
                "start time": None,
                "end time": None
            },
            "job 1 at pharmacy 2": {
                "ID": 2,
                "name": "Vincent Doom",
                "recommended": 190,
                "hourly rate": f"${75:.2f}/h",
                "date": None,
                "start time": None,
                "end time": None
            },
            "job 1 at pharmacy 1": {
                "ID": 3,
                "name": "Frank Castle",
                "recommended": 20,
                "hourly rate": f"${55:.2f}/h",
                "date": None,
                "start time": None,
                "end time": None
            }
        }

        # Create widgets
        widget_title = toga.Label("Locations", style=Pack(padding=10))
        
        self.emp_table = toga.Selection(
            items=list(self.data.keys()),
            on_select=self.job_listing_change,
            style=Pack(padding=5)
        )
        
        #AI generated code (Claude)
        self.result_set = toga.MultilineTextInput(
            readonly=True,
            style=Pack(padding=5, flex=1)
        )

        # Create content box without profile image initially
        self.content_box = toga.Box(
            children=[widget_title, self.emp_table, self.result_set],
            style=Pack(direction=COLUMN, alignment="left", padding=20)
        )
        
        # Create and show window
        window = toga.Window(title="Job Listings")
        window.content = self.content_box
        window.show()

    # AI generated code (Claude)
    def job_listing_change(self, widget, **kwargs):
        if widget.value:
            # Get job details
            job_details = self.data[widget.value]
            
            # Format and display the results
            result_text = f"Details for {widget.value}:\n\n"
            for key, value in job_details.items():
                result_text += f"{key}: {value}\n"
            
            self.result_set.value = result_text
            
            # Update profile picture (CLAUDE)
            staff_id = job_details["ID"]
            if staff_id in self.profile_images:
                # Remove old image if it exists
                for child in self.content_box.children:
                    if isinstance(child, toga.ImageView):
                        self.content_box.remove(child)
                
                # Add new image after the selection box but before results
                self.content_box.insert(2, self.profile_images[staff_id])

def main():
    return TempApp("Temp App", "org.example.bewareapp")

if __name__ == "__main__":
    app = main()
    app.main_loop()