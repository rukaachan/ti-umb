import toga
from toga import App, MainWindow, Box, Label, Selection, NumberInput, Button, Table, Divider, ConfirmDialog, InfoDialog, ImageView, Image
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, LEFT, RIGHT, CENTER, BOLD, TOP
from toga.colors import WHITE, BLACK, GRAY

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
SMELL_IMAGE_NAME = "ruka.jpg"
COFFEE_IMAGE_NAME = "ruka.jpg"
REST_IMAGE_NAME = "ruka.jpg"
DEFAULT_IMAGE_NAME = "ruka.jpg"

# --- Style Constants - iOS Calculator Light Theme ---
COLOR_BACKGROUND = '#F5F5F5'
COLOR_INPUT_AREA_BG = '#E0E0E0'
COLOR_FUNC_BUTTON_BG = '#BDBDBD'
# FIX: Define Orange using its hex code
COLOR_ACTION_BUTTON_BG = '#FFA500'
COLOR_ACTION_BUTTON_TEXT = WHITE
COLOR_FUNC_BUTTON_TEXT = BLACK
COLOR_TEXT_PRIMARY = BLACK
COLOR_DIVIDER = '#CCCCCC'

MARGIN_LARGE = 15
MARGIN_MEDIUM = 10
MARGIN_SMALL = 5
MARGIN_AROUND_BUTTON = MARGIN_SMALL

class SocialEnergyCalculator(toga.App):

    def startup(self):
        """Construct and show the Toga application with emojis and mood image."""
        self.activity_points = DEFAULT_ACTIVITY_POINTS.copy()
        self.all_activities = []

        # --- Main Container ---
        main_box = Box(
            style=Pack(
                direction=COLUMN,
                margin=MARGIN_LARGE, # Use margin
                background_color=COLOR_BACKGROUND
            )
        )

        # --- 1. Input Section ---
        input_section_box = Box(
            style=Pack(
                direction=COLUMN,
                background_color=COLOR_INPUT_AREA_BG,
                margin=MARGIN_MEDIUM # Use margin
            )
        )
        input_section_title = Label(
            "📝 Log New Activity",
            style=Pack(font_weight=BOLD, margin_bottom=MARGIN_MEDIUM, color=COLOR_TEXT_PRIMARY) # Use margin_bottom
        )

        # Activity Type Row
        activity_row = Box(style=Pack(direction=ROW, margin_bottom=MARGIN_SMALL, align_items=CENTER)) # Use margin_bottom, align_items
        activity_label = Label(
            "Activity:",
            style=Pack(margin_right=MARGIN_SMALL, text_align=RIGHT, color=COLOR_TEXT_PRIMARY) # Use margin_right
        )
        self.activity_selection = Selection(
            items=list(self.activity_points.keys()),
            style=Pack(flex=1)
        )
        activity_row.add(activity_label)
        activity_row.add(self.activity_selection)

        # Duration Row
        duration_row = Box(style=Pack(direction=ROW, margin_bottom=MARGIN_MEDIUM, align_items=CENTER)) # Use margin_bottom, align_items
        duration_label = Label(
            "⏰ Duration:",
            style=Pack(margin_right=MARGIN_SMALL, text_align=RIGHT, color=COLOR_TEXT_PRIMARY) # Use margin_right
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
        button_row = Box(style=Pack(direction=ROW, align_items=CENTER, margin_top=MARGIN_SMALL)) # Use align_items, margin_top
        add_button = Button(
            "➕ Add Activity",
            on_press=self.add_activity,
            style=Pack(
                margin=MARGIN_AROUND_BUTTON, # Use margin for space around button
                background_color=COLOR_ACTION_BUTTON_BG, # Uses the hex code now
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
            style=Pack(margin_top=MARGIN_LARGE, margin_bottom=MARGIN_MEDIUM, color=COLOR_DIVIDER) # Use margin_*
        )

        # --- 2. Log and Totals Section ---
        log_totals_outer_box = Box(style=Pack(direction=ROW, flex=1, margin_bottom=MARGIN_MEDIUM)) # Use margin_bottom

        # 2a. Today's Log Sub-section
        log_box = Box(style=Pack(direction=COLUMN, flex=3, margin_right=MARGIN_MEDIUM)) # Use margin_right
        log_title = Label(
            "📅 Today's Energy Log",
            style=Pack(font_weight=BOLD, margin_bottom=MARGIN_SMALL, color=COLOR_TEXT_PRIMARY) # Use margin_bottom
        )
        self.activity_table = Table(
            headings=["Activity Type", "Duration (hr)", "Energy Points"],
            missing_value="-",
            style=Pack(flex=1)
        )
        log_box.add(log_title)
        log_box.add(self.activity_table)

        # 2b. Totals and Image Sub-section
        totals_image_box = Box(style=Pack(direction=COLUMN, flex=1, align_items=CENTER)) # Use align_items

        # Totals Title and Label
        totals_title = Label(
            "⚡️ Energy Balance",
            style=Pack(font_weight=BOLD, margin_bottom=MARGIN_SMALL, color=COLOR_TEXT_PRIMARY, text_align=CENTER) # Use margin_bottom
        )
        self.daily_total_label = Label(
            "Daily: +0.00",
            style=Pack(font_weight=BOLD, font_size=14, color=COLOR_TEXT_PRIMARY, text_align=CENTER, margin_bottom=MARGIN_MEDIUM) # Use margin_bottom
        )

        # Mood Image View
        mood_image_title = Label(
            "😊 Mood:",
             style=Pack(font_weight=BOLD, margin_bottom=MARGIN_SMALL, color=COLOR_TEXT_PRIMARY, text_align=CENTER) # Use margin_bottom
        )
        self.mood_image_view = ImageView(
            style=Pack(width=100, height=100, align_items=CENTER) # align_items might be needed here for centering within column
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
            style=Pack(margin_top=MARGIN_MEDIUM, margin_bottom=MARGIN_MEDIUM, color=COLOR_DIVIDER) # Use margin_*
        )

        # --- 3. Controls Section ---
        controls_box = Box(style=Pack(direction=ROW, align_items=CENTER)) # Use align_items
        clear_today_button = Button(
            "🗑️ Clear Today",
            on_press=self.clear_today,
            style=Pack(
                margin=MARGIN_AROUND_BUTTON, # Use margin for space around button
                background_color=COLOR_FUNC_BUTTON_BG,
                color=COLOR_FUNC_BUTTON_TEXT,
                font_weight=BOLD
            )
        )
        controls_box.add(clear_today_button)

        # --- Assemble Main Layout ---
        main_box.add(input_section_box)
        main_box.add(divider1)
        main_box.add(log_totals_outer_box)
        main_box.add(divider2)
        main_box.add(controls_box)

        # --- Main Window Setup ---
        self.main_window = MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

        # --- Load Data and Initial Display ---
        self.all_activities = self.load_data()
        self.update_display()

    # --- Action Handlers ---
    # (add_activity logic remains the same)
    def add_activity(self, widget):
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

    # (update_display logic remains the same)
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
        target_image_name = DEFAULT_IMAGE_NAME

        if 71 <= daily_total <= 100:
            target_image_name = SMELL_IMAGE_NAME
        elif 31 <= daily_total <= 70:
            target_image_name = COFFEE_IMAGE_NAME
        elif 0 <= daily_total <= 30:
            target_image_name = REST_IMAGE_NAME

        try:
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

            if hasattr(self, 'mood_image_view'):
                 self.mood_image_view.image = loaded_image
            else:
                 print("Error: self.mood_image_view widget not found during update.")

        except AttributeError:
             print("Error: self.paths.app not available yet. Cannot determine image resource path.")
             if hasattr(self, 'mood_image_view'): self.mood_image_view.image = None
        except FileNotFoundError:
             print(f"Error: Image file not found at expected location (tried {image_path}).")
             if hasattr(self, 'mood_image_view'): self.mood_image_view.image = None
        except Exception as e:
            print(f"Error loading or setting image: {e}")
            if hasattr(self, 'mood_image_view'): self.mood_image_view.image = None

    # (clear_today logic remains the same)
    async def clear_today(self, widget):
        """Removes all activity entries for the current day using async dialog."""
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
    # (show_info_dialog logic remains the same)
    def show_info_dialog(self, title, message):
        if hasattr(self, 'main_window') and self.main_window:
            self.main_window.info_dialog(title, message)
        else:
            print(f"INFO: {title} - {message}")

    # (show_error_dialog logic remains the same)
    def show_error_dialog(self, title, message):
        if hasattr(self, 'main_window') and self.main_window:
             self.main_window.error_dialog(title, message)
        else:
             print(f"ERROR: {title} - {message}")

    # --- Data Persistence ---
    # (data_path logic remains the same)
    @property
    def data_path(self) -> Path:
        if hasattr(self, 'paths') and self.paths:
             return self.paths.data / DATA_FILE
        else:
             print("Warning: self.paths not available. Using fallback path for data.")
             return Path(".") / DATA_FILE

    # (load_data logic remains the same)
    def load_data(self):
        data_file_path = self.data_path
        try:
            if data_file_path.exists():
                with data_file_path.open("r", encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list): return data
                    else:
                        print(f"Warning: Data file '{data_file_path}' format incorrect.")
                        return []
            else: return []
        except (IOError, json.JSONDecodeError, Exception) as e:
            print(f"Error loading data file '{data_file_path}': {e}. Starting empty.")
            return []

    # (save_data logic remains the same)
    def save_data(self):
        data_file_path = self.data_path
        try:
            data_file_path.parent.mkdir(parents=True, exist_ok=True)
            with data_file_path.open("w", encoding='utf-8') as f:
                json.dump(self.all_activities, f, indent=4)
        except (IOError, TypeError, Exception) as e:
            print(f"Error saving data file '{data_file_path}': {e}")
            self.show_error_dialog("Save Error", f"Could not save data:\n{e}")

# --- Main Entry Point ---
def main():
    return SocialEnergyCalculator()