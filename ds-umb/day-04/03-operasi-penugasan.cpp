#include <iostream>

using namespace std;

int main(){
    float nilai, *p1, *p2;
    nilai = 14.54;
    cout << "nilai = " << nilai << ", alamatnya" << &nilai << endl;

    p1 = &nilai;
    p2 = p1; // operasi pemberian nilai, berarti alamat x2 sama dengan x1
    cout << "nilai p1 = " << p2 << ", p1 menunjuk alamat " << p1 << endl << endl;

    // pada awalnya p2 masih dangling pointer
    cout << "mula-mulai nilai p2 = " << *p2 << ", p2 menunjuk alamat " << p2 << endl;
    cout << "sekarang nilai p2 = " << *p2 << ", p2 menunjuk alamat " << p2 << endl;

    return 0;
}