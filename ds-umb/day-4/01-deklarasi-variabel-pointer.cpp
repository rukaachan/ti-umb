#include <iostream>

using namespace std;

int main(){
    int nil1 = 5, nil2 = 15;
    int *ptr;

    ptr = &nil1;
    *ptr = 10;

    ptr = &nil2;
    *ptr = 20;

    cout << "Nilai 1 = " << nil1 << " dan nilai 2 = " << nil2<< endl;

    return 0;
}