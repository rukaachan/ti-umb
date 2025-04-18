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

print("AYAM")

ayam1 = Ayam("fauzi", 12, "putih", "betina")
ayam1.bersuara()
ayam1.thr()

print("==================================")

print("BEBEK")

bebek1 = Bebek("fauzi", 12, "putih", "jantan")
bebek1.bersuara()
bebek1.thr()

# Linked List

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def delete(self, key):
        current = self.head
        previous = None
        
        while current is not None and current.data.nama != key:
            previous = current
            current = current.next

        if current is None:
            print(f"Element {key} not found.")
            return

        if previous is None:
            self.head = current.next
        else:
            previous.next = current.next

    def reverse(self):
        previous = None
        current = self.head

        while current is not None:
            next_node = current.next
            current.next = previous
            previous = current
            current = next_node

        self.head = previous

    def display(self):
        current = self.head
        if not current:
            print("The list is empty.")
            return

        while current:
            current.data.bersuara()
            current = current.next
        print()

print("==================================")

print("Linked List Insert")        

linked_list = LinkedList()
linked_list.insert(Ayam("zonar", 12, "putih", "betina"))
linked_list.insert(Bebek("ikhan", 12, "putih", "jantan"))
linked_list.insert(Bebek("kolam", 12, "putih", "jantan"))
linked_list.display()

print("==================================")

print("Linked List Delete")

linked_list.delete('zonar')
linked_list.display()