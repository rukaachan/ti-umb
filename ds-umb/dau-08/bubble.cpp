#include <iostream>
using namespace std;

int main() {
  int x[] = {6, 2, 1, 3, 7};
  int j = sizeof(x) / sizeof(*x);
  int temp;

  cout << "x : ";
  for (int i = 0; i < j; i++) {
    cout << x[i] << " ";
  }

  cout << endl;

  // Proses Sorting
  for (int i = 0; i < j; i++) {
    int acak = 0;
    for (int h = 0; h < j - 1; h++) {
      if (x[h] > x[h + 1]) {
        temp = x[h];
        x[h] = x[h + 1];
        x[h + 1] = temp;
        acak++;
      }
    }

    if (acak == 0) {
      break; // Jika tidak ada pertukaran, array sudah terurut
    }
    cout << endl;
    cout << "tahap " << i + 1 << " : ";
    for (int a = 0; a < j; a++) {
      cout << x[a] << " ";
    }
  }

  cout << endl;
  cout << endl;
  cout << "Hasil Sorting : ";

  for (int a = 0; a < j; a++) {
    cout << x[a] << " ";
  }

  return 0;
}