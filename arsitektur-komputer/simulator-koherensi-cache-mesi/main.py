import tkinter as tk
from tkinter import ttk, font, Toplevel

# Konfigurasi Konstanta
CACHE_SIZE = 4
NUM_CORES = 2
MEM_SIZE = 16

# State MESI
MODIFIED = 'M'
EXCLUSIVE = 'E'
SHARED = 'S'
INVALID = 'I'

class CacheLine:
    """Mewakili satu baris/blok dalam cache."""
    def __init__(self):
        self.state = INVALID
        self.tag = -1
        self.data = 0

class Cache:
    """Mewakili L1 Cache untuk satu core."""
    def __init__(self, cache_id):
        self.id = cache_id
        self.lines = [CacheLine() for _ in range(CACHE_SIZE)]

    def find_line(self, tag):
        for line in self.lines:
            if line.tag == tag:
                return line
        return None

    def get_empty_line(self):
        for line in self.lines:
            if line.state == INVALID:
                return line
        return self.lines[0]

class Core:
    """Mewakili satu core CPU dengan L1 Cache-nya."""
    def __init__(self, core_id, bus):
        self.id = core_id
        self.cache = Cache(core_id)
        self.bus = bus

    def read(self, address):
        tag = address % CACHE_SIZE
        line = self.cache.find_line(tag)
        if line is None or line.state == INVALID:
            self.bus.log(f"C{self.id}: Read Miss di Alamat {address}")
            self.bus.broadcast_read(self.id, address)
        else:
            self.bus.log(f"C{self.id}: Read Hit di Alamat {address} (State: {line.state})")
        return True

    def write(self, address):
        tag = address % CACHE_SIZE
        line = self.cache.find_line(tag)
        if line is None or line.state == INVALID:
            self.bus.log(f"C{self.id}: Write Miss di Alamat {address}")
            self.bus.broadcast_read_exclusive(self.id, address)
        elif line.state == SHARED:
            self.bus.log(f"C{self.id}: Write Hit di Alamat {address} (State: S -> M)")
            self.bus.broadcast_invalidate(self.id, address)
            line.state = MODIFIED
        elif line.state == EXCLUSIVE:
            self.bus.log(f"C{self.id}: Write Hit di Alamat {address} (State: E -> M)")
            line.state = MODIFIED
        elif line.state == MODIFIED:
            self.bus.log(f"C{self.id}: Write Hit di Alamat {address} (State: M)")
        return True

class SystemBus:
    """Mewakili bus sistem yang menghubungkan semua core dan memori."""
    def __init__(self, gui):
        self.cores = []
        self.memory = [0] * MEM_SIZE
        self.gui = gui
        self.bus_traffic = 0
        self.invalidations = 0
        self.cache_transfers = 0

    def add_core(self, core):
        self.cores.append(core)

    def log(self, message):
        self.gui.log_message(message)

    def broadcast_read(self, origin_core_id, address):
        tag = address % CACHE_SIZE
        self.bus_traffic += 1
        self.gui.animate_bus(f"C{origin_core_id}: BusRd (Addr {address})")
        shared_found = False
        for core in self.cores:
            if core.id != origin_core_id:
                line = core.cache.find_line(tag)
                if line and line.state != INVALID:
                    if line.state == MODIFIED:
                        self.log(f"  - C{core.id} (snoop): Punya data M. Writeback & kirim data.")
                        self.log(f"  - C{core.id}: State M -> S")
                        line.state = SHARED
                        self.cache_transfers += 1
                        shared_found = True
                        break
                    elif line.state in [EXCLUSIVE, SHARED]:
                        self.log(f"  - C{core.id} (snoop): Punya data {line.state}. State -> S.")
                        if line.state == EXCLUSIVE: self.cache_transfers += 1
                        line.state = SHARED
                        shared_found = True
        origin_core = self.cores[origin_core_id]
        new_line = origin_core.cache.get_empty_line()
        new_line.tag = tag
        if shared_found:
            self.log(f"C{origin_core_id}: Menerima data dari cache lain. State -> S")
            new_line.state = SHARED
        else:
            self.log(f"C{origin_core_id}: Menerima data dari memori. State -> E")
            new_line.state = EXCLUSIVE

    def broadcast_read_exclusive(self, origin_core_id, address):
        tag = address % CACHE_SIZE
        self.bus_traffic += 1
        self.gui.animate_bus(f"C{origin_core_id}: BusRdX (Addr {address})")
        for core in self.cores:
            if core.id != origin_core_id:
                line = core.cache.find_line(tag)
                if line and line.state != INVALID:
                    self.log(f"  - C{core.id} (snoop): Menerima BusRdX. State {line.state} -> I")
                    if line.state == MODIFIED: self.log(f"  - C{core.id}: Writeback data.")
                    line.state = INVALID
                    self.invalidations += 1
        origin_core = self.cores[origin_core_id]
        new_line = origin_core.cache.get_empty_line()
        new_line.tag = tag
        new_line.state = MODIFIED
        self.log(f"C{origin_core_id}: Menerima data. State -> M")

    def broadcast_invalidate(self, origin_core_id, address):
        tag = address % CACHE_SIZE
        self.bus_traffic += 1
        self.gui.animate_bus(f"C{origin_core_id}: Invalidate (Addr {address})")
        for core in self.cores:
            if core.id != origin_core_id:
                line = core.cache.find_line(tag)
                if line and line.state == SHARED:
                    self.log(f"  - C{core.id} (snoop): Menerima Invalidate. State S -> I")
                    line.state = INVALID
                    self.invalidations += 1

class SimulatorGUI(tk.Tk):
    """Kelas utama untuk antarmuka pengguna grafis."""
    def __init__(self):
        super().__init__()
        self.title("MESI Cache Coherence Simulator")
        self.geometry("1000x750")
        self.bus = SystemBus(self)
        self.cores = [Core(i, self.bus) for i in range(NUM_CORES)]
        for core in self.cores: self.bus.add_core(core)
        self.create_widgets()
        self.update_display()

    # --- FUNGSI YANG DIPERBARUI ---
    def show_user_guide(self):
        guide_window = Toplevel(self)
        guide_window.title("Panduan Penggunaan")
        guide_window.geometry("580x500") # Ukuran disesuaikan
        guide_window.transient(self)
        guide_window.grab_set()

        # Frame utama untuk konten dan tombol
        main_frame = ttk.Frame(guide_window, padding="10")
        main_frame.pack(expand=True, fill="both")

        # Frame untuk menampung Text widget dan Scrollbar
        text_container = ttk.Frame(main_frame)
        text_container.pack(expand=True, fill="both", pady=(0, 10))

        # Buat Scrollbar
        scrollbar = ttk.Scrollbar(text_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Buat Text widget
        guide_text_widget = tk.Text(
            text_container,
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
            font=("Arial", 10),
            padx=10,
            pady=10,
            spacing1=2, # Jarak antar baris
            spacing3=8, # Jarak antar paragraf
            borderwidth=0,
            highlightthickness=0, # Hilangkan border
            bg="#f0f0f0" # Samakan warna dengan background
        )
        guide_text_widget.pack(side=tk.LEFT, expand=True, fill="both")

        # Hubungkan scrollbar ke text widget
        scrollbar.config(command=guide_text_widget.yview)

        # Tambahkan teks panduan yang lebih lengkap
        guide_text = """Selamat datang di Simulator MESI!

1. Mode Interaktif:
   - Masukkan perintah di kotak input dengan format:
     C<id> <R/W> <Alamat>
   - Contoh: C0 R 100 (Core 0 membaca alamat 100)
   - Contoh: C1 W 50 (Core 1 menulis ke alamat 50)
   - Klik "Execute Step" untuk menjalankan perintah.

2. Membaca Visualisasi:
   - Private L1 Caches: Menampilkan status setiap blok cache untuk masing-masing core.
     Warna State:
       M (Modified)  = Merah
       E (Exclusive) = Oranye
       S (Shared)    = Hijau
       I (Invalid)   = Abu-abu

   - System Bus: Menampilkan transaksi bus yang sedang terjadi, seperti BusRd (baca) atau BusRdX (tulis).
   
   - Activity Log: Memberikan rincian narasi dari setiap langkah yang terjadi, termasuk hit/miss dan aktivitas snooping.

3. Menganalisis Statistik:
   - Bus Traffic: Total transaksi yang menggunakan bus. Semakin tinggi, semakin besar potensi bottleneck.
   - Invalidations: Jumlah blok cache yang dibatalkan. Ini adalah overhead langsung dari koherensi tulis.
   - Cache-to-Cache Transfers: Jumlah data yang ditransfer antar cache. Ini adalah optimisasi yang bagus karena menghindari akses ke memori utama yang lambat.

4. Skenario untuk Dicoba:
   - Dari Kosong ke Exclusive: C0 R 100
   - Dari Exclusive ke Shared: C1 R 100
   - Dari Shared ke Modified: C0 W 100
   - Konflik Tulis (Write Conflict): C1 W 100 (setelah skenario sebelumnya)
"""
        
        # Masukkan teks dan buat menjadi read-only
        guide_text_widget.config(state=tk.NORMAL) # Buka kunci untuk memasukkan teks
        guide_text_widget.insert(tk.END, guide_text.strip())
        guide_text_widget.config(state=tk.DISABLED) # Kunci kembali agar tidak bisa diedit

        # Tombol tutup
        close_button = ttk.Button(main_frame, text="Tutup", command=guide_window.destroy)
        close_button.pack()
    # --- AKHIR DARI FUNGSI YANG DIPERBARUI ---

    def show_about_info(self):
        about_window = Toplevel(self)
        about_window.title("Tentang Aplikasi")
        about_window.geometry("500x350")
        about_window.resizable(False, False)
        about_window.transient(self)
        about_window.grab_set()
        text_frame = ttk.Frame(about_window, padding="15")
        text_frame.pack(expand=True, fill="both")
        about_text = """
Simulator Koherensi Cache Multi-Core (MESI)

Aplikasi ini dirancang untuk memvisualisasikan dan
mendidik tentang cara kerja protokol koherensi cache MESI
dalam arsitektur komputer multi-core.

Fitur Utama:
- Simulasi arsitektur multi-core dengan cache privat.
- Visualisasi dinamis lalu lintas bus dan snooping.
- Analisis kuantitatif overhead koherensi.
- Mode interaktif untuk debugging dan pembelajaran.

Dibangun menggunakan Python dan Tkinter.
"""
        label = ttk.Label(text_frame, text=about_text, justify=tk.LEFT, font=("Arial", 10))
        label.pack(anchor="w", pady=10)
        close_button = ttk.Button(text_frame, text="Tutup", command=about_window.destroy)
        close_button.pack(pady=15)

    def create_widgets(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Bantuan", menu=help_menu)
        help_menu.add_command(label="Panduan Penggunaan", command=self.show_user_guide)
        help_menu.add_command(label="Tentang Aplikasi", command=self.show_about_info)
        help_menu.add_separator()
        help_menu.add_command(label="Keluar", command=self.quit)
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="Arial", size=10)
        bold_font = font.Font(family="Arial", size=12, weight="bold")
        mono_font = font.Font(family="Courier New", size=10)
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        caches_frame = ttk.LabelFrame(main_frame, text="Private L1 Caches", padding="10")
        caches_frame.pack(fill=tk.X, pady=5)
        self.cache_tables = []
        for i in range(NUM_CORES):
            core_frame = ttk.Frame(caches_frame)
            core_frame.pack(side=tk.LEFT, padx=20, fill=tk.X, expand=True)
            ttk.Label(core_frame, text=f"Core {i} Cache", font=bold_font).pack()
            cols = ("Block", "State", "Tag")
            table = ttk.Treeview(core_frame, columns=cols, show='headings', height=CACHE_SIZE)
            for col in cols:
                table.heading(col, text=col)
                table.column(col, width=80, anchor=tk.CENTER)
            self.cache_tables.append(table)
            table.pack()
        bus_frame = ttk.LabelFrame(main_frame, text="System Bus", padding="10")
        bus_frame.pack(fill=tk.X, pady=10)
        self.bus_label = ttk.Label(bus_frame, text="Idle", font=bold_font, foreground="green")
        self.bus_label.pack()
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        interactive_frame = ttk.LabelFrame(bottom_frame, text="Interactive Mode (Fitur 4)", padding="10")
        interactive_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        ttk.Label(interactive_frame, text="Command:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.cmd_entry = ttk.Entry(interactive_frame, width=25, font=mono_font)
        self.cmd_entry.grid(row=1, column=0, columnspan=2, pady=5)
        self.cmd_entry.insert(0, "C0 R 100")
        ttk.Label(interactive_frame, text="Format: C<id> <R/W> <Addr>", font=("Arial", 8)).grid(row=2, column=0, columnspan=2, sticky=tk.W)
        exec_button = ttk.Button(interactive_frame, text="Execute Step", command=self.execute_command)
        exec_button.grid(row=3, column=0, columnspan=2, pady=10)
        stats_frame = ttk.LabelFrame(bottom_frame, text="Coherence & Bus Statistics (Fitur 3)", padding="10")
        stats_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.stats_labels = {}
        stats = ["Bus Traffic", "Invalidations", "Cache-to-Cache Transfers"]
        for i, stat_name in enumerate(stats):
            ttk.Label(stats_frame, text=f"{stat_name}:").grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            self.stats_labels[stat_name] = ttk.Label(stats_frame, text="0", font=bold_font)
            self.stats_labels[stat_name].grid(row=i, column=1, sticky=tk.W, padx=5)
        log_frame = ttk.LabelFrame(bottom_frame, text="Activity Log (Fitur 2)", padding="10")
        log_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        log_scrollbar = ttk.Scrollbar(log_frame)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text = tk.Text(log_frame, wrap=tk.WORD, height=15, yscrollcommand=log_scrollbar.set, font=mono_font, bg="#f0f0f0")
        self.log_text.pack(fill=tk.BOTH, expand=True)
        log_scrollbar.config(command=self.log_text.yview)

    def execute_command(self):
        cmd = self.cmd_entry.get().strip().upper()
        parts = cmd.split()
        self.log_text.insert(tk.END, f"\n>>> EXECUTING: {cmd}\n", "command")
        self.log_text.tag_config("command", font=("Arial", 10, "bold"), foreground="blue")
        try:
            core_id, op, addr = int(parts[0][1:]), parts[1], int(parts[2])
            if not (0 <= core_id < NUM_CORES):
                self.log_message(f"Error: Core ID {core_id} tidak valid.")
                return
            if op not in ['R', 'W']:
                self.log_message(f"Error: Operasi '{op}' tidak valid. Gunakan 'R' atau 'W'.")
                return
            core = self.cores[core_id]
            if op == 'R': core.read(addr)
            elif op == 'W': core.write(addr)
        except (IndexError, ValueError) as e:
            self.log_message(f"Error: Perintah tidak valid. Format: 'C<id> <R/W> <Addr>'. Error: {e}")
        self.update_display()
        self.log_text.see(tk.END)

    def update_display(self):
        state_colors = {MODIFIED: "red", EXCLUSIVE: "orange", SHARED: "green", INVALID: "gray"}
        for i, table in enumerate(self.cache_tables):
            for item in table.get_children(): table.delete(item)
            core = self.cores[i]
            for j, line in enumerate(core.cache.lines):
                tag_display = str(line.tag) if line.tag != -1 else "---"
                values = (j, line.state, tag_display)
                table.insert("", tk.END, values=values, tags=(line.state,))
            for state, color in state_colors.items():
                table.tag_configure(state, background=color, foreground="white")
        self.stats_labels["Bus Traffic"].config(text=str(self.bus.bus_traffic))
        self.stats_labels["Invalidations"].config(text=str(self.bus.invalidations))
        self.stats_labels["Cache-to-Cache Transfers"].config(text=str(self.bus.cache_transfers))

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
    
    def animate_bus(self, message):
        self.bus_label.config(text=message, foreground="red")
        self.update()
        self.after(1000, lambda: self.bus_label.config(text="Idle", foreground="green"))

if __name__ == "__main__":
    app = SimulatorGUI()
    app.mainloop()