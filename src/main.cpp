#include <iostream>
#include <fstream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <cmath>
#include <string>
#include <sstream>

#include "omp.h"

class Spins
{
private:
    int levels[5];
    size_t L;
    std::vector<bool> spins; 
public:
    
    Spins(double beta, size_t L)
    {
        //srand(time(NULL));
        srand(0);
        
        spins = std::vector<bool>(L*L);
        this->L = L;
        
        //std::cout << "probabilities:\n";
        for (int i = 0; i < 5; i++)
        {
            int n = 2 * i - 4;
            double p = std::min(1.0, exp( - beta * 2 * n));
            levels[i] = p * RAND_MAX;
            //std::cout << p << "\n";
        }
        //std::cout << "\n";
        
        for (size_t i = 0; i < L*L; i++)
        {
            spins[i] = true;
        }
    }
    
    ~Spins()
    {
        
    }
    
    void metropolisStep()
    {
        int spinIndex = rand() % (L * L);
        
        int sum = 0;
        int i = spinIndex / L;
        int j = spinIndex % L;
        
        sum += spins[i * L + ((j - 1) % L + L) % L];
        sum += spins[i * L + (j + 1) % L];
        sum += spins[(((i - 1) % L + L) % L) * L + j];
        sum += spins[((i + 1) % L) * L + j];
        
        sum = (sum - 2) * (2 * spins[spinIndex] - 1) + 2;
        bool flip = rand() < levels[sum];
        
        spins[spinIndex] = spins[spinIndex] != flip;
    }
    
    double m()
    {
        uint32_t sum = 0;
        for (int i = 0; i < L*L; i++)
            sum += spins[i];
        return 2.0 * sum / L / L - 1;
    }
    
    friend std::ostream& operator<<(std::ostream& os, Spins spins)
    {
        for (int i = 0; i < spins.L; i++)
        {
            for (int j = 0; j < spins.L; j++)
            {
                os << (spins.spins[i * spins.L + j] ? "x" : "o");
            }
            os << "\n";
        }
        return os;
    }
};


void simulate(size_t L, double beta)
{
    std::cout.precision(10);
    
    std::vector<double> ms;
    Spins* ice = new Spins(beta, L);
    
    for (int j = 0; j < 1024 * 16; j++)
    {
        for (int i = 0; i < L*L; i++)
        {
            ice->metropolisStep();
        }
        double m = ice->m();
        //std::cout << m << "\n";
        ms.push_back(m);
    }
    
    delete ice;
    
    std::fstream file;
    std::ostringstream filename;
    filename << "L=" << L << "_beta=" << beta << ".txt";
    file.open(filename.str(), std::ios::out);
    
    if (!file.is_open())
    {
        std::cerr << "File couldn't be opened!\n";
        exit(-1);
    }
    file.precision(10);
    
    for (double m : ms)
    {
        file << m << "\n";
    }
}

int main(int argc, char** arg)
{
    double beta = 0.45;
    
    #pragma omp parallel for
    for (uint32_t i = 1; i <= 16; i++)
    {
        size_t L = 64 * i;
        simulate(L, beta);
        std::cout << "i=" << i << " done.\n";
    }
    
    return 0;
}