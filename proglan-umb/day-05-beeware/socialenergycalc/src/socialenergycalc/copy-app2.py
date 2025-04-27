import toga
# Import the specific dialog type
from toga import ConfirmDialog, InfoDialog
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, LEFT, RIGHT, CENTER, BOLD
from datetime import date, timedelta
import json
from pathlib import Path
import warnings # To potentially filter known deprecations if needed

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

class SocialEnergyCalculator(toga.App):

    def startup(self):
        """Construct and show the Toga application."""
        self.activity_points = DEFAULT_ACTIVITY_POINTS.copy()
        self.all_activities = []

        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        input_box = toga.Box(style=Pack(direction=COLUMN, padding_bottom=15))

        activity_label = toga.Label("Activity Type:", style=Pack(padding=(0, 5)))
        self.activity_selection = toga.Selection(
            items=list(self.activity_points.keys()),
            style=Pack(flex=1)
        )

        duration_label = toga.Label("Duration (hours):", style=Pack(padding=(0, 5)))
        # Apply fix for min_value deprecation
        self.duration_input = toga.NumberInput(
            min=0.1, # Use 'min' instead of 'min_value'
            step=0.25,
            value=1.0,
            style=Pack(flex=1)
        )

        add_button = toga.Button("Add Activity Entry", on_press=self.add_activity, style=Pack(padding_top=10))

        input_box.add(toga.Box(style=Pack(direction=ROW, padding_bottom=5), children=[activity_label, self.activity_selection]))
        input_box.add(toga.Box(style=Pack(direction=ROW), children=[duration_label, self.duration_input]))
        input_box.add(add_button)

        display_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
        table_label = toga.Label("Today's Log:", style=Pack(font_weight=BOLD, padding_bottom=5))
        self.activity_table = toga.Table(
            headings=["Activity Type", "Duration (hr)", "Energy Points"],
            missing_value="-",
            style=Pack(flex=1)
        )

        totals_box = toga.Box(style=Pack(direction=COLUMN, padding_top=10))
        self.daily_total_label = toga.Label("Daily Energy Balance: 0", style=Pack(font_weight=BOLD))
        self.weekly_total_label = toga.Label("Weekly Energy Balance: 0", style=Pack(font_weight=BOLD))
        totals_box.add(self.daily_total_label)
        totals_box.add(self.weekly_total_label)

        display_box.add(table_label)
        display_box.add(self.activity_table)
        display_box.add(totals_box)

        control_box = toga.Box(style=Pack(direction=ROW, padding_top=15))
        # The handler clear_today is now async, Toga handles calling async handlers correctly
        clear_today_button = toga.Button("Clear Today's Entries", on_press=self.clear_today, style=Pack(padding_right=10))
        control_box.add(clear_today_button)

        main_box.add(input_box)
        main_box.add(display_box)
        main_box.add(control_box)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

        self.all_activities = self.load_data()
        self.update_display()

    # --- Action Handlers ---

    # Add activity remains synchronous unless it needs dialogs
    def add_activity(self, widget):
        """Handles the 'Add Activity Entry' button press."""
        try:
            activity_type = self.activity_selection.value
            duration_str = self.duration_input.value
            duration = float(duration_str) if duration_str is not None else 0.0

            if not activity_type:
                # Consider making info dialog async too for consistency if needed
                self.main_window.info_dialog("Selection Error", "Please select an activity type.")
                # Example async info dialog (if info_dialog causes issues):
                # info = InfoDialog("Selection Error", "Please select an activity type.")
                # await self.main_window.dialog(info) # Requires add_activity to be async def
                return

            if duration <= 0:
                self.main_window.info_dialog("Input Error", "Duration must be a positive number.")
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
             self.main_window.error_dialog("Input Error", f"Invalid duration entered: '{duration_str}'. Please enter a number.")
        except Exception as e:
            print(f"An unexpected error occurred in add_activity: {e}")
            self.main_window.error_dialog("Error", f"An unexpected error occurred: {e}")

    def update_display(self):
        """Updates the activity table and total labels based on current data."""
        today = date.today()
        today_str = today.isoformat()
        todays_table_data = []
        daily_total = 0

        for activity in self.all_activities:
            if activity.get("date") == today_str:
                duration = activity.get('duration', 0)
                points = activity.get('points', 0)
                todays_table_data.append({
                    "activity_type": activity.get("type", "N/A"),
                    "duration_hr": f"{float(duration):.2f}",
                    "energy_points": f"{float(points):.2f}",
                })
                daily_total += float(points)

        try:
            self.activity_table.data = todays_table_data
        except TypeError:
             self.activity_table.data = []

        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        weekly_total = 0

        for activity in self.all_activities:
            try:
                activity_date_str = activity.get("date", "")
                if activity_date_str:
                    activity_date = date.fromisoformat(activity_date_str)
                    if start_of_week <= activity_date <= end_of_week:
                        weekly_total += float(activity.get("points", 0))
            except (ValueError, TypeError):
                continue

        self.daily_total_label.text = f"Daily Energy Balance: {daily_total:.2f}"
        self.weekly_total_label.text = f"Weekly Energy Balance: {weekly_total:.2f}"

    # FIX: Make the handler async
    async def clear_today(self, widget):
        """Removes all activity entries for the current day."""
        today_str = date.today().isoformat()
        initial_activities = list(self.all_activities) # Make a copy

        filtered_activities = [
            activity for activity in self.all_activities
            if activity.get("date") != today_str
        ]

        if len(filtered_activities) < len(initial_activities):
            # FIX: Use the new asynchronous dialog pattern
            confirm_dialog = ConfirmDialog(
                "Confirm Clear",
                "Are you sure you want to remove all entries for today?",
            )
            # Await the result
            result = await self.main_window.dialog(confirm_dialog)

            if result: # result is now True or False
                self.all_activities = filtered_activities
                self.save_data()
                self.update_display()
            # No 'else' needed if cancelling does nothing
        else:
            # Use info_dialog (check if it needs to be async too if issues arise)
            self.main_window.info_dialog("No Entries", "There are no entries logged for today.")
            # Async alternative:
            # info = InfoDialog("No Entries", "There are no entries logged for today.")
            # await self.main_window.dialog(info)


    # --- Data Persistence ---

    @property
    def data_path(self) -> Path:
        """Returns the path to the data file within the app's data directory."""
        if hasattr(self, 'paths') and self.paths:
             return self.paths.data / DATA_FILE
        else:
             print("Warning: self.paths not available when accessing data_path.")
             return Path(".") / DATA_FILE # Fallback

    def load_data(self):
        """Loads activity data from a JSON file."""
        data_file_path = self.data_path
        try:
            if data_file_path.exists():
                data_file_path.parent.mkdir(parents=True, exist_ok=True) # Ensure dir exists
                with data_file_path.open("r", encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list): return data
                    else:
                        print(f"Warning: Data file '{data_file_path}' format incorrect.")
                        return []
            else: return []
        except (IOError, json.JSONDecodeError, Exception) as e:
            print(f"Error loading data file '{data_file_path}': {e}. Starting empty.")
            if hasattr(self, 'main_window') and self.main_window:
                 self.main_window.error_dialog("Load Error", f"Could not load data file:\n{e}")
            return []

    def save_data(self):
        """Saves the current activity data to a JSON file."""
        data_file_path = self.data_path
        try:
            data_file_path.parent.mkdir(parents=True, exist_ok=True) # Ensure dir exists
            with data_file_path.open("w", encoding='utf-8') as f:
                json.dump(self.all_activities, f, indent=4)
        except (IOError, TypeError, Exception) as e:
            print(f"Error saving data file '{data_file_path}': {e}")
            if hasattr(self, 'main_window') and self.main_window:
                self.main_window.error_dialog("Save Error", f"Could not save data:\n{e}")


def main():
    return SocialEnergyCalculator()