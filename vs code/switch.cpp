#include<iostream>
using namespace std;

int main(){
    char button;
    cout<<"input a character:";
    cin>>button;

    switch (button)
    {
        case'a':
        cout<<"hello"<<endl;
        break;
        case'b':
        cout<<"halo"<<endl;
        break;
        case'c':
        cout<<"ciao"<<endl;
        break;
        case'd':
        cout<<"namaste"<<endl;
        break;
    defaul:
         cout<<"i'm still learning more"<<endl;
         break;
    }
    return 0;
     
}