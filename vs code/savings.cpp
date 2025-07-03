#include<iostream>
using namespace std;
 
int main(){
    int saving;
    cin>>saving;
    if(saving>7000) {
        if(saving>10000){
            cout<<"roadtrip with neha\n";
        }else {
            cout<<"shopping with neha\n";
        }
        
    }else if(saving>2000){
        cout<<"rashmi\n";
    }else {
        cout<<"friends\n";
    }
}