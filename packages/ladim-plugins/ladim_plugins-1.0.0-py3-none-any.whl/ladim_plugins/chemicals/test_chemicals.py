import numpy as np
import pytest
from ladim_plugins.chemicals import gridforce, IBM


class Test_nearest_unmasked:
    def test_correct_when_all_unmasked(self):
        mask = np.zeros((4, 3))
        i = np.array([1, 1, 2])
        j = np.array([2, 3, 3])
        ii, jj = gridforce.nearest_unmasked(mask, i, j)
        assert ii.tolist() == i.tolist()
        assert jj.tolist() == j.tolist()

    def test_correct_when_south_edge(self):
        mask_south = np.array([[0, 0, 0, 0], [1, 1, 1, 1], [1, 1, 1, 1]])
        i = np.array([0, 1, 2.51])
        j = np.array([0, 1, 1.49])
        ii, jj = gridforce.nearest_unmasked(mask_south, i, j)
        assert ii.tolist() == [0, 1, 3]
        assert jj.tolist() == [0, 0, 0]

    def test_correct_when_corner(self):
        mask = np.array([[0, 0, 0, 0], [0, 1, 1, 1], [0, 1, 1, 0]])
        i = np.array([0.51, 0.51, 0.99, 1.49, 1.51, 2.00, 3.00])
        j = np.array([0.52, 0.98, 0.52, 1.01, 1.01, 1.01, 1.01])
        ii, jj = gridforce.nearest_unmasked(mask, i, j)
        assert ii.tolist() == [0, 0, 1, 1, 2, 2, 3]
        assert jj.tolist() == [1, 1, 0, 0, 0, 0, 2]


class Test_ibm_land_collision:
    @pytest.fixture()
    def config(self):
        from ladim_plugins.tests.test_examples import get_config
        from ladim.configuration import configure
        return configure(get_config('chemicals'))

    @pytest.fixture()
    def grid(self, config):
        from ladim.gridforce import Grid
        return Grid(config)

    @pytest.fixture()
    def forcing(self, config, grid):
        from ladim.gridforce import Forcing
        return Forcing(config, grid)

    @pytest.fixture()
    def state(self, config, grid):
        from ladim.state import State
        return State(config, grid)

    @pytest.fixture()
    def ibm_chemicals(self, config):
        return IBM(config)

    def test_land_collision(self, ibm_chemicals, grid, state, forcing):
        np.random.seed(0)

        state.X = np.float32([1, 1, 1])
        state.Y = np.float32([1, 1, 1])
        state.Z = np.float32([1, 1, 1])
        state.pid = np.int32([0, 1, 2])
        ibm_chemicals.update_ibm(grid, state, forcing)

        assert state.X.tolist() == [1, 1, 1]
        assert state.Y.tolist() == [1, 1, 1]

        state.X = np.float32([1, 2, 3, 4])
        state.Y = np.float32([1, 1, 1, 1])
        state.Z = np.float32([1, 1, 1, 1])
        state.pid = np.int32([1, 2, 3, 4])
        ibm_chemicals.update_ibm(grid, state, forcing)

        assert state.X.tolist() == [1.4636627435684204, 2, 3, 4]
        assert state.Y.tolist() == [0.8834415078163147, 1, 1, 1]
