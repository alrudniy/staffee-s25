'''
This program holds the view that will be used to display the activate staff members 
with a description that will include:
1. hourly rate 
2. date and time slot they are scheduled
3. counter tracking the # of number of clients 'recommending' individual 
4. 'fulfilled' button : allows owner to indicate completion and recommend (optional)
5. 'cancel' button : allows owner to terminate current employee for any reason (i.e. improper conduct)
. Will include a confirmation pop up to confirm this action.

'''
import os
import toga
from toga.style import Pack
from toga.constants import *
from staffee.profile_view import ProfileView
from staffee.resizeimg import resize_profile_pictures

# ensuring that the class is exportable (CLAUDE)
__all__ = ['OwnerViewStaff']

class OwnerViewStaff:
    def __init__(self, app):
        # Store the app instance
        self.app = app

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
            },
            "job 43 at pharmacy ABC": {
                "ID": 6, "name": "John Doe", "recommended": 9,
                "hourly rate": f"${15:.2f}/h", "date": None,
                "start time": None, "end time": None
            }
        }

        # Create image dictionary mapping IDs to profile pictures
        self.profile_images = {}
        try:
            # Try to use the app's default profile image if available
            profile_pics_dir = self.app.paths.app / "resources" / "profile_pics"

            # Resize profile pictures during initialization
            resize_profile_pictures(profile_pics_dir)

            default_profile_path = os.path.join(profile_pics_dir, "defaultpfp.png")

            default_image = toga.ImageView(default_profile_path)
            
            default_image.style.update(width=35, height=35, padding=5)
            # Map each ID to the default profile picture
            self.profile_images = {1: default_image, 2: default_image, 3: default_image, 4: default_image, 6: default_image}
        except Exception as e:
            print(f"Error loading profile images: {e}")
            self.profile_images = {}

    def create_content(self):
        # Get back button from icon manager
        back_button = self.app.icon_manager.create_back_button(self.navigate_back)
        
        # Header
        title_label = toga.Label('Active Staff View', style=Pack(font_size=18, font_weight='bold', padding=(20, 20, 10, 20)))
        
        # Add back button to the header
        header_box = toga.Box(
            children=[back_button, title_label],
            style=Pack(direction=ROW, alignment='center', padding=(0, 10))
        )

        # Get action box (new job and calendar) from icon manager
        action_box = self.app.icon_manager.create_action_box(self.placeholder_action)

        # Post label
        post_label = toga.Label('Active staff', style=Pack(padding=(10, 20)))
        
        # Add a prompt label
        self.prompt_label = toga.Label(
            'Select a job to view details',
            style=Pack(padding=10, text_align='center')
        )

        # Create a box for the scrollable content
        self.scrollable_content = toga.Box(
            style=Pack(direction=COLUMN, padding=10)
        )
        
        # Generate job buttons for scrollable content
        self.generate_job_buttons()
        
        # Create the scroll container with proper styling
        job_scroll_container = toga.ScrollContainer(
            content=self.scrollable_content,
            style=Pack(flex=1, padding=5, height=300),  # Added height constraint
            horizontal=False,  # Disable horizontal scrolling
            vertical=True      # Enable vertical scrolling
        )

        # Use the icon manager to create the navigation bar
        nav_box = self.app.icon_manager.create_nav_bar(self.placeholder_action)

        # Create a container for dynamic content
        self.dynamic_content = toga.Box(
            children=[self.prompt_label],
            style=Pack(direction=COLUMN, padding=4)
        )

        # Main container with updated layout
        content_box = toga.Box(
            children=[
                header_box,
                action_box,
                toga.Box(children=[post_label], style=Pack(direction=ROW)),
                job_scroll_container,  # Using the scroll container here
                self.dynamic_content,
                toga.Box(style=Pack(flex=1)),  # Spacer
                nav_box
            ],
            style=Pack(direction=COLUMN)
        )
        
        return content_box

    def navigate_back(self, widget):
        """Navigate back to the main view"""
        # Access the main app to switch back to the main view
        self.app.main_window.title = self.app.formal_name
        self.app.main_window.content = self.app.main_content
        
        # If the app has navigation history, update it
        if hasattr(self.app, 'navigation_history') and hasattr(self.app, 'current_view'):
            if self.app.navigation_history:
                self.app.navigation_history.pop()  # Remove current view from history
            
            self.app.current_view = "main"  # Set current view back to main

    def generate_job_buttons(self):
        """Generate individual job buttons for scrollable content"""
        # Sort job keys for better organization
        sorted_keys = sorted(self.data.keys())
        
        # Add job buttons to the scrollable content
        for job_key in sorted_keys:
            job_data = self.data[job_key]
            
            job_button = toga.Button(
                f"{job_key} - {job_data['name']}",
                on_press=lambda widget, key=job_key: self.select_job(key),
                style=Pack(
                padding=(3, 6, 3, 6),  # top, right, bottom, left padding
                width=200,
                height=50,
                alignment='left',
                background_color='#f0f0f0'
            )
            )
            
            self.scrollable_content.add(job_button)

    def select_job(self, job_key):
        """Handler for clicking a job button"""
        if job_key in self.data:
            # Store the current selection
            self.current_selection = job_key
            
            # Get job details
            job_details = self.data[job_key]
            
            # Get the profile picture for this staff
            staff_id = job_details["ID"]
            profile_pic = self.profile_images.get(staff_id, None)
            
            # Open the profile view for this job
            self.open_profile_view(job_key, job_details, profile_pic)

    def open_profile_view(self, job_key, job_details, profile_pic):
        """Open the profile view for the selected job"""
        # Save current view to history for back navigation
        self.app.navigation_history.append(self.app.current_view)
        self.app.current_view = "profile_view"
    
        # Update the main window title
        self.app.main_window.title = f"Profile: {job_details['name']}"
    
        # Update main window content with profile view, passing job_key
        profile_view = ProfileView(self.app) 
        profile_content = profile_view.create_content(job_details, profile_pic, job_key)
        self.app.main_window.content = profile_content

    def clear_job_display(self):
        """Clear all job-related display elements"""
        # Remove all children from dynamic content
        self.dynamic_content.remove(*self.dynamic_content.children)
        
        # Add back the prompt label
        self.dynamic_content.add(self.prompt_label)
        
        # Clear current selection
        self.current_selection = None
    
    def remove_selected_job(self):
        """Remove the selected job from the data and refresh the display."""
        if self.current_selection and self.current_selection in self.data:
            # Remove the job from the data dictionary
            del self.data[self.current_selection]
        
            # Clear the dynamic content
            self.dynamic_content.remove(*self.dynamic_content.children)
            self.dynamic_content.add(self.prompt_label)
        
            # Refresh the job buttons
            self.refresh_job_buttons()
        
            # Reset current selection
            self.current_selection = None

    def refresh_job_buttons(self):
        """Refresh job buttons after job removal"""
        # Remove all existing children except the dropdown
        self.scrollable_content.remove(*self.scrollable_content.children)
        
        # Regenerate job buttons
        self.generate_job_buttons()
    
    def placeholder_action(self, widget):
        """Placeholder for button actions"""
        pass