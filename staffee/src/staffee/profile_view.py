'''
This module contains the ProfileView class for displaying staff member details.
It works with the main application window, similar to the OwnerViewStaff class.
'''

import toga
from toga.style import Pack
from toga.constants import *

__all__ = ['ProfileView']

class ProfileView:
    def __init__(self, app):
        # Initialize the ProfileView.
        self.app = app
        
    def create_content(self, staff_data, profile_pic=None, job_key=None):
        """
        Create the content for the profile view.
    
        Args:
            staff_data: Dictionary containing staff member details
            profile_pic: Optional ImageView with the staff member's photo
            job_key: The key identifying this job in the data dictionary
        """
        # Store references to data for use in button handlers
        self.staff_data = staff_data
        self.job_key = job_key

        async def action_fulfill_button(widget):
            """Handle fulfillment confirmation and job completion."""
            confirm_question = await self.app.main_window.dialog(toga.ConfirmDialog(
                "Confirm fulfillment",
                "Has this job been completed?",
            ))

            if confirm_question:
                # Ask if they want to recommend the staff member
                recommend_question = await self.app.main_window.dialog(toga.QuestionDialog(
                "Recommend staff",
                "Do you recommend this applicant?",
                ))
            
                if recommend_question and hasattr(self.app, 'staff_view'):
                    # Update the recommendation count in the original data
                    staff_id = staff_data["ID"]
                    if job_key in self.app.staff_view.data:
                        self.app.staff_view.data[job_key]["recommended"] += 1
            
                # Remove the job from the original data
                self.complete_job()

        async def action_cancel_button(widget):
            """Handle termination confirmation and job removal."""
            confirm_question = await self.app.main_window.dialog(toga.ConfirmDialog(
                "Confirm termination",
                "Terminate this employee?",
            ))
        
            if confirm_question:
                self.complete_job()


        back_button = toga.Button(
            '← Back',
            on_press=self.navigate_back,
            style=Pack(
                padding=0,
                width=80,
                height=40,
                background_color='#228b22',
                color='#FFFFFF',
                font_size = 7,
                text_align = "center"
            )
        )
        
        # Title with staff name
        title_label = toga.Label(
            f"Profile: {staff_data.get('name', 'Staff Member')}",
            style=Pack(font_size=18, font_weight='bold', padding=(20, 20, 10, 20))
        )
        
        # Header with back button and title
        header_box = toga.Box(
            children=[back_button, title_label],
            style=Pack(direction=ROW, alignment='center', padding=(0, 10))
        )
        
        # Create profile picture container
        profile_container = toga.Box(
            style=Pack(direction=COLUMN, alignment='center', padding=10)
        )
        
        if profile_pic:
            profile_container.add(profile_pic)
        
        # Create text display with staff details
        details_text = self.format_staff_details(staff_data)
        details_display = toga.MultilineTextInput(
            readonly=True,
            value=details_text,
            style=Pack(padding=10, flex=1, height=200)
        )
        
        # Create 'fulfill' and 'cancel' buttons 
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
        button_container = toga.Box(
            children=[self.fulfill_button, self.cancel_button],
            style=Pack(direction=ROW, padding=5, alignment='center')
        )
        
        # Main container with the complete profile view
        main_box = toga.Box(
            children=[
                header_box,
                profile_container,
                details_display,
                button_container,
                toga.Box(style=Pack(flex=1)),  # Spacer
                # We could add navigation here if needed using:
                # self.app.icon_manager.create_nav_bar(self.placeholder_action)
            ],
            style=Pack(direction=COLUMN, padding=10)
        )
        
        return main_box
        
    def format_staff_details(self, staff_data):
        """Format staff data into a readable text format"""
        details = []
        
        # Add name and ID
        details.append(f"Name: {staff_data.get('name', 'Unknown')}")
        details.append(f"ID: {staff_data.get('ID', 'Unknown')}")
        
        # Add hourly rate if available
        if 'hourly rate' in staff_data:
            details.append(f"Rate: {staff_data['hourly rate']}")
            
        # Add recommendations if available
        if 'recommended' in staff_data:
            details.append(f"Recommendations: {staff_data['recommended']}")
            
        # Add date and time info if available
        if staff_data.get('date'):
            details.append(f"Date: {staff_data['date']}")
            
        if staff_data.get('start time') and staff_data.get('end time'):
            details.append(f"Hours: {staff_data['start time']} - {staff_data['end time']}")
            
        
        # Join all details with newlines
        return "\n".join(details)
        
    def navigate_back(self, widget):
        """Navigate back to the previous view"""
        # Access the main app to handle navigation
        if hasattr(self.app, 'navigation_history') and hasattr(self.app, 'current_view'):
            if self.app.navigation_history:
                previous_view = self.app.navigation_history.pop()
                self.app.current_view = previous_view
                
                if previous_view == "main":
                    self.app.main_window.title = self.app.formal_name
                    self.app.main_window.content = self.app.main_content
                elif previous_view == "staff_view":
                    self.app.main_window.title = "Staff View"
                    if hasattr(self.app, 'staff_view'):
                        self.app.main_window.content = self.app.staff_view.create_content()
                        
    def complete_job(self):
        """Remove the job from staff_view data and navigate back"""
        # Remove the job from the original data source
        if hasattr(self.app, 'staff_view') and self.job_key in self.app.staff_view.data:
            del self.app.staff_view.data[self.job_key]
        
        # Navigate back to the staff view
        self.navigate_back(None)  # No widget needed for programmatic navigation

    def placeholder_action(self, widget):
        """Placeholder for button actions"""
        pass