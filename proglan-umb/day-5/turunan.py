class Unggas:
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
        pass

    def thr(self):
        pass

    def cetakpanen(self):
        panen = ""
        if self.usia > 10:
            panen = "sudah siap panen"
        else:
            panen = "belum siap panen"
        print(self.nama + " " + panen)

# Child
class Ayam(Unggas):
    def bersuara(self):
        suara = ''
        if self.sex == "betina":
            suara = "tekotek"
        else:
            suara = "kukuruyuk"
        print("Suara Ayam: " + suara)

    def thr(self):
        ekspresi = ''
        if self.sex == "jantan":
            for i in range(3):
                ekspresi = "mantul"
                print(ekspresi)
        else:
             for i in range(2):
                ekspresi = "ok"
                print(ekspresi)

# Child
class Bebek(Unggas):
     def bersuara(self):
        suara = ''
        if self.sex == "betina":
            suara = "tekotek"
        else:
            suara = "kukuruyuk"
        print("Suara Bebek: " + suara)

     def thr(self):
        ekspresi = ''
        if self.sex == "jantan":
             for i in range(3):
                ekspresi = "mantab"
                print(ekspresi)
        else:
             for i in range(3):
                ekspresi = "lancar"
                print(ekspresi)

print("\nAYAM")

ayam1 = Ayam("fauzi", 12, "putih", "betina")
ayam1.bersuara()
ayam1.thr()

print("==================================")

print("\nBEBEK")

bebek1 = Bebek("fauzi", 12, "putih", "jantan")
bebek1.bersuara()
bebek1.thr()