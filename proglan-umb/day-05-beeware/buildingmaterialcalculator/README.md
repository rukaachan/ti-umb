# 🏗️ Building Material Calculator

A simple desktop application built with Python and the BeeWare framework (Toga toolkit) to estimate basic building material requirements based on building dimensions.

## 🎯 Objective

This tool aims to provide quick, approximate calculations for common building materials like bricks, cement, and sand needed for simple construction projects (e.g., a single-story rectangular structure).

## ✨ Features

- Accepts building dimensions (Length, Width, Height) in meters.
- Calculates required materials:
  - Bricks (for walls)
  - Cement (for wall plastering and floor base)
  - Sand (for floor base)
- Basic input validation (checks for positive numerical values).
- Simple, cross-platform user interface powered by BeeWare/Toga.
- Clear display of input dimensions, calculated areas, and estimated materials.
- Includes fun emojis for a slightly more engaging UI! ✨

## 💻 Technology Stack

- **Python 3**
- **BeeWare**
  - **Toga:** GUI toolkit for cross-platform native interfaces.
  - **Briefcase:** Tool for packaging and deploying BeeWare applications.

## ⚙️ Setup and Installation

1.  **Prerequisites:**

    - Python 3 installed.
    - `pip` (Python package installer).

2.  **Install Briefcase:**

    ```bash
    pip install cookiecutter briefcase
    ```

3.  **Navigate to Project Directory:**

    ```bash
    cd buildingmaterialcalculator
    ```

4.  **Create and Activate Virtual Environment (Recommended):**

    - **macOS/Linux:**
      ```bash
      python3 -m venv beeware-venv
      source beeware-venv/bin/activate
      ```
    - **Windows:**
      ```bash
      python -m venv beeware-venv
      beeware-venv\Scripts\activate
      ```

5.  **Install Project Dependencies:**
    _(Briefcase usually handles Toga installation during the first `briefcase dev` run, but you might install the project itself in editable mode)_
    ```bash
    pip install -e src/buildingmaterialcalculator
    ```
    _(Or let `briefcase dev` handle dependencies)_

## ▶️ Running the Application

1.  Ensure your virtual environment is activated.
2.  Navigate to the project's root directory (`buildingmaterialcalculator`).
3.  Run the application in developer mode using Briefcase:
    ```bash
    briefcase dev
    ```
    _(The first time you run this, Briefcase will download and install the necessary Toga backend for your operating system.)_

## 🧮 Formulas Used

The calculations are based on the following inputs and formulas:

**Inputs:**

- `Length` (L): Building length in meters (m)
- `Width` (W): Building width in meters (m)
- `Height` (H): Building height in meters (m)

**Intermediate Calculations:**

1.  **Wall Area (A_wall):** Calculates the total surface area of the four walls.
    ```
    A_wall = (L + W) * 2 * H  (m²)
    ```
2.  **Floor Area (A_floor):** Calculates the area of the building's floor.
    ```
    A_floor = L * W  (m²)
    ```

**Material Estimation Constants (from `MATERIALS_DB`):**

- Bricks per m² of Wall (`bricks_per_sqm_wall`): `70` units/m²
- Cement per m² for Plastering (`cement_per_sqm_plaster`): `10` kg/m²
- Cement per m² for Floor Base (`cement_per_sqm_floor`): `5` kg/m²
- Sand per m² of Floor Base (`sand_per_cubic_meter_floor`): `0.05` m³/m² _(Note: This constant represents m³ of sand per m² of floor area)_

**Final Material Calculations:**

1.  **Bricks Required:**

    ```
    Bricks = A_wall * bricks_per_sqm_wall  (units)
    ```

    _Example: Bricks = A_wall _ 70\*

2.  **Cement Required (Total):** Sum of cement needed for wall plastering and floor base.

    - Cement for Plaster (`Cement_plaster`) = `A_wall * cement_per_sqm_plaster` (kg)
      _Example: Cement_plaster = A_wall _ 10\*
    - Cement for Floor (`Cement_floor`) = `A_floor * cement_per_sqm_floor` (kg)
      _Example: Cement_floor = A_floor _ 5\*
    - Total Cement = `Cement_plaster + Cement_floor` (kg)

3.  **Sand Required:**
    ```
    Sand = A_floor * sand_per_cubic_meter_floor  (m³)
    ```
    _Example: Sand = A_floor _ 0.05\*

## 📜 License

This project is licensed under the BSD License - see the LICENSE file for details.
