#include<iostream>
using namespace std;

/* A binary tree node has data, pointer to children */
struct Node {
	Node* left;
	Node* right;
	int data;

	Node(int val) {
		left=NULL;
		right=NULL;
		data=val;
	}
};

/* Recursive approach */
Node* findLCA(Node* root, int n1, int n2) {
    // Base case
    if (root == NULL) return NULL;

    // If n1 or n2 is the root, return root
    if (root->data == n1 || root->data == n2)
        return root;

    // Look for keys in left and right subtrees
    Node *left_lca  = findLCA(root->left, n1, n2);
    Node *right_lca = findLCA(root->right, n1, n2);

    if (left_lca==NULL && right_lca==NULL)  return NULL;
    if (left_lca!=NULL && right_lca!=NULL)  return root;

    // Otherwise check if left subtree or right subtree is LCA
    return (left_lca != NULL) ? left_lca: right_lca;
}

int main() {
	Node* root = new Node(3);
	root->left = new Node(5);
	root->right = new Node(1);
	root->left->left = new Node(6);
	root->left->right = new Node(2);
	root->right->left = new Node(0);
	root->right->right = new Node(8);
	root->left->right->left = new Node(7);
	root->left->right->right = new Node(4);
	cout<<"LCA of 5 and 1 is "<<findLCA(root,5,1)->data<<endl;
	cout<<"LCA of 6 and 2 is "<<findLCA(root,6,2)->data<<endl;
	cout<<"LCA of 4 and 8 is "<<findLCA(root,4,8)->data<<endl;
	cout<<"LCA of 2 and 4 is "<<findLCA(root,2,4)->data<<endl;
	cout<<"LCA of 3 and 7 is "<<findLCA(root,3,7)->data;
	return 0;
}
