#include <iostream>
using namespace std;

#define max 5
string data[max];
int top = 0;

bool isEmpty()
{
  if (top == 0)
  {
    return true;
  }
  else
  {
    return false;
  }
}

bool isFull()
{
  if (top >= max)
  {
    return true;
  }
  else
  {
    return false;
  }
}

void display()
{
  if (!isEmpty())
  {
    cout << "Data Tersimpan: " << endl;
    for (int a = 0; a < top; a++)
    {
      cout << a + 1 << ". " << data[a] << endl;
    }

    if (isFull())
    {
      cout << "Stack Penuh" << endl;
    }

    cout << endl;
  }
  else
  {
    cout << "Data Tidak Tersedia !\n"
         << endl;
  }
}

void push()
{
  if (!isFull())
  {
    cout << "Masukkan Data: ";
    cin >> data[top];
    top++;
  }
}

void pop()
{
  if (!isEmpty())
  {
    top--;
  }
}

int main()
{
  int pil;
  string isi;

stack:
  system("cls");
  display();
  cout
      << "Menu Utama\n1. Push\n2. Pop\nPilih: ";
  cin >> pil;

  if (pil == 1)
  {
    system("cls");
    push();
    goto stack;
  }
  else if (pil == 2)
  {
    pop();
    goto stack;
  }
  system("cls");
  cout << "Program Selesai";
}