#include <iostream>
#include <vector>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <fstream>

void wolff(std::vector<bool> &spins, double p, unsigned int L)
{
    int n = rand() % (L * L);
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

            int k = ((i - 1) % L + L) % L;
            int l = ((j + 0) % L + L) % L;
            int neighbor = k * L + l;
            if ((spins[neighbor] == sc) && (rand() < p * RAND_MAX))
            {
                newlist.push_back(neighbor);
                spins[neighbor] = !spins[neighbor];
            }

            k = ((i + 1) % L + L) % L;
            l = ((j + 0) % L + L) % L;
            neighbor = k * L + l;
            if ((spins[neighbor] == sc) && (rand() < p * RAND_MAX))
            {
                newlist.push_back(neighbor);
                spins[neighbor] = !spins[neighbor];
            }

            k = ((i + 0) % L + L) % L;
            l = ((j - 1) % L + L) % L;
            neighbor = k * L + l;
            if ((spins[neighbor] == sc) && (rand() < p * RAND_MAX))
            {
                newlist.push_back(neighbor);
                spins[neighbor] = !spins[neighbor];
            }

            k = ((i + 0) % L + L) % L;
            l = ((j + 1) % L + L) % L;
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

double magnetization(std::vector<bool> spins)
{
    int sum = 0;
    for (bool s : spins)
        sum += 2 * s - 1;
    return static_cast<double>(sum) / spins.size();
}

double var(const std::vector<double> &ms)
{
    double a = 0;
    double b = 0;
    for (double m : ms)
    {
        a += m * m;
        b += std::abs(m);
    }
    a /= ms.size();
    b /= ms.size();
    return (a - b * b) * ms.size() / (ms.size() - 1);
}

std::vector<double> block(const std::vector<double> &ms)
{
    double alpha = 1 / std::sqrt(2);
    std::vector<double> newms;
    for (int i = 0; 2 * i + 1 < ms.size(); i++)
    {
        newms.push_back((ms[2 * i] + ms[2 * i + 1]) * alpha);
    }
    return newms;
}

int main(int argc, char **argv)
{
    // usage: cluster [beta] [L] []
    if (argc != 3)
    {
        std::cout << "usage: cluster [beta] [L]\n";
        return 0;
    }
    double beta = atof(argv[1]);
    int L = atoi(argv[2]);
    
    srand(time(0));
    
    std::vector<bool> spins = std::vector<bool>(L * L);
    for (int i = 0; i < L * L; i++)
        spins[i] = true;
    double p = 1 - exp(-2 * beta);
    double m = MAXFLOAT;
    while (m > magnetization(spins))
    {
        m = magnetization(spins);
        for (int i = 0; i < 10; i++) wolff(spins, p, L);
    }

    std::vector<double> ms;
    int i = 0;
    int imax = 128;
    while (true)
    {
        for (; i < imax; i++)
        {
            wolff(spins, p, L);
            double m = std::abs(magnetization(spins));
            ms.push_back(m);
        }
        
        std::vector<double> tempm = ms;
        std::vector<double> chis;
        while (tempm.size() >= 32)
        {
            double chi = var(tempm) * L * L;
            chis.push_back(chi);
            tempm = block(tempm);
        }
        
        bool chifound = false;
        //find first decrease in chi --> chis[j-1] > chis[j]
        int j = 1;
        for (; j < chis.size(); j++) if (chis[j-1] > chis[j]) break;
        //find next increase in chi --> chis[k-1] < chis[k]
        int k = j;
        for (; k < chis.size(); k++) if (chis[k-1] < chis[k]) 
        {
            chifound = true;
            break;
        }
        if (chifound)
        {
            // std::cout << "chi=" << chis[j-1] << " " << chis[k-1] << "\nimax=" << imax << "\nchis:\n";
            // for (double c : chis) std::cout << c << "\n";
            std::cout.precision(10);
            std::cout << (chis[j-1] + chis[k-1]) / 2;
            break;
        }
        imax *= 2;
    }
    
    // std::fstream file;
    // file.open("a.out", std::ios::out);
    // if (!file.is_open())
    // {
    //     std::cerr << "File couldn't be opened!\n";
    //     exit(-1);
    // }
    // file.precision(10);
    // for (double m : ms) file << m << "\n";
    // file.close();

    return 0;
}
