#include <iostream>
#include <string>
#include <cctype>
#include <map>
using namespace std;

class Wheel {
public:
    int left[26];
    int right[26];

    Wheel(int a[], int b[]) {
        for (int i = 0; i < 26; i++) {
            left[i] = a[i];
            right[i] = b[i];
        }
    }

    void turn() {
        int temp1 = left[25];
        int temp2 = right[25];
        for (int i = 25; i > 0; i--) {
            left[i] = left[i - 1];
            right[i] = right[i - 1];
        }
        left[0] = temp1;
        right[0] = temp2;
    }

    int getIndex(int x) {
        for (int i = 0; i < 26; i++) {
            if (left[x] == right[i]) {
                return i;
            }
        }
        return -1;
    }

    int getOriginalIndex(int x) {
        for (int i = 0; i < 26; i++) {
            if (right[x] == left[i]) {
                return i;
            }
        }
        return -1;
    }

    void setInitialPosition(int shift) {
        for (int i = 0; i < shift; i++) {
            turn();
        }
    }
};

class Reflector {
public:
    int reflect[26];

    Reflector() {
        int mapping[26] = { 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0 };
        for (int i = 0; i < 26; i++) {
            reflect[i] = mapping[i];
        }
    }

    int reflectIndex(int x) {
        return reflect[x];
    }
};

class Plugboard {
public:
    map<char, char> wiring;

    Plugboard() {
        for (char c = 'A'; c <= 'Z'; c++) {
            wiring[c] = c;
        }
    }

    void setPlugboard(string pairs) {
        for (size_t i = 0; i < pairs.length(); i += 2) {
            if (i + 1 < pairs.length()) {
                char a = toupper(pairs[i]);
                char b = toupper(pairs[i + 1]);
                if (a != b && wiring[a] == a && wiring[b] == b) {
                    wiring[a] = b;
                    wiring[b] = a;
                }
            }
        }
    }

    char swap(char c) {
        return wiring[c];
    }
};

int main() {
    int slowl[26] = { 24, 25, 26, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23 };
    int slowr[26] = { 21, 3, 15, 1, 19, 10, 14, 26, 20, 8, 16, 7, 22, 4, 11, 5, 17, 9, 12, 23, 18, 2, 25, 6, 24, 13 };
    int midl[26] = { 26, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25 };
    int midr[26] = { 20, 1, 6, 4, 15, 3, 14, 12, 23, 5, 16, 2, 22, 19, 11, 18, 25, 24, 13, 7, 10, 8, 21, 9, 26, 17 };
    int fastl[26] = { 26, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25 };
    int fastr[26] = { 14, 8, 18, 26, 17, 20, 22, 10, 3, 13, 11, 4, 23, 5, 24, 9, 12, 25, 16, 19, 6, 15, 21, 2, 7, 1 };

    string letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    while (true) {
        int shift1, shift2, shift3;
        cout << "Enter three initial rotor offsets (0-25), separated by spaces (-1 to exit): ";
        cin >> shift1;
        if (shift1 == -1) {
            cout << "Program exited." << endl;
            break;
        }
        cin >> shift2 >> shift3;
        cin.ignore();

        Plugboard plugboard;
        string plugboardPairs;
        cout << "Enter plugboard pairs (e.g. AB CD EF, press enter to skip): ";
        getline(cin, plugboardPairs);
        plugboard.setPlugboard(plugboardPairs);

        Wheel wheel1(slowl, slowr);
        Wheel wheel2(midl, midr);
        Wheel wheel3(fastl, fastr);
        Reflector reflector;

        wheel1.setInitialPosition(shift1);
        wheel2.setInitialPosition(shift2);
        wheel3.setInitialPosition(shift3);

        string input;
        cout << "Enter text: " << endl;
        getline(cin, input);

        string output = "";
        int count1 = 0, count2 = 0, count3 = 0;

        for (char c : input) {
            if (isdigit(c)) {
                output += c;
            }
            else if (isalpha(c)) {
                char uppercase = toupper(c);
                uppercase = plugboard.swap(uppercase);
                int index = letters.find(uppercase);
                if (index != string::npos) {
                    index = wheel1.getIndex(index);
                    index = wheel2.getIndex(index);
                    index = wheel3.getIndex(index);
                    index = reflector.reflectIndex(index);
                    index = wheel3.getOriginalIndex(index);
                    index = wheel2.getOriginalIndex(index);
                    index = wheel1.getOriginalIndex(index);
                    char encryptedChar = letters[index];
                    encryptedChar = plugboard.swap(encryptedChar);
                    output += encryptedChar;
                    count3++;
                    wheel3.turn();
                    if (count3 == 26) { count3 = 0; count2++; wheel2.turn(); }
                    if (count2 == 26) { count2 = 0; count1++; wheel1.turn(); }
                }
            }
        }
        cout << "Converted text: " << endl << output << endl;
    }
    return 0;
}
