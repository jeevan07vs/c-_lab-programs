/*#include <iostream>
#include <vector>
#include <string>

using namespace std;

int main()
{
    vector<string> msg {"Hello", "C++", "World", "from", "VS Code", "and the C++ extension!"};



    for (const string& word : msg)
    {
        cout << word << " ";
    }
    cout << endl;
}
*/


#include <iostream>
using namespace std;

int main() {
    string s = "Hello World";
    for (int i = 0; i < 5; i++)
        cout << s << endl;
    return 0;
}