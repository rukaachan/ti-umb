#include <iostream>

using namespace std;
int main() {
    // Membuat Array

    // Pemberian nilai array bisa seperti ini
    int nilai[5] = {0,1,2,3,4};

    // atau seperti ini
    nilai[0] = 0;
    nilai[1] = 1;
    nilai[2] = 2;
    nilai[3] = 3;
    nilai[4] = 4;

    cout << &nilai[0] << " Nilainya adalah: " << nilai[0] << endl;
    cout << &nilai[1] << " Nilainya adalah: " << nilai[1] << endl;
    cout << &nilai[2] << " Nilainya adalah: " << nilai[2] << endl;
    cout << &nilai[3] << " Nilainya adalah: " << nilai[3] << endl;
    cout << &nilai[4] << " Nilainya adalah: " << nilai[4] << endl;


    cout << "=======\n";

    // Manipulasi Array
    
    // Contoh dengan pointer

    // Mengubah index ke 2 adders ke 2
    // Menjadi nilai 6
    int *ptr = nilai;
    *(ptr + 2) = 6;

    // Kemudian cara lainnya
    // Index ke-3, merubah nilai ya
    nilai[3] = 7;

    cout << &nilai[0] << " Nilainya adalah: " << nilai[0] << endl;
    cout << &nilai[1] << " Nilainya adalah: " << nilai[1] << endl;
    cout << &nilai[2] << " Nilainya adalah: " << nilai[2] << endl;
    cout << &nilai[3] << " Nilainya adalah: " << nilai[3] << endl;
    cout << &nilai[4] << " Nilainya adalah: " << nilai[4] << endl;

    cout << "=======\n";
    cout << "Ukuran array: " << sizeof(nilai) << endl;

    // Di aray tidak terdapat penjumlahan total dari member array
    // Maka di perlukan perhitungan tersendiri

    cout << "Jumlah Member Array: " << sizeof(nilai)/sizeof(int) << endl;

    return 0; 
}
