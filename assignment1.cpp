#include <iostream>
using namespace std;

inline int square(int x) { return x * x; }
double area(double r) { return 3.14 * r * r; }
int area(int l, int b) { return l * b; }
double area(double b, double h) { return 0.5 * b * h; }

int main() {
    cout << "cube = " << square(1) << endl;
    cout << "cuboid l=3 b=3 h=3=" << area(3, 3) << endl;
    cout << "cylinder r=2 h=2=" << area(2.0, 2.0) << endl;
    return 0;
}
    