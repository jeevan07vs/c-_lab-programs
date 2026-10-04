#include <iostream>
#include <cctype>
using namespace std;

int main() 
{
      string s;
    cout << "Enter a sentence: ";
    getline(cin, s);

    int vowels = 0, consonants = 0;

    for (int i = 0; i < s.length(); i++)
    
    {
       char ch = tolower(s[i]);

        if (isalpha(ch)) 
        {
       if (ch == 'a' || ch == 'e' || ch == 'i' || ch == 'o' || ch == 'u')
       vowels++;
       else
        consonants++;
        }
    }

    cout << "Vowels: " << vowels << endl;
    cout << "Consonants: " << consonants << endl;

    return 0;
}