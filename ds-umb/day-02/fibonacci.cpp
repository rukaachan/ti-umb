#include <iostream>

using namespace std;

int fibonacci(int n);

int main() {
    int angka, hasil;

    cout << "Menghitung Fibonacci Ke-N : ";
    cin >> angka;

    hasil = fibonacci(angka);
    cout << "Nilainya adalah: " << hasil << endl;

    return 0; 
}

int fibonacci(int n){
    // cout << "Fibonacci " << n << endl;
    if ((n == 0) || (n == 1)) {
        return n;
    } else {
        cout << "Fibonacci " << n << endl;

        return fibonacci(n - 1) + fibonacci(n - 2);
    }
}

// Dengan hal ini membuktikan bahwa
// Dalam melakukan fibonacci lebih dengan iterasi
// Dengan serentak pada looping ya