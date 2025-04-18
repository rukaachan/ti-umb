#include <iostream>

using namespace std;

int main(){
    int nilai1 = 4;
    int nilai2 = 5;    
    float nilai3 = 3.5;
    char nama[11] = "abcdefghij";

    int *nilai_p1 = &nilai1;
    int *nilai_p2 = &nilai2;
    char *nilai_p4 = nama;
    float *nilai_p3 = &nilai3;
    
    cout << "nilai 1 = " << *nilai_p1 << ", alamat1 = " << &nilai_p1 << endl;
    cout << "nilai 2 = " << *nilai_p2 << ", alamat2 = " << &nilai_p2 << endl;
    cout << "nilai 3 = " << *nilai_p3 << ", alamat3 = " << &nilai_p3 << endl;
    cout << "nilai 4 = " << *nilai_p4 << ", alamat4 = " << &nilai_p4 << endl;

    return 0;
}