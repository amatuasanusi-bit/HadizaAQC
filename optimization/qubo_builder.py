class QUBOBuilder:

    def build(self, energy_matrix):

        Q = {}

        n = len(energy_matrix)

        for i in range(n):

            for j in range(n):

                if energy_matrix[i][j] != 0:

                    Q[(i, j)] = energy_matrix[i][j]

        return Q