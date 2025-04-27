import toga
# Import necessary UI elements and styling tools
# Added ImageView
from toga import App, MainWindow, Box, Label, Selection, NumberInput, Button, Table, Divider, ConfirmDialog, InfoDialog, ImageView, Image
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, LEFT, RIGHT, CENTER, BOLD, TOP # Added TOP
# Import color definitions or define hex codes
from toga.colors import WHITE, BLACK, GRAY, ORANGE # Basic colors

from datetime import date, timedelta
import json
from pathlib import Path
import warnings

# --- Configuration ---
DEFAULT_ACTIVITY_POINTS = {
    "Work Meeting": -10,
    "Focused Work (Solo)": -5,
    "Casual Chat (Colleague)": -2,
    "Hanging out (Friends)": 8,
    "Deep Conversation (Friend/Partner)": 5,
    "Family Call": 3,
    "Family Gathering": -8,
    "Alone Time (Relaxing)": 10,
    "Alone Time (Productive/Hobby)": 7,
    "Errands/Commute": -4,
    "Large Social Event": -15,
    "Exercise (Group)": 2,
    "Exercise (Solo)": 6,
}
DATA_FILE = "social_energy_data.json"

# --- Resource Paths ---
SMELL_IMAGE_NAME = "smile-ruka.jpg"
COFFEE_IMAGE_NAME = "smile-ruka.jpg"
REST_IMAGE_NAME = "smile-ruka.jpg"
DEFAULT_IMAGE_NAME = "smile-ruka.jpg"

# --- Style Constants - iOS Calculator Light Theme ---
COLOR_BACKGROUND = '#F5F5F5'       # Very light gray background
COLOR_INPUT_AREA_BG = '#E0E0E0'  # Medium-light gray for input section background
COLOR_FUNC_BUTTON_BG = '#BDBDBD' # Darker gray for function buttons (like Clear)
COLOR_ACTION_BUTTON_BG = ORANGE  # Orange for the primary action button (Add)
COLOR_ACTION_BUTTON_TEXT = WHITE # White text for the action button
COLOR_FUNC_BUTTON_TEXT = BLACK   # Black text for function buttons
COLOR_TEXT_PRIMARY = BLACK       # Black for most text labels and totals
COLOR_DIVIDER = '#CCCCCC'        # Light gray for dividers

PADDING_LARGE = 15
PADDING_MEDIUM = 10
PADDING_SMALL = 5
PADDING_INSIDE_BUTTON = (8, 15) # Vertical, Horizontal padding inside buttons


