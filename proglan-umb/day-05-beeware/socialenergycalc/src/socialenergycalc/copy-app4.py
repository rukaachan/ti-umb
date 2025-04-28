import toga
# Import necessary UI elements and styling tools
from toga import MainWindow, Box, Label, Selection, TextInput, Button, Table, Divider, ConfirmDialog,ImageView
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, RIGHT, CENTER, BOLD
# Import color definitions or define hex codes
from toga.colors import WHITE, BLACK, RED

from datetime import date
import json
from pathlib import Path
import traceback # For detailed error logging

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
DATA_FILE = "social_energy_state.json"
BASE_ENERGY = 100.0

# --- Resource Paths ---
EXCITED_GIF_NAME = "excited.gif" # 81+
STABLE_GIF_NAME = "stable.gif"   # 80-51
TIRED_GIF_NAME = "tired.gif"     # 50-21
SAD_GIF_NAME = "sad.gif"         # 20 or less (including negative)
DEFAULT_GIF_NAME = "neutral.gif" # Fallback/Default

# --- Style Constants ---
COLOR_BACKGROUND = '#F5F5F5'
COLOR_INPUT_AREA_BG = '#E0E0E0'
COLOR_FUNC_BUTTON_BG = RED
COLOR_ACTION_BUTTON_BG = '#FFA500'
COLOR_ACTION_BUTTON_TEXT = WHITE
COLOR_FUNC_BUTTON_TEXT = WHITE
COLOR_TEXT_PRIMARY = BLACK
COLOR_TEXT_LOG = "#4061A0"
COLOR_ENERGY_BALANCE= "#FFBF00"
COLOR_TEXT_MOOD="#FF69B4"
COLOR_DIVIDER = '#CCCCCC'

PADDING_LARGE = 15
PADDING_MEDIUM = 10
PADDING_SMALL = 5
PADDING_AROUND_BUTTON = PADDING_SMALL

