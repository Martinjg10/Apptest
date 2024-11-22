from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.utils import platform
from datetime import datetime
from kivy.metrics import sp, dp
import ast
import os
if platform == "android":
    from android.permissions import request_permissions, Permission, check_permission  # pylint: disable=import-error # type: ignore
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

class TidstagningMJGApp(App):
    def build(self):
        self.main_layout = FloatLayout()  # Use FloatLayout for precise positioning
        self.startAntalKamre = None
        self.slutAntalKamre = None
        self.current_matrix = 0  # Track which matrix is displayed (0, 1, 2, or 3)
        self.populated_ratio = 0
        self.currenttimeseconds = 0  # Initialize the seconds counter
        self.timer_event = None  # Holds the Clock event for the timer
        current_date = "currenttime"
        currenttimefile = f"{current_date}.txt"
        self.laststatecalled = False
        self.timestarted = False
        self.timeatstart = ""
        self.currenttime ="00:00:00"

        # Set the file path based on the platform
        if platform == 'android':  # Assuming Android runs on Linux
            self.filepath2 = os.path.join('/sdcard/Documents', currenttimefile)
        else:
            self.filepath2 = os.path.join(os.path.expanduser("~"), currenttimefile)

        # Add "Current time" label at the center upper part
        self.titelnavnapp = Label(
            text="Tidstagningsapp - Vers. 1.0",
            font_size=sp(28),
            pos_hint={'center_x': 0.5, 'y': 0.35}  # Centered horizontally at the top
        )
        self.main_layout.add_widget(self.titelnavnapp)
        
        # Add "Current time" label at the center upper part
        self.udviklernavnonlaunch = Label(
            text="Made by MJG",
            font_size=sp(10),
            pos_hint={'center_x': 0.5, 'y': 0.3}  # Centered horizontally at the top
        )
        self.main_layout.add_widget(self.udviklernavnonlaunch)

                # Add "Current time" label at the center upper part
        self.udviklernavnmainscreen = Label(
            text="MJG - Vers. 1.0",
            font_size=sp(14),
            pos_hint={'center_x': 0.82, 'y': 0.47}  # Centered horizontally at the top
        )
        self.main_layout.add_widget(self.udviklernavnmainscreen)

        # Add "Current time" label at the center upper part
        self.time_label = Label(
            text="Current time:",
            font_size=sp(20),
            pos_hint={'center_x': 0.5, 'y': 0.28}  # Centered horizontally at the top
        )
        self.main_layout.add_widget(self.time_label)

        # Add "Current time" label at the center upper part
        self.timeatstart_label = Label(
            text=f"Time at start: {self.timeatstart}",
            font_size=sp(20),
            pos_hint={'center_x': 0.5, 'y': 0.38}  # Centered horizontally at the top
        )
        self.main_layout.add_widget(self.timeatstart_label)

        # Add a horizontal line
        #with self.main_layout.canvas:
        #    Color(1, 1, 1, 1)  # White color
        #    self.horizontal_line = Rectangle(size=(self.main_layout.width, 1), pos=(0, self.main_layout.height / 2))

        # Add a vertical line
        #with self.main_layout.canvas:
        #    Color(1, 1, 1, 1)  # White color
        #    self.vertical_line = Rectangle(size=(1, self.main_layout.height), pos=(self.main_layout.width / 2, 0))

        # Bind to window resize to reposition lines correctly if the window is resized
        #self.main_layout.bind(size=self.update_lines_position)

        # Create a button in the upper left corner and save its reference
        #self.upper_left_button = Button(
        #    text="Print matrix",
        #    size_hint=(None, None),
        #    size=(dp(100), dp(40)),
        #    pos_hint={'x': 0.03, 'y': 0.93}
        #)
        #self.upper_left_button.bind(on_release=self.on_upper_left_button_press)
        #self.main_layout.add_widget(self.upper_left_button)

        # Create the new button just below "Print matrix"
        self.starttid = Button(
            text="Start timer",
            size_hint=(None, None),
            size=(dp(100), dp(40)),
            pos_hint={'x': 0.03, 'y': 0.9}  # Position below "Print matrix"
        )
        # The new button currently has no functionality
        self.starttid.bind(on_release=self.start_timer)  # Bind start timer
        self.main_layout.add_widget(self.starttid)

        # Create the new button just below "Print matrix"
        self.stoptid = Button(
            text="Stop timer",
            size_hint=(None, None),
            size=(dp(100), dp(40)),
            pos_hint={'x': 0.03, 'y': 0.8}  # Position below "Print matrix"
        )
        # The new button currently has no functionality
        self.stoptid.bind(on_release=self.stop_timer)  # Bind stop timer
        self.main_layout.add_widget(self.stoptid)

        # Create a button in the upper right corner with functionality to add "recorded time"
        self.upper_right_button = Button(
            text="Save time",
            size_hint=(None, None),
            size=(dp(150), dp(45)),
            font_size=sp(22),
            pos_hint={'x': 0.3, 'y': 0.67}  # Adjusted to be in the upper right corner
        )
        self.upper_right_button.bind(on_release=self.add_and_write)
        self.main_layout.add_widget(self.upper_right_button)

        # Create a button in the upper right corner with functionality to add "recorded time"
        self.gendanstateknap = Button(
            text="Load last state",
            size_hint=(None, None),
            size=(dp(90), dp(38)),
            font_size=sp(12),
            pos_hint={'x': 0.7, 'y': 0.8}  # Adjusted to be in the upper right corner
        )
        self.gendanstateknap.bind(on_release=self.gendantidogskema)

        self.main_layout.add_widget(self.gendanstateknap)
        self.knapperpaamainscreen = [
                            self.upper_right_button,
                            self.starttid,
                            self.stoptid,
                            self.time_label,
                            self.gendanstateknap,
                            self.timeatstart_label,
                            self.udviklernavnmainscreen]

        # Loop through widgets and remove all except those in the excluded list
        for widget in self.main_layout.children[:]:
            if widget in self.knapperpaamainscreen:
                self.main_layout.remove_widget(widget)

        self.show_popup()
        return self.main_layout
    
    def gendantidogskema(self, instance):
        if self.timestarted == False:
            self.load_last_time()
            self.read_matrices_from_file()
        
            # Display Tidstagningsskema0 initially
            self.display_table(self.Tidstagningsskema0, matrix_index=0)
        else:
            pass

    def add_and_write(self, instance):
        if self.laststatecalled == False:
            self.createsavelastmatrixstatefile(instance)
            self.laststatecalled = True
        else:
            pass
        self.add_recorded_time(instance)
        self.write_matrices_to_file()
        self.write_raw_matrices_to_file()

    def start_timer(self, instance):
        def proceed_with_timer(*args):
            # Close the popup and proceed with starting the timer
            popup.dismiss()

            # Attempt to create the file
            try:
                with open(self.filepath2, 'w') as file:
                    file.write("0\n")  # Initialize file with 0 seconds
                print(f"File created at {self.filepath2}")
            except Exception as e:
                print(f"Failed to create file: {e}")

            # Start the timer, updating `currenttimeseconds` every second
            if not self.timer_event:  # Avoid starting multiple timers
                self.timer_event = Clock.schedule_interval(self.update_seconds, 1)
                print("Timer started.")

            if self.timestarted == False:
                self.timeatstart = datetime.now().strftime("%H:%M:%S")
                self.timestarted = True
                self.timeatstart_label.text = f"Time at start: {self.timeatstart}"
            else:
                pass

        def cancel_timer_start(*args):
            # Close the popup and do nothing
            popup.dismiss()

        # Create the popup content
        popup_content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        popup_content.add_widget(Label(text="Are you sure you want to start the timer? \n \n Starting the timer will overwrite \n the last saved time state", halign="center", valign="middle"))

        # Add "Yes" and "No" buttons
        button_layout = BoxLayout(orientation='horizontal', spacing=10)
        yes_button = Button(
            text="Yes",
            background_color=(0, 1, 0, 1),  # Green color (RGBA)
            
            on_press=proceed_with_timer
        )
        no_button = Button(
            text="No",
            background_color=(1, 0, 0, 1),  # Red color (RGBA)
            
            on_press=cancel_timer_start
        )
        button_layout.add_widget(yes_button)
        button_layout.add_widget(no_button)

        popup_content.add_widget(button_layout)

        # Create and display the popup
        popup = Popup(
            title="Confirm Timer Start",
            content=popup_content,
            size_hint=(0.8, 0.4),
            auto_dismiss=False  # Prevent the popup from closing without user input
        )
        popup.open()


    def stop_timer(self, instance):
        def proceed_with_stop(*args):
            # Close the popup and stop the timer
            popup.dismiss()

            # Stop the timer if it's running
            if self.timer_event:
                self.timer_event.cancel()
                self.timer_event = None
                print("Timer stopped.")

        def cancel_stop(*args):
            # Close the popup and exit the function
            popup.dismiss()

        # Create the popup content
        popup_content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        popup_content.add_widget(Label(text="Are you sure you want to stop the timer?", halign="center", valign="middle"))

        # Add "Yes" and "No" buttons
        button_layout = BoxLayout(orientation='horizontal', spacing=10)
        yes_button = Button(text="Yes", background_color=(0, 1, 0, 1), on_press=proceed_with_stop)
        no_button = Button(text="No",background_color=(1, 0, 0, 1), on_press=cancel_stop)
        button_layout.add_widget(no_button)
        button_layout.add_widget(yes_button)

        popup_content.add_widget(button_layout)

        # Create and display the popup
        popup = Popup(
            title="Confirm Stop Timer",
            content=popup_content,
            size_hint=(0.8, 0.4),
            auto_dismiss=False  # Prevent the popup from closing without user input
        )
        popup.open()


    def update_seconds(self, dt):
        # Increment the current time in seconds
        self.currenttimeseconds += 1

        # Convert current time in seconds to "HH:MM:SS" format
        hours, remainder = divmod(self.currenttimeseconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.currenttime = f"{hours:02}:{minutes:02}:{seconds:02}"

        # Update the label with the formatted time
        if self.time_label:
            self.time_label.text = f"Current time: {self.currenttime}"
        print("Current time:", self.currenttime)

        # Write the current time in seconds to the file
        try:
            with open(self.filepath2, 'w') as file:
                tid = str(self.currenttimeseconds)
                file.write(tid)
        except Exception as e:
            print(f"Failed to write time to file: {e}")

    def load_last_time(self, instance=None):
        # Check if filepath2 exists and read the last recorded time
        try:
            with open(self.filepath2, 'r') as file:
                lines = file.readlines()
                if lines:
                    # Get the last line and convert it to an integer
                    self.currenttimeseconds = int(lines[-1].strip())
                    print(f"Loaded time from file: {self.currenttimeseconds} seconds")
                else:
                    # File is empty, start from 0
                    self.currenttimeseconds = 0
                    print("File is empty. Starting from 0 seconds.")
        except FileNotFoundError:
            print("File not found. Starting from 0 seconds.")
            self.currenttimeseconds = 0
        except Exception as e:
            print(f"Failed to load time from file: {e}")
            self.currenttimeseconds = 0

        # Convert current time in seconds to "HH:MM:SS" format
        hours, remainder = divmod(self.currenttimeseconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.currenttime = f"{hours:02}:{minutes:02}:{seconds:02}"

        # Update the label with the formatted time
        if self.time_label:
            self.time_label.text = f"Current time: {self.currenttime}"
        print("Current time:", self.currenttime)

    def update_lines_position(self, *args):
        # Update the position and size of the center lines to keep them centered
        self.horizontal_line.pos = (0, self.main_layout.height / 2)
        self.horizontal_line.size = (self.main_layout.width, 1)
        self.vertical_line.pos = (self.main_layout.width / 2, 0)
        self.vertical_line.size = (1, self.main_layout.height)

    def on_upper_left_button_press(self, instance):
        # Print the matrices when the upper left button is pressed
        print("Tidstagningsskema0:", self.Tidstagningsskema0)
        print("Tidstagningsskema1:", self.Tidstagningsskema1)
        print("Tidstagningsskema2:", self.Tidstagningsskema2)
        print("Tidstagningsskema3:", self.Tidstagningsskema3)

    def show_popup(self):
        # Create two spinners for startAntalKamre and slutAntalKamre with numbers from 1 to 24
        self.start_spinner = Spinner(
            text='Select start', values=[str(i) for i in range(1, 25)],
            size_hint=(1, 0.3)
        )
        self.slut_spinner = Spinner(
            text='Select end', values=[str(i) for i in range(1, 25)],
            size_hint=(1, 0.3)
        )

        # Create a confirm button for the popup
        confirm_button = Button(text="Confirm", size_hint=(1, 0.3))
        
        # Layout for the popup content
        layout = BoxLayout(orientation="vertical")
        layout.add_widget(Label(text="Start chamber number:"))
        layout.add_widget(self.start_spinner)
        layout.add_widget(Label(text="End chamber number:"))
        layout.add_widget(self.slut_spinner)
        layout.add_widget(confirm_button)
        
        # Create a modal popup to prevent interaction with the background
        popup = Popup(title="Select number of first and last chamber", content=layout, size_hint=(0.5, 0.5), auto_dismiss=False)
        popup.background_color = (0, 0, 0, 1)
        
        # Bind the confirm button to validate and confirm selection
        confirm_button.bind(on_release=lambda *args: self.confirm_selection(popup))
        
        # Open the popup
        popup.open()

    def show_knapperpaamainscreen(self):
        # Loop through the list of widgets and add them back to the layout
        for widget in self.knapperpaamainscreen:
            if widget not in self.main_layout.children:
                self.main_layout.add_widget(widget)

    def confirm_selection(self, popup):
        try:
            # Convert the selected texts to integers
            self.startAntalKamre = int(self.start_spinner.text)
            self.slutAntalKamre = int(self.slut_spinner.text)
        except ValueError:
            # Handle the case where the values are not integers
            popup.title = "Please select start and end chamber"
            return  # Do nothing and exit the function

        # Check if the end value is greater than or equal to the start value
        if self.slutAntalKamre >= self.startAntalKamre:
            popup.dismiss()  # Close the popup

            # Generate four matrices with placeholders ("_") instead of empty strings
            self.Tidstagningsskema0 = [(i, "_", "_") for i in range(self.startAntalKamre, self.slutAntalKamre + 1)]
            self.Tidstagningsskema1 = [(i, "_", "_") for i in range(self.startAntalKamre, self.slutAntalKamre + 1)]
            self.Tidstagningsskema2 = [(i, "_", "_") for i in range(self.startAntalKamre, self.slutAntalKamre + 1)]
            self.Tidstagningsskema3 = [(i, "_", "_") for i in range(self.startAntalKamre, self.slutAntalKamre + 1)]

            # Get the current date and time for the filename
            current_date = datetime.now().strftime("%Y%m%d")
            current_time = datetime.now().strftime("%H%M%S")
            tidstagninghovedfil = f"{current_time}_{current_date}_{self.startAntalKamre}-{self.slutAntalKamre}.txt"

            # Set the file path based on the platform
            if platform == 'android':  # Assuming Android runs on Linux
                self.filepath1 = os.path.join('/sdcard/Documents', tidstagninghovedfil)
            else:
                self.filepath1 = os.path.join(os.path.expanduser("~"), tidstagninghovedfil)

            # Attempt to create the file
            try:
                with open(self.filepath1, 'w') as file:
                    file.write("")  # Create an empty file for now; data can be added later
                print(f"File created at {self.filepath1}")
            except Exception as e:
                print(f"Failed to create file: {e}")
            
            # Display Tidstagningsskema0 initially
            self.display_table(self.Tidstagningsskema0, matrix_index=0)
            self.show_knapperpaamainscreen()

        else:
            popup.title = "Error: End must be >= Start"

    def write_matrices_to_file(self, instance = None):
        # Open the file at filepath1 in write mode
        with open(self.filepath1, 'w') as file:
            file.write(f"Chamber/kammer: {self.startAntalKamre}-{self.slutAntalKamre} - Time at start: {self.timeatstart}\n")

            # Iterate through each matrix and write it to the file
            for i, matrix in enumerate([self.Tidstagningsskema0, self.Tidstagningsskema1, 
                                        self.Tidstagningsskema2, self.Tidstagningsskema3]):
                # Write the matrix header
                file.write(f"t{i}:\n")
                
                # Write each row in the matrix
                for row in matrix:
                    # Join each element in the row with a tab or space and write to the file
                    file.write('\t'.join(map(str, row)) + '\n')
                
                # Add a newline after each matrix for readability
                file.write('\n')

        print(f"Matrices written to {self.filepath1}")
    

    def display_table(self, matrix, matrix_index=0):
        # Define the buttons to exclude in a list
        excluded_buttons = [
                            self.upper_right_button,
                            self.starttid,
                            self.stoptid,
                            self.time_label,
                            self.gendanstateknap,
                            self.timeatstart_label,
                            self.udviklernavnmainscreen]

        # Loop through widgets and remove all except those in the excluded list
        for widget in self.main_layout.children[:]:
            if widget not in excluded_buttons:
                self.main_layout.remove_widget(widget)

        # Set current_matrix to track which table is being displayed
        self.current_matrix = matrix_index

        # Create a layout for the label and the buttons
        label_layout = FloatLayout(size_hint=(None, None), size=(dp(100), dp(40)))
        label_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.6}

        # Label to display above the table, indicating which matrix is shown
        matrix_label = Label(
            text=f"t{self.current_matrix}", 
            font_size=sp(24), 
            size_hint=(None, None),
            size=(dp(100), dp(40)),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )
        label_layout.add_widget(matrix_label)

        # Add navigation buttons based on the current matrix
        if self.current_matrix == 0:
            next_button = Button(text="Next", size_hint=(None, None), size=(dp(60), dp(40)))
            next_button.pos_hint = {'x': 0.7, 'y': 0.2}
            next_button.bind(on_release=lambda *args: self.display_table(self.Tidstagningsskema1, 1))
            label_layout.add_widget(next_button)

        elif self.current_matrix == 1:
            prev_button = Button(text="Prev", size_hint=(None, None), size=(dp(60), dp(40)))
            prev_button.pos_hint = {'x': -0.3, 'y': 0.2}
            prev_button.bind(on_release=lambda *args: self.display_table(self.Tidstagningsskema0, 0))
            label_layout.add_widget(prev_button)

            next_button = Button(text="Next", size_hint=(None, None), size=(dp(60), dp(40)))
            next_button.pos_hint = {'x': 0.7, 'y': 0.2}
            next_button.bind(on_release=lambda *args: self.display_table(self.Tidstagningsskema2, 2))
            label_layout.add_widget(next_button)

        elif self.current_matrix == 2:
            prev_button = Button(text="Prev", size_hint=(None, None), size=(dp(60), dp(40)))
            prev_button.pos_hint = {'x': -0.3, 'y': 0.2}
            prev_button.bind(on_release=lambda *args: self.display_table(self.Tidstagningsskema1, 1))
            label_layout.add_widget(prev_button)

            next_button = Button(text="Next", size_hint=(None, None), size=(dp(60), dp(40)))
            next_button.pos_hint = {'x': 0.7, 'y': 0.2}
            next_button.bind(on_release=lambda *args: self.display_table(self.Tidstagningsskema3, 3))
            label_layout.add_widget(next_button)

        elif self.current_matrix == 3:
            prev_button = Button(text="Prev", size_hint=(None, None), size=(dp(60), dp(40)))
            prev_button.pos_hint = {'x': -0.3, 'y': 0.2}
            prev_button.bind(on_release=lambda *args: self.display_table(self.Tidstagningsskema2, 2))
            label_layout.add_widget(prev_button)

        # Add the label layout to the main layout
        self.main_layout.add_widget(label_layout)

        # Create a ScrollView for the table
        scroll_view = ScrollView(size_hint=(None, 0.5), pos_hint={'center_x': 1.15, 'center_y': 0.3}, width=dp(800))

        # Define the total width for the grid based on the column widths
        grid_width = 800

        # Create a GridLayout for the table with three columns
        grid = GridLayout(cols=3, spacing=[dp(20), dp(10)], size_hint_y=None, width=dp(grid_width))
        grid.bind(minimum_height=grid.setter('height'))

        # Add the headers
        grid.add_widget(Label(text="Chamber", size_hint=(None, None), height=dp(30), width=dp(80)))
        grid.add_widget(Label(text="Time", size_hint=(None, None), height=dp(30), width=dp(100)))
        grid.add_widget(Label(text="Comment", size_hint=(None, None), height=dp(30), width=dp(100)))

        # Populate the grid with rows from the selected matrix
        for i, row in enumerate(matrix):
            chamber_label = Label(text=str(row[0]), size_hint=(None, None), height=dp(30), width=dp(80))
            grid.add_widget(chamber_label)

            time_entry = row[1] if len(row) > 1 else ""
            time_button = Button(text=str(time_entry), size_hint=(None, None), height=dp(30), width=dp(100))
            time_button.bind(on_release=lambda btn, m=matrix, idx=i: self.delete_entry(m, idx))
            grid.add_widget(time_button)

            additional_entry = row[2] if len(row) > 2 else ""
            additional_button = Button(text=str(additional_entry), size_hint=(None, None), height=dp(30), width=dp(100))
            # Bind the additional button to the popup method
            additional_button.bind(on_release=lambda btn, idx=i: self.show_textinput(idx))
            grid.add_widget(additional_button)

        # Add the grid to the ScrollView
        scroll_view.add_widget(grid)
        self.main_layout.add_widget(scroll_view)

        # Set the scroll position based on populated_ratio
        scroll_view.scroll_y = 1 - self.populated_ratio

    def show_textinput(self, row_index):
        # Create a TextInput for user input
        text_input = TextInput(hint_text="Enter additional information", size_hint=(1, 0.3))
        
        # Create a confirm button for the popup
        confirm_button = Button(text="Confirm", size_hint=(1, 0.3))

        # Layout for the popup content
        layout = BoxLayout(orientation="vertical")
        layout.add_widget(text_input)
        layout.add_widget(confirm_button)
        
        # Create a modal popup to prevent interaction with the background
        popup = Popup(title="Add Additional Entry", content=layout, size_hint=(0.5, 0.5), auto_dismiss=False)
        popup.background_color = (0, 0, 0, 1)

        # Bind the confirm button to update the matrix entry and dismiss the popup
        confirm_button.bind(on_release=lambda *args: self.confirm_additional_entry(row_index, text_input.text, popup))
        
        # Open the popup
        popup.open()

    def confirm_additional_entry(self, row_index, text, popup):
        # Update the corresponding entry in the current matrix at index 2
        matrix = [self.Tidstagningsskema0, self.Tidstagningsskema1, self.Tidstagningsskema2, self.Tidstagningsskema3][self.current_matrix]
        matrix[row_index] = (matrix[row_index][0], matrix[row_index][1], text)  # Update index 2 with the input text
        
        popup.dismiss()  # Close the popup

        self.write_matrices_to_file()
        self.write_raw_matrices_to_file()

        # Refresh the display
        self.display_table(matrix, matrix_index=self.current_matrix)

    def delete_entry(self, matrix, index):
        def proceed_with_deletion(*args):
            # Close the popup and proceed with deletion
            popup.dismiss()

            # Set the second element to "_" while keeping the tuple size consistent
            matrix[index] = (matrix[index][0], "_", matrix[index][2])

            # Find the first occurrence of "_" in index 1 and set populated_count to its row number
            populated_count = next((i for i, row in enumerate(matrix) if row[1] == "_"), None)

            # If no empty entry is found, set populated_count to the total number of rows
            populated_count = populated_count if populated_count is not None else len(matrix)

            total_chambers = self.slutAntalKamre - self.startAntalKamre + 1
            self.populated_ratio = populated_count / total_chambers if total_chambers > 0 else 0
            print("Populated Ratio after deletion:", self.populated_ratio)  # Print the ratio for debugging

            self.write_matrices_to_file()
            self.write_raw_matrices_to_file()

            # Refresh the table display
            self.display_table(matrix, matrix_index=self.current_matrix)

        def cancel_deletion(*args):
            # Close the popup and exit the function
            popup.dismiss()

        # Get the chamber number or entry index for the title
        entry_number = matrix[index][0]  # Assuming the first element in the tuple is the chamber number

        # Create the popup content
        popup_content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        popup_content.add_widget(Label(text="Are you sure you want to delete this entry?", halign="center", valign="middle"))

        # Add "Yes" and "No" buttons with customized sizes
        button_layout = BoxLayout(orientation='horizontal', spacing=10)
        yes_button = Button(text="Yes", size_hint=(0.3, 1), background_color=(0, 1, 0, 1), on_press=proceed_with_deletion)  # Smaller button
        no_button = Button(text="No", size_hint=(0.7, 1), background_color=(1, 0, 0, 1), on_press=cancel_deletion)  # Larger button
        button_layout.add_widget(no_button)
        button_layout.add_widget(yes_button)

        popup_content.add_widget(button_layout)

        # Create and display the popup with the dynamic title
        popup = Popup(
            title=f"Confirm deletion of time for chamber {entry_number}",
            content=popup_content,
            size_hint=(0.8, 0.4),
            auto_dismiss=False  # Prevent the popup from closing without user input
        )
        popup.open()


    def add_recorded_time(self, instance):
        # List of matrices to iterate through
        matrices = [self.Tidstagningsskema0, self.Tidstagningsskema1, self.Tidstagningsskema2, self.Tidstagningsskema3]

        for matrix in matrices:
            for i, entry in enumerate(matrix):
                # Check if the second column (index 1) is the placeholder ("_"), indicating it's empty
                if entry[1] == "_":  # This condition checks for the empty entry
                    # Append current time in seconds instead of "recorded time"
                    matrix[i] = (entry[0], str(self.currenttime), entry[2])
                    
                    # Calculate the populated ratio
                    populated_count = sum(1 for row in matrix if row[1] != "_")  # Count non-placeholder entries
                    total_chambers = self.slutAntalKamre - self.startAntalKamre + 1
                    self.populated_ratio = populated_count / total_chambers if total_chambers > 0 else 0

                    # Refresh the table display after updating the entry
                    self.display_table(matrices[self.current_matrix], matrix_index=self.current_matrix)
                    print("Populated Ratio after adding:", self.populated_ratio)  # Print the ratio for debugging
                    return  # Exit after filling the first available spot
    
        # If all matrices are fully populated, display a message or handle as needed
        print("All matrices are fully populated with the current time")

    def createsavelastmatrixstatefile(self, instance):
            # Set the file path based on the platform
            if platform == 'android':  # Assuming Android runs on Linux
                self.filepath3 = os.path.join('/sdcard/Documents', "laststateskema.txt")
            else:
                self.filepath3 = os.path.join(os.path.expanduser("~"), "laststateskema.txt")

            # Attempt to create the file
            try:
                with open(self.filepath3, 'w') as file:
                    file.write("")  # Create an empty file for now; data can be added later
                print(f"File created at {self.filepath1}")
            except Exception as e:
                print(f"Failed to create file: {e}")

    def write_raw_matrices_to_file(self, instance=None):
        # Open the file at filepath3 in write mode
        with open(self.filepath3, 'w') as file:
            # Iterate through each matrix and write it to the file
            for matrix in [self.Tidstagningsskema0, self.Tidstagningsskema1, 
                        self.Tidstagningsskema2, self.Tidstagningsskema3]:
                # Write each matrix on its own line
                file.write(str(matrix) + '\n')

        print(f"Matrices written on separate lines to {self.filepath3}")

    def read_matrices_from_file(self, instance=None):
            # Set the file path based on the platform
        if platform == 'android':  # Assuming Android runs on Linux
            self.filepath3 = os.path.join('/sdcard/Documents', "laststateskema.txt")
        else:
            self.filepath3 = os.path.join(os.path.expanduser("~"), "laststateskema.txt")
       
        # Open the file at filepath3 in read mode
        with open(self.filepath3, 'r') as file:
            # Read each line and set each matrix variable accordingly
            lines = file.readlines()
            if len(lines) > 0:
                self.Tidstagningsskema0 = ast.literal_eval(lines[0].strip())
            if len(lines) > 1:
                self.Tidstagningsskema1 = ast.literal_eval(lines[1].strip())
            if len(lines) > 2:
                self.Tidstagningsskema2 = ast.literal_eval(lines[2].strip())
            if len(lines) > 3:
                self.Tidstagningsskema3 = ast.literal_eval(lines[3].strip())

        print(f"Matrices loaded from {self.filepath3}")

if __name__ == '__main__':
    TidstagningMJGApp().run()
