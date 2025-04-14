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
import mysql.connector
from toga.style import Pack
from toga.constants import *
from staffee.profile_view import ProfileView
from staffee.resizeimg import resize_profile_pictures

# ensuring that the class is exportable (CLAUDE)
__all__ = ['OwnerViewStaff']

class OwnerViewStaff:
    def __init__(self, app, DB_details):
        # Store the app instance
        self.app = app
        self.DB_details = DB_details

        # Connect to the database
        self.db_conn = mysql.connector.connect(**DB_details)
        
        # Fetch staff data from the database
        self.fetch_staff_data()

    def fetch_staff_data(self):
        """Fetch staff data from the database"""
        try:
            # Create a cursor
            cursor = self.db_conn.cursor(dictionary=True)
            
            # SQL query to fetch required columns
            query = """
            SELECT first_name, last_name, UID, desired_hourly_rate, recommendations 
            FROM applicant_info
            WHERE job_listings = True  # Assuming there's an active column to filter active staff
            """
            
            # Execute the query
            cursor.execute(query)
            
            # Fetch all results
            staff_results = cursor.fetchall()
            
            # Convert results to a dictionary for existing code compatibility
            self.data = {}
            self.profile_images = {}
            
            for staff in staff_results:
                # Create a unique key for each staff member
                job_key = f"{staff['first_name']} {staff['last_name']}"
                
                # Store staff data
                self.data[job_key] = {
                    'name': job_key,
                    'ID': staff['UID'],
                    'first_name': staff['first_name'],
                    'last_name': staff['last_name'],
                    'hourly_rate': staff['desired_hourly_rate'],
                    'recommendations': staff['recommendations']
                }
                
                # Fetch and store profile image if available
                profile_pic = self.fetch_profile_image(staff['UID'])
                if profile_pic:
                    self.profile_images[staff['UID']] = profile_pic
            
            # Close the cursor
            cursor.close()
        
        except mysql.connector.Error as err:
            print(f"Error fetching staff data: {err}")
            self.data = {}
            self.profile_images = {}

    def fetch_profile_image(self, staff_id):
        """Fetch profile image for a given staff ID"""
        try:
            cursor = self.db_conn.cursor()
            query = "SELECT profile_image FROM staff WHERE UID = %s"
            cursor.execute(query, (staff_id,))
            result = cursor.fetchone()
            cursor.close()
            
            return result[0] if result and result[0] else None
        
        except mysql.connector.Error as err:
            print(f"Error fetching profile image: {err}")
            return None

    def generate_job_buttons(self):
        """Generate individual job buttons for scrollable content"""
        # Sort job keys for better organization
        sorted_keys = sorted(self.data.keys())
        
        # Add job buttons to the scrollable content
        for job_key in sorted_keys:
            job_data = self.data[job_key]
            
            # Format button text to show key information
            button_text = (
                f"{job_data['first_name']} {job_data['last_name']} | "
                f"ID: {job_data['ID']} | "
                f"Rate: ${job_data['hourly_rate']}/hr | "
                f"Recommendations: {job_data['recommendations']}"
            )
            
            job_button = toga.Button(
                button_text,
                on_press=lambda widget, key=job_key: self.select_job(key),
                style=Pack(
                padding=(3, 6, 3, 6),  # top, right, bottom, left padding
                width=400,  # Increased width to accommodate more text
                height=60,  # Slightly increased height
                alignment='left',
                background_color='#f0f0f0'
            )
            )
            
            self.scrollable_content.add(job_button)

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
        nav_box = self.app.icon_manager.create_nav_bar()

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