class SocialEnergyCalculator(toga.App):

    def startup(self):
        """Construct and show the Toga application with persistent energy balance."""
        # warnings.filterwarnings("ignore", category=DeprecationWarning, module="travertino")

        self.activity_points = DEFAULT_ACTIVITY_POINTS.copy()
        self.current_balance = BASE_ENERGY
        self.all_activities = []
        self.load_data()

        # --- Main Container ---
        main_box = Box(
            style=Pack(direction=COLUMN, padding=PADDING_LARGE, background_color=COLOR_BACKGROUND)
        )

        # --- 1. Input Section ---
        input_section_box = Box(
            style=Pack(direction=COLUMN, background_color=COLOR_INPUT_AREA_BG, padding=PADDING_MEDIUM)
        )
        input_section_title = Label("📝 Log New Activity", style=Pack(font_weight=BOLD, padding_bottom=PADDING_MEDIUM, color=COLOR_TEXT_LOG))

        activity_row = Box(style=Pack(direction=ROW, padding_bottom=PADDING_SMALL, alignment=CENTER))
        activity_label = Label("📋 Activity:", style=Pack(padding_right=PADDING_SMALL, text_align=RIGHT, color=COLOR_TEXT_PRIMARY))
        self.activity_selection = Selection(items=list(self.activity_points.keys()), style=Pack(flex=1))
        activity_row.add(activity_label)
        activity_row.add(self.activity_selection)

        duration_row = Box(style=Pack(direction=ROW, padding_bottom=PADDING_MEDIUM, alignment=CENTER))
        duration_label = Label("⏰ Duration:", style=Pack(padding_right=PADDING_SMALL, text_align=RIGHT, color=COLOR_TEXT_PRIMARY))
        self.duration_input = TextInput(placeholder='e.g., 1.5 or 2,5', style=Pack(flex=1))
        self.duration_input.value = '1.0' # Set initial value after creation
        duration_row.add(duration_label)
        duration_row.add(self.duration_input)

        # --- Add Note Input Row ---
        note_row = Box(style=Pack(direction=ROW, padding_bottom=PADDING_MEDIUM, alignment=CENTER))
        note_label = Label("✏️ Note:", style=Pack(padding_right=PADDING_SMALL, text_align=RIGHT, color=COLOR_TEXT_PRIMARY))
        self.note_input = TextInput(placeholder='(Optional)', style=Pack(flex=1)) # Make placeholder indicate optionality
        note_row.add(note_label)
        note_row.add(self.note_input)
        # --- End Note Input Row ---

        button_row = Box(style=Pack(direction=ROW, alignment=CENTER, padding_top=PADDING_SMALL))
        add_button = Button("➕ Add Activity", on_press=self.add_activity, style=Pack(padding=PADDING_AROUND_BUTTON, background_color=COLOR_ACTION_BUTTON_BG, color=COLOR_ACTION_BUTTON_TEXT, font_weight=BOLD))
        button_row.add(add_button)

        input_section_box.add(input_section_title)
        input_section_box.add(activity_row)
        input_section_box.add(duration_row)
        input_section_box.add(note_row) # Add the note row to the layout
        input_section_box.add(button_row)

        # --- Divider ---
        divider1 = Divider(direction=Divider.HORIZONTAL, style=Pack(padding_top=PADDING_LARGE, padding_bottom=PADDING_MEDIUM, color=COLOR_DIVIDER))

        # --- 2. Log and Balance/Mood Section ---
        log_balance_outer_box = Box(style=Pack(direction=ROW, flex=1, padding_bottom=PADDING_MEDIUM))

        # 2a. Today's Log Sub-section
        log_box = Box(style=Pack(direction=COLUMN, flex=3, padding_right=PADDING_MEDIUM))
        log_title = Label("📅 Today's Energy Log", style=Pack(font_weight=BOLD, padding_bottom=PADDING_SMALL, color=COLOR_TEXT_PRIMARY))
        # --- Add "Note" Heading to Table ---
        self.activity_table = Table(
            headings=["Activity Type", "Duration (hr)", "Points", "Note"], # Added Note heading
            missing_value="-",
            style=Pack(flex=1)
        )
        # --- End Table Heading Change ---
        log_box.add(log_title)
        log_box.add(self.activity_table)

        # 2b. Balance and Image Sub-section
        balance_image_box = Box(style=Pack(direction=COLUMN, flex=1, alignment=CENTER))
        balance_title = Label("⚡️ Current Energy Balance", style=Pack(font_weight=BOLD, padding_bottom=PADDING_SMALL, color=COLOR_ENERGY_BALANCE, text_align=CENTER))
        self.energy_balance_label = Label(f"{self.current_balance:+.2f}", style=Pack(font_weight=BOLD, font_size=18, color=COLOR_TEXT_PRIMARY, text_align=CENTER, padding_bottom=PADDING_MEDIUM))
        mood_image_title = Label("😊 Mood:", style=Pack(font_weight=BOLD, padding_bottom=PADDING_SMALL, color=COLOR_TEXT_MOOD, text_align=CENTER))
        self.mood_image_view = ImageView(style=Pack(flex=1, alignment=CENTER, padding=PADDING_SMALL)) # Responsive image view
        balance_image_box.add(balance_title)
        balance_image_box.add(self.energy_balance_label)
        balance_image_box.add(mood_image_title)
        balance_image_box.add(self.mood_image_view)

        log_balance_outer_box.add(log_box)
        log_balance_outer_box.add(balance_image_box)

        # --- Divider ---
        divider2 = Divider(direction=Divider.HORIZONTAL, style=Pack(padding_top=PADDING_MEDIUM, padding_bottom=PADDING_MEDIUM, color=COLOR_DIVIDER))

        # --- 3. Controls Section ---
        controls_box = Box(style=Pack(direction=ROW, alignment=CENTER))
        clear_today_button = Button("🗑️ Revert Today", on_press=self.clear_today, style=Pack(padding=PADDING_AROUND_BUTTON, background_color=COLOR_FUNC_BUTTON_BG, color=COLOR_FUNC_BUTTON_TEXT, font_weight=BOLD))
        controls_box.add(clear_today_button)

        # --- Assemble Main Layout ---
        main_box.add(input_section_box)
        main_box.add(divider1)
        main_box.add(log_balance_outer_box)
        main_box.add(divider2)
        main_box.add(controls_box)

        # --- Main Window Setup ---
        self.main_window = MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

        # --- Initial Display Update ---
        self.update_display()

    # --- Action Handlers ---
    def add_activity(self, widget):
        """Adds activity points to the current balance and logs the activity."""
        try:
            activity_type = self.activity_selection.value
            duration_input_str = self.duration_input.value.strip()
            # --- Get Note Input ---
            note_input_str = self.note_input.value.strip()
            # --- End Get Note Input ---

            if not activity_type:
                self.show_info_dialog("Selection Error", "Please select an activity type.")
                return

            if not duration_input_str:
                self.show_error_dialog("Input Error", "Duration cannot be empty. Please enter a number.")
                return

            duration_str_normalized = duration_input_str.replace(',', '.')
            try:
                duration = float(duration_str_normalized)
            except ValueError:
                self.show_error_dialog("Input Error", f"Invalid duration format: '{duration_input_str}'. Please enter a valid number (e.g., 1.5 or 2,5).")
                return

            # Optional positive duration check
            # if duration <= 0:
            #     self.show_info_dialog("Input Error", "Duration must be a positive number.")
            #     return

            points_per_hour = self.activity_points.get(activity_type, 0)
            calculated_points = round(duration * points_per_hour, 2)
            today_str = date.today().isoformat()

            new_activity = {
                "date": today_str,
                "type": activity_type,
                "duration": duration,
                "points": calculated_points,
                "note": note_input_str # --- Store the note ---
            }

            self.current_balance += calculated_points
            self.all_activities.append(new_activity)
            self.save_data()
            self.update_display()
            self.duration_input.value = '1.0'
            # --- Clear Note Input ---
            self.note_input.value = ''
            # --- End Clear Note Input ---

        except Exception as e:
            print(f"An unexpected error occurred in add_activity: {e}")
            traceback.print_exc()
            self.show_error_dialog("Error", f"An unexpected error occurred: {e}")


    def update_display(self):
        """Updates table (today's entries), energy balance label, and mood GIF."""
        today_str = date.today().isoformat()
        todays_table_data = []

        for activity in self.all_activities:
            if activity.get("date") == today_str:
                # --- Prepare Note for Display ---
                note_text = activity.get("note", "") # Get note, default to empty string
                display_note = note_text if note_text else "-" # Show "-" if note is empty
                # --- End Prepare Note ---

                todays_table_data.append({
                    "activity_type": activity.get("type", "N/A"),
                    "duration_hr": f"{float(activity.get('duration', 0.0)):.2f}",
                    "points": f"{float(activity.get('points', 0.0)):+.2f}",
                    "note": display_note # --- Add note to table data ---
                })

        todays_table_data.reverse() # Show newest first

        try:
            self.activity_table.data = todays_table_data
        except Exception as e:
             print(f"Error updating table data: {e}")
             self.activity_table.data = []

        self.energy_balance_label.text = f"{self.current_balance:+.2f}"
        self.energy_balance_label.style.update(color=COLOR_TEXT_PRIMARY)

        target_image_name = DEFAULT_GIF_NAME
        current_balance = self.current_balance

        if 81 <= current_balance: target_image_name = EXCITED_GIF_NAME
        elif 51 <= current_balance <= 80: target_image_name = STABLE_GIF_NAME
        elif 21 <= current_balance <= 50: target_image_name = TIRED_GIF_NAME
        elif current_balance <= 20: target_image_name = SAD_GIF_NAME

        try:
            base_path = self.paths.app
            image_path = base_path / "resources" / target_image_name
            default_path = base_path / "resources" / DEFAULT_GIF_NAME

            loaded_image = None
            if image_path.exists(): loaded_image = toga.Image(image_path)
            elif default_path.exists(): loaded_image = toga.Image(default_path); print(f"Warning: GIF {target_image_name} not found. Using default.")
            else: print(f"Warning: Target ({target_image_name}) and default GIFs not found. Clearing image.")

            if hasattr(self, 'mood_image_view'):
                 self.mood_image_view.image = loaded_image
            else:
                 print("Error: self.mood_image_view widget not found during update.")

        except AttributeError: print("Error: self.paths.app not available yet."); self._clear_mood_image()
        except FileNotFoundError: print(f"Error: Image file not found."); self._clear_mood_image()
        except Exception as e: print(f"Error loading or setting image: {e}"); self._clear_mood_image()

    def _clear_mood_image(self):
        """Helper to safely clear the mood image."""
        if hasattr(self, 'mood_image_view'):
            self.mood_image_view.image = None

    async def clear_today(self, widget):
        """Removes today's entries from log AND reverts their effect on the balance."""
        today_str = date.today().isoformat()

        points_to_revert = 0.0
        activities_today_indices = []
        for i, activity in enumerate(self.all_activities):
            if activity.get("date") == today_str:
                points_to_revert += float(activity.get("points", 0.0))
                activities_today_indices.append(i)

        if not activities_today_indices:
            self.show_info_dialog("No Entries", "There are no entries logged for today to revert.")
            return

        confirm = ConfirmDialog(
            "Confirm Revert Today",
            f"This will remove today's {len(activities_today_indices)} log entries and revert {points_to_revert:+.2f} points from the balance. Proceed?"
        )
        result = await self.main_window.dialog(confirm)

        if result:
            self.current_balance -= points_to_revert
            self.all_activities = [act for i, act in enumerate(self.all_activities) if i not in activities_today_indices]
            self.save_data()
            self.update_display()

    # --- Helper methods for Dialogs ---
    def show_info_dialog(self, title, message):
        if hasattr(self, 'main_window') and self.main_window: self.main_window.info_dialog(title, message)
        else: print(f"INFO: {title} - {message}")

    def show_error_dialog(self, title, message):
        if hasattr(self, 'main_window') and self.main_window: self.main_window.error_dialog(title, message)
        else: print(f"ERROR: {title} - {message}")

    # --- Data Persistence ---
    @property
    def data_path(self) -> Path:
        if hasattr(self, 'paths') and self.paths: return self.paths.data / DATA_FILE
        else: print("Warning: self.paths not available. Using fallback path for data."); return Path(".") / DATA_FILE

    def load_data(self):
        data_file_path = self.data_path
        if data_file_path.exists():
            try:
                with data_file_path.open("r", encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict) and 'current_balance' in data and 'activity_log' in data:
                        self.current_balance = float(data['current_balance'])
                        # Ensure loaded log is a list
                        if isinstance(data['activity_log'], list):
                            # Optionally validate structure of items in activity_log here
                            self.all_activities = data['activity_log']
                        else:
                            print("Warning: Loaded 'activity_log' is not a list. Ignoring."); self.all_activities = []
                        print(f"Loaded state: Balance={self.current_balance}, Log Entries={len(self.all_activities)}")
                    else:
                        print("Warning: Data file format is incorrect. Using default state."); self._reset_state()
            except (IOError, json.JSONDecodeError, ValueError, Exception) as e:
                print(f"Error loading data file '{data_file_path}': {e}. Using default state."); self._reset_state()
        else:
            print("No data file found. Starting with default state."); self._reset_state()

    def _reset_state(self):
        self.current_balance = BASE_ENERGY
        self.all_activities = []

    def save_data(self):
        data_file_path = self.data_path
        state_data = {"current_balance": self.current_balance, "activity_log": self.all_activities}
        try:
            data_file_path.parent.mkdir(parents=True, exist_ok=True)
            with data_file_path.open("w", encoding='utf-8') as f:
                json.dump(state_data, f, indent=4)
        except (IOError, TypeError, Exception) as e:
            print(f"Error saving data file '{data_file_path}': {e}")
            self.show_error_dialog("Save Error", f"Could not save state:\n{e}")

# --- Main Entry Point ---
def main():
    return SocialEnergyCalculator()