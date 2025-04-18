# Create a Class
# Membuat class dengan menggunakan string
# class MyClass:
#     x = 5
    
# print(MyClass)

# Class Object
# Di dalam sebuah class, terdapat sebuah atribut
# Dan juga terdapat sebuah method (aksi)

class Ayam:
    def __init__(self, nama, usia, warna, sex):
        self.nama = nama
        self.usia = usia
        self.warna = warna
        self.sex = sex

    def cetak(self):
        print("Hello Ayam " + self.nama)

    def cetakmsg(self, msg):
        print("Hello Ayam " + msg + " " + self.nama)
    
    def cetakusia(self):
        print("Umur ayam" + self.usia)

    def cetaksemua(self):
        print("Nama:" + self.nama + "Umur")

    def bersuara(self):
        suara = ''
        if self.sex == "betina":
            suara = "tekotek"
        else:
            suara = "kukuruyuk"
        print(self.nama + " " + suara)

    def cetakpanen(self):
        panen = ""
        if self.usia > 10:
            panen = "sudah siap panen"
        else:
            panen = "belum siap panen"
        print(self.nama + " " + panen)

ayam1 = Ayam("fikri", 12, "putih", "betina")
ayam1.cetak()
ayam1.cetakmsg("libur")

print(ayam1.nama)

# Tambahkan metode untuk mengganti usia
ayam1.usia = 20
print(ayam1.usia)

usia = str(ayam1.usia)
print(usia)

# Tambahkan metode untuk mencetak ayam secara lengkap
print(vars(ayam1))

# Tambahkan metode untuk ayam berbicara
ayam1.bersuara()

# Kondisi di atas 10 bulan, maka panen
ayam1.cetakpanen()