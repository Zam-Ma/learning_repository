#include <iostream>
#include <cstring>
#include "Mystring.h"

/* No-args constructor
 * 1. Null out a pointer.
 * 2. Allocate a space for a pointer on heap.
 * 3. Because there was no arguments, the pointer when dereferenced will lead to a null character (finishing the string)
 */
Mystring::Mystring()
    : str{nullptr} {
        str = new char[1];
        *str = '\0';
}
    
/* Overloaded constructor
 * 1. Null out a pointer.
 * 2. Handle a scenario when the object is initiated with an empty string, by doing the same code as a no args constructor.
 * 3. If the input is not a null pointer then allocate space for the length of the given string + 1 for the null character.
 * 4. then copy the string over from the input to the member variable.
 */
Mystring::Mystring(const char *source_string)
    : str{nullptr} {
        if (source_string==nullptr) {
            str = new char[1];
            *str = '\0';
        } else {
            str = new char[std::strlen(source_string) + 1];
            std::strcpy(str, source_string);
        }
}

/* Copy constructor
 * 1. Null out a pointer.
 * 2. Allocate space on heap for the length of the input member variable + 1 for the null character.
 * 3. Copy from the input member variable to 'this' member variable.
 */
Mystring::Mystring(const Mystring &source)
    : str{nullptr} {
        str = new char[std::strlen(source.str) +1];
        std::strcpy(str, source.str);
}

/* Move constructor
 * 1. Steal source pointer to this pointer.
 * 2. Null out the source pointer.
 */
Mystring::Mystring(Mystring &&source)
    : str{source.str} {
        source.str = nullptr;
    }
    
/* Destructor
 * 1. Delete the whole string of a class object member variable.
 */
Mystring::~Mystring() {
    delete [] str;
}

/* Copy assignment
 * 1. Handle if right hand side refrence is the same as 'this' by returning dereferenced this.
 * 2. Delete whole 'this'.
 * 3. Allocate space on heap for the whole length of the right hand side member variable + 1 for the null character.
 * 4. Copy right hand side member variable to the 'this' member variable.
 * 5. Return dereferenced 'this'.
 */
Mystring &Mystring::operator=(const Mystring &rhs) {
    if (this == &rhs) 
        return *this;
    else {
    str = new char[std::strlen(rhs.str) + 1];
    std::strcpy(str, rhs.str);
    return *this;
    }
}

/* Move assignment
 * 1. Handle if right hand side refrence is the same as 'this' by returning dereferenced this.
 * 2. Steal the pointer of the right hand side member variable and assign it to current member variable.
 * 3. Null out the pointer of the right hand side member variable
 * 4. Return dereferenced 'this'.
 */
Mystring &Mystring::operator=(Mystring &&rhs) {
    if (this == &rhs)
        return *this;
    else {
        str = rhs.str;
        rhs.str = nullptr;
    return *this;
    }
}

/* Display method
 * 1. Display the pointer (if it's a pointer to the 'char' member variable it will display the whole string by default - its std::cout object function)
 * 2. Display length of the string.
 */
void Mystring::display() const {
    std::cout << str << " : " << get_length() << std::endl;
}

/* getters
 * 1. Return 'strlen' of the string.
 */
int Mystring::get_length() const {
    return std::strlen(str);
}

/* 1. Return the string.
 */
const char *Mystring::get_str() const {
    return str;
}
/* Overloaded insertion operator
 * 1. Take the output stream object and output the string of the right hand side object.
 * 2. Return output stream object so you can chain multiple output statements (the result of the output stream is output stream (becomes left hand side of another <<)).
 */
std::ostream &operator<<(std::ostream &os, const Mystring &rhs) {
    os << rhs.str;
    return os;
}

/* Overloaded extraction operator
 * 1. Create a character buffer for the input on _heap_.
 * 2. Insert the characters into the buffer.
 * 3. Assing object initiated with the buffer to the right hand side object.
 * 4. Delete the whole buffer.
 * 5. Return the insertion object so you can chain multiple insertions.
 */
std::istream &operator>>(std::istream &in, Mystring &rhs) {
    char *buff = new char[1000];
    in >> buff;
    rhs = Mystring{buff};
    delete [] buff;
    return in;
}

/* Overloaded unary minus operator which creates a temporary object of lower case string.
 * 1. Crate a temporary buffer for the string length on the heap.
 * 2. Copy the string to the buffer.
 * 3. Loop through each of the characters of the buffer up to the length of the buffer and use std::tolower function to make all letter lowercase
 * 4. Initialize a new temporary object with the created string on the buffer (heap)
 * 5. Delete the buffer (no longer needed. The object has 'taken' the string)
 * 6. Return the temporary object. 
 */
Mystring Mystring::operator-() const{
    char *buff = new char [std::strlen(str)+1];
    std::strcpy(buff, str);
    for (size_t i=0; i <std::strlen(buff); i++)
        buff[i] = std::tolower(buff[i]);
    Mystring temp{buff};
    delete [] buff;
    return temp;
}
/* Overloaded equality operator which compares two strings.
 * 1. return the comparison to 0 of the comparison of left hand side reference to an object and right hand side reference to an object which are both constant (as we dont want to change either)
 * Compare the strings by using std::strcmp function.
 */
