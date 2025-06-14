"""
Food History feature for TraceApp.
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from datetime import datetime

class FoodHistoryView:
    def __init__(self, app):
        self.app = app
        self.content_box = toga.Box(style=Pack(direction=COLUMN, margin=15, flex=1, background_color='#f1f8e9'))
        self.items_box = toga.Box(style=Pack(direction=COLUMN, margin=5))
        self.setup_ui()

    def setup_ui(self):
        """Set up the UI for Food History."""
        title = toga.Label('Riwayat Makanan 🍔', style=Pack(font_size=22, margin_bottom=15, color='#388E3C', font_weight='bold'))
        self.content_box.add(title)
        
        # Add new food entry
        box_add = toga.Box(style=Pack(direction=COLUMN, margin=10, background_color='#c8e6c9'))
        box_add.add(toga.Label('Tambah Data Baru ➕', style=Pack(font_size=16, margin_bottom=10, color='#43A047', font_weight='bold')))
        
        date_box = toga.Box(style=Pack(direction=ROW, margin=5, align_items='center'))
        date_box.add(toga.Label('Tanggal: 📅', style=Pack(width=120, color='#689F38', font_weight='bold')))
        self.date_input = toga.DateInput(value=datetime.now().date(), style=Pack(flex=1))
        date_box.add(self.date_input)
        
        food_box = toga.Box(style=Pack(direction=ROW, margin=5, align_items='center'))
        food_box.add(toga.Label('Nama Makanan: 🍴', style=Pack(width=120, color='#689F38', font_weight='bold')))
        self.food_input = toga.TextInput(style=Pack(flex=1))
        food_box.add(self.food_input)
        
        location_box = toga.Box(style=Pack(direction=ROW, margin=5, align_items='center'))
        location_box.add(toga.Label('Lokasi: 📍', style=Pack(width=120, color='#689F38', font_weight='bold')))
        self.location_input = toga.TextInput(style=Pack(flex=1))
        location_box.add(self.location_input)
        
        notes_box = toga.Box(style=Pack(direction=ROW, margin=5, align_items='center'))
        notes_box.add(toga.Label('Catatan: 📝', style=Pack(width=120, color='#689F38', font_weight='bold')))
        self.notes_input = toga.TextInput(style=Pack(flex=1))
        notes_box.add(self.notes_input)
        
        add_btn = toga.Button('Tambah ✅', on_press=self.add_food_entry, style=Pack(margin=10, background_color='#66BB6A', color='white', font_weight='bold'))
        
        box_add.add(date_box)
        box_add.add(food_box)
        box_add.add(location_box)
        box_add.add(notes_box)
        box_add.add(add_btn)
        self.content_box.add(box_add)
        
        # List of food entries
        list_box = toga.Box(style=Pack(direction=COLUMN, margin=10, flex=1))
        list_box.add(toga.Label('Daftar Riwayat Makanan 🍽️📜', style=Pack(font_size=16, margin_bottom=10, color='#388E3C', font_weight='bold')))
        
        scroll_container = toga.ScrollContainer(style=Pack(flex=1))
        scroll_container.content = self.items_box
        
        list_box.add(scroll_container)
        self.content_box.add(list_box)
        self.refresh_list()

    def add_food_entry(self, widget):
        """Add a new food entry to the database."""
        cursor = self.app.conn.cursor()
        date_str = self.date_input.value.isoformat() if self.date_input.value else datetime.now().date().isoformat()
        cursor.execute("INSERT INTO food_history (date, food_name, location, notes) VALUES (?, ?, ?, ?)",
                       (date_str, self.food_input.value, self.location_input.value, self.notes_input.value))
        self.app.conn.commit()
        self.food_input.value = ''
        self.location_input.value = ''
        self.notes_input.value = ''
        self.refresh_list()

    def refresh_list(self):
        """Refresh the list of food entries from the database."""
        for child in self.items_box.children[:]:
            self.items_box.remove(child)
        cursor = self.app.conn.cursor()
        cursor.execute("SELECT * FROM food_history ORDER BY date DESC")
        for row in cursor.fetchall():
            item_box = toga.Box(style=Pack(direction=COLUMN, margin=10, background_color='#e8f5e9'))
            item_box.add(toga.Label(f"Tanggal: 📅 {row[1]}", style=Pack(color='#333')))
            item_box.add(toga.Label(f"Nama Makanan: 🍴 {row[2]}", style=Pack(color='#333')))
            item_box.add(toga.Label(f"Lokasi: 📍 {row[3]}", style=Pack(color='#333')))
            if row[4]:
                item_box.add(toga.Label(f"Catatan: 📝 {row[4]}", style=Pack(color='#333')))
            
            btn_box = toga.Box(style=Pack(direction=ROW))
            edit_btn = toga.Button('Edit ✏️', on_press=lambda w, r=row: self.app.show_edit_dialog('food_history', r, self.refresh_list), style=Pack(margin=5, background_color='#FFA726', color='black', font_weight='bold'))
            delete_btn = toga.Button('Hapus 🗑️', on_press=lambda w, rid=row[0]: self.delete_item(rid), style=Pack(margin=5, background_color='#EF5350', color='white', font_weight='bold'))
            btn_box.add(edit_btn)
            btn_box.add(delete_btn)
            item_box.add(btn_box)
            self.items_box.add(item_box)

    def delete_item(self, item_id):
        """Delete a food entry from the database."""
        cursor = self.app.conn.cursor()
        cursor.execute("DELETE FROM food_history WHERE id=?", (item_id,))
        self.app.conn.commit()
        self.refresh_list()

    def get_content(self):
        """Return the content box for this view."""
        return self.content_box
