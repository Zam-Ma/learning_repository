#include <iostream>
#include <string>

using namespace std;

int main(){
    cout << "Enter the text for the pyramid: ";
    string message {};
    getline(cin, message);
    
    for (size_t i{}; i < message.size(); ++i){ //iterating message.size() number of times
        
        string  leading(message.size() - 1 - i, ' '); //leading of spaces before pyramide calculation
        cout    << leading << message.substr(0,i+1); //first part of the pyramid from the leading and thourgh the left part to it's middle - calculation and output
        
        for (int j= i-1; j >= 0; j--) //second part of the pyramid towards it's right end calculation and backwards output
            cout << message.at(j);
        cout << endl;
    }
    return 0;
}
