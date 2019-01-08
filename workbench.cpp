#include <iostream>
using namespace std;

void for_loop();

int main()
{


    string s = "10=5+3+2";
    string delimiter = "+";

    size_t last = 0;
    size_t next = 0; 
    while ((next = s.find(delimiter, last)) != string::npos) 
    {
         cout << s.substr(last, next-last) << endl; 
         last = next + 1; 
    }
    cout << s.substr(last) << endl;
    for_loop();
    
    return 0;
} 

void for_loop()
{
    for (int i = 0; i < 10; i++)
    {
        cout << i;
    }
}