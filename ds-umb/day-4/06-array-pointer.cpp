#include <iostream>

using namespace std;

const int arraySize = 5;

int main(){
    int A [arraySize];
    const int *pInt = A;
    for (int i=0; i < arraySize; i++) {
        cout << "Input array: ";
        cin >> A[i]; 
    }

    for (int n=0; n < arraySize; n++) {
        cout << "Element [" << n << "] = " << *(pInt) << endl;
        pInt++;
    }

    return 0;
}