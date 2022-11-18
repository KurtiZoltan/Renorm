#include <iostream>
#include <vector>
#include <cmath>

void wolff(std::vector<bool>& spins, double p, unsigned int L)
{
    //choose random spin 
    int n = rand() % (L*L);
    bool sc = spins[n];
    spins[n] = !spins[n];
    std::vector<unsigned int> list, newlist;
    list.push_back(n);
    
    while (!list.empty())
    {
        for (unsigned int s : list)
        {
            int i = s / L;
            int j = s % L;
            
            int k = ((i-1) % L + L) % L;
            int l = ((j+0) % L + L) % L;
            int neighbor = k * L + l;
            if ((spins[neighbor] == sc) && (rand() < p * RAND_MAX))
            {
                newlist.push_back(neighbor);
                spins[neighbor] = !spins[neighbor];
            }
            
            k = ((i+1) % L + L) % L;
            l = ((j+0) % L + L) % L;
            neighbor = k * L + l;
            if ((spins[neighbor] == sc) && (rand() < p * RAND_MAX))
            {
                newlist.push_back(neighbor);
                spins[neighbor] = !spins[neighbor];
            }
            
            k = ((i+0) % L + L) % L;
            l = ((j-1) % L + L) % L;
            neighbor = k * L + l;
            if ((spins[neighbor] == sc) && (rand() < p * RAND_MAX))
            {
                newlist.push_back(neighbor);
                spins[neighbor] = !spins[neighbor];
            }
            
            k = ((i+0) % L + L) % L;
            l = ((j+1) % L + L) % L;
            neighbor = k * L + l;
            if ((spins[neighbor] == sc) && (rand() < p * RAND_MAX))
            {
                newlist.push_back(neighbor);
                spins[neighbor] = !spins[neighbor];
            }
        }
        list = newlist;
        newlist.clear();
    }
}

double magnetization(std::vector<bool> spins, int L)
{
    int sum = 0;
    for (bool s : spins) sum += 2 * s - 1;
    return static_cast<double>(sum) / (L*L);
}

int main(int argc, char** arg)
{
    srand(time(0));
    int L = 1024;
    double beta = 0.5;
    std::vector<bool> spins = std::vector<bool>(L*L);
    for (int i = 0; i < L*L; i++) spins[i] = true;
    
    double p = 1 - exp(-2 * beta);
    for (int i = 0; i < 1024; i++)
    {
        wolff(spins, p, L);
        //std::cout << std::abs(magnetization(spins, L)) << "\n";
        std::cout << magnetization(spins, L) << "\n";
    }
    
    return 0;
}
