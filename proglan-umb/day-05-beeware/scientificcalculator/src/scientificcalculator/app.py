import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import math


class ScientificCalculatorApp(toga.App):
    def startup(self):
        # Create main window with formal app name
        self.main_window = toga.MainWindow(title=self.formal_name)

        # Header label for interest
        self.header_label = toga.Label(
            '🧮 Scientific Calculator',
            style=Pack(padding=10, font_size=18, color='#2c3e50', alignment='center')
        )

        # Input field for number entry with emoji
        self.input_field = toga.TextInput(
            placeholder='🔢 Enter a number',
            style=Pack(flex=1, padding=10, background_color='#ffffff', color='#333333')
        )

        # Unit selection (Degrees or Radians)
        self.unit_toggle = toga.Selection(
            items=['Degrees', 'Radians'],
            style=Pack(padding=(10, 10), width=120)
        )
        self.unit_toggle.value = 'Degrees'

        # Calculate button with emoji
        self.calc_button = toga.Button(
            '🧠 Calculate',
            on_press=self.calculate,
            style=Pack(padding=10, background_color='#3498db', color='#ffffff', font_size=14)
        )

        # Clear button for resetting inputs and outputs
        self.clear_button = toga.Button(
            '🗑️ Clear',
            on_press=self.clear,
            style=Pack(padding=10, background_color='#e74c3c', color='#ffffff', font_size=14)
        )

        # Labels for results with emojis
        self.sin_label = toga.Label(
            '📐 sin(x):',
            style=Pack(padding=5, font_size=12, color='#2c3e50')
        )
        self.cos_label = toga.Label(
            '📐 cos(x):',
            style=Pack(padding=5, font_size=12, color='#2c3e50')
        )
        self.tan_label = toga.Label(
            '📐 tan(x):',
            style=Pack(padding=5, font_size=12, color='#2c3e50')
        )

        # Layout containers
        input_box = toga.Box(
            children=[self.input_field, self.unit_toggle, self.calc_button, self.clear_button],
            style=Pack(direction=ROW, padding=10, background_color='#ecf0f1', alignment='center')
        )

        result_box = toga.Box(
            children=[self.sin_label, self.cos_label, self.tan_label],
            style=Pack(direction=COLUMN, padding=10, background_color='#ffffff')
        )

        main_box = toga.Box(
            children=[self.header_label, input_box, result_box],
            style=Pack(direction=COLUMN, padding=20, alignment='center')
        )

        self.main_window.content = main_box
        self.main_window.show()

    def calculate(self, widget):
        """
        Parse input, convert if needed, compute trig values, and update labels.
        """
        try:
            x = float(self.input_field.value)
        except ValueError:
            self._display_invalid()
            return

        # Convert degrees to radians if necessary
        angle = math.radians(x) if self.unit_toggle.value == 'Degrees' else x

        # Compute trig values
        sin_x = math.sin(angle)
        cos_x = math.cos(angle)
        tan_x = math.tan(angle)

        # Display results with emojis and 6 decimal places
        self.sin_label.text = f'📐 sin(x): {sin_x:.6f}'
        self.cos_label.text = f'📐 cos(x): {cos_x:.6f}'
        self.tan_label.text = f'📐 tan(x): {tan_x:.6f}'

    def clear(self, widget):
        """
        Reset input field and result labels to default state.
        """
        self.input_field.value = ''
        self.sin_label.text = '📐 sin(x):'
        self.cos_label.text = '📐 cos(x):'
        self.tan_label.text = '📐 tan(x):'

    def _display_invalid(self):
        """
        Show error message for invalid input with warning emoji.
        """
        self.sin_label.text = '⚠️ sin(x): Invalid input'
        self.cos_label.text = '⚠️ cos(x): Invalid input'
        self.tan_label.text = '⚠️ tan(x): Invalid input'


def main():
    return ScientificCalculatorApp()
