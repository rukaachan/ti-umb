"""
Travel History feature for TraceApp.
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from datetime import datetime

class TravelHistoryView:
    def __init__(self, app):
        self.app = app
        self.content_box = toga.Box(style=Pack(direction=COLUMN, margin=15, flex=1, background_color='#fffde7'))
        self.items_box = toga.Box(style=Pack(direction=COLUMN, margin=5))
        self.setup_ui()

    def setup_ui(self):
        """Set up the UI for Travel History."""
        title = toga.Label('Riwayat Perjalanan ✈️', style=Pack(font_size=22, margin_bottom=15, color='#F57C00', font_weight='bold'))
        self.content_box.add(title)
        
        # Add new travel entry
        box_add = toga.Box(style=Pack(direction=COLUMN, margin=10, background_color='#ffecb3'))
        box_add.add(toga.Label('Tambah Data Baru ➕', style=Pack(font_size=16, margin_bottom=10, color='#FB8C00', font_weight='bold')))
        
        date_box = toga.Box(style=Pack(direction=ROW, margin=5, align_items='center'))
        date_box.add(toga.Label('Tanggal: 📅', style=Pack(width=120, color='#E65100', font_weight='bold')))
        self.date_input = toga.DateInput(value=datetime.now().date(), style=Pack(flex=1))
        date_box.add(self.date_input)
        
        dest_box = toga.Box(style=Pack(direction=ROW, margin=5, align_items='center'))
        dest_box.add(toga.Label('Tujuan: 🗺️', style=Pack(width=120, color='#E65100', font_weight='bold')))
        self.dest_input = toga.TextInput(style=Pack(flex=1))
        dest_box.add(self.dest_input)
        
        duration_box = toga.Box(style=Pack(direction=ROW, margin=5, align_items='center'))
        duration_box.add(toga.Label('Durasi: ⏳', style=Pack(width=120, color='#E65100', font_weight='bold')))
        self.duration_input = toga.TextInput(style=Pack(flex=1))
        duration_box.add(self.duration_input)
        
        notes_box = toga.Box(style=Pack(direction=ROW, margin=5, align_items='center'))
        notes_box.add(toga.Label('Catatan: 📝', style=Pack(width=120, color='#E65100', font_weight='bold')))
        self.notes_input = toga.TextInput(style=Pack(flex=1))
        notes_box.add(self.notes_input)
        
        add_btn = toga.Button('Tambah ✅', on_press=self.add_travel_entry, style=Pack(margin=10, background_color='#FF9800', color='white', font_weight='bold'))
        
        box_add.add(date_box)
        box_add.add(dest_box)
        box_add.add(duration_box)
        box_add.add(notes_box)
        box_add.add(add_btn)
        self.content_box.add(box_add)
        
        # List of travel entries
        list_box = toga.Box(style=Pack(direction=COLUMN, margin=10, flex=1))
        list_box.add(toga.Label('Daftar Riwayat Perjalanan 🗺️🚀', style=Pack(font_size=16, margin_bottom=10, color='#F57C00', font_weight='bold')))
        
        scroll_container = toga.ScrollContainer(style=Pack(flex=1))
        scroll_container.content = self.items_box
        
        list_box.add(scroll_container)
        self.content_box.add(list_box)
        self.refresh_list()

    def add_travel_entry(self, widget):
        """Add a new travel entry to the database."""
        cursor = self.app.conn.cursor()
        date_str = self.date_input.value.isoformat() if self.date_input.value else datetime.now().date().isoformat()
        cursor.execute("INSERT INTO travel_history (date, destination, duration, notes) VALUES (?, ?, ?, ?)",
                       (date_str, self.dest_input.value, self.duration_input.value, self.notes_input.value))
        self.app.conn.commit()
        self.dest_input.value = ''
        self.duration_input.value = ''
        self.notes_input.value = ''
        self.refresh_list()

    def refresh_list(self):
        """Refresh the list of travel entries from the database."""
        for child in self.items_box.children[:]:
            self.items_box.remove(child)
        cursor = self.app.conn.cursor()
        cursor.execute("SELECT * FROM travel_history ORDER BY date DESC")
        for row in cursor.fetchall():
            item_box = toga.Box(style=Pack(direction=COLUMN, margin=10, background_color='#fff3e0'))
            item_box.add(toga.Label(f"Tanggal: 📅 {row[1]}", style=Pack(color='#333')))
            item_box.add(toga.Label(f"Tujuan: 🗺️ {row[2]}", style=Pack(color='#333')))
            item_box.add(toga.Label(f"Durasi: ⏳ {row[3]}", style=Pack(color='#333')))
            if row[4]:
                item_box.add(toga.Label(f"Catatan: 📝 {row[4]}", style=Pack(color='#333')))
            
            btn_box = toga.Box(style=Pack(direction=ROW))
            edit_btn = toga.Button('Edit ✏️', on_press=lambda w, r=row: self.app.show_edit_dialog('travel_history', r, self.refresh_list), style=Pack(margin=5, background_color='#FFA726', color='black', font_weight='bold'))
            delete_btn = toga.Button('Hapus 🗑️', on_press=lambda w, rid=row[0]: self.delete_item(rid), style=Pack(margin=5, background_color='#EF5350', color='white', font_weight='bold'))
            btn_box.add(edit_btn)
            btn_box.add(delete_btn)
            item_box.add(btn_box)
            self.items_box.add(item_box)

    def delete_item(self, item_id):
        """Delete a travel entry from the database."""
        cursor = self.app.conn.cursor()
        cursor.execute("DELETE FROM travel_history WHERE id=?", (item_id,))
        self.app.conn.commit()
        self.refresh_list()

    def get_content(self):
        """Return the content box for this view."""
        return self.content_box
