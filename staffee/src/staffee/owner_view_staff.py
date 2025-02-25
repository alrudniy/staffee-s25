'''
This program holds the window that will be used to display the activate staff members 
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

# ensuring that the class is exportable (CLAUDE)
__all__ = ['OwnerViewStaffWindow']

class OwnerViewStaffWindow(toga.Window):
    def __init__(self):
        super().__init__(title="Owner View Staff", size=(800, 600))

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
            
            "job 2 at pharmacy 1": {
                "ID": 1, "name": "Arthur Read", "recommended": 0,
                "hourly rate": f"${25:.2f}/h", "date": None,
                "start time": None, "end time": None
            },
            "job 2 at pharmacy 2": {
                "ID": 2, "name": "Tony Barks", "recommended": 5.4,
                "hourly rate": f"${75:.2f}/h", "date": None,
                "start time": None, "end time": None
            },
            "job 2 at pharmacy 3": {
                "ID": 3, "name": "Howard Hughes", "recommended": 4,
                "hourly rate": f"${55:.2f}/h", "date": None,
                "start time": None, "end time": None
            },
            
            "job 3 at pharmacy 1": {
                "ID": 1, "name": "John Smith", "recommended": 0,
                "hourly rate": f"${25:.2f}/h", "date": None,
                "start time": None, "end time": None
            },
            "job 3 at pharmacy 2": {
                "ID": 2, "name": "Luka Doncic", "recommended": 5.4,
                "hourly rate": f"${75:.2f}/h", "date": None,
                "start time": None, "end time": None
            },
            "job 3 at pharmacy 3": {
                "ID": 3, "name": "Alex Len", "recommended": 4,
                "hourly rate": f"${55:.2f}/h", "date": None,
                "start time": None, "end time": None
            },
            
            "job 4 at pharmacy 1": {
                "ID": 1, "name": "Arthur Smith", "recommended": 0,
                "hourly rate": f"${25:.2f}/h", "date": None,
                "start time": None, "end time": None
            },
            "job 5 at pharmacy 2": {
                "ID": 2, "name": "Vincent Doom", "recommended": 5.4,
                "hourly rate": f"${75:.2f}/h", "date": None,
                "start time": None, "end time": None
            },
            "job 6 at pharmacy 3": {
                "ID": 3, "name": "Frank Castle", "recommended": 4,
                "hourly rate": f"${55:.2f}/h", "date": None,
                "start time": None, "end time": None
            },
            
            "job 18 at pharmacy 1": {
                "ID": 1, "name": "Arthur Smith", "recommended": 0,
                "hourly rate": f"${25:.2f}/h", "date": None,
                "start time": None, "end time": None
            },
            "job 13 at pharmacy 2": {
                "ID": 2, "name": "Vincent Doom", "recommended": 5.4,
                "hourly rate": f"${75:.2f}/h", "date": None,
                "start time": None, "end time": None
            },
            "job 15 at pharmacy 3": {
                "ID": 3, "name": "Frank Castle", "recommended": 4,
                "hourly rate": f"${55:.2f}/h", "date": None,
                "start time": None, "end time": None
            },
            
            "job 1 at pharmacy 11": {
                "ID": 1, "name": "Arthur Smith", "recommended": 0,
                "hourly rate": f"${25:.2f}/h", "date": None,
                "start time": None, "end time": None
            },
            "job 1 at pharmacy 23": {
                "ID": 2, "name": "Vincent Doom", "recommended": 5.4,
                "hourly rate": f"${75:.2f}/h", "date": None,
                "start time": None, "end time": None
            },
            "job 1 at pharmacy 30": {
                "ID": 3, "name": "Frank Castle", "recommended": 4,
                "hourly rate": f"${55:.2f}/h", "date": None,
                "start time": None, "end time": None
            },
            
            "job 1 at pharmacy 14": {
                "ID": 1, "name": "Arthur Smith", "recommended": 0,
                "hourly rate": f"${25:.2f}/h", "date": None,
                "start time": None, "end time": None
            },
            "job 1 at pharmacy 23": {
                "ID": 2, "name": "Vincent Doom", "recommended": 5.4,
                "hourly rate": f"${75:.2f}/h", "date": None,
                "start time": None, "end time": None
            },
            "job 1 at pharmacy 35": {
                "ID": 3, "name": "Frank Castle", "recommended": 4,
                "hourly rate": f"${55:.2f}/h", "date": None,
                "start time": None, "end time": None
            }
        }

        self.create_owner_view_staff()
    
    def create_owner_view_staff(self):

        self.current_selection = None

        async def action_fulfill_button(widget):
            """Handle fulfillment confirmation and remove job if confirmed."""
            if self.current_selection:
                confirm_question = await self.dialog(toga.ConfirmDialog(
                    "Confirm fulfillment",
                    "Has this job been completed?",
                ))

                ''' adding a 'review' feature in lack of star review system 
                (Claude helped with implementation, I chose the question dialog)'''

                if confirm_question:
                    # Ask if they want to recommend the staff member
                    recommend_question = await self.dialog(toga.QuestionDialog(
                        "Recommend staff",
                        "Do you recommend this applicant ?", # YES == True, NO == FALSE
                    ))
                    if recommend_question:
                        # Increment the recommended count
                        staff_id = self.data[self.current_selection]["ID"]
                        self.data[self.current_selection]["recommended"] += 1
                    
                    self.remove_selected_job()

        async def action_cancel_button(widget):
            """Handle termination confirmation and remove job if confirmed."""
            if self.current_selection:
                confirm_question = await self.dialog(toga.ConfirmDialog(
                    "Confirm termination",
                    "Terminate this employee?",
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
        

        # Get the current directory and set up image path (CLAUDE)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(current_dir, "resources" , "images")
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
        title_label = toga.Label('Active Staff View', style=Pack(font_size=18, font_weight='bold', padding=(20, 20, 10, 20)))
        
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
            style=Pack(direction=COLUMN, padding=4)
        )

        # Main container with updated layout
        self.content_box = toga.Box(
            children=[
                header_box,
                toga.Box(children=[post_label], style=Pack(direction=ROW)),
                job_scroll_container,  # Using the scroll container here
                self.dynamic_content,
                toga.Box(style=Pack(flex=1)),  # Spacer
                nav_box
            ],
            style=Pack(direction=COLUMN)
        )
        
        self.content = self.content_box

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
                width=280,
                height=50,
                alignment='left',
                background_color='#f0f0f0'
            )
        )
            
            self.scrollable_content.add(job_button)

    def select_job(self, job_key):
        """Handler for clicking a job button"""
        if job_key in self.data:
            # Clear the dynamic content
            self.dynamic_content.remove(*self.dynamic_content.children)
            self.current_selection = job_key
        
            # Get job details
            job_details = self.data[job_key]
        
            # Create a box for profile picture
            profile_container = toga.Box(
                style=Pack(direction=COLUMN, alignment='center', padding=5)
            )
        
            # Get and add profile picture
            staff_id = job_details["ID"]
            if staff_id in self.profile_images:
                profile_pic = self.profile_images[staff_id]
                profile_container.add(profile_pic)
        
            # Create text display for job details
            result_text = f"Details for {job_key}:\n\n"
            result_text += f"Name: {job_details['name']}\n"
            result_text += f"ID: {job_details['ID']}\n"
            result_text += f"Hourly Rate: {job_details['hourly rate']}\n"
            result_text += f"Recommendations: {job_details['recommended']}\n"
        
            result_display = toga.MultilineTextInput(
                readonly=True,
                value=result_text,
                style=Pack(padding=5, flex=1, height=150)  # Reduced height to fit better
            )
        
        # Create a container for content
        content_box = toga.Box(
            children=[
                profile_container,
                result_display,
                self.button_container  # Add the existing button container
            ],
            style=Pack(direction=COLUMN, padding=5, alignment='center')
        )
        
        # Add the content box to dynamic content
        self.dynamic_content.add(content_box)

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


def main():
    return OwnerViewStaffWindow