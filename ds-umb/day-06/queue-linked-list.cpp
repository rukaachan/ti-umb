#include <iostream>
using namespace std;

// Node berisi ID order
struct Node
{
    int id;
    Node *next;
    Node(int i) : id(i), next(nullptr) {}
};

class Queue
{
    Node *front = nullptr;
    Node *rear = nullptr;

public:
    void enqueue(int id)
    {
        Node *n = new Node(id);
        if (!rear)
            front = n;
        else
            rear->next = n;
        rear = n;
        cout << "Enqueue: " << id << "\n";
    }
    void dequeue()
    {
        if (!front)
        {
            cout << "Queue kosong\n";
            return;
        }
        int id = front->id;
        Node *t = front;
        front = front->next;
        if (!front)
            rear = nullptr;
        delete t;
        cout << "Dequeue: " << id << "\n";
    }
    void display() const
    {
        cout << "Queue [Front->]: ";
        for (Node *cur = front; cur; cur = cur->next)
            cout << cur->id << " ";
        cout << "\n";
    }
};

int main()
{
    Queue q;
    int pilihan, id;
    do
    {
        cout << "\n=== Queue Menu ===\n";
        cout << "1. Enqueue\n";
        cout << "2. Dequeue\n";
        cout << "3. Tampilkan Queue\n";
        cout << "0. Keluar\n";
        cout << endl;
        cout << "Pilihan: ";
        cin >> pilihan;
        switch (pilihan)
        {
        case 1:
            cout << "Masukkan ID order: ";
            cin >> id;
            q.enqueue(id);
            break;
        case 2:
            q.dequeue();
            break;
        case 3:
            q.display();
            break;
        case 0:
            cout << "Keluar program Queue.\n";
            break;
        default:
            cout << "Pilihan tidak valid.\n";
        }
    } while (pilihan != 0);
    return 0;
}