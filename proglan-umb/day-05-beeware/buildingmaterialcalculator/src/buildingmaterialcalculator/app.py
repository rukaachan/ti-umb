# -*- coding: utf-8 -*-
import toga
from toga.style import Pack
# Import CENTER again for alignment
from toga.style.pack import COLUMN, ROW, CENTER, LEFT

# --- Material Database (Constants based on the example) ---
MATERIALS_DB = {
    'bricks_per_sqm_wall': 70,
    'cement_per_sqm_plaster': 10,
    'cement_per_sqm_floor': 5,
    'sand_per_cubic_meter_floor': 0.05
}

class BuildingMaterialCalculator(toga.App):

    def startup(self):
        """
        Construct and show the Toga application using deprecated (but working) styles.
        """
        # --- UI Elements ---
        # Use padding (deprecated)
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=20))
        input_box = toga.Box(style=Pack(direction=COLUMN, padding_bottom=20)) # Use padding_bottom (deprecated)
        # Use padding_top (deprecated)
        results_outer_box = toga.Box(style=Pack(direction=COLUMN, padding_top=10))

        # --- Input Fields ---
        # Use padding_right (deprecated)
        length_label = toga.Label("📏 Building Length (m):", style=Pack(text_align=LEFT, width=170, padding_right=10))
        self.length_input = toga.TextInput(placeholder="e.g., 10", style=Pack(flex=1))
        length_box = toga.Box(style=Pack(direction=ROW, padding_bottom=10)) # Use padding_bottom (deprecated)
        length_box.add(length_label)
        length_box.add(self.length_input)

        # Use padding_right (deprecated)
        width_label = toga.Label("📏 Building Width (m):", style=Pack(text_align=LEFT, width=170, padding_right=10))
        self.width_input = toga.TextInput(placeholder="e.g., 8", style=Pack(flex=1))
        width_box = toga.Box(style=Pack(direction=ROW, padding_bottom=10)) # Use padding_bottom (deprecated)
        width_box.add(width_label)
        width_box.add(self.width_input)

        # Use padding_right (deprecated)
        height_label = toga.Label("📏 Building Height (m):", style=Pack(text_align=LEFT, width=170, padding_right=10))
        self.height_input = toga.TextInput(placeholder="e.g., 3", style=Pack(flex=1))
        height_box = toga.Box(style=Pack(direction=ROW, padding_bottom=10)) # Use padding_bottom (deprecated)
        height_box.add(height_label)
        height_box.add(self.height_input)

        input_box.add(length_box)
        input_box.add(width_box)
        input_box.add(height_box)

        # --- Buttons ---
        button_calculate = toga.Button(
            "🧮 Calculate Materials",
            on_press=self.calculate_materials,
            style=Pack(padding=5, flex=1) # Use padding (deprecated)
        )
        button_reset = toga.Button(
            "🔄 Reset",
            on_press=self.reset_fields,
            style=Pack(padding=5, flex=1) # Use padding (deprecated)
        )
        # Use alignment=CENTER and padding_bottom (deprecated)
        button_box = toga.Box(style=Pack(direction=ROW, alignment=CENTER, padding_bottom=20))
        button_box.add(button_calculate)
        button_box.add(button_reset)

        # --- Results Display Area (Using Labels) ---
        self.results_title_label = toga.Label(
            "📊 Calculation Results:",
            # Use padding_bottom (deprecated)
            style=Pack(font_weight='bold', padding_bottom=5, text_align=LEFT)
        )
        self.summary_header_label = toga.Label(
            "", # Start empty
            # Use padding_top and padding_bottom (deprecated)
            style=Pack(padding_top=5, padding_bottom=5, text_align=LEFT)
        )
        # Labels for each section of the results
        # Use padding_bottom (deprecated)
        self.input_dims_details_label = toga.Label("", style=Pack(text_align=LEFT, padding_bottom=10))
        self.calc_areas_details_label = toga.Label("", style=Pack(text_align=LEFT, padding_bottom=10)) # Use padding_bottom (deprecated)
        self.material_reqs_details_label = toga.Label("", style=Pack(text_align=LEFT))
        # Label for displaying calculation errors or status
        # Use padding_top (deprecated)
        self.status_label = toga.Label("", style=Pack(text_align=LEFT, color='red', padding_top=10))


        # Add elements to the results_outer_box
        results_outer_box.add(self.results_title_label)
        results_outer_box.add(self.summary_header_label)
        results_outer_box.add(self.input_dims_details_label)
        results_outer_box.add(self.calc_areas_details_label)
        results_outer_box.add(self.material_reqs_details_label)
        results_outer_box.add(self.status_label) # Add status label at the end


        # Add all sections to main_box
        main_box.add(input_box)
        main_box.add(button_box)
        main_box.add(results_outer_box)


        # --- Main Window Setup ---
        self.main_window = toga.MainWindow(title="🏗️ Building Material Calculator")
        self.main_window.content = main_box
        self.main_window.show()

    def validate_input(self, value_str, field_name):
        """ Helper function to validate numerical input """
        # Use field_name directly which now includes the emoji
        if not value_str:
             self.status_label.text = f"⚠️ Error: {field_name} cannot be empty."
             return None
        try:
            value = float(value_str)
            if value <= 0:
                 self.status_label.text = f"⚠️ Error: {field_name} must be a positive number."
                 return None
            # Clear error *only if* this validation step passes
            # Avoid clearing a previous error from another field prematurely
            # self.status_label.text = "" # Removed for safer error handling
            return value
        except ValueError:
            self.status_label.text = f"⚠️ Error: Invalid number entered for {field_name}: '{value_str}'"
            return None

    def clear_results(self):
        """ Helper function to clear all result labels """
        self.summary_header_label.text = ""
        self.input_dims_details_label.text = ""
        self.calc_areas_details_label.text = ""
        self.material_reqs_details_label.text = ""
        self.status_label.text = ""

    def calculate_materials(self, widget):
        """ Callback function for the Calculate button """
        # Clear previous results and status first
        self.clear_results()
        validation_passed = True # Flag to track validation status

        # --- Input Module: Get and Validate Data ---
        # Pass the label text directly for clearer error messages
        length = self.validate_input(self.length_input.value, "📏 Building Length (m):")
        if length is None: validation_passed = False

        width = self.validate_input(self.width_input.value, "📏 Building Width (m):")
        # Only update validation status if it hasn't failed already
        if width is None and validation_passed: validation_passed = False

        height = self.validate_input(self.height_input.value, "📏 Building Height (m):")
        # Only update validation status if it hasn't failed already
        if height is None and validation_passed: validation_passed = False


        # Check if any validation failed
        if not validation_passed:
             # Ensure an error message is displayed if multiple fields are invalid
             if not self.status_label.text:
                 self.status_label.text = "⚠️ Error: Please check input fields."
             return # Stop calculation

        # --- Calculation Logic ---
        try:
            # Calculate Areas
            wall_area = (length + width) * 2 * height
            floor_area = length * width

            # Calculate Material Needs
            bricks_needed = wall_area * MATERIALS_DB['bricks_per_sqm_wall']
            cement_for_plaster = wall_area * MATERIALS_DB['cement_per_sqm_plaster']
            cement_for_floor = floor_area * MATERIALS_DB['cement_per_sqm_floor']
            total_cement_needed = cement_for_plaster + cement_for_floor
            sand_needed = floor_area * MATERIALS_DB['sand_per_cubic_meter_floor']

            # --- Output Module: Update Labels with Emojis and Styling ---

            # Set the summary header - made more exciting!
            self.summary_header_label.text = "✨ Your Building Blueprint! ✨\n--------------------------------"

            # Format and set text for each result label with emojis
            self.input_dims_details_label.text = (
                f"📐 Input Dimensions:\n"
                f"  → Length: {length:.2f} m\n"
                f"  → Width:  {width:.2f} m\n"
                f"  → Height: {height:.2f} m"
            )
            self.calc_areas_details_label.text = (
                f"🟧 Calculated Areas:\n"
                f"  🧱 Total Wall Area: {wall_area:.2f} m²\n"
                f"  🏠 Floor Area:      {floor_area:.2f} m²"
            )
            # Using unicode symbols that might render better than pure emojis sometimes
            self.material_reqs_details_label.text = (
                f"🛠️ Estimated Material Needs:\n"
                f"  🧱 Bricks: {bricks_needed:,.0f} units\n"
                f"  ⚪ Cement: {total_cement_needed:,.2f} kg\n"
                f"  ⏳ Sand:   {sand_needed:.2f} m³"
            )
            # Clear status label on success and show completion message
            self.status_label.text = "✅ Calculation Complete!"
            # Ensure status label color isn't stuck on red from previous error
            # Note: Dynamically changing style like color might be backend-dependent
            # self.status_label.style.update(color='green') # Example, might not work reliably everywhere

        except Exception as e:
            # Catch unexpected errors during calculation
            error_message = f"❌ Calculation Error: An unexpected error occurred: {e}"
            self.status_label.text = error_message
            # Ensure error color is set (redundant if default is red, but safe)
            # self.status_label.style.update(color='red')
            # Clear other result fields on calculation error
            self.summary_header_label.text = ""
            self.input_dims_details_label.text = ""
            self.calc_areas_details_label.text = ""
            self.material_reqs_details_label.text = ""


    def reset_fields(self, widget):
        """ Callback function for the Reset button """
        self.length_input.value = ""
        self.width_input.value = ""
        self.height_input.value = ""
        self.clear_results() # Use the helper function to clear all results/status
        self.length_input.focus() # Set focus back to the first field


def main():
    return BuildingMaterialCalculator()