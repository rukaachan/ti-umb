"""
Wishlist feature for TraceApp.
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class WishlistView:
    def __init__(self, app):
        self.app = app
        self.content_box = toga.Box(style=Pack(direction=COLUMN, margin=15, flex=1, background_color='#e1f5fe'))
        self.items_box = toga.Box(style=Pack(direction=COLUMN, margin=5))
        self.setup_ui()

    def setup_ui(self):
        """Set up the UI for Wishlist."""
        title = toga.Label('Daftar Wishlist 🎁', style=Pack(font_size=22, margin_bottom=15, color='#1976D2', font_weight='bold'))
        self.content_box.add(title)
        
        # Add new wishlist item
        box_add = toga.Box(style=Pack(direction=COLUMN, margin=10, background_color='#b3e5fc'))
        box_add.add(toga.Label('Tambah Data Baru ➕', style=Pack(font_size=16, margin_bottom=10, color='#1E88E5', font_weight='bold')))
        
        item_box = toga.Box(style=Pack(direction=ROW, margin=5, align_items='center'))
        item_box.add(toga.Label('Nama Barang: 🛍️', style=Pack(width=120, color='#1565C0', font_weight='bold')))
        self.item_input = toga.TextInput(style=Pack(flex=1))
        item_box.add(self.item_input)
        
        price_box = toga.Box(style=Pack(direction=ROW, margin=5, align_items='center'))
        price_box.add(toga.Label('Harga (Rp): 💵', style=Pack(width=120, color='#1565C0', font_weight='bold')))
        self.price_input = toga.TextInput(style=Pack(flex=1))
        price_box.add(self.price_input)
        
        priority_box = toga.Box(style=Pack(direction=ROW, margin=5, align_items='center'))
        priority_box.add(toga.Label('Prioritas: ⭐', style=Pack(width=120, color='#1565C0', font_weight='bold')))
        self.priority_input = toga.TextInput(style=Pack(flex=1))
        priority_box.add(self.priority_input)
        
        notes_box = toga.Box(style=Pack(direction=ROW, margin=5, align_items='center'))
        notes_box.add(toga.Label('Catatan: 📝', style=Pack(width=120, color='#1565C0', font_weight='bold')))
        self.notes_input = toga.TextInput(style=Pack(flex=1))
        notes_box.add(self.notes_input)
        
        add_btn = toga.Button('Tambah ✅', on_press=self.add_wishlist_item, style=Pack(margin=10, background_color='#2196F3', color='white', font_weight='bold'))
        
        box_add.add(item_box)
        box_add.add(price_box)
        box_add.add(priority_box)
        box_add.add(notes_box)
        box_add.add(add_btn)
        self.content_box.add(box_add)
        
        # List of wishlist items
        list_box = toga.Box(style=Pack(direction=COLUMN, margin=10, flex=1))
        list_box.add(toga.Label('Daftar Barang Wishlist 🛒📋', style=Pack(font_size=16, margin_bottom=10, color='#1976D2', font_weight='bold')))
        
        scroll_container = toga.ScrollContainer(style=Pack(flex=1))
        scroll_container.content = self.items_box
        
        list_box.add(scroll_container)
        self.content_box.add(list_box)
        self.refresh_list()

    def add_wishlist_item(self, widget):
        """Add a new wishlist item to the database."""
        cursor = self.app.conn.cursor()
        try:
            price = float(self.price_input.value) if self.price_input.value else 0.0
            cursor.execute("INSERT INTO wishlist (item_name, price, priority, notes) VALUES (?, ?, ?, ?)",
                           (self.item_input.value, price, self.priority_input.value, self.notes_input.value))
            self.app.conn.commit()
            self.item_input.value = ''
            self.price_input.value = ''
            self.priority_input.value = ''
            self.notes_input.value = ''
            self.refresh_list()
        except ValueError:
            self.app.main_window.error_dialog('Error', 'Harga harus berupa angka.')

    def refresh_list(self):
        """Refresh the list of wishlist items from the database."""
        for child in self.items_box.children[:]:
            self.items_box.remove(child)
        cursor = self.app.conn.cursor()
        cursor.execute("SELECT * FROM wishlist")
        for row in cursor.fetchall():
            item_box = toga.Box(style=Pack(direction=COLUMN, margin=10, background_color='#e3f2fd'))
            item_box.add(toga.Label(f"Nama Barang: 🛍️ {row[1]}", style=Pack(color='#333')))
            item_box.add(toga.Label(f"Harga (Rp): 💵 {row[2]:,.2f}", style=Pack(color='#333')))
            item_box.add(toga.Label(f"Prioritas: ⭐ {row[3]}", style=Pack(color='#333')))
            if row[4]:
                item_box.add(toga.Label(f"Catatan: 📝 {row[4]}", style=Pack(color='#333')))
            
            btn_box = toga.Box(style=Pack(direction=ROW))
            edit_btn = toga.Button('Edit ✏️', on_press=lambda w, r=row: self.app.show_edit_dialog('wishlist', r, self.refresh_list), style=Pack(margin=5, background_color='#FFA726', color='black', font_weight='bold'))
            delete_btn = toga.Button('Hapus 🗑️', on_press=lambda w, rid=row[0]: self.delete_item(rid), style=Pack(margin=5, background_color='#EF5350', color='white', font_weight='bold'))
            btn_box.add(edit_btn)
            btn_box.add(delete_btn)
            item_box.add(btn_box)
            self.items_box.add(item_box)

    def delete_item(self, item_id):
        """Delete a wishlist item from the database."""
        cursor = self.app.conn.cursor()
        cursor.execute("DELETE FROM wishlist WHERE id=?", (item_id,))
        self.app.conn.commit()
        self.refresh_list()

    def get_content(self):
        """Return the content box for this view."""
        return self.content_box
