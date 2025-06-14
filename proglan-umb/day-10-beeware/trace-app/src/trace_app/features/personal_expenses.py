"""
Personal Expenses feature for TraceApp.
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from datetime import datetime

class PersonalExpensesView:
    def __init__(self, app):
        self.app = app
        self.content_box = toga.Box(style=Pack(direction=COLUMN, margin=15, flex=1, background_color='#ffe0e0'))
        self.items_box = toga.Box(style=Pack(direction=COLUMN, margin=5))
        self.setup_ui()

    def setup_ui(self):
        """Set up the UI for Personal Expenses."""
        title = toga.Label('Pengeluaran Pribadi 💰', style=Pack(font_size=22, margin_bottom=15, color='#D32F2F', font_weight='bold'))
        self.content_box.add(title)
        
        # Add new expense entry
        box_add = toga.Box(style=Pack(direction=COLUMN, margin=10, background_color='#ffcdd2'))
        box_add.add(toga.Label('Tambah Data Baru ➕', style=Pack(font_size=16, margin_bottom=10, color='#C2185B', font_weight='bold')))
        
        date_box = toga.Box(style=Pack(direction=ROW, margin=5, align_items='center'))
        date_box.add(toga.Label('Tanggal: 📅', style=Pack(width=120, color='#AD1457', font_weight='bold')))
        self.date_input = toga.DateInput(value=datetime.now().date(), style=Pack(flex=1))
        date_box.add(self.date_input)
        
        amount_box = toga.Box(style=Pack(direction=ROW, margin=5, align_items='center'))
        amount_box.add(toga.Label('Jumlah (Rp): 💵', style=Pack(width=120, color='#AD1457', font_weight='bold')))
        self.amount_input = toga.TextInput(style=Pack(flex=1))
        amount_box.add(self.amount_input)
        
        category_box = toga.Box(style=Pack(direction=ROW, margin=5, align_items='center'))
        category_box.add(toga.Label('Kategori: 🏷️', style=Pack(width=120, color='#AD1457', font_weight='bold')))
        self.category_input = toga.TextInput(style=Pack(flex=1))
        category_box.add(self.category_input)
        
        desc_box = toga.Box(style=Pack(direction=ROW, margin=5, align_items='center'))
        desc_box.add(toga.Label('Deskripsi: 📝', style=Pack(width=120, color='#AD1457', font_weight='bold')))
        self.desc_input = toga.TextInput(style=Pack(flex=1))
        desc_box.add(self.desc_input)
        
        add_btn = toga.Button('Tambah ✅', on_press=self.add_expense_entry, style=Pack(margin=10, background_color='#E91E63', color='white', font_weight='bold'))
        
        box_add.add(date_box)
        box_add.add(amount_box)
        box_add.add(category_box)
        box_add.add(desc_box)
        box_add.add(add_btn)
        self.content_box.add(box_add)
        
        # List of expense entries
        list_box = toga.Box(style=Pack(direction=COLUMN, margin=10, flex=1))
        list_box.add(toga.Label('Daftar Pengeluaran 💸📊', style=Pack(font_size=16, margin_bottom=10, color='#D32F2F', font_weight='bold')))
        
        scroll_container = toga.ScrollContainer(style=Pack(flex=1))
        scroll_container.content = self.items_box
        
        list_box.add(scroll_container)
        self.content_box.add(list_box)
        self.refresh_list()

    def add_expense_entry(self, widget):
        """Add a new expense entry to the database."""
        cursor = self.app.conn.cursor()
        try:
            amount = float(self.amount_input.value)
            date_str = self.date_input.value.isoformat() if self.date_input.value else datetime.now().date().isoformat()
            cursor.execute("INSERT INTO personal_expenses (date, amount, category, description) VALUES (?, ?, ?, ?)",
                           (date_str, amount, self.category_input.value, self.desc_input.value))
            self.app.conn.commit()
            self.amount_input.value = ''
            self.category_input.value = ''
            self.desc_input.value = ''
            self.refresh_list()
        except ValueError:
            self.app.main_window.error_dialog('Error', 'Jumlah harus berupa angka.')

    def refresh_list(self):
        """Refresh the list of expense entries from the database."""
        for child in self.items_box.children[:]:
            self.items_box.remove(child)
        cursor = self.app.conn.cursor()
        cursor.execute("SELECT * FROM personal_expenses ORDER BY date DESC")
        for row in cursor.fetchall():
            item_box = toga.Box(style=Pack(direction=COLUMN, margin=10, background_color='#ffebee'))
            item_box.add(toga.Label(f"Tanggal: 📅 {row[1]}", style=Pack(color='#333')))
            item_box.add(toga.Label(f"Jumlah (Rp): 💵 {row[2]:,.2f}", style=Pack(color='#333')))
            item_box.add(toga.Label(f"Kategori: 🏷️ {row[3]}", style=Pack(color='#333')))
            if row[4]:
                item_box.add(toga.Label(f"Deskripsi: 📝 {row[4]}", style=Pack(color='#333')))
            
            btn_box = toga.Box(style=Pack(direction=ROW))
            edit_btn = toga.Button('Edit ✏️', on_press=lambda w, r=row: self.app.show_edit_dialog('personal_expenses', r, self.refresh_list), style=Pack(margin=5, background_color='#FFA726', color='black', font_weight='bold'))
            delete_btn = toga.Button('Hapus 🗑️', on_press=lambda w, rid=row[0]: self.delete_item(rid), style=Pack(margin=5, background_color='#EF5350', color='white', font_weight='bold'))
            btn_box.add(edit_btn)
            btn_box.add(delete_btn)
            item_box.add(btn_box)
            self.items_box.add(item_box)

    def delete_item(self, item_id):
        """Delete an expense entry from the database."""
        cursor = self.app.conn.cursor()
        cursor.execute("DELETE FROM personal_expenses WHERE id=?", (item_id,))
        self.app.conn.commit()
        self.refresh_list()

    def get_content(self):
        """Return the content box for this view."""
        return self.content_box
