import os
import toga
from toga.style import Pack
from toga.constants import *
from staffee.owner_view_staff import OwnerViewStaff
from staffee.profile_view import ProfileView
from staffee.icon_manager import IconManager

class MainApp(toga.App):
    def startup(self):
        # Create main window
        self.main_window = toga.MainWindow(title=self.formal_name)
        
        # Initialize icon manager
        self.icon_manager = IconManager(self)
        
        # Create main content
        self.main_content = self.create_main_content()
        
        # Initialize view modules
        self.staff_view = OwnerViewStaff(self)
        self.profile_view = ProfileView(self)
        
        # Set initial content
        self.main_window.content = self.main_content
        self.main_window.show()
        
        # Keep track of navigation history for back button functionality
        self.navigation_history = []
        self.current_view = "main"
        
    
    def create_main_content(self):
        # Button to open the Owner View Staff screen
        open_staff_view_button = toga.Button(
            'Open Owner View Staff',
            on_press=self.open_owner_view_staff,
            style=Pack(
                padding=(20, 5),
                width=200,
                height=40,
                background_color='#228b22',
                color='#FFFFFF',
                font_size = 10
            )
        )

        # Header
        title_label = toga.Label('Main Application', style=Pack(font_size=18, font_weight='bold', padding=(20, 20, 10, 20)))

        # Get action box (new job button and calendar button) from icon manager
        action_box = self.icon_manager.create_action_box(self.placeholder_action)

        header_box = toga.Box(
            children=[title_label, action_box],
            style=Pack(direction=ROW, alignment='center', padding=(0, 10))
        )

        ############ END OF CODE INVOLVING HEADER ############

        ############ NAVIGATION BAR CODE HERE ################ 

        # Navigation bar - use the icon manager to create it
        nav_box = self.icon_manager.create_nav_bar(self.placeholder_action)
        
        # Main content layout
        main_content = toga.Box(
            children=[
                header_box,
                open_staff_view_button,
                toga.Box(style=Pack(flex=1)),  # Spacer
                nav_box
            ],
            style=Pack(direction=COLUMN, padding=20)
        )
        
        return main_content
    
    def open_owner_view_staff(self, widget):
        """
        Navigate to the Owner View Staff screen by replacing the content
        of the main window instead of creating a secondary window
        """
        try:
            # Save current view to history for back navigation
            self.navigation_history.append(self.current_view)
            self.current_view = "staff_view"
            
            # Get the content from the OwnerViewStaff
            print("Getting content from OwnerViewStaff")
            staff_content = self.staff_view.create_content()
            
            # Update the main window title and content
            print("Updating main window content")
            self.main_window.title = "Staff View"
            self.main_window.content = staff_content
            
            print("Successfully switched to staff view")
        except Exception as e:
            print(f"Error in open_owner_view_staff: {e}")
        
    def placeholder_action(self, widget):
        """Placeholder for button actions"""
        print("Placeholder action triggered")
        pass

def main():
    return MainApp("Staffee Demo", "org.example.demoApp")