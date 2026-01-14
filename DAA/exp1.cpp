#include <bits/stdc++.h>
using namespace std;
using namespace std::chrono;

void complexRec(int n) {
    int count=0;
    if (n <= 2) {
       return;
   }

   int p = n;
   while (p > 0) {
       vector<int> temp(n);
       for (int i = 0; i < n; i++) {
           temp[i] = i ^ p;
           
       }
       p >>= 1;
       count++;
   }

   vector<int> small(n);
   for (int i = 0; i < n; i++) {
       small[i] = i * i;
       count++;
   }

   if (n % 3 == 0) {
       reverse(small.begin(), small.end());
       count++;
   } else {
       reverse(small.begin(), small.end());
       count++;
   }

   complexRec(n / 2);
   complexRec(n / 2);
   complexRec(n / 2);
   cout<<count;
}
// recursive relation = 3T(n/2) + n*log(n) + n
// Complexity = O(n ^ (log (base b)a))

int main(){
    auto start = high_resolution_clock::now();
    complexRec(20);
        auto end =  high_resolution_clock::now();
        auto duration = duration_cast<milliseconds>(end-start);
        cout<<duration;

}
