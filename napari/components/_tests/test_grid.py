from napari.components.grid import GridCanvas


def test_grid_creation():
    """Test creating grid object"""
    grid = GridCanvas()
    assert grid is not None
    assert not grid.enabled
    assert grid.size == (-1, -1)
    assert grid.stride == 1


def test_size_stride_creation():
    """Test creating grid object"""
    grid = GridCanvas(size=(3, 4), stride=2)
    assert grid.size == (3, 4)
    assert grid.stride == 2


def test_actual_size_and_position():
    """Test actual size"""
    grid = GridCanvas(enabled=True)
    assert grid.enabled

    # 9 layers get put in a (3, 3) grid
    assert grid.actual_size(9) == (3, 3)
    assert grid.position(0, 9) == (0, 0)
    assert grid.position(2, 9) == (0, 2)
    assert grid.position(3, 9) == (1, 0)
    assert grid.position(8, 9) == (2, 2)

    # 5 layers get put in a (2, 3) grid
    assert grid.actual_size(5) == (2, 3)
    assert grid.position(0, 5) == (0, 0)
    assert grid.position(2, 5) == (0, 2)
    assert grid.position(3, 5) == (1, 0)

    # 10 layers get put in a (3, 4) grid
    assert grid.actual_size(10) == (3, 4)
    assert grid.position(0, 10) == (0, 0)
    assert grid.position(2, 10) == (0, 2)
    assert grid.position(3, 10) == (0, 3)
    assert grid.position(8, 10) == (2, 0)


def test_actual_size_with_stride():
    """Test actual size"""
    grid = GridCanvas(enabled=True, stride=2)
    assert grid.enabled

    # 7 layers get put in a (2, 2) grid
    assert grid.actual_size(7) == (2, 2)
    assert grid.position(0, 7) == (0, 0)
    assert grid.position(1, 7) == (0, 0)
    assert grid.position(2, 7) == (0, 1)
    assert grid.position(3, 7) == (0, 1)
    assert grid.position(6, 7) == (1, 1)

    # 3 layers get put in a (1, 2) grid
    assert grid.actual_size(3) == (1, 2)
    assert grid.position(0, 3) == (0, 0)
    assert grid.position(1, 3) == (0, 0)
    assert grid.position(2, 3) == (0, 1)


def test_actual_size_and_position_negative_stride():
    """Test actual size"""
    grid = GridCanvas(enabled=True, stride=-1)
    assert grid.enabled

    # 9 layers get put in a (3, 3) grid
    assert grid.actual_size(9) == (3, 3)
    assert grid.position(0, 9) == (2, 2)
    assert grid.position(2, 9) == (2, 0)
    assert grid.position(3, 9) == (1, 2)
    assert grid.position(8, 9) == (0, 0)


def test_actual_size_grid_disabled():
    """Test actual size with grid disabled"""
    grid = GridCanvas()
    assert not grid.enabled
    assert grid.actual_size(9) == (1, 1)
    assert grid.position(3, 9) == (0, 0)
