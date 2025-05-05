import toga
import mysql.connector
from toga.style import Pack
from toga.constants import COLUMN, ROW
from datetime import datetime

class ChatView:
    def __init__(self, app, db_config):
        """Initialize the chat view with application context and database configuration."""
        self.app = app
        self.db_config = db_config
        self.user_id = None
        self.user_type = None
        self.business_id = None
        self.current_chat_with = None
        self.chats = []
        self.messages = []
        
        # UI Components
        self.chat_list_box = None
        self.message_list_box = None
        self.message_input = None
        self.send_button = None
        self.new_chat_button = None
        self.chat_contact_selection = None
        self.new_chat_dialog = None
        
    def create_content(self):
        """Create the main chat interface layout without SplitContainer."""
        # Main container
        main_box = toga.Box(style=Pack(direction=COLUMN, flex=1))

        # Create header with back button and title
        header_box = self._create_header()
        main_box.add(header_box)

        # Chat area container (replaces SplitContainer with horizontal Box)
        chat_area_box = toga.Box(style=Pack(direction=ROW, flex=1))

        # Left side - Chat list
        self.chat_list_box = toga.Box(style=Pack(direction=COLUMN, flex=1, padding=5))
        left_container = toga.ScrollContainer(content=self.chat_list_box, style=Pack(width=200))

        # Right side - Messages and input
        right_container = toga.Box(style=Pack(direction=COLUMN, flex=2))

        # Messages area
        self.message_list_box = toga.Box(style=Pack(direction=COLUMN, padding=5))
        message_container = toga.ScrollContainer(content=self.message_list_box, style=Pack(flex=1))

        # Input area
        input_box = toga.Box(style=Pack(direction=ROW, padding=5))
        self.message_input = toga.MultilineTextInput(
            placeholder="Type a message...",
            style=Pack(flex=1, height=60)
        )
        self.send_button = toga.Button(
            "Send",
            on_press=self.send_message,
            style=Pack(width=80, padding=5, background_color='green', color='white')
        )
        input_box.add(self.message_input)
        input_box.add(self.send_button)

        # Assemble right container
        right_container.add(message_container)
        right_container.add(input_box)

        # Add both containers to the horizontal box
        chat_area_box.add(left_container)
        chat_area_box.add(right_container)

        # Add chat area to main box
        main_box.add(chat_area_box)

        return main_box
    
    def _create_header(self):
        """Create the header with back button and new chat button."""
        header_box = toga.Box(style=Pack(direction=ROW, padding=10))
        
        # Back button
        back_button = toga.Button(
            "Back",
            on_press=self.go_back,
            style=Pack(width=80, padding=5)
        )
        
        # Title
        title = toga.Label(
            "Messages",
            style=Pack(flex=1, text_align="center", font_size=18, font_weight="bold")
        )
        
        # New chat button
        self.new_chat_button = toga.Button(
            "New Chat",
            on_press=self.show_new_chat_dialog,
            style=Pack(width=100, padding=5, background_color='blue', color='white')
        )
        
        header_box.add(back_button)
        header_box.add(title)
        header_box.add(self.new_chat_button)
        
        return header_box
    
    def go_back(self, widget):
        """Navigate back to the previous screen."""
        if self.app.navigation_history:
            previous_view = self.app.navigation_history.pop()
            
            if previous_view == "main":
                self.app.current_view = "main"
                self.app.main_window.content = self.app.main_content
            elif previous_view == "staff_view":
                self.app.open_owner_view_staff(None)
    
    def initialize_user_data(self, user_id, user_type):
        """Initialize user data and load chats."""
        self.user_id = user_id
        self.user_type = user_type
        
        # If user is a business owner, get their business ID
        if user_type == "Business Owner":
            self.business_id = self.get_business_id_for_owner(user_id)
        
        # Load existing chats
        self.load_chats()
        self.populate_chat_list()
    
    def get_business_id_for_owner(self, owner_id):
        """Get the business ID associated with a business owner."""
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            query = "SELECT BUSID FROM Business WHERE UID = %s"
            cursor.execute(query, (owner_id,))
            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if result:
                return result[0]
            return None
            
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return None
    
    def load_chats(self):
        """Load all chats for the current user based on their type."""
        self.chats = []
        
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor(dictionary=True)
            
            if self.user_type == "Business Owner":
                # For business owners: get all unique applicant IDs who have communicated with this business
                query = """
                SELECT DISTINCT 
                    CASE 
                        WHEN sender_uid = %s THEN receiver_uid 
                        ELSE sender_uid 
                    END AS contact_id
                FROM Messages 
                WHERE (sender_uid = %s OR receiver_uid = %s) AND busid = %s
                """
                cursor.execute(query, (self.user_id, self.user_id, self.user_id, self.business_id))
                
                # Get applicant details for each contact
                for row in cursor.fetchall():
                    applicant_id = row['contact_id']
                    
                    # Get applicant details
                    user_query = "SELECT first_name, last_name FROM Users WHERE UID = %s"
                    cursor.execute(user_query, (applicant_id,))
                    user_details = cursor.fetchone()
                    
                    if user_details:
                        # Get last message
                        last_message_query = """
                        SELECT message_text, created_at 
                        FROM Messages 
                        WHERE ((sender_uid = %s AND receiver_uid = %s) OR (sender_uid = %s AND receiver_uid = %s)) 
                            AND busid = %s
                        ORDER BY created_at DESC LIMIT 1
                        """
                        cursor.execute(last_message_query, (self.user_id, applicant_id, applicant_id, self.user_id, self.business_id))
                        last_message = cursor.fetchone()
                        
                        # Count unread messages
                        unread_query = """
                        SELECT COUNT(*) as unread 
                        FROM Messages 
                        WHERE sender_uid = %s AND receiver_uid = %s AND busid = %s AND is_read = 0
                        """
                        cursor.execute(unread_query, (applicant_id, self.user_id, self.business_id))
                        unread_count = cursor.fetchone()['unread']
                        
                        self.chats.append({
                            'contact_id': applicant_id,
                            'name': f"{user_details['first_name']} {user_details['last_name']}",
                            'last_message': last_message['message_text'] if last_message else "",
                            'timestamp': last_message['created_at'] if last_message else None,
                            'unread_count': unread_count,
                            'business_id': self.business_id
                        })
            
            else:  # Applicant
                # For applicants: get all unique business IDs they've communicated with
                query = """
                SELECT DISTINCT busid
                FROM Messages 
                WHERE sender_uid = %s OR receiver_uid = %s
                """
                cursor.execute(query, (self.user_id, self.user_id))
                
                # Get business details for each contact
                for row in cursor.fetchall():
                    business_id = row['busid']
                    
                    # Get business details and owner ID
                    business_query = "SELECT bus_name, UID FROM Business WHERE BUSID = %s"
                    cursor.execute(business_query, (business_id,))
                    business_details = cursor.fetchone()
                    
                    if business_details:
                        business_owner_id = business_details['UID']
                        
                        # Get last message
                        last_message_query = """
                        SELECT message_text, created_at 
                        FROM Messages 
                        WHERE ((sender_uid = %s AND receiver_uid = %s) OR (sender_uid = %s AND receiver_uid = %s)) 
                            AND busid = %s
                        ORDER BY created_at DESC LIMIT 1
                        """
                        cursor.execute(last_message_query, (self.user_id, business_owner_id, business_owner_id, self.user_id, business_id))
                        last_message = cursor.fetchone()
                        
                        # Count unread messages
                        unread_query = """
                        SELECT COUNT(*) as unread 
                        FROM Messages 
                        WHERE sender_uid = %s AND receiver_uid = %s AND busid = %s AND is_read = 0
                        """
                        cursor.execute(unread_query, (business_owner_id, self.user_id, business_id))
                        unread_count = cursor.fetchone()['unread']
                        
                        self.chats.append({
                            'contact_id': business_owner_id,
                            'name': business_details['bus_name'],
                            'last_message': last_message['message_text'] if last_message else "",
                            'timestamp': last_message['created_at'] if last_message else None,
                            'unread_count': unread_count,
                            'business_id': business_id
                        })
            
            # Sort chats by timestamp (most recent first)
            self.chats.sort(key=lambda x: x['timestamp'] if x['timestamp'] else datetime.min, reverse=True)
            
            cursor.close()
            conn.close()
            
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
    
    def populate_chat_list(self):
        """Populate the chat list with available chats."""
        # Clear existing chats
        for child in list(self.chat_list_box.children):
            self.chat_list_box.remove(child)
        
        if not self.chats:
            # Show "No chats" message
            no_chats_label = toga.Label(
                "No conversations yet",
                style=Pack(padding=20, text_align="center")
            )
            self.chat_list_box.add(no_chats_label)
            return
        
        # Add each chat to the list
        for chat in self.chats:
            chat_item = self._create_chat_item(chat)
            self.chat_list_box.add(chat_item)
    
    def _create_chat_item(self, chat):
        """Create a UI component for a chat item."""
        # Main box for the chat item
        chat_box = toga.Box(style=Pack(direction=ROW, padding=10, width=250))
        
        # Contact info container
        info_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
        
        # Contact name with bold font
        name_label = toga.Label(
            chat['name'],
            style=Pack(font_weight="bold", padding_bottom=2)
        )
        
        # Last message preview (truncated)
        last_message = chat['last_message']
        if len(last_message) > 30:
            last_message = last_message[:30] + "..."
            
        message_label = toga.Label(
            last_message,
            style=Pack(font_size=14, color='gray')
        )
        
        info_box.add(name_label)
        info_box.add(message_label)
        
        # Right side with timestamp and unread count
        right_box = toga.Box(style=Pack(direction=COLUMN, width=80, text_align="right"))
        
        # Format timestamp
        time_str = ""
        if chat['timestamp']:
            now = datetime.now()
            timestamp = chat['timestamp']
            
            if timestamp.date() == now.date():
                # Today, show just the time
                time_str = timestamp.strftime("%I:%M %p")
            elif (now.date() - timestamp.date()).days < 7:
                # This week, show the day name
                time_str = timestamp.strftime("%a")
            else:
                # Older, show date
                time_str = timestamp.strftime("%m/%d/%y")
        
        time_label = toga.Label(
            time_str,
            style=Pack(font_size=12, color='gray', padding_bottom=5)
        )
        right_box.add(time_label)
        
        # Unread count indicator
        if chat['unread_count'] > 0:
            unread_label = toga.Label(
                str(chat['unread_count']),
                style=Pack(
                    background_color='blue',
                    color='white',
                    padding=5,
                    width=25,
                    height=25,
                    text_align="center"
                )
            )
            right_box.add(unread_label)
        
        # Add components to main chat box
        chat_box.add(info_box)
        chat_box.add(right_box)
        
        # Make the chat item clickable
        chat_box.on_press = lambda widget: self.open_chat(
            chat['contact_id'], 
            chat['name'], 
            chat['business_id']
        )
        
        return chat_box
    
    def open_chat(self, contact_id, contact_name, business_id):
        """Open a chat conversation with the selected contact."""
        self.current_chat_with = {
            'id': contact_id,
            'name': contact_name,
            'business_id': business_id
        }
        
        # Clear existing messages
        for child in list(self.message_list_box.children):
            self.message_list_box.remove(child)
        
        # Add conversation header
        header = toga.Label(
            f"Conversation with {contact_name}",
            style=Pack(font_size=16, font_weight="bold", padding=10, text_align="center")
        )
        self.message_list_box.add(header)
        
        # Load and display messages
        self.load_messages(contact_id, business_id)
        
        # Mark messages as read
        self.mark_messages_as_read(contact_id, business_id)
        
        # Refresh chat list to update unread counts
        self.load_chats()
        self.populate_chat_list()
    
    def load_messages(self, contact_id, business_id):
        """Load messages for a specific conversation."""
        self.messages = []
        
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor(dictionary=True)
            
            # Get messages between the current user and the contact
            query = """
            SELECT message_id, sender_uid, receiver_uid, message_text, 
                   attachment_url, is_read, created_at
            FROM Messages
            WHERE ((sender_uid = %s AND receiver_uid = %s) OR 
                  (sender_uid = %s AND receiver_uid = %s)) AND
                  busid = %s
            ORDER BY created_at
            """
            cursor.execute(query, (self.user_id, contact_id, contact_id, self.user_id, business_id))
            
            self.messages = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            # Display messages
            self.display_messages()
            
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
    
    def display_messages(self):
        """Display messages in the UI."""
        # Skip the header - it's already added
        start_index = 1
        
        # Group messages by date for separators
        current_date = None
        
        for message in self.messages:
            # Check if we need to add a date separator
            message_date = message['created_at'].date()
            if current_date != message_date:
                current_date = message_date
                
                # Add date separator
                now = datetime.now().date()
                if message_date == now:
                    date_str = "Today"
                elif message_date == now - datetime.timedelta(days=1):
                    date_str = "Yesterday"
                else:
                    date_str = message_date.strftime("%B %d, %Y")
                
                date_separator = toga.Label(
                    date_str,
                    style=Pack(
                        text_align="center",
                        padding=5,
                        font_size=12,
                        color='gray'
                    )
                )
                self.message_list_box.add(date_separator)
            
            # Create message bubble
            is_from_me = message['sender_uid'] == self.user_id
            message_box = self._create_message_bubble(message, is_from_me)
            self.message_list_box.add(message_box)
    
    def _create_message_bubble(self, message, is_from_me):
        """Create a UI component for a message bubble."""
        # Container for alignment
        container = toga.Box(style=Pack(
            direction=ROW,
            padding=5,
            alignment="right" if is_from_me else "left"
        ))
        
        # Message bubble
        bubble = toga.Box(style=Pack(
            padding=10,
            background_color='#DCF8C6' if is_from_me else '#ECECEC',
            width=200
        ))
        
        # Message text
        text_label = toga.Label(
            message['message_text'],
            style=Pack(padding_bottom=5)
        )
        bubble.add(text_label)
        
        # Time
        time_str = message['created_at'].strftime("%I:%M %p")
        time_label = toga.Label(
            time_str,
            style=Pack(font_size=10, color='gray', text_align="right")
        )
        bubble.add(time_label)
        
        # Show attachment if present
        if message['attachment_url']:
            attachment_label = toga.Label(
                f"📎 Attachment",
                style=Pack(padding_top=5, color='blue')
            )
            bubble.add(attachment_label)
        
        # Add message bubble to container
        if is_from_me:
            container.add(toga.Box(style=Pack(flex=1)))  # Spacer
            container.add(bubble)
        else:
            container.add(bubble)
            container.add(toga.Box(style=Pack(flex=1)))  # Spacer
        
        return container
    
    def mark_messages_as_read(self, contact_id, business_id):
        """Mark all messages from contact as read."""
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            query = """
            UPDATE Messages
            SET is_read = 1
            WHERE sender_uid = %s AND receiver_uid = %s AND busid = %s AND is_read = 0
            """
            cursor.execute(query, (contact_id, self.user_id, business_id))
            conn.commit()
            
            cursor.close()
            conn.close()
            
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
    
    def send_message(self, widget):
        """Send a message to the current contact."""
        if not self.current_chat_with or not self.message_input.value.strip():
            return
        
        print(f"DEBUG: current_chat_with = {self.current_chat_with}")

        message_text = self.message_input.value.strip()
        contact_id = self.current_chat_with['id']
        business_id = self.current_chat_with['business_id']
        
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Insert the new message
            query = """
            INSERT INTO Messages 
            (sender_uid, receiver_uid, busid, message_text, is_read, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            now = datetime.now()
            cursor.execute(query, (
                self.user_id,
                contact_id,
                business_id,
                message_text,
                0,  # Not read initially
                now
            ))
            conn.commit()
            
            # Clear the input field
            self.message_input.value = ""
            
            # Add the new message to the UI
            new_message = {
                'message_id': cursor.lastrowid,
                'sender_uid': self.user_id,
                'receiver_uid': contact_id,
                'message_text': message_text,
                'attachment_url': None,
                'is_read': 0,
                'created_at': now
            }
            self.messages.append(new_message)
            
            # Add message to UI
            message_box = self._create_message_bubble(new_message, True)
            self.message_list_box.add(message_box)
            
            # Update the chat list to show the latest message
            self.load_chats()
            self.populate_chat_list()
            
            cursor.close()
            conn.close()
            
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
    
    def show_new_chat_dialog(self, widget):
        """Show a new screen to start a new chat."""
        self.app.navigation_history.append(self.app.current_view)
        self.app.current_view = "new_chat"

        if self.user_type == "Business Owner" and self.business_id is None:
            self.business_id = self.get_business_id_for_owner(self.user_id)

        new_chat_box = toga.Box(style=Pack(direction=COLUMN, padding=20))

        title_label = toga.Label(
            "Start a New Chat",
            style=Pack(font_size=20, font_weight="bold", padding_bottom=20, text_align="center")
        )
        new_chat_box.add(title_label)

        # FIRST create empty dropdown
        self.contact_selection = toga.Selection(items=[], style=Pack(padding=10))
        new_chat_box.add(self.contact_selection)

        # THEN load contacts
        self.load_available_contacts()

        start_chat_button = toga.Button(
            "Start Chat",
            on_press=self.start_chat_with_selected_contact,
            style=Pack(padding=10, background_color='green', color='white')
        )
        new_chat_box.add(start_chat_button)

        back_button = toga.Button(
            "Back",
            on_press=self.go_back,
            style=Pack(padding=10)
        )
        new_chat_box.add(back_button)

        self.app.main_window.title = "New Chat"
        self.app.main_window.content = new_chat_box
        
   
    def load_available_contacts(self):
        """Load available contacts based on user type."""
        self.available_contacts = []
        
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor(dictionary=True)
            
            if self.user_type == "Business Owner":
                # For business owners, show all applicants
                query = """
                SELECT UID, first_name, last_name 
                FROM Users 
                WHERE type = 'Applicant'
                """
                cursor.execute(query)
                
                for user in cursor.fetchall():
                    self.available_contacts.append({
                        'id': user['UID'],
                        'name': f"{user['first_name']} {user['last_name']}",
                        'business_id': self.business_id
                    })
                
            else:  # Applicant
                # For applicants, show all businesses
                query = """
                SELECT b.BUSID, b.bus_name, b.UID
                FROM Business b
                INNER JOIN Users u ON b.UID = u.UID
                """
                cursor.execute(query)
                
                for business in cursor.fetchall():
                    self.available_contacts.append({
                        'id': business['UID'],  # Owner's ID
                        'name': business['bus_name'],
                        'business_id': business['BUSID']
                    })
            
            # Populate the selection widget
            items = [contact['name'] for contact in self.available_contacts]
            self.contact_selection.items = items
            
            cursor.close()
            conn.close()
            
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
    
    def filter_contact_options(self, widget):
        """Filter contact options based on search input."""
        search_text = widget.value.lower()
        
        # Filter available contacts
        filtered_contacts = [
            contact for contact in self.available_contacts
            if search_text in contact['name'].lower()
        ]
        
        # Update selection items
        self.chat_contact_selection.items = [
            contact['name'] for contact in filtered_contacts
        ]
    
    def handle_new_chat_result(self, dialog, result):
        """Handle the result of the new chat dialog."""
        if result != "start" or not self.chat_contact_selection.value:
            return
        
        # Find the selected contact
        selected_name = self.chat_contact_selection.value
        selected_contact = next(
            (contact for contact in self.available_contacts 
             if contact['name'] == selected_name), 
            None
        )
        
        if selected_contact:
            # Start a new chat with this contact
            self.open_chat(
                selected_contact['id'],
                selected_contact['name'],
                selected_contact['business_id']
            )
    def start_chat_with_selected_contact(self, widget):
        """Start chat with the selected contact."""
        selected_name = self.contact_selection.value
        selected_contact = next(
            (contact for contact in self.available_contacts if contact['name'] == selected_name),
            None
        )
        if selected_contact:
            # Store selected contact safely
            self.current_chat_with = {
                'id': selected_contact['id'],
                'name': selected_contact['name'],
                'business_id': selected_contact['business_id']
            }

            # Reset back to full chat view layout
            self.app.current_view = "chat_view"
            self.app.main_window.title = "Chat View"

            # Recreate the chat interface
            chat_content = self.create_content()
            self.app.main_window.content = chat_content

            # 🛑 DO NOT call initialize_user_data() again here
            # Just open the chat directly
            self.open_chat(
                selected_contact['id'],
                selected_contact['name'],
                selected_contact['business_id']
            )
