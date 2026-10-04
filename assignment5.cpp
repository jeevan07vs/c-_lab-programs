#include <iostream>
#include <cctype>
using namespace std;

bool isAnagram(string s1, string s2) 
{
    for (int i = 0; i < s1.length(); i++)
    s1[i] = tolower(s1[i]);
    for (int i = 0; i < s2.length(); i++)
    s2[i] = tolower(s2[i]);
    if (s1.length() != s2.length())
    return false;
    int freq[26] = {0};

    for (int i = 0; i < s1.length(); i++)
    freq[s1[i] - 'a']++;
    for (int i = 0; i < s2.length(); i++)
    freq[s2[i] - 'a']--;
    for (int i = 0; i < 26; i++) 
    {
    if (freq[i] != 0)
    return false;
    }

    return true;
}

int main()  
{
    string word1, word2;

    cout << "Enter first word: ";
    cin >> word1;
    cout << "Enter second word: ";
    cin >> word2;

    if (isAnagram(word1, word2))
   cout << word1 << " and " << word2 << " are anagrams." << endl;
    else
  cout << word1 << " and " << word2 << " are NOT anagrams." << endl;

 return 0;
}