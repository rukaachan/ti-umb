import toga
from toga.style import Pack
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
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=20))
        input_box = toga.Box(style=Pack(direction=COLUMN, padding_bottom=20))
        results_outer_box = toga.Box(style=Pack(direction=COLUMN, padding_top=10))

        # --- Input Fields ---
        length_label = toga.Label("📏 Panjang Bangunan (m):", style=Pack(text_align=LEFT, width=170, padding_right=10))
        self.length_input = toga.TextInput(placeholder="misalnya, 10", style=Pack(flex=1))
        length_box = toga.Box(style=Pack(direction=ROW, padding_bottom=10))
        length_box.add(length_label)
        length_box.add(self.length_input)

        width_label = toga.Label("📏 Lebar Bangunan (m):", style=Pack(text_align=LEFT, width=170, padding_right=10))
        self.width_input = toga.TextInput(placeholder="misalnya, 8", style=Pack(flex=1))
        width_box = toga.Box(style=Pack(direction=ROW, padding_bottom=10))
        width_box.add(width_label)
        width_box.add(self.width_input)

        height_label = toga.Label("📏 Tinggi Bangunan (m):", style=Pack(text_align=LEFT, width=170, padding_right=10))
        self.height_input = toga.TextInput(placeholder="misalnya, 3", style=Pack(flex=1))
        height_box = toga.Box(style=Pack(direction=ROW, padding_bottom=10))
        height_box.add(height_label)
        height_box.add(self.height_input)

        input_box.add(length_box)
        input_box.add(width_box)
        input_box.add(height_box)

        # --- Buttons ---
        button_calculate = toga.Button(
            "🧮 Hitung Material",
            on_press=self.calculate_materials,
            style=Pack(padding=5, flex=1)
        )
        button_reset = toga.Button(
            "🔄 Atur Ulang",
            on_press=self.reset_fields,
            style=Pack(padding=5, flex=1)
        )
        button_box = toga.Box(style=Pack(direction=ROW, alignment=CENTER, padding_bottom=20))
        button_box.add(button_calculate)
        button_box.add(button_reset)

        # --- Results Display Area (Using Labels) ---
        self.results_title_label = toga.Label(
            "📊 Hasil Perhitungan:",
            style=Pack(font_weight='bold', padding_bottom=5, text_align=LEFT)
        )
        self.summary_header_label = toga.Label(
            "",
            style=Pack(padding_top=5, padding_bottom=5, text_align=LEFT)
        )
        self.input_dims_details_label = toga.Label("", style=Pack(text_align=LEFT, padding_bottom=10))
        self.calc_areas_details_label = toga.Label("", style=Pack(text_align=LEFT, padding_bottom=10))
        self.material_reqs_details_label = toga.Label("", style=Pack(text_align=LEFT))
        self.status_label = toga.Label("", style=Pack(text_align=LEFT, color='red', padding_top=10))

        # Add elements to the results_outer_box
        results_outer_box.add(self.results_title_label)
        results_outer_box.add(self.summary_header_label)
        results_outer_box.add(self.input_dims_details_label)
        results_outer_box.add(self.calc_areas_details_label)
        results_outer_box.add(self.material_reqs_details_label)
        results_outer_box.add(self.status_label)

        # Add all sections to main_box
        main_box.add(input_box)
        main_box.add(button_box)
        main_box.add(results_outer_box)

        # --- Main Window Setup ---
        self.main_window = toga.MainWindow(title="🏗️ Kalkulator Material Bangunan")
        self.main_window.content = main_box
        self.main_window.show()

    def validate_input(self, value_str, field_name):
        """ Helper function to validate numerical input """
        if not value_str:
             self.status_label.text = f"⚠️ Kesalahan: {field_name} tidak boleh kosong."
             return None
        try:
            value = float(value_str)
            if value <= 0:
                 self.status_label.text = f"⚠️ Kesalahan: {field_name} harus berupa angka positif."
                 return None
            return value
        except ValueError:
            self.status_label.text = f"⚠️ Kesalahan: Angka tidak valid untuk {field_name}: '{value_str}'"
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
        self.clear_results()
        validation_passed = True

        # --- Input Module: Get and Validate Data ---
        length = self.validate_input(self.length_input.value, "📏 Panjang Bangunan (m):")
        if length is None: validation_passed = False

        width = self.validate_input(self.width_input.value, "📏 Lebar Bangunan (m):")
        if width is None and validation_passed: validation_passed = False

        height = self.validate_input(self.height_input.value, "📏 Tinggi Bangunan (m):")
        if height is None and validation_passed: validation_passed = False

        if not validation_passed:
             if not self.status_label.text:
                 self.status_label.text = "⚠️ Kesalahan: Silakan periksa kolom input."
             return

        # --- Calculation Logic ---
        try:
            wall_area = (length + width) * 2 * height
            floor_area = length * width

            bricks_needed = wall_area * MATERIALS_DB['bricks_per_sqm_wall']
            cement_for_plaster = wall_area * MATERIALS_DB['cement_per_sqm_plaster']
            cement_for_floor = floor_area * MATERIALS_DB['cement_per_sqm_floor']
            total_cement_needed = cement_for_plaster + cement_for_floor
            sand_needed = floor_area * MATERIALS_DB['sand_per_cubic_meter_floor']

            # --- Output Module: Update Labels with Emojis and Styling ---
            self.summary_header_label.text = "✨ Cetak Biru Bangunan Anda! ✨\n--------------------------------"

            self.input_dims_details_label.text = (
                f"📐 Dimensi Input:\n"
                f"  → Panjang: {length:.2f} m\n"
                f"  → Lebar:   {width:.2f} m\n"
                f"  → Tinggi:  {height:.2f} m"
            )
            self.calc_areas_details_label.text = (
                f"🟧 Luas yang Dihitung:\n"
                f"  🧱 Total Luas Dinding: {wall_area:.2f} m²\n"
                f"  🏠 Luas Lantai:       {floor_area:.2f} m²"
            )
            self.material_reqs_details_label.text = (
                f"🛠️ Estimasi Kebutuhan Material:\n"
                f"  🧱 Batu Bata: {bricks_needed:,.0f} unit\n"
                f"  ⚪ Semen:     {total_cement_needed:,.2f} kg\n"
                f"  ⏳ Pasir:     {sand_needed:.2f} m³"
            )
            self.status_label.text = "✅ Perhitungan Selesai!"

        except Exception as e:
            error_message = f"❌ Kesalahan Perhitungan: Terjadi kesalahan tak terduga: {e}"
            self.status_label.text = error_message
            self.summary_header_label.text = ""
            self.input_dims_details_label.text = ""
            self.calc_areas_details_label.text = ""
            self.material_reqs_details_label.text = ""

    def reset_fields(self, widget):
        """ Callback function for the Reset button """
        self.length_input.value = ""
        self.width_input.value = ""
        self.height_input.value = ""
        self.clear_results()
        self.length_input.focus()

def main():
    return BuildingMaterialCalculator()