import pytest

import numpy as np

from geneal.applications.tsp.travelling_salesman_problem import TravellingSalesmanProblemSolver
from tests.mock_fixtures.mock_fixtures import mock_matplotlib, mock_logging
from tests.applications.fixtures.tsp_test_fixture import G


class TestTravellingSalesmanProblemSolver:
    @pytest.mark.parametrize(
        "problem_type, expected_result",
        [
            pytest.param(
                int,
                np.array([[ 9,  2,  6,  1,  8,  3, 10,  5,  4,  7],
                           [ 1,  2,  9,  6,  4,  5,  8, 10,  7,  3],
                           [10,  3,  1,  7,  9,  6,  4,  8,  2,  5],
                           [ 2,  8,  7,  3,  9,  1,  4,  5,  6, 10],
                           [ 2,  6,  5,  9,  1,  8,  7,  4,  3, 10]]),
                id="initialize_population",
            ),
        ],
    )
    def test_initialize_population(self, problem_type, expected_result):

        pop_size = 5
        n_genes = len(G.nodes)

        tsp_solver = TravellingSalesmanProblemSolver(
            G,
            pop_size=pop_size,
            random_state=42,
        )

        population = tsp_solver.initialize_population(
            tsp_solver.pop_size, tsp_solver.n_genes
        )

        assert population.shape[0] == pop_size
        assert population.shape[1] == n_genes

        for route in population:
            assert len(set(route)) == n_genes

        assert np.allclose(population, expected_result, rtol=1e-05)

    @pytest.mark.parametrize(
        "crossover_pt, expected_first_offspring, expected_second_offspring",
        [
            pytest.param(
                np.array([0, 5]),
                np.array([1, 3, 4, 7, 2, 6, 5, 8]),
                np.array([5, 2, 3, 8, 1, 6, 4, 7]),
                id="crossover_points=0-5",
            ),
            pytest.param(
                np.array([2, 3]),
                np.array([2, 3, 4, 8, 1, 6, 7, 5]),
                np.array([1, 4, 3, 7, 2, 5, 8, 6]),
                id="crossover_points=2-3",
            ),
            pytest.param(
                np.array([3, 7]),
                np.array([1, 6, 4, 7, 2, 5, 8, 3]),
                np.array([7, 2, 5, 8, 1, 6, 4, 3]),
                id="crossover_points=3-7",
            ),
            pytest.param(
                np.array([1, 1]),
                np.array([5, 2, 3, 8, 1, 6, 4, 7]),
                np.array([1, 3, 4, 7, 2, 5, 8, 6]),
                id="crossover_points=1-1",
            ),
        ],
    )
    def test_create_offspring(
        self, crossover_pt, expected_first_offspring, expected_second_offspring
    ):

        pop_size = 5

        tsp_solver = TravellingSalesmanProblemSolver(
            G,
            pop_size=pop_size,
            random_state=42,
        )

        first_parent = np.array([1, 3, 4, 7, 2, 5, 8, 6])
        sec_parent = np.array([5, 2, 3, 8, 1, 6, 4, 7])

        first_offspring = tsp_solver.create_offspring(
            first_parent, sec_parent, crossover_pt, "first"
        )

        second_offspring = tsp_solver.create_offspring(
            sec_parent, first_parent, crossover_pt, "second"
        )

        assert np.allclose(first_offspring, expected_first_offspring, rtol=1e-5)
        assert np.allclose(second_offspring, expected_second_offspring, rtol=1e-5)

    def test_get_worst_gene(self):

        pop_size = 5

        tsp_solver = TravellingSalesmanProblemSolver(G, random_state=42)

        route = np.arange(1, len(G.nodes))

        np.random.shuffle(route)

        assert tsp_solver.find_worst_gene(route) == 7

    @pytest.mark.parametrize(
        "mutation_strategy, expected_mutated_population",
        [
            pytest.param(
                "2-opt",
                np.array([
                    [ 9,  2,  6,  1,  8,  3, 10,  5,  4,  7],
                    [ 1,  2,  9,  6,  4,  5,  8, 10,  7,  3],
                    [ 7,  9,  6,  1,  3, 10,  5,  2,  8,  4],
                    [ 2,  8,  7,  3,  9,  1,  4,  5,  6, 10],
                    [ 7,  4,  3, 10,  2,  6,  8,  1,  9,  5]
                ]),
                id="2-opt",
            ),
            pytest.param(
                "random_swap",
                np.array([
                    [ 9,  2,  6,  1,  8,  3, 10,  5,  4,  7],
                    [ 1,  2,  9,  6,  4,  5,  8, 10,  7,  3],
                    [10,  3,  1,  5,  9,  6,  4,  8,  2,  7],
                    [ 2,  8,  7,  3,  9,  1,  4,  5,  6, 10],
                    [ 3,  6,  5,  9,  1,  8,  7,  4,  2, 10]
                ]),
                id="random_swap",
            ),
            pytest.param(
                "random_gene_around_nearest_neighbour",
                np.array([
                    [ 9,  2,  6,  1,  8,  3, 10,  5,  4,  7],
                    [ 1,  2,  9,  6,  4,  5,  8, 10,  7,  3],
                    [10,  3,  1,  7,  9,  6,  4,  8,  2,  5],
                    [ 2,  8,  7,  3,  9,  1,  4,  5,  6, 10],
                    [ 2,  6,  5,  9,  1,  8,  7,  4,  3, 10]
                ]),
                id="random_gene_around_nearest_neighbour",
            ),
            pytest.param(
                "random_gene_nearest_neighbour",
                np.array([
                    [ 9,  2,  6,  1,  8,  3, 10,  5,  4,  7],
                    [ 1,  2,  9,  6,  4,  5,  8, 10,  7,  3],
                    [10,  1,  3,  7,  9,  6,  4,  8,  2,  5],
                    [ 2,  8,  7,  3,  9,  1,  4,  5,  6, 10],
                    [ 2,  6,  5,  9,  8,  7,  1,  4,  3, 10]
                ]),
                id="random_gene_nearest_neighbour",
            ),
            pytest.param(
                "worst_gene_random",
                np.array([
                    [ 9,  2,  6,  1,  8,  3, 10,  5,  4,  7],
                    [ 1,  2,  9,  6,  4,  5,  8, 10,  7,  3],
                    [10,  8,  1,  7,  9,  6,  4,  3,  2,  5],
                    [ 2,  8,  7,  3,  9,  1,  4,  5,  6, 10],
                    [ 2,  6,  1,  9,  5,  8,  7,  4,  3, 10]
                ]),
                id="worst_gene_random",
            ),
            pytest.param(
                "worst_gene_nearest_neighbour",
                np.array([
                    [ 9,  2,  6,  1,  8,  3, 10,  5,  4,  7],
                    [ 1,  2,  9,  6,  4,  5,  8, 10,  7,  3],
                    [10,  8,  1,  7,  9,  6,  4,  3,  2,  5],
                    [ 2,  8,  7,  3,  9,  1,  4,  5,  6, 10],
                    [ 2,  6,  1,  9,  5,  8,  7,  4,  3, 10]
                ]),
                id="worst_gene_nearest_neighbour",
            ),
            pytest.param(
                "random_inversion",
                np.array([
                    [ 9,  2,  6,  1,  8,  3, 10,  5,  4,  7],
                    [ 1,  2,  9,  6,  4,  5,  8, 10,  7,  3],
                    [ 1,  3, 10,  7,  9,  6,  4,  8,  2,  5],
                    [ 2,  8,  7,  3,  9,  1,  4,  5,  6, 10],
                    [ 2,  6,  1,  9,  5,  8,  7,  4,  3, 10]
                ]),
                id="random_inversion",
            ),
            pytest.param(
                "select_any_mutation",
                np.array([
                    [ 9,  2,  6,  1,  8,  3, 10,  5,  4,  7],
                    [ 1,  2,  9,  6,  4,  5,  8, 10,  7,  3],
                    [10,  8,  1,  7,  9,  6,  4,  3,  2,  5],
                    [ 2,  1,  7,  3,  9,  8,  4,  5,  6, 10],
                    [ 2,  6,  5,  9,  1,  8,  7,  4,  3, 10]
                ]),
                id="select_any_mutation",
            ),
        ],
    )
    def test_mutate_population(self, mutation_strategy, expected_mutated_population):

        pop_size = 5

        tsp_solver = TravellingSalesmanProblemSolver(
            G,
            mutation_strategy=mutation_strategy,
            pop_size=pop_size,
            random_state=42,
        )

        population = np.array([
            [ 9,  2,  6,  1,  8,  3, 10,  5,  4,  7],
            [ 1,  2,  9,  6,  4,  5,  8, 10,  7,  3],
            [10,  3,  1,  7,  9,  6,  4,  8,  2,  5],
            [ 2,  8,  7,  3,  9,  1,  4,  5,  6, 10],
            [ 2,  6,  5,  9,  1,  8,  7,  4,  3, 10]
        ])

        mutated_population = tsp_solver.mutate_population(population, 2 * tsp_solver.n_genes)

        print(mutated_population)

        assert np.allclose(mutated_population, expected_mutated_population, rtol=1e-5)
    #
    # @pytest.mark.parametrize(
    #     "fitness_function, n_genes, expected_best_fitness, expected_best_individual",
    #     [
    #         pytest.param(
    #             1, 1, -1.0817, np.array([-0.09017]), id="continuous_fitness_function=1",
    #         ),
    #         pytest.param(
    #             2,
    #             1,
    #             -4.072e-05,
    #             np.array([-0.0625]),
    #             id="continuous_fitness_function=2",
    #         ),
    #         pytest.param(
    #             3,
    #             2,
    #             -0.0046863,
    #             np.array([-0.009534, 0.0677]),
    #             id="continuous_fitness_function=3",
    #         ),
    #         pytest.param(
    #             4,
    #             3,
    #             17.0614,
    #             np.array([-4.2077,  4.2812,  3.8996]),
    #             id="continuous_fitness_function=4",
    #         ),
    #         pytest.param(
    #             5, 1, 248.3267, np.array([16.172]), id="continuous_fitness_function=5",
    #         ),
    #         pytest.param(
    #             6,
    #             2,
    #             18.2684,
    #             np.array([9.0142, 8.5550]),
    #             id="continuous_fitness_function=6",
    #         ),
    #     ],
    # )
    # def test_solve(
    #         self,
    #         mock_matplotlib,
    #         mock_logging,
    #         fitness_function,
    #         n_genes,
    #         expected_best_fitness,
    #         expected_best_individual,
    # ):
    #
    #     solver = ContinuousGenAlgSolver(
    #         n_genes,
    #         fitness_functions_continuous(fitness_function),
    #         pop_size=10,
    #         max_gen=50,
    #         mutation_rate=0.05,
    #         selection_rate=0.5,
    #         random_state=42,
    #     )
    #
    #     solver.solve()
    #
    #     print(solver.best_fitness_)
    #
    #     assert np.allclose(solver.best_fitness_, expected_best_fitness, rtol=1e-2)
    #     assert np.allclose(solver.best_individual_, expected_best_individual, rtol=1e-2)