bool Mystring::operator==(const Mystring &rhs) const {
    return (std::strcmp(str, rhs.str) == 0);
}

/* Overloaded NOT equality operator which compares two strings.
 * 1. Use std::strcmp to return a comparison and compare it to 0 (std::strcmp returns a 0 value if lhs and rhs strings are equal)
 */
bool Mystring::operator!=(const Mystring &rhs) const{
    return !(std::strcmp(str, rhs.str) == 0);
}
/* Overloaded less then operator returns true if lhs is lexically less then rhs
 * 1. Use std::strcmp to return a comparison and compare less then to 0 (std::strcmp returns a negative value if lhs appears before rhs in lexicographical order)
 */
bool Mystring::operator<(const Mystring &rhs) const{
    return (std::strcmp(str, rhs.str) < 0);
}

/* Overloaded more then operator returns true if lhs is lexically less then rhs
 * 1. Use std::strcmp to return a comparison and compare more then to 0 (std::strcmp returns a postivie value if lhs appears after rhs in lexicographical order)
 */
bool Mystring::operator>(const Mystring &rhs) const{
    return (std::strcmp(str, rhs.str) > 0);
}

/* Concatentation
 * 1. Allocate a character buffer on heap for the length of the both strings.
 * 2. Copy left hand side string in to the character buffer by using std::strcpy.
 * 3. Concatentate right hand side string to the buffer by using std::strcat.
 * 4. Create a temporary object intialized with the buffer.
 * 5. Delete the whole buffer.
 * 6. Return the temporary object.
 */
Mystring Mystring::operator+(const Mystring &rhs) const {
    char *buff = new char[std::strlen(str)+std::strlen(rhs.str)+1];
    std::strcpy(buff, str);
    std::strcat(buff, rhs.str);
    Mystring temp{buff};
    delete [] buff;
    return temp;
}

/* Concatenate and store the result in the lhs object
 * 1. Use concatentation algorithm from operator+.
 * 2. Return *this.
 */
Mystring &Mystring::operator+=(const Mystring &rhs) {
    *this = *this + rhs;
    return *this;
}

/* Multiplying the string x times.
 * 1. Create a buffer for x number of times of the strlen of the string + 1 for the null character.
 * 2. strcat left hand side string to the buffer exactly x time with a for loop.
 * 3. Initialize the temporary object with the buffer.
 * 4. Delete the whole buffer.
 * 5. Return the temporary object.
 */
Mystring Mystring::operator*(int number) const{
    char *buff = new char[(std::strlen(str)*number) + 1];
    std::strcpy(buff, str);
    for (int i = 1; i < number; i++)
        std::strcat(buff, str);
    Mystring temp{buff};
    delete [] buff;
    return temp;
}

/* Multiplying the string x times and storing the result in the left hand side object.
 * 1. Use overloaded operator*.
 * 2. Return *this.
 */
Mystring &Mystring::operator*=(int number) {
    *this = *this * number;
    return *this;
}

/* Pre-increment ++ overloaded operator - makes all letter uppercase
 * 1. Iterate through the length of the sources string and make each letter uppercase by using the std::toupper.
 * 2. Return dereferenced 'this'.
 */
Mystring &Mystring::operator++() {
    for (size_t i=0; i < std::strlen(str); i++)
        str[i] = std::toupper(str[i]);
    return *this;
}

/* Post-increment ++ overloaded operator - makes all letter uppercase
 * 1. Create a temporary object initiated with the current '*this' object.
 * 2. Callout pre-increment.
 * 2. Return the temporary object.
 */
Mystring Mystring::operator++(int) {
    Mystring temp{*this};
    operator++();
    return temp;
}

/* Pre-increment -- overloaded operator - rewrites the string backwars
 * 1. Create a buffer for a string of the source's string length on the heap.
 * 2. Iterate through the buffer coming from the beginning to the end of the string and iterate simultanously through the sources string from the end to the beginning
 * and while doing so - assign the values to the positions in the string.
 * 3. Add null terminated character at the end of the buffer's string
 * 4. Assign the buffer string to the source object.
 * 5. Delete the whole buffer.
 * 6. Return the source object.
 */
Mystring &Mystring::operator--() {
    char *buff = new char[std::strlen(str)+1];
    for (size_t i=0, y=strlen(str)-1; i < std::strlen(str); i++, y--)
        buff[i] = str[y];
    buff[std::strlen(str)] = '\0';
    *this = buff;
    delete [] buff;
    return *this;
}

/* Post-increment -- overloaded operator - rewrites the string backwars
 * 1. Create a temporary object initiated with source.
 * 2. Call pre incremented -- operator
 * 3. Return the temporary object (with old values before the increment)
 */
Mystring Mystring::operator--(int) {
    Mystring temp{*this};
    operator--();
    return temp;
}
