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
import threading
import mysql.connector
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from staffee.profile_view import ProfileView

# Database connection details
DB_CONFIG = {
    "host": "34.125.69.91",
    "user": "staffee_user",
    "password": "SmoothS@iling",
    "database": "staffee",
    "charset": "utf8mb4",
    "collation": "utf8mb4_general_ci"
}

class OwnerViewStaff:
    def __init__(self, app, widget, business_owner_uid):
        # Store the app instance
        self.app = app
        self.widget = widget
        self.business_owner_uid = business_owner_uid
        self.DB_details = DB_CONFIG

        self.data = {}
        self.profile_images = {}
        
        # Create loading indicator
        self.loading_label = toga.Label('Loading staff data...', style=Pack(padding=20))
        self.scrollable_content = toga.Box(style=Pack(direction=COLUMN, padding=10))
        self.current_selection = None
        
        # Show initial loading UI
        main_box = toga.Box(
            children=[self.loading_label],
            style=Pack(direction=COLUMN, padding=10)
        )
        
        # Set initial content
        self.app.main_window.content = main_box
        
        # Initialize dynamic content (needed later)
        self.dynamic_content = None
        self.prompt_label = None
        
        # Start background thread to fetch data
        threading.Thread(target=self.fetch_and_prepare_data, name="fetch_and_prepare_data").start()

    def fetch_and_prepare_data(self):
        """Fetch staff data and prepare UI components in a background thread."""
        connection = None
        try:
            # Create connection explicitly
            connection = mysql.connector.connect(**self.DB_details)
            self.db_conn = connection
            self.fetch_staff_data()

            # Once data is ready, schedule UI update on main thread using Toga's mechanisms
            self.app.loop.call_soon_threadsafe(self.update_ui)

        except mysql.connector.Error as err:
            print(f"Error in DB thread: {err}")
            # Post error message to UI thread
            self.app.loop.call_soon_threadsafe(lambda: self.show_error(str(err)))
        finally:
            # Ensure connection is closed even if an exception occurred
            if connection and connection.is_connected():
                connection.close()
                print("Database connection closed")

    def update_ui(self):
        """Update the UI with fetched data (called on main thread)"""
        content = self.create_content()
        self.app.main_window.content = content
    
    def show_error(self, error_message):
        """Show an error message on the main thread."""
        error_label = toga.Label(f"Error: {error_message}", style=Pack(padding=20))
        retry_button = toga.Button(
            "Retry", 
            on_press=lambda widget: threading.Thread(target=self.fetch_and_prepare_data).start(),
            style=Pack(padding=10)
        )
        
        error_box = toga.Box(
            children=[error_label, retry_button],
            style=Pack(direction=COLUMN, padding=10, alignment='center')
        )
        
        self.app.main_window.content = error_box

    def fetch_staff_data(self):
        """Fetch staff data from the database."""
        try:
            cursor = self.db_conn.cursor(dictionary=True)
            query = """
            SELECT 
                u.UID,
                u.first_name,
                u.last_name,
                jl.JID,
                jl.job_position,
                jl.start_date,
                jl.end_date,
                jl.start_time,
                jl.end_time,
                jl.settled_hr_rate,
                jl.BUSID,
                b.bus_name,
                COALESCE(ai.Recommended, 0) as recommendations
            FROM 
                Users u
            JOIN 
                job_listings jl ON u.UID = jl.UID
            JOIN 
                Business b ON jl.BUSID = b.BUSID
            JOIN 
                applicant_info ai ON u.UID = ai.UID
            WHERE 
                b.UID = %s
                AND jl.is_active = 1
                AND jl.UID IS NOT NULL
            ORDER BY 
                jl.start_date, jl.start_time;
            """
            
            cursor.execute(query, (self.business_owner_uid,))
            staff_results = cursor.fetchall()

            for staff in staff_results:
                job_key = f"{staff['JID']}"
                
                self.data[job_key] = {
                    'JID': job_key,
                    'ID': staff['UID'],
                    'first_name': staff['first_name'],
                    'last_name': staff['last_name'],
                    'hourly_rate': staff['settled_hr_rate'],
                    'recommendations': staff['recommendations'],
                    'start_time': staff['start_time'],
                    'end_time': staff['end_time'],
                    'start_date': staff['start_date'],
                    'end_date': staff['end_date'],
                    'job_position': staff['job_position'],
                    'BUSID': staff['BUSID'],
                    'bus_name': staff['bus_name']
                }

                # Fetch and store profile image if available
                profile_pic = self.fetch_profile_image(staff['UID'])
                if profile_pic:
                    self.profile_images[staff['UID']] = profile_pic
            
            cursor.close()

        except mysql.connector.Error as err:
            print(f"Error fetching staff data: {err}")
            raise  # Re-throw to handle in the calling function

    def fetch_profile_image(self, staff_id):
        """Fetch profile image for a given staff ID."""
        try:
            cursor = self.db_conn.cursor()
            query = "SELECT pfp_path FROM Users WHERE UID = %s"
            cursor.execute(query, (staff_id,))
            result = cursor.fetchone()
            cursor.close()

            return result[0] if result and result[0] else None

        except mysql.connector.Error as err:
            print(f"Error fetching profile image: {err}")
            return None

    def generate_job_buttons(self):
        """Generate individual job buttons for scrollable content."""
        # Clear any existing children first
        if self.scrollable_content.children:
            self.scrollable_content.remove(*self.scrollable_content.children)
            
        sorted_keys = sorted(self.data.keys())

        for job_key in sorted_keys:
            job_data = self.data[job_key]
            button_text = (
                f"{job_data['first_name']} {job_data['last_name']} | "
                f"Job: {job_data['job_position']}"
            )

            job_button = toga.Button(
                button_text,
                on_press=lambda widget, key=job_key: self.select_job(key),
                style=Pack(
                    padding=(3, 6, 3, 6),
                    width=400,
                    height=60,
                    alignment='left',
                    background_color='#f0f0f0'
                )
            )

            self.scrollable_content.add(job_button)

    def create_content(self):
        """Create the main content for this view."""
        # Back button
        back_button = self.app.icon_manager.create_back_button(self.navigate_back)
        
        # Header
        title_label = toga.Label('Active Staff View', style=Pack(font_size=18, font_weight='bold', padding=(20, 20, 10, 20)))
        header_box = toga.Box(
            children=[back_button, title_label],
            style=Pack(direction=ROW, alignment='center', padding=(0, 10))
        )

        # Action box
        action_box = self.app.icon_manager.create_action_box(self.placeholder_action)
        
        # Post label
        post_label = toga.Label('Active staff', style=Pack(padding=(10, 20)))
        
        # Prompt label
        self.prompt_label = toga.Label('Select a job to view details', style=Pack(padding=10, text_align='center'))
        
        # Create scrollable content for jobs
        self.generate_job_buttons()
        job_scroll_container = toga.ScrollContainer(
            content=self.scrollable_content,
            style=Pack(flex=1, padding=5, height=300),
            horizontal=False,
            vertical=True
        )

        # Navigation bar
        nav_box = self.app.icon_manager.create_nav_bar(self.placeholder_action)

        # Dynamic content container
        self.dynamic_content = toga.Box(
            children=[self.prompt_label],
            style=Pack(direction=COLUMN, padding=4)
        )

        # Main content container
        content_box = toga.Box(
            children=[
                header_box,
                action_box,
                toga.Box(children=[post_label], style=Pack(direction=ROW)),
                job_scroll_container,
                self.dynamic_content,
                toga.Box(style=Pack(flex=1)),  # Spacer
                nav_box
            ],
            style=Pack(direction=COLUMN)
        )
        
        return content_box

    def navigate_back(self, widget):
        """Navigate back to the main view."""
        self.app.main_window.title = self.app.formal_name
        self.app.main_window.content = self.app.main_content
        
        if hasattr(self.app, 'navigation_history') and hasattr(self.app, 'current_view'):
            if self.app.navigation_history:
                self.app.navigation_history.pop()
            self.app.current_view = "main"

    def select_job(self, job_key):
        """Handler for clicking a job button."""
        if job_key in self.data:
            self.current_selection = job_key
            job_details = self.data[job_key]
            staff_id = job_details["ID"]
            profile_pic = self.profile_images.get(staff_id, None)
            self.open_profile_view(job_key, job_details, profile_pic)

    def open_profile_view(self, job_key, job_details, profile_pic):
        """Open the profile view for the selected job."""
        self.app.navigation_history.append(self.app.current_view)
        self.app.current_view = "profile_view"
    
        self.app.main_window.title = f"Business: {job_details['bus_name']}"
    
        profile_view = ProfileView(self.app)
        profile_content = profile_view.create_content(job_details, profile_pic, job_key)
        self.app.main_window.content = profile_content

    def clear_job_display(self):
        """Clear all job-related display elements."""
        self.dynamic_content.remove(*self.dynamic_content.children)
        self.dynamic_content.add(self.prompt_label)
        self.current_selection = None

    def remove_selected_job(self):
        """Remove the selected job from the data and refresh the display."""
        if self.current_selection and self.current_selection in self.data:
            del self.data[self.current_selection]
        
            self.dynamic_content.remove(*self.dynamic_content.children)
            self.dynamic_content.add(self.prompt_label)
        
            self.refresh_job_buttons()
        
            self.current_selection = None

    def refresh_job_buttons(self):
        """Refresh job buttons after job removal."""
        # Use Toga's thread-safe method to update UI from any thread
        self.app.loop.call_soon_threadsafe(self._refresh_job_buttons_ui)
        
    def _refresh_job_buttons_ui(self):
        """Actually refresh the job buttons (called on main thread)"""
        self.generate_job_buttons()

    def placeholder_action(self, widget):
        """Placeholder for button actions."""
        pass