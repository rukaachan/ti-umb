#include <iostream>

using namespace std;

int main() {
    char array[5];
    char *p;

    p = array; *p = 'a';
    p++;

    *p = 'b';
    p = &array[2];

    *p = 'c';
    p = array + 3;

    *p = 'd';
    p = array;

    *(p+4) = 'e';

    for (int n=0; n<5; n++) {
        cout << array[n] << ", ";
    }

    cout << endl;

    return 0;
}