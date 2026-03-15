optimization/classical_solver.py
import random
import numpy as np

class ClassicalAnnealer:

    def solve(self, Q):

        n = max(max(i,j) for i,j in Q.keys()) + 1

        x = np.random.randint(0,2,n)

        T = 10

        def energy(v):

            e = 0

            for (i,j), w in Q.items():

                e += w*v[i]*v[j]

            return e

        best = x.copy()

        best_e = energy(x)

        while T > 0.1:

            i = random.randint(0,n-1)

            new = x.copy()

            new[i] = 1 - new[i]

            if energy(new) < energy(x):

                x = new

            if energy(x) < best_e:

                best = x.copy()
                best_e = energy(x)

            T *= 0.95

        return best, best_e