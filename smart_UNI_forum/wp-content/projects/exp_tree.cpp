//============================================================================
// Name        : exp_tree.cpp
// Author      : Darekar Amey Chandrakant
// Description : Expression Tree
//============================================================================
#include<iostream>
#include<stdlib.h>
#include<string.h>
#define MAX 30

using namespace std;


class node{
	char data;
	node *left, *right;

	public:
	friend class tree;
	friend class Stack;
	node(char val){
		this->data = val;
		this->left = NULL;
		this->right = NULL;
	}

	char getvalue(){
		return this->data;
	}
	void setvalue(int val){
		this->data = val;
	}

};

class Stack
{
	int top;
	node *a[MAX];

public :

	Stack(){
		top=-1;
 	}

	int is_full(){
		if(top == MAX-1){
			return 1;
		}
		return 0;
	}

	int is_empty(){
		if(top == -1){
			return 1;
		}else{
			return 0;
		}
	}

	void push(node *x){
		if(!is_full()){
			top++;
			a[top] = x;
		}
	}

	node *pop(){
		if(!is_empty()){
			return a[top--];
		}
		return NULL;
	}
};

class CharStack
{
	int top;
	char a[MAX];

public :

	CharStack(){
		top=-1;
 	}

	int is_full(){
		if(top == MAX-1){
			return 1;
		}
		return 0;
	}

	int is_empty(){
		if(top == -1){
			return 1;
		}else{
			return 0;
		}
	}

	void push(char x){
		if(!is_full()){
			top++;
			a[top] = x;
		}
	}

	char pop(){
		if(!is_empty()){
			return a[top--];
		}else{
			cout<<"Invalid Expression!";
			exit(1);
		}
	}

	char peak(){
		return a[top];
	}

};



class tree{
	node *root;

	public:

	void __init(){
			root = NULL;
	}

	tree(){
		__init();
	}

	int is_operator(char data){
		switch (data){
			case '+':
			case '-':
			case '*':
			case '/':
			case '^':
				return 1;
			default:
				return 0;
		}
	}

	int prcd(char data){
			switch (data){
				case '+':
				case '-':
					return 2;
				case '*':
				case '/':
					return 4;
				case '^':
					return 5;
				default:
					return 0;
			}
		}

	int conv_into_postf(char infix[],char postfix[]) {
		int i,j=0;
		char symbol;
		CharStack stack;
		stack.push('#');

		for(i=0;i<strlen(infix);i++) {
			symbol=infix[i];
			if(is_operator(symbol)==0) {
				postfix[j]=symbol;
				j++;
			}else {
				if(symbol=='(') {
					stack.push(symbol);
				}else if(symbol==')') {
					while(stack.peak()!='(') {
						postfix[j]=stack.pop();
						j++;
					}
					stack.pop();//pop out (.
				}else if(is_operator(symbol) == 1){
					if(prcd(symbol)>prcd(stack.peak())) {
						stack.push(symbol);
					}else {
						while(prcd(symbol)<=prcd(stack.peak())) {
							postfix[j]=stack.pop();
							j++;
						}
						stack.push(symbol);
					}
				}else{
					cout<<"Character Exception!"<<symbol<<endl<<endl;
				}
			}
		}

		while(stack.peak()!='#') {
			postfix[j]=stack.pop();
			j++;
		}
		postfix[j]='\0';
		return j;
	}

	void create(char *exp){
		int i, length;
		char symbol,post_exp[40];
		length = conv_into_postf(exp,post_exp);
		Stack s;
		for(i=0;i<length;i++){
			symbol = post_exp[i];
			if(!is_operator(symbol)){
				s.push(new node(symbol));
		}else if(is_operator(symbol)){
				node *temp = new node(symbol);
				temp->right = s.pop();
				temp->left = s.pop();
				s.push(temp);
			}else{
				cout<<"Character Exception!"<<symbol<<endl<<endl;
			}
		}
		root = s.pop();
	}

	void traverse(){
			if(root){
				cout<<endl<<"Preorder :\t";
				pre_trav(root);
				cout<<endl<<"Inorder :\t";
				in_trav(root);
				cout<<endl<<"Postorder :\t";
				post_trav(root);
			}else{
				cout<<endl<<"Tree is Empty"<<endl;
			}
		}

	void pre_trav(node *root){
		if(root){
			cout<<root->getvalue()<<"\t";
			pre_trav(root->left);
			pre_trav(root->right);
		}
	}

	void in_trav(node *root){
		if(root){
			in_trav(root->left);
			cout<<root->getvalue()<<"\t";
			in_trav(root->right);
		}
	}

	void post_trav(node *root){
		if(root){
			post_trav(root->left);
			post_trav(root->right);
			cout<<root->getvalue()<<"\t";
		}
	}

};

int main(){
	tree t;
	int choice;
	char exp[40],post_exp[40];
	while(1){
		cout<<"\n1. Enter Expression\n2. Traverse Tree\n3. clear tree \n4. Exit\n";
		cin>>choice;
		switch(choice){
		case 1:
			cout<<"Enter Infix Expression: \t";
			cin>>exp;
			t.create(exp);
			cout<<"Tree Created!\n";
			break;
		case 2:
			cout<<"Traversing the tree"<<endl;
			t.traverse();
			break;
		case 3:
			t.__init();
			break;
		case 4:
			exit(1);
		}
	}
	return 0;
}