class SocialEnergyCalculator(toga.App):

    def startup(self):
        """Construct and show the Toga application with dynamic mood image."""
        self.activity_points = DEFAULT_ACTIVITY_POINTS.copy()
        self.all_activities = []

        # --- Main Container ---
        main_box = Box(
            style=Pack(
                direction=COLUMN,
                padding=PADDING_LARGE,
                background_color=COLOR_BACKGROUND # Apply main background color
            )
        )

        # --- 1. Input Section ---
        input_section_box = Box(
            style=Pack(
                direction=COLUMN,
                background_color=COLOR_INPUT_AREA_BG, # iOS darker gray area
                padding=PADDING_MEDIUM
            )
        )
        input_section_title = Label(
            "Log New Activity",
            style=Pack(font_weight=BOLD, padding_bottom=PADDING_MEDIUM, color=COLOR_TEXT_PRIMARY)
        )

        # Activity Type Row
        activity_row = Box(style=Pack(direction=ROW, padding_bottom=PADDING_SMALL, alignment=CENTER))
        activity_label = Label(
            "Activity:", # Shorter label
            style=Pack(width=80, padding_right=PADDING_SMALL, text_align=RIGHT, color=COLOR_TEXT_PRIMARY)
        )
        self.activity_selection = Selection(
            items=list(self.activity_points.keys()),
            style=Pack(flex=1)
        )
        activity_row.add(activity_label)
        activity_row.add(self.activity_selection)

        # Duration Row
        duration_row = Box(style=Pack(direction=ROW, padding_bottom=PADDING_MEDIUM, alignment=CENTER))
        duration_label = Label(
            "Duration:", # Shorter label
            style=Pack(width=80, padding_right=PADDING_SMALL, text_align=RIGHT, color=COLOR_TEXT_PRIMARY)
        )
        self.duration_input = NumberInput(
            min=0.1,
            step=0.25,
            value=1.0,
            style=Pack(flex=1)
        )
        duration_row.add(duration_label)
        duration_row.add(self.duration_input)

        # Add Button (Orange)
        button_row = Box(style=Pack(direction=ROW, alignment=CENTER, padding_top=PADDING_SMALL))
        add_button = Button(
            "Add Activity",
            on_press=self.add_activity,
            style=Pack(
                padding=PADDING_INSIDE_BUTTON,
                background_color=COLOR_ACTION_BUTTON_BG,
                color=COLOR_ACTION_BUTTON_TEXT,
                font_weight=BOLD
            )
        )
        button_row.add(add_button)

        # Assemble Input Section
        input_section_box.add(input_section_title)
        input_section_box.add(activity_row)
        input_section_box.add(duration_row)
        input_section_box.add(button_row)

        # --- Divider ---
        divider1 = Divider(
            direction=Divider.HORIZONTAL,
            style=Pack(padding_top=PADDING_LARGE, padding_bottom=PADDING_MEDIUM, color=COLOR_DIVIDER)
        )

        # --- 2. Log and Totals Section ---
        # Use ROW to put Log Table and Totals/Image side-by-side if window is wide enough
        # Or keep COLUMN if preferred vertical stacking
        # Let's try ROW for potential side-by-side layout
        log_totals_outer_box = Box(style=Pack(direction=ROW, flex=1, padding_bottom=PADDING_MEDIUM))

        # 2a. Today's Log Sub-section (Takes most space)
        log_box = Box(style=Pack(direction=COLUMN, flex=3, padding_right=PADDING_MEDIUM)) # Give more flex space
        log_title = Label(
            "Today's Energy Log",
            style=Pack(font_weight=BOLD, padding_bottom=PADDING_SMALL, color=COLOR_TEXT_PRIMARY)
        )
        self.activity_table = Table(
            headings=["Activity Type", "Duration (hr)", "Energy Points"],
            missing_value="-",
            style=Pack(flex=1) # Table takes available vertical space in this box
        )
        log_box.add(log_title)
        log_box.add(self.activity_table)

        # 2b. Totals and Image Sub-section (Smaller part)
        totals_image_box = Box(style=Pack(direction=COLUMN, flex=1, alignment=CENTER)) # Center items vertically

        # Totals Title and Label
        totals_title = Label(
            "Energy Balance",
            style=Pack(font_weight=BOLD, padding_bottom=PADDING_SMALL, color=COLOR_TEXT_PRIMARY, text_align=CENTER)
        )
        self.daily_total_label = Label(
            "Daily: +0.00",
            style=Pack(font_weight=BOLD, font_size=14, color=COLOR_TEXT_PRIMARY, text_align=CENTER, padding_bottom=PADDING_MEDIUM)
        )
        # REMOVED: self.weekly_total_label creation

        # Mood Image View
        mood_image_title = Label(
            "Mood:",
             style=Pack(font_weight=BOLD, padding_bottom=PADDING_SMALL, color=COLOR_TEXT_PRIMARY, text_align=CENTER)
        )
        # Create the ImageView, initially empty or with default
        self.mood_image_view = ImageView(
            # Load default image during startup if possible, else handle in update_display
            # image=None, # Start empty
            style=Pack(width=100, height=100, alignment=CENTER) # Fixed size for the image view
        )

        # Assemble Totals and Image Box
        totals_image_box.add(totals_title)
        totals_image_box.add(self.daily_total_label)
        totals_image_box.add(mood_image_title)
        totals_image_box.add(self.mood_image_view)

        # Assemble Log and Totals Outer Box
        log_totals_outer_box.add(log_box)
        log_totals_outer_box.add(totals_image_box)


        # --- Divider ---
        divider2 = Divider(
            direction=Divider.HORIZONTAL,
            style=Pack(padding_top=PADDING_MEDIUM, padding_bottom=PADDING_MEDIUM, color=COLOR_DIVIDER)
        )

        # --- 3. Controls Section ---
        controls_box = Box(style=Pack(direction=ROW, alignment=CENTER)) # Center controls
        clear_today_button = Button(
            "Clear Today",
            on_press=self.clear_today,
            style=Pack(
                padding=PADDING_INSIDE_BUTTON,
                background_color=COLOR_FUNC_BUTTON_BG,
                color=COLOR_FUNC_BUTTON_TEXT,
                font_weight=BOLD
            )
        )
        controls_box.add(clear_today_button)

        # --- Assemble Main Layout ---
        main_box.add(input_section_box)
        main_box.add(divider1)
        main_box.add(log_totals_outer_box) # Add the box containing log and totals/image
        main_box.add(divider2)
        main_box.add(controls_box)

        # --- Main Window Setup ---
        self.main_window = MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

        # --- Load Data and Initial Display ---
        self.all_activities = self.load_data()
        self.update_display() # This will now also set the initial image

    # --- Action Handlers ---

    def add_activity(self, widget):
        # (Logic unchanged from previous version)
        try:
            activity_type = self.activity_selection.value
            duration_str = self.duration_input.value
            duration = float(duration_str) if duration_str is not None else 0.0

            if not activity_type:
                self.show_info_dialog("Selection Error", "Please select an activity type.")
                return
            if duration <= 0:
                self.show_info_dialog("Input Error", "Duration must be a positive number.")
                return

            points_per_hour = self.activity_points.get(activity_type, 0)
            calculated_points = round(duration * points_per_hour, 2)
            today_str = date.today().isoformat()
            new_activity = {"date": today_str, "type": activity_type, "duration": duration, "points": calculated_points}

            self.all_activities.append(new_activity)
            self.save_data()
            self.update_display()
            self.duration_input.value = 1.0

        except ValueError:
             self.show_error_dialog("Input Error", f"Invalid duration entered: '{duration_str}'. Please enter a number.")
        except Exception as e:
            print(f"An unexpected error occurred in add_activity: {e}")
            self.show_error_dialog("Error", f"An unexpected error occurred: {e}")

    def update_display(self):
        """Updates table, daily total label, and mood image."""
        today = date.today()
        today_str = today.isoformat()
        todays_table_data = []
        daily_total = 0.0

        # Calculate Daily Total
        for activity in self.all_activities:
            if activity.get("date") == today_str:
                duration = activity.get('duration', 0.0)
                points = activity.get('points', 0.0)
                todays_table_data.append({
                    "activity_type": activity.get("type", "N/A"),
                    "duration_hr": f"{float(duration):.2f}",
                    "energy_points": f"{float(points):+.2f}",
                })
                daily_total += float(points)

        # Update Table
        try:
            self.activity_table.data = todays_table_data
        except Exception as e:
             print(f"Error updating table data: {e}")
             self.activity_table.data = []

        # Update Daily Total Label
        self.daily_total_label.text = f"Daily: {daily_total:+.2f}"
        self.daily_total_label.style.update(color=COLOR_TEXT_PRIMARY)

        # Determine and Update Mood Image
        target_image_name = DEFAULT_IMAGE_NAME # Default image filename

        if 71 <= daily_total <= 100:
            target_image_name = SMELL_IMAGE_NAME
        elif 31 <= daily_total <= 70:
            target_image_name = COFFEE_IMAGE_NAME
        elif 0 <= daily_total <= 30:
            target_image_name = REST_IMAGE_NAME
        # else: handles < 0 or > 100 by keeping DEFAULT_IMAGE_NAME

        try:
            # Construct path relative to the app's source code directory
            # self.paths.app should point to the src/socialenergycalc directory
            base_path = self.paths.app
            image_path = base_path / "resources" / target_image_name
            default_path = base_path / "resources" / DEFAULT_IMAGE_NAME

            loaded_image = None
            if image_path.exists():
                loaded_image = toga.Image(image_path)
            elif default_path.exists():
                 print(f"Warning: Image not found at {image_path}. Using default.")
                 loaded_image = toga.Image(default_path)
            else:
                 print(f"Warning: Target image and default image not found ({image_path}, {default_path}). Clearing image.")
                 # loaded_image remains None

            # Update the ImageView widget (ensure it exists)
            if hasattr(self, 'mood_image_view'):
                 self.mood_image_view.image = loaded_image
            else:
                 print("Error: self.mood_image_view widget not found during update.")

        except AttributeError:
             print("Error: self.paths.app not available yet. Cannot determine image resource path.")
             if hasattr(self, 'mood_image_view'):
                 self.mood_image_view.image = None # Clear image if path fails
        except FileNotFoundError:
             print(f"Error: Image file not found at expected location (tried {image_path}).")
             if hasattr(self, 'mood_image_view'):
                 self.mood_image_view.image = None # Clear image if file not found
        except Exception as e:
            print(f"Error loading or setting image: {e}")
            if hasattr(self, 'mood_image_view'):
                self.mood_image_view.image = None # Clear image on other errors


    async def clear_today(self, widget):
        """Removes all activity entries for the current day using async dialog."""
        # (Logic unchanged from previous version)
        today_str = date.today().isoformat()
        initial_activities = list(self.all_activities)
        filtered_activities = [act for act in self.all_activities if act.get("date") != today_str]

        if len(filtered_activities) < len(initial_activities):
            confirm = ConfirmDialog("Confirm Clear", "Clear all entries for today?")
            result = await self.main_window.dialog(confirm)
            if result:
                self.all_activities = filtered_activities
                self.save_data()
                self.update_display()
        else:
            self.show_info_dialog("No Entries", "There are no entries logged for today.")

    # --- Helper methods for Dialogs ---
    def show_info_dialog(self, title, message):
        # (Logic unchanged from previous version)
        if hasattr(self, 'main_window') and self.main_window:
            self.main_window.info_dialog(title, message)
        else:
            print(f"INFO: {title} - {message}")

    def show_error_dialog(self, title, message):
        # (Logic unchanged from previous version)
        if hasattr(self, 'main_window') and self.main_window:
             self.main_window.error_dialog(title, message)
        else:
             print(f"ERROR: {title} - {message}")


    # --- Data Persistence ---
    @property
    def data_path(self) -> Path:
        # Use app data path for persistence
        if hasattr(self, 'paths') and self.paths:
             # Use paths.data for user-specific writable data
             return self.paths.data / DATA_FILE
        else:
             print("Warning: self.paths not available. Using fallback path for data.")
             # Fallback to current directory ONLY for dev convenience, not ideal for deployment
             return Path(".") / DATA_FILE

    def load_data(self):
        # (Logic mostly unchanged, ensure directory exists)
        data_file_path = self.data_path
        try:
            if data_file_path.exists():
                # No need to create parent dir here, loading assumes it might exist
                with data_file_path.open("r", encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list): return data
                    else:
                        print(f"Warning: Data file '{data_file_path}' format incorrect.")
                        return []
            else: return [] # File doesn't exist, return empty list
        except (IOError, json.JSONDecodeError, Exception) as e:
            print(f"Error loading data file '{data_file_path}': {e}. Starting empty.")
            # Avoid showing dialog during initial load if window isn't ready
            # self.show_error_dialog("Load Error", f"Could not load data file:\n{e}")
            return []

    def save_data(self):
        # (Logic mostly unchanged, ensure directory exists)
        data_file_path = self.data_path
        try:
            # Ensure the directory exists before writing
            data_file_path.parent.mkdir(parents=True, exist_ok=True)
            with data_file_path.open("w", encoding='utf-8') as f:
                json.dump(self.all_activities, f, indent=4)
        except (IOError, TypeError, Exception) as e:
            print(f"Error saving data file '{data_file_path}': {e}")
            self.show_error_dialog("Save Error", f"Could not save data:\n{e}")

def main():
    return SocialEnergyCalculator()