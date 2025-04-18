#include <iostream>
using namespace std;

int main(){
    int bilangan;

    // Contoh pengaksesan fungsi anggota di cin
    cout << "Ketikkan 4 digit: ";
    cin.ignore(2) >> bilangan;
    cout << "Bilangan: " << bilangan << endl;

    // Contoh pengaksesan anggota data di cin
    cout << "Isi cin.oct: " << cin.oct << endl;

    return 0;
}