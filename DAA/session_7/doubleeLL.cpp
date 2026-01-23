#include <iostream>
using namespace std;

class Node {
public:
    int data;
    Node* prev;
    Node* next;

    Node(int val){
        data = val;
        prev = NULL;
        next = NULL;
    }
};

class DoublyLinkedList {
public:
    Node* head;

    DoublyLinkedList(){
        head = NULL;
    }

    void insertAtEnd(int val){
        Node* newNode = new Node(val);
        if(head == NULL){
            head = newNode;
            return;
        }
        Node* temp = head;
        while(temp->next){
            temp = temp->next;
        }
        temp->next = newNode;
        newNode->prev = temp;
    }

    void insertAtStart(int val){
        Node* newNode = new Node(val);
        if(head == NULL){
            head = newNode;
            return;
        }
        newNode->next = head;
        head->prev = newNode;
        head = newNode;
    }

    void deleteNode(int val){
        Node* temp = head;
        while(temp){
            if(temp->data == val){
                if(temp->prev)
                    temp->prev->next = temp->next;
                else
                    head = temp->next;

                if(temp->next)
                    temp->next->prev = temp->prev;

                delete temp;
                return;
            }
            temp = temp->next;
        }
    }

    void display(){
        Node* temp = head;
        while(temp){
            cout << temp->data << " ";
            temp = temp->next;
        }
        cout << endl;
    }
};
