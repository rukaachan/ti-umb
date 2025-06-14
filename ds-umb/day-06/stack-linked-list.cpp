#include <iostream>
using namespace std;

// Node berisi ID barang
struct Node
{
    int id;
    Node *next;
    Node(int i) : id(i), next(nullptr) {}
};

class Stack
{
    Node *top = nullptr;

public:
    void push(int id)
    {
        Node *n = new Node(id);
        n->next = top;
        top = n;
        cout << "Push: " << id << "\n";
    }
    void pop()
    {
        if (!top)
        {
            cout << "Stack kosong\n";
            return;
        }
        int id = top->id;
        Node *t = top;
        top = top->next;
        delete t;
        cout << "Pop : " << id << "\n";
    }
    void display() const
    {
        cout << "Stack [Top->]: ";
        for (Node *cur = top; cur; cur = cur->next)
            cout << cur->id << " ";
        cout << "\n";
    }
};

int main()
{
    Stack st;
    int pilihan, id;
    do
    {
        cout << "\n=== Stack Menu ===\n";
        cout << "1. Push\n";
        cout << "2. Pop\n";
        cout << "3. Tampilkan Stack\n";
        cout << "0. Keluar\n";
        cout << endl;
        cout << "Pilihan: ";
        cin >> pilihan;
        switch (pilihan)
        {
        case 1:
            cout << "Masukkan ID barang: ";
            cin >> id;
            st.push(id);
            break;
        case 2:
            st.pop();
            break;
        case 3:
            st.display();
            break;
        case 0:
            cout << "Keluar program Stack.\n";
            break;
        default:
            cout << "Pilihan tidak valid.\n";
        }
    } while (pilihan != 0);
    return 0;
}