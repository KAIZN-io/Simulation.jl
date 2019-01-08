#include <iostream>
#include <string>
#include <typeinfo>
// fstream for handling files
#include <fstream>
#include <vector>
// #include <pqxx/stringconv>

#include "/usr/local/Cellar/postgresql/11.1/include/libpq/libpq-fs.h" 
#include <pqxx/pqxx>
using namespace std;
// using namespace pqxx;

/*
A C++ function called by another function can return a value.
empty parantheses mean that the main() function takes no information.
when you run a C++ program, execution always begins at the beginning of
the main() function.
*/


int test(int);
void csv();

int main()
{
    // a common practice is to use all uppercase for the name to help remind yoursef that MONTHS is a constant
    const float MONTHS = +4.2E-2;
    cout << MONTHS << endl;
    char name[10];

    // get the type of a variable
    cout << "get the type : " << typeid(MONTHS).name() << endl;
    
    unsigned int test_variable;
    cout << "Hello World" << endl;
    int number = test(3);
    cout << number << endl;

    string passwort_test = "master";
    cout << passwort_test << " : " << passwort_test.length() << endl;

    // conditional operator if else --> variable = (Condition) ? X : Y;
    int var_year;
    var_year = (MONTHS > 0) ? 1 : 2;
    cout << "conditional operator result : " << var_year << endl;

    // create an array --> like a list in python 
    short months[12];
    int yam[3] = {2,3,4};
    months[2] = 2;

    cout << "4 / 5 = " << (float) 4 / 5 << endl;
    // if statement
    if (months[2] == 3)
    {
        cout << "csv file will be generated" << endl;
        csv();
    }

    // a switch statement allows a var to be tested for equality against a list of values
    switch(months[2]) 
    {
        case 1:
            cout << "hi" << endl;
            break;
        case 2:
            cout << "hey" << endl;
            break;
        case 3:
            cout << "Hallo" << endl;
            break;
        default:
            cout << "not a nice number" << endl;
            
    } 
    // // work with 'type in' numbers
    // string numberGuessed;
    // int intNumberGuessed;
    // getline(cin, numberGuessed);
    // // stoi() transforms string to int
    // intNumberGuessed = stoi(numberGuessed);
    // cout << "your number with the factor 2 = " << intNumberGuessed * 2 << endl;
    return 0;
}

// void means that the function does not return a value
int test(int n)
{
    cout << "my number is: " << n << '!'  << endl;
    return n * 3;
}

void csv()
{
   // create .csv file
    ofstream myfile;
    myfile.open ("example.csv");
    myfile << "This is the first cell in the first column.\n";
    myfile << "b,b,c,\n";
    myfile << "c,s,v,\n";
    myfile << "1,2,3.4536\n";
    myfile << "semi;colon";
    myfile.close();
}

