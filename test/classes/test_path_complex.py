"""Test path complex class."""

import hypernetx as hnx
import networkx as nx
import numpy as np
import pytest

from toponetx.classes.path import Path
from toponetx.classes.path_complex import PathComplex
from toponetx.classes.reportviews import NodeView


class TestPathComplex:
    """Test path complex class."""

    def test_init_empty_path_complex(self):
        """Test empty path complex."""
        PX = PathComplex()
        assert len(PX.paths) == 0
        assert len(PX.nodes) == 0
        assert PX.dim == -1

    def test_iterable_paths(self):
        """Test TypeError when paths is not iterable."""
        with pytest.raises(TypeError):
            _ = PathComplex(paths=1)

    def test_shape_property(self):
        """Test shape property."""
        PX = PathComplex([[1, 2, 3], [1, 2, 4]])
        assert PX.shape == (4, 3, 2)

        PX = PathComplex()
        assert PX.shape == tuple()

    def test_dim_property(self):
        """Test dim property."""
        PX = PathComplex([[1, 2, 3], [1, 2, 4]])
        assert PX.dim == 2

        PX = PathComplex()
        assert PX.dim == -1  # empty path complex

    def test_nodes_property(self):
        """Test nodes property."""
        PX = PathComplex([[1, 2, 3], [1, 2, 4]])
        nodes = PX.nodes
        assert len(nodes) == 4
        assert (1,) in nodes.nodes
        assert (2,) in nodes.nodes
        assert (6,) not in nodes.nodes

    def test_path_property(self):
        """Test path property."""
        PX = PathComplex([[1, 2, 3], [1, 2, 4]])
        assert [1, 2, 3] in PX.paths
        assert [1, 2, 4] in PX.paths
        assert [1, 2] in PX.paths
        assert 4 in PX.paths

    def test_add_path(self):
        """Test add path."""
        PX = PathComplex()
        PX.add_path([1, 2, 3])
        assert [1, 2, 3] in PX.paths
        assert [1, 2] in PX.paths
        assert 3 in PX.paths

        with pytest.raises(ValueError):
            PX.add_path([3, 2])

        with pytest.raises(ValueError):
            PX.add_path([3, 2, 2])

        with pytest.raises(ValueError):
            PX.add_path([3, 2, 3])

        PX = PathComplex(reserve_sequence_order=True)
        PX.add_path([3, 2, 1])
        assert [3, 2, 1] in PX.paths

        PX = PathComplex()
        PX.add_path([1, 2])
        PX.add_path([2, 3])
        assert [
            1,
            2,
            3,
        ] not in PX.paths  # because manually adding subpaths does not add superpath. Future features?
        assert [1, 2] in PX.paths
        assert [2, 3] in PX.paths

    def test_constructor_using_graph(self):
        """Test constructor using graph."""
        G = nx.Graph()
        G.add_edge(1, 2)
        G.add_edge(2, 3)
        PX = PathComplex(G)

        assert [1, 2, 3] in PX.paths  # because constructing from graph
        assert [1, 2] in PX.paths
        assert [2, 3] in PX.paths
        assert 1 in PX.paths
        assert 2 in PX.paths
        assert 3 in PX.paths

        PX = PathComplex(G, allowed_paths=[[1], [2], [3], [1, 2]])
        assert [2, 3] in PX.paths
        assert PX._allowed_paths == set([(1,), (2,), (3,), (1, 2), (2, 3), (1, 2, 3)])

        G = nx.Graph()
        G.add_edge(3, 2)
        PX = PathComplex(G)
        assert [2, 3] in PX.paths
        assert [3, 2] not in PX.paths

    def test_clone(self):
        """Test clone."""
        PX = PathComplex([[1, 2, 3], [1, 2, 4]])
        PX_clone = PX.clone()
        assert set(PX_clone.paths) == set(PX.paths)
        assert PX_clone is not PX

    def test_skeleton_raise_errors(self):
        """Test skeleton raise errors."""
        PX = PathComplex([[1, 2, 3], [1, 3]])
        with pytest.raises(ValueError):
            PX.skeleton(-1)

        with pytest.raises(TypeError):
            PX.skeleton(1.5)

        with pytest.raises(TypeError):
            PX.skeleton(1, 2)

        with pytest.raises(ValueError):
            PX.skeleton(3)

    def test_str(self):
        """Test str."""
        PX = PathComplex([[1, 2, 3], [1, 2, 4]], name="PX")
        assert str(PX) == "Path Complex with shape (4, 3, 2) and dimension 2"

    def test_add_str_nodes(self):
        """Test add str nodes."""
        PX = PathComplex([[1, 2, 3], [2, 4, "a"]])
        assert "a" in PX.paths

        with pytest.raises(ValueError):
            PX.add_path(["a", 1, 2])

    def test_repr_str(self):
        """Test repr str."""
        PX = PathComplex([[1, 2, 3], [1, 2, 4]], name="PX")
        assert (repr(PX)) == "PathComplex(name='PX')"
        assert PX.name == "PX"

    def test_getittem(self):
        """Test getitem."""
        PX = PathComplex([[1, 2, 3], [1, 2, 4]])
        assert PX[[1, 2, 3]] == {}
        assert PX[1] == {}

        with pytest.raises(KeyError):
            PX[5]

        PX.add_path([1, 2, 5], heat=55)
        assert PX[[1, 2, 5]] == {"heat": 55}

        PX[[1, 2, 5]]["heat"] = 66
        assert PX[[1, 2, 5]] == {"heat": 66}

    def test_get_len_(self):
        """Test get size of the path complex."""
        PX = PathComplex()
        PX.add_paths_from([[1, 2, 3], [1, 2, 4]])
        assert len(PX) == 9

    def test_add_paths_from(self):
        """Test add paths from graph."""
        PX = PathComplex()
        PX.add_paths_from([[1, 2, 3], [1, 2, 4]])
        assert [1, 2, 3] in PX.paths
        assert [1, 2] in PX.paths
        assert [2, 3] in PX.paths
        assert 1 in PX.paths
        assert 2 in PX.paths
        assert 3 in PX.paths

        with pytest.raises(TypeError):
            PX.add_paths_from(1)

    def test_add_node(self):
        """Test add node."""
        PX = PathComplex()
        PX.add_node(1)
        assert 1 in PX.paths
        assert [1] in PX.paths

        with pytest.raises(TypeError):
            PX.add_node([1, 2])

        PX.add_node(Path(2))
        assert 2 in PX.paths
        assert [2] in PX.paths

        with pytest.raises(ValueError):
            PX.add_node(Path([2, 3]))

    def test_remove_nodes(self):
        """Test remove_nodes method."""
        PX = PathComplex([[0, 1], [1, 2, 3], [1, 3, 2], [2, 1, 3]])
        assert 1 in PX.paths
        PX.remove_nodes([1])
        assert 1 not in PX.paths
        assert [1, 2] not in PX.paths
        assert [1, 3] not in PX.paths

    def test_incidence_matrix(self):
        """Test incidence matrix."""
        PX = PathComplex(
            [[0, 1], [1, 2, 3], [1, 3, 2], [2, 1, 3], [0, 1, 2], [0, 1, 3]]
        )
        assert np.all(PX.incidence_matrix(0).todense == np.zeros((0, len(PX.nodes))))
        assert np.all(
            PX.incidence_matrix(1, signed=False).todense()
            == np.array([[1, 0, 0, 0], [1, 1, 1, 0], [0, 1, 0, 1], [0, 0, 1, 1]])
        )
        assert np.all(
            PX.incidence_matrix(2, signed=False).todense()
            == np.array(
                [[1, 1, 0, 0, 0], [1, 0, 1, 1, 1], [0, 1, 1, 1, 1], [0, 0, 1, 1, 1]]
            )
        )

        with pytest.raises(ValueError):
            PX.incidence_matrix(-1)

        with pytest.raises(ValueError):
            PX.incidence_matrix(3)

        row, col, B = PX.incidence_matrix(0, index=True)
        assert row == {}
        assert col == {(0,): 0, (1,): 1, (2,): 2, (3,): 3}
        assert np.all(B.todense() == np.zeros((0, len(PX.nodes))))

        row, col, B = PX.incidence_matrix(1, index=True)
        assert row == {(0,): 0, (1,): 1, (2,): 2, (3,): 3}
        assert col == {(0, 1): 0, (1, 2): 1, (1, 3): 2, (2, 3): 3}
        assert np.all(
            B.todense()
            == np.array([[-1, 0, 0, 0], [1, -1, -1, 0], [0, 1, 0, -1], [0, 0, 1, 1]])
        )

        row, col, B = PX.incidence_matrix(2, index=True)
        assert row == {(0, 1): 0, (1, 2): 1, (1, 3): 2, (2, 3): 3}
        assert col == {
            (0, 1, 2): 0,
            (0, 1, 3): 1,
            (1, 2, 3): 2,
            (1, 3, 2): 3,
            (2, 1, 3): 4,
        }
        assert np.all(
            B.todense()
            == np.array(
                [[1, 1, 0, 0, 0], [1, 0, 1, -1, 1], [0, 1, -1, 1, 1], [0, 0, 1, 1, -1]]
            )
        )

    def test_up_laplacian_matrix(self):
        """Test up laplacian matrix."""
        PX = PathComplex(
            [[0, 1], [1, 2, 3], [1, 3, 2], [2, 1, 3], [0, 1, 2], [0, 1, 3]]
        )
        with pytest.raises(ValueError):
            PX.up_laplacian_matrix(-1)
        with pytest.raises(ValueError):
            PX.up_laplacian_matrix(2)

        row, L_up = PX.up_laplacian_matrix(0, index=True)
        row_B, col_B, B = PX.incidence_matrix(1, index=True)
        L_up_tmp = B.todense() @ B.todense().T

        assert np.all(L_up.todense() == L_up_tmp)
        assert row == row_B

        L_up = PX.up_laplacian_matrix(1)
        B = PX.incidence_matrix(2)
        L_up_tmp = B.todense() @ B.todense().T

        assert np.all(L_up.todense() == L_up_tmp)

        L_up = PX.up_laplacian_matrix(1, signed=True)
        B = PX.incidence_matrix(2, signed=True)
        L_up_tmp = B.todense() @ B.todense().T

        assert np.all(L_up.todense() == L_up_tmp)

    def test_down_laplacian_matrix(self):
        """Test down laplacian matrix."""
        PX = PathComplex(
            [[0, 1], [1, 2, 3], [1, 3, 2], [2, 1, 3], [0, 1, 2], [0, 1, 3]]
        )
        with pytest.raises(ValueError):
            PX.down_laplacian_matrix(0)
        with pytest.raises(ValueError):
            PX.down_laplacian_matrix(3)

        row, L_down = PX.down_laplacian_matrix(1, index=True)
        row_B, col_B, B = PX.incidence_matrix(1, index=True)
        L_down_tmp = B.todense().T @ B.todense()

        assert np.all(L_down.todense() == L_down_tmp)
        assert row == row_B

        L_down = PX.down_laplacian_matrix(2)
        B = PX.incidence_matrix(2)
        L_down_tmp = B.todense().T @ B.todense()

        assert np.all(L_down.todense() == L_down_tmp)

        L_down = PX.down_laplacian_matrix(2, signed=True)
        B = PX.incidence_matrix(2, signed=True)
        L_down_tmp = B.todense().T @ B.todense()

        assert np.all(L_down.todense() == L_down_tmp)

    def test_adjacency_matrix(self):
        """Test adjacency matrix."""
        PX = PathComplex(
            [[0, 1], [1, 2, 3], [1, 3, 2], [2, 1, 3], [0, 1, 2], [0, 1, 3]]
        )
        with pytest.raises(ValueError):
            PX.adjacency_matrix(-1)
        with pytest.raises(ValueError):
            PX.adjacency_matrix(2)

        adj_0 = PX.adjacency_matrix(0, signed=False).todense()
        assert np.all(
            adj_0 == np.array([[0, 1, 0, 0], [1, 0, 1, 1], [0, 1, 0, 1], [0, 1, 1, 0]])
        )

        adj_1 = PX.adjacency_matrix(1, signed=False).todense()

        assert np.all(
            adj_1 == np.array([[0, 1, 1, 0], [1, 0, 1, 1], [1, 1, 0, 1], [0, 1, 1, 0]])
        )

    def test_coadjacency_matrix(self):
        """Test coadjacency matrix."""
        PX = PathComplex(
            [[0, 1], [1, 2, 3], [1, 3, 2], [2, 1, 3], [0, 1, 2], [0, 1, 3]]
        )
        with pytest.raises(ValueError):
            PX.coadjacency_matrix(0)
        with pytest.raises(ValueError):
            PX.coadjacency_matrix(3)

        coadj_1 = PX.coadjacency_matrix(1, signed=False).todense()
        assert np.all(
            coadj_1
            == np.array([[0, 1, 1, 0], [1, 0, 1, 1], [1, 1, 0, 1], [0, 1, 1, 0]])
        )

        coadj_2 = PX.coadjacency_matrix(2, signed=False).todense()
        assert np.all(
            coadj_2
            == np.array(
                [
                    [0, 1, 1, 1, 1],
                    [1, 0, 1, 1, 1],
                    [1, 1, 0, 1, 1],
                    [1, 1, 1, 0, 1],
                    [1, 1, 1, 1, 0],
                ]
            )
        )

    def test_to_hypergraph(self):
        """Convert a PathComplex to a HyperGraph, then compare the number of nodes and edges."""
        PX = PathComplex(
            [[0, 1], [1, 2, 3], [1, 3, 2], [2, 1, 3], [0, 1, 2], [0, 1, 3]], max_rank=3
        )
        HG = PX.to_hypergraph()

        expected_results = hnx.Hypergraph(
            {
                "e0": [0, 1],
                "e1": [1, 2],
                "e2": [1, 3],
                "e3": [2, 3],
                "e4": [0, 1, 2],
                "e5": [0, 1, 3],
                "e6": [1, 2, 3],
                "e7": [1, 3, 2],
                "e8": [2, 1, 3],
            },
            name="",
            static=True,
        )

        assert len(HG.edges) == len(expected_results.edges)
        assert set(HG.nodes) == set(expected_results.nodes)
