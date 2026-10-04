#include <iostream>
#include <string>
using namespace std;

int main()
{
    string s;
    cout<<"Enter a word:";
    cin >> s;

    cout << "Length :"<< s.length() << endl;
    cout << "upper :";
    for (char c:s) cout << (char)toupper(c);
    cout << endl;

    bool Pal = true;
    for (size_t i=0, j=s .size()-1; i<j; i++, --j)

    if (s[i] != s[j] )
    {
        Pal = false; break; 
    }
    cout <<s<< (Pal ?"Is":" is Not ")<<" a Palindrome\n";

    size_t pos = s.find ("an");
    if (pos != string :: npos) cout <<" 'an' found at index" <<pos<< endl;
    else cout<<"'an' not found\n";
    return 0;
} 