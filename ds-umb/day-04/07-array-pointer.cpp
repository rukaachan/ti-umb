#include <iostream>

using namespace std;

int main(){
    int tgl_lahir[] = { 13, 9, 1982 };
    int *ptgl;
    ptgl = tgl_lahir; // ptgl berisi alamat array

    cout << "Diakses dengan pointer" << endl;
    cout << "Tanggal = " << *ptgl << endl;
    cout << "Bulan = " << *(ptgl + 1) << endl;
    cout << "Tahun = " << *(ptgl + 2) << endl;

    cout << endl;

    cout << "Diakses dengan array biasa" << endl;
    cout << "Tanggal = " << tgl_lahir[0] << endl;
    cout << "Bulan = " << tgl_lahir[1] << endl;
    cout << "Tahun = " << tgl_lahir[2] << endl;

    return 0;
}