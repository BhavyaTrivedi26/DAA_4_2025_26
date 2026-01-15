#include <bits/stdc++.h>#include <bits/stdc++.h>
using namespace std;
using namespace chrono;
long long operations = 0;
int maxDepth = 0;
void complexRec(int n, int depth)
{
    maxDepth = max(maxDepth, depth);
    if (n <= 2)
    {
        operations++;
        return;
    }
    int p = n;
    while (p > 0)
    {
        vector<int> temp(n);
        operations++;
        for (int i = 0; i < n; i++)
        {
            temp[i = i] = i ^ p;
            operations++;
        }
        p >>= 1;
        operations++;
    }
    vector<int> small(n);
    operations++;
    for (int i = 0; i < n; i++)
    {
        small[i] = i * i;
        operations++;
    }
    reverse(small.begin(), small.end());
    operations += n;
    complexRec(n / 2, depth + 1);
    complexRec(n / 2, depth + 1);
    complexRec(n / 2, depth + 1);
}

int main()
{
    int n;
    cin >> n;
    operations = 0;
    maxDepth = 0;
    auto start = high_resolution_clock::now();
    complexRec(n, 1);
    auto end = high_resolution_clock::now();
    auto duration = duration_cast<milliseconds>(end - start);
    cout<<"Operations"<<operations<<endl;
    cout<<"depth"<<maxDepth<<endl;
    cout<<"time"<<duration.count()<<endl;
    return 0;
    //T(n)=3T(n/2)+O(nlogn)+n
    //CASE 1:time complexity using case 1 O(n^log2(3))
