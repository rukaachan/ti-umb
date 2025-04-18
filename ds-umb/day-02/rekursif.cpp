#include <iostream>

using namespace std;

// Fungsi Iterasi
// Analoginya adalah dengan membuka seluruh kotak, pada waktu bersamaan (aksi)
int pangkatIterasi(int a, int b){
    int hasil = a;
    cout << "Hasil: " << hasil << endl;

    for (int i = 1; i < b; i++) {
        cout << "For Hasil: " << hasil << endl;
        cout << "For a: " << a << endl;
        hasil = hasil * a;
    }
    return hasil;
}

int pangkatRekrusif(int a, int b){
    if (b == 1) {
        cout << "Akhir Batasan Rekrusif" << endl;
        return a;
    } else {
        cout << "Rekrusif: " << a << endl;
        return a * pangkatRekrusif(a, (b -1));
    }    
}

int main() {
    int a, b;

    cout << "Angka: ";
    cin >> a;

    cout << "Pangkat: ";
    cin >> b;

    cout << "Hasil Iterasi: " << pangkatIterasi(a, b) << endl;

    cout << "======\n";

    cout << "Hasil Rekursif: " << pangkatRekrusif(a, b) << endl;
    return 0; 
}
