#include <iostream>
using namespace std;

// Struktur node untuk binary tree
struct Node {
    char data;
    Node* left;
    Node* right;
    
    Node(char value) {
        data = value;
        left = right = NULL;
    }
};

// Fungsi untuk menyisipkan node baru ke dalam BST
Node* insert(Node* root, char value) {
    if (root == NULL) {
        return new Node(value);
    }

    if (value < root->data) {
        root->left = insert(root->left, value);
    } else if (value > root->data) {
        root->right = insert(root->right, value);
    }
    return root;
}

// Pre-order traversal: root -> left -> right
void preorder(Node* root) {
    if (root != NULL) {
        cout << root->data << " ";
        preorder(root->left);
        preorder(root->right);
    }
}

// In-order traversal: left -> root -> right
void inorder(Node* root) {
    if (root != NULL) {
        inorder(root->left);
        cout << root->data << " ";
        inorder(root->right);
    }
}

// Post-order traversal: left -> right -> root
void postorder(Node* root) {
    if (root != NULL) {
        postorder(root->left);
        postorder(root->right);
        cout << root->data << " ";
    }
}

int main() {
    Node* root = NULL;
    
    // Daftar huruf
    char nodes[] = {'Q', 'M', 'T', 'B', 'E', 'J', 'U', 'X', 'N', 'O', 'C', 'R',
                    'W', 'D', 'H', 'Y', 'G', 'Z', 'A', 'F', 'K', 'V', 'L', 'S', 'I', 'P'};

    int n = sizeof(nodes)/sizeof(nodes[0]);

    // Masukkan semua huruf ke dalam tree
    for (int i = 0; i < n; i++) {
        root = insert(root, nodes[i]);
    }

    cout << "Pre-order Traversal: ";
    preorder(root);
    cout << "\n";

    cout << "In-order Traversal: ";
    inorder(root);
    cout << "\n";

    cout << "Post-order Traversal: ";
    postorder(root);
    cout << "\n";

    return 0;
}
