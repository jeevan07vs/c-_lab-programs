#include <iostream>
using namespace std;

inline int minVal(int a, int b) {
    return (a < b) ? a : b;
}

inline int minVal(int a, int b, int c) {
    return minVal(minVal(a, b), c);
}

int main() {
    cout << "Min of 10, 4: " << minVal(10, 4) << endl;
    cout << "Min of 10, 4, 7: " << minVal(10, 4, 7) << endl;
    cout << "Min of 5, 5, 5: " << minVal(5, 5, 5) << endl;
    cout << "Min of -3, 8, -9: " << minVal(-3, 8, -9) << endl;
    return 0;
}