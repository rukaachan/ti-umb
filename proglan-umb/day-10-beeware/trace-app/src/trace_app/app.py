"""
A BeeWare application for tracking personal data including food history, personal expenses, wishlist items, and travel history.
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import sqlite3
from .features.food_history import FoodHistoryView
from .features.personal_expenses import PersonalExpensesView
from .features.wishlist import WishlistView
from .features.travel_history import TravelHistoryView

class TraceApp(toga.App):
    def startup(self):
        """
        Construct and show the Toga application.
        """
        import os
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', 'database', 'trace_app.db')
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
        
        self.main_box = toga.Box(style=Pack(direction=COLUMN, margin=15, background_color='#f0f4f8'))
        
        # Navigation buttons
        self.nav_box = toga.Box(style=Pack(direction=ROW, margin=10, background_color='#d9e6ff'))
        self.btn_food = toga.Button('Makanan 🍔', on_press=self.show_food_history, style=Pack(margin=10, background_color='#4CAF50', color='white', font_weight='bold'))
        self.btn_expenses = toga.Button('Pengeluaran 💰', on_press=self.show_personal_expenses, style=Pack(margin=10, background_color='#FF5252', color='white', font_weight='bold'))
        self.btn_wishlist = toga.Button('Wishlist 🎁', on_press=self.show_wishlist, style=Pack(margin=10, background_color='#2196F3', color='white', font_weight='bold'))
        self.btn_travel = toga.Button('Perjalanan ✈️', on_press=self.show_travel_history, style=Pack(margin=10, background_color='#FF9800', color='white', font_weight='bold'))
        
        self.nav_box.add(self.btn_food)
        self.nav_box.add(self.btn_expenses)
        self.nav_box.add(self.btn_wishlist)
        self.nav_box.add(self.btn_travel)
        
        self.content_box = toga.Box(style=Pack(direction=COLUMN, margin=15, flex=1, background_color='#f5f9ff'))
        self.main_box.add(self.nav_box)
        self.main_box.add(self.content_box)
        
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()
        
        # Initialize views
        self.food_view = FoodHistoryView(self)
        self.expenses_view = PersonalExpensesView(self)
        self.wishlist_view = WishlistView(self)
        self.travel_view = TravelHistoryView(self)
        
        # Default view
        self.current_view = self.food_view
        self.content_box.add(self.food_view.get_content())

    def create_tables(self):
        """Create database tables if they don't exist."""
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS food_history
                         (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, food_name TEXT, location TEXT, notes TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS personal_expenses
                         (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, amount REAL, category TEXT, description TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS wishlist
                         (id INTEGER PRIMARY KEY AUTOINCREMENT, item_name TEXT, price REAL, priority TEXT, notes TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS travel_history
                         (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, destination TEXT, duration TEXT, notes TEXT)''')
        self.conn.commit()

    def clear_content(self):
        """Clear the content area for a new view."""
        for child in self.content_box.children[:]:
            self.content_box.remove(child)

    def update_nav_buttons(self, active_widget):
        """Update navigation button styles to indicate active section."""
        self.btn_food.style.background_color = '#4CAF50'
        self.btn_food.style.color = 'white'
        self.btn_expenses.style.background_color = '#FF5252'
        self.btn_expenses.style.color = 'white'
        self.btn_wishlist.style.background_color = '#2196F3'
        self.btn_wishlist.style.color = 'white'
        self.btn_travel.style.background_color = '#FF9800'
        self.btn_travel.style.color = 'white'
        active_widget.style.background_color = '#8BC34A'
        active_widget.style.color = 'white'

    def show_food_history(self, widget=None):
        """Display Food History section."""
        self.update_nav_buttons(self.btn_food)
        self.clear_content()
        self.current_view = self.food_view
        self.content_box.add(self.food_view.get_content())

    def show_personal_expenses(self, widget=None):
        """Display Personal Expenses section."""
        self.update_nav_buttons(self.btn_expenses)
        self.clear_content()
        self.current_view = self.expenses_view
        self.content_box.add(self.expenses_view.get_content())

    def show_wishlist(self, widget=None):
        """Display Wishlist section."""
        self.update_nav_buttons(self.btn_wishlist)
        self.clear_content()
        self.current_view = self.wishlist_view
        self.content_box.add(self.wishlist_view.get_content())

    def show_travel_history(self, widget=None):
        """Display Travel History section."""
        self.update_nav_buttons(self.btn_travel)
        self.clear_content()
        self.current_view = self.travel_view
        self.content_box.add(self.travel_view.get_content())

    def show_edit_dialog(self, table_name, row, refresh_callback):
        """Show dialog for editing an existing entry."""
        dialog_box = toga.Box(style=Pack(direction=COLUMN, margin=15, background_color='#f7f9fc'))
        dialog_window = toga.Window(title='Edit Data', size=(300, 400))
        dialog_window.content = dialog_box
        
        dialog_box.add(toga.Label('Edit Data ✏️', style=Pack(font_size=16, margin_bottom=15, color='#333', font_weight='bold')))
        
        inputs = []
        if table_name == 'food_history':
            fields = [('Tanggal:', row[1]), ('Nama Makanan:', row[2]), ('Lokasi:', row[3]), ('Catatan:', row[4])]
            for label, value in fields:
                field_box = toga.Box(style=Pack(direction=ROW, margin=5))
                field_box.add(toga.Label(label, style=Pack(width=100, color='#555')))
                input_field = toga.TextInput(value=value, style=Pack(flex=1))
                field_box.add(input_field)
                dialog_box.add(field_box)
                inputs.append(input_field)
        elif table_name == 'personal_expenses':
            fields = [('Tanggal:', row[1]), ('Jumlah (Rp):', str(row[2])), ('Kategori:', row[3]), ('Deskripsi:', row[4])]
            for label, value in fields:
                field_box = toga.Box(style=Pack(direction=ROW, margin=5))
                field_box.add(toga.Label(label, style=Pack(width=100, color='#555')))
                input_field = toga.TextInput(value=value, style=Pack(flex=1))
                field_box.add(input_field)
                dialog_box.add(field_box)
                inputs.append(input_field)
        elif table_name == 'wishlist':
            fields = [('Nama Barang:', row[1]), ('Harga (Rp):', str(row[2])), ('Prioritas:', row[3]), ('Catatan:', row[4])]
            for label, value in fields:
                field_box = toga.Box(style=Pack(direction=ROW, margin=5))
                field_box.add(toga.Label(label, style=Pack(width=100, color='#555')))
                input_field = toga.TextInput(value=value, style=Pack(flex=1))
                field_box.add(input_field)
                dialog_box.add(field_box)
                inputs.append(input_field)
        elif table_name == 'travel_history':
            fields = [('Tanggal:', row[1]), ('Tujuan:', row[2]), ('Durasi:', row[3]), ('Catatan:', row[4])]
            for label, value in fields:
                field_box = toga.Box(style=Pack(direction=ROW, margin=5))
                field_box.add(toga.Label(label, style=Pack(width=100, color='#555')))
                input_field = toga.TextInput(value=value, style=Pack(flex=1))
                field_box.add(input_field)
                dialog_box.add(field_box)
                inputs.append(input_field)
        
        def save_changes(widget):
            cursor = self.conn.cursor()
            try:
                if table_name == 'food_history':
                    cursor.execute("UPDATE food_history SET date=?, food_name=?, location=?, notes=? WHERE id=?",
                                   (inputs[0].value, inputs[1].value, inputs[2].value, inputs[3].value, row[0]))
                elif table_name == 'personal_expenses':
                    amount = float(inputs[1].value)
                    cursor.execute("UPDATE personal_expenses SET date=?, amount=?, category=?, description=? WHERE id=?",
                                   (inputs[0].value, amount, inputs[2].value, inputs[3].value, row[0]))
                elif table_name == 'wishlist':
                    price = float(inputs[1].value) if inputs[1].value else 0.0
                    cursor.execute("UPDATE wishlist SET item_name=?, price=?, priority=?, notes=? WHERE id=?",
                                   (inputs[0].value, price, inputs[2].value, inputs[3].value, row[0]))
                elif table_name == 'travel_history':
                    cursor.execute("UPDATE travel_history SET date=?, destination=?, duration=?, notes=? WHERE id=?",
                                   (inputs[0].value, inputs[1].value, inputs[2].value, inputs[3].value, row[0]))
                self.conn.commit()
                refresh_callback()
                dialog_window.close()
            except ValueError:
                self.main_window.error_dialog('Error', 'Input numerik tidak valid.')
        
        save_btn = toga.Button('Simpan', on_press=save_changes, style=Pack(margin=5, background_color='#43A047', color='white'))
        cancel_btn = toga.Button('Batal', on_press=lambda w: dialog_window.close(), style=Pack(margin=5, background_color='#E53935', color='white'))
        btn_box = toga.Box(style=Pack(direction=ROW, margin_top=10))
        btn_box.add(save_btn)
        btn_box.add(cancel_btn)
        dialog_box.add(btn_box)
        
        dialog_window.show()

def main():
    return TraceApp()
