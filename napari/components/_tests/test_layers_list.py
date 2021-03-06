import os

import numpy as np
import pytest

from napari.components import LayerList
from napari.layers import Image


def test_empty_layers_list():
    """
    Test instantiating an empty LayerList object
    """
    layers = LayerList()

    assert len(layers) == 0


def test_initialize_from_list():
    layers = LayerList(
        [Image(np.random.random((10, 10))), Image(np.random.random((10, 10)))]
    )
    assert len(layers) == 2


def test_adding_layer():
    """
    Test adding a Layer
    """
    layers = LayerList()
    layer = Image(np.random.random((10, 10)))
    layers.append(layer)

    # LayerList should err if you add anything other than a layer
    with pytest.raises(TypeError):
        layers.append('something')

    assert len(layers) == 1


def test_removing_layer():
    """
    Test removing a Layer
    """
    layers = LayerList()
    layer = Image(np.random.random((10, 10)))
    layers.append(layer)
    layers.remove(layer)

    assert len(layers) == 0


def test_indexing():
    """
    Test indexing into a LayerList
    """
    layers = LayerList()
    layer = Image(np.random.random((10, 10)), name='image')
    layers.append(layer)

    assert layers[0] == layer
    assert layers['image'] == layer


def test_insert():
    """
    Test inserting into a LayerList
    """
    layers = LayerList()
    layer_a = Image(np.random.random((10, 10)), name='image_a')
    layer_b = Image(np.random.random((15, 15)), name='image_b')
    layers.append(layer_a)
    layers.insert(0, layer_b)

    assert list(layers) == [layer_b, layer_a]


def test_get_index():
    """
    Test getting indexing from LayerList
    """
    layers = LayerList()
    layer_a = Image(np.random.random((10, 10)), name='image_a')
    layer_b = Image(np.random.random((15, 15)), name='image_b')
    layers.append(layer_a)
    layers.append(layer_b)

    assert layers.index(layer_a) == 0
    assert layers.index('image_a') == 0
    assert layers.index(layer_b) == 1
    assert layers.index('image_b') == 1


def test_reordering():
    """
    Test indexing into a LayerList by name
    """
    layers = LayerList()
    layer_a = Image(np.random.random((10, 10)), name='image_a')
    layer_b = Image(np.random.random((15, 15)), name='image_b')
    layer_c = Image(np.random.random((15, 15)), name='image_c')
    layers.append(layer_a)
    layers.append(layer_b)
    layers.append(layer_c)

    # Rearrange layers by tuple
    layers[:] = layers[(1, 0, 2)]
    assert list(layers) == [layer_b, layer_a, layer_c]

    # Swap layers by name
    layers['image_b', 'image_c'] = layers['image_c', 'image_b']
    assert list(layers) == [layer_c, layer_a, layer_b]

    # Reverse layers
    layers.reverse()
    assert list(layers) == [layer_b, layer_a, layer_c]


def test_naming():
    """
    Test unique naming in LayerList
    """
    layers = LayerList()
    layer_a = Image(np.random.random((10, 10)), name='img')
    layer_b = Image(np.random.random((15, 15)), name='img')
    layers.append(layer_a)
    layers.append(layer_b)

    assert [lay.name for lay in layers] == ['img', 'img [1]']

    layer_b.name = 'chg'
    assert [lay.name for lay in layers] == ['img', 'chg']

    layer_a.name = 'chg'
    assert [lay.name for lay in layers] == ['chg [1]', 'chg']


def test_selection():
    """
    Test only last added is selected.
    """
    layers = LayerList()
    layer_a = Image(np.random.random((10, 10)))
    layers.append(layer_a)
    assert layers[0].selected is True

    layer_b = Image(np.random.random((15, 15)))
    layers.append(layer_b)
    assert [lay.selected for lay in layers] == [False, True]

    layer_c = Image(np.random.random((15, 15)))
    layers.append(layer_c)
    assert [lay.selected for lay in layers] == [False] * 2 + [True]

    for lay in layers:
        lay.selected = True
    layer_d = Image(np.random.random((15, 15)))
    layers.append(layer_d)
    assert [lay.selected for lay in layers] == [False] * 3 + [True]


def test_unselect_all():
    """
    Test unselecting
    """
    layers = LayerList()
    layer_a = Image(np.random.random((10, 10)))
    layer_b = Image(np.random.random((15, 15)))
    layer_c = Image(np.random.random((15, 15)))
    layers.append(layer_a)
    layers.append(layer_b)
    layers.append(layer_c)

    layers.unselect_all()
    assert [lay.selected for lay in layers] == [False] * 3

    for lay in layers:
        lay.selected = True
    layers.unselect_all(ignore=layer_b)
    assert [lay.selected for lay in layers] == [False, True, False]


def test_remove_selected():
    """
    Test removing selected layers
    """
    layers = LayerList()
    layer_a = Image(np.random.random((10, 10)))
    layer_b = Image(np.random.random((15, 15)))
    layer_c = Image(np.random.random((15, 15)))
    layer_d = Image(np.random.random((15, 15)))
    layers.append(layer_a)
    layers.append(layer_b)
    layers.append(layer_c)

    # remove last added layer as only one selected
    layers.remove_selected()
    assert list(layers) == [layer_a, layer_b]

    # check that the next to last layer is now selected
    assert [lay.selected for lay in layers] == [False, True]

    layers.remove_selected()
    assert list(layers) == [layer_a]
    assert [lay.selected for lay in layers] == [True]

    # select and remove first layer only
    layers.append(layer_b)
    layers.append(layer_c)
    assert list(layers) == [layer_a, layer_b, layer_c]
    layer_a.selected = True
    layer_b.selected = False
    layer_c.selected = False
    layers.remove_selected()
    assert list(layers) == [layer_b, layer_c]
    assert [lay.selected for lay in layers] == [True, False]

    # select and remove first and last layer of four
    layers.append(layer_a)
    layers.append(layer_d)
    assert list(layers) == [layer_b, layer_c, layer_a, layer_d]
    layer_a.selected = False
    layer_b.selected = True
    layer_c.selected = False
    layer_d.selected = True
    layers.remove_selected()
    assert list(layers) == [layer_c, layer_a]
    assert [lay.selected for lay in layers] == [True, False]

    # select and remove middle two layers of four
    layers.append(layer_b)
    layers.append(layer_d)
    layer_a.selected = True
    layer_b.selected = True
    layer_c.selected = False
    layer_d.selected = False
    layers.remove_selected()
    assert list(layers) == [layer_c, layer_d]
    assert [lay.selected for lay in layers] == [True, False]

    # select and remove all layersay
    for lay in layers:
        lay.selected = True
    layers.remove_selected()
    assert len(layers) == 0


def test_move_selected():
    """
    Test removing selected layers
    """
    layers = LayerList()
    layer_a = Image(np.random.random((10, 10)))
    layer_b = Image(np.random.random((15, 15)))
    layer_c = Image(np.random.random((15, 15)))
    layer_d = Image(np.random.random((15, 15)))
    layers.append(layer_a)
    layers.append(layer_b)
    layers.append(layer_c)
    layers.append(layer_d)

    # Check nothing moves if given same insert and origin
    layers.unselect_all()
    layers.move_selected(2, 2)
    assert list(layers) == [layer_a, layer_b, layer_c, layer_d]
    assert [lay.selected for lay in layers] == [False, False, True, False]

    # Move middle element to front of list and back
    layers.unselect_all()
    layers.move_selected(2, 0)
    assert list(layers) == [layer_c, layer_a, layer_b, layer_d]
    assert [lay.selected for lay in layers] == [True, False, False, False]
    layers.unselect_all()
    layers.move_selected(0, 2)
    assert list(layers) == [layer_a, layer_b, layer_c, layer_d]
    assert [lay.selected for lay in layers] == [False, False, True, False]

    # Move middle element to end of list and back
    layers.unselect_all()
    layers.move_selected(2, 3)
    assert list(layers) == [layer_a, layer_b, layer_d, layer_c]
    assert [lay.selected for lay in layers] == [False, False, False, True]
    layers.unselect_all()
    layers.move_selected(3, 2)
    assert list(layers) == [layer_a, layer_b, layer_c, layer_d]
    assert [lay.selected for lay in layers] == [False, False, True, False]

    # Select first two layers only
    for layer, s in zip(layers, [True, True, False, False]):
        layer.selected = s
    # Move unselected middle element to front of list even if others selected
    layers.move_selected(2, 0)
    assert list(layers) == [layer_c, layer_a, layer_b, layer_d]
    # Move selected first element back to middle of list
    layers.move_selected(0, 2)
    assert list(layers) == [layer_a, layer_b, layer_c, layer_d]

    # Select first two layers only
    for layer, s in zip(layers, [True, True, False, False]):
        layer.selected = s
    # Check nothing moves if given same insert and origin and multiple selected
    layers.move_selected(0, 0)
    assert list(layers) == [layer_a, layer_b, layer_c, layer_d]
    assert [lay.selected for lay in layers] == [True, True, False, False]

    # Check nothing moves if given same insert and origin and multiple selected
    layers.move_selected(1, 1)
    assert list(layers) == [layer_a, layer_b, layer_c, layer_d]
    assert [lay.selected for lay in layers] == [True, True, False, False]

    # Move first two selected to middle of list
    layers.move_selected(0, 1)
    assert list(layers) == [layer_c, layer_a, layer_b, layer_d]
    assert [lay.selected for lay in layers] == [False, True, True, False]

    # Move middle selected to front of list
    layers.move_selected(2, 0)
    assert list(layers) == [layer_a, layer_b, layer_c, layer_d]
    assert [lay.selected for lay in layers] == [True, True, False, False]

    # Move first two selected to middle of list
    layers.move_selected(1, 2)
    assert list(layers) == [layer_c, layer_a, layer_b, layer_d]
    assert [lay.selected for lay in layers] == [False, True, True, False]

    # Move middle selected to front of list
    layers.move_selected(1, 0)
    assert list(layers) == [layer_a, layer_b, layer_c, layer_d]
    assert [lay.selected for lay in layers] == [True, True, False, False]

    # Select first and third layers only
    for layer, s in zip(layers, [True, False, True, False]):
        layer.selected = s
    # Move selection together to middle
    layers.move_selected(2, 2)
    assert list(layers) == [layer_b, layer_a, layer_c, layer_d]
    assert [lay.selected for lay in layers] == [False, True, True, False]
    layers[:] = layers[(1, 0, 2, 3)]

    # Move selection together to middle
    layers.move_selected(0, 1)
    assert list(layers) == [layer_b, layer_a, layer_c, layer_d]
    assert [lay.selected for lay in layers] == [False, True, True, False]
    layers[:] = layers[(1, 0, 2, 3)]

    # Move selection together to end
    layers.move_selected(2, 3)
    assert list(layers) == [layer_b, layer_d, layer_a, layer_c]
    assert [lay.selected for lay in layers] == [False, False, True, True]
    layers[:] = layers[(2, 0, 3, 1)]

    # Move selection together to end
    layers.move_selected(0, 2)
    assert list(layers) == [layer_b, layer_d, layer_a, layer_c]
    assert [lay.selected for lay in layers] == [False, False, True, True]
    layers[:] = layers[(2, 0, 3, 1)]

    # Move selection together to end
    layers.move_selected(0, 3)
    assert list(layers) == [layer_b, layer_d, layer_a, layer_c]
    assert [lay.selected for lay in layers] == [False, False, True, True]
    layers[:] = layers[(2, 0, 3, 1)]

    layer_e = Image(np.random.random((15, 15)))
    layer_f = Image(np.random.random((15, 15)))
    layers.append(layer_e)
    layers.append(layer_f)
    # Check current order is correct
    assert list(layers) == [
        layer_a,
        layer_b,
        layer_c,
        layer_d,
        layer_e,
        layer_f,
    ]
    # Select second and firth layers only
    for layer, s in zip(layers, [False, True, False, False, True, False]):
        layer.selected = s

    # Move selection together to middle
    layers.move_selected(1, 2)
    assert list(layers) == [
        layer_a,
        layer_c,
        layer_b,
        layer_e,
        layer_d,
        layer_f,
    ]
    assert [lay.selected for lay in layers] == [
        False,
        False,
        True,
        True,
        False,
        False,
    ]


def test_toggle_visibility():
    """
    Test toggling layer visibility
    """
    layers = LayerList()
    layer_a = Image(np.random.random((10, 10)))
    layer_b = Image(np.random.random((15, 15)))
    layer_c = Image(np.random.random((15, 15)))
    layer_d = Image(np.random.random((15, 15)))
    layers.append(layer_a)
    layers.append(layer_b)
    layers.append(layer_c)
    layers.append(layer_d)

    layers[0].visible = False
    layers[1].visible = True
    layers[2].visible = False
    layers[3].visible = True

    layers.select_all()
    layers[0].selected = False

    layers.toggle_selected_visibility()

    assert [lay.visible for lay in layers] == [False, False, True, False]

    layers.toggle_selected_visibility()

    assert [lay.visible for lay in layers] == [False, True, False, True]


# the layer_data_and_types fixture is defined in napari/conftest.py
def test_layers_save(tmpdir, layer_data_and_types):
    """Test saving all layer data."""
    list_of_layers, _, _, filenames = layer_data_and_types
    layers = LayerList(list_of_layers)

    path = os.path.join(tmpdir, 'layers_folder')

    # Check folder does not exist
    assert not os.path.isdir(path)

    # Write data
    layers.save(path, plugin='builtins')

    # Check folder now exists
    assert os.path.isdir(path)

    # Check individual files now exist
    for f in filenames:
        assert os.path.isfile(os.path.join(path, f))

    # Check no additional files exist
    assert set(os.listdir(path)) == set(filenames)
    assert set(os.listdir(tmpdir)) == set(['layers_folder'])


# the layer_data_and_types fixture is defined in napari/conftest.py
def test_layers_save_none_selected(tmpdir, layer_data_and_types):
    """Test saving all layer data."""
    list_of_layers, _, _, filenames = layer_data_and_types
    layers = LayerList(list_of_layers)
    layers.unselect_all()

    path = os.path.join(tmpdir, 'layers_folder')

    # Check folder does not exist
    assert not os.path.isdir(path)

    # Write data (will get a warning that nothing is selected)
    with pytest.warns(UserWarning):
        layers.save(path, selected=True, plugin='builtins')

    # Check folder still does not exist
    assert not os.path.isdir(path)

    # Check individual files still do not exist
    for f in filenames:
        assert not os.path.isfile(os.path.join(path, f))

    # Check no additional files exist
    assert set(os.listdir(tmpdir)) == set('')


# the layer_data_and_types fixture is defined in napari/conftest.py
def test_layers_save_seleteced(tmpdir, layer_data_and_types):
    """Test saving all layer data."""
    list_of_layers, _, _, filenames = layer_data_and_types
    layers = LayerList(list_of_layers)
    layers.unselect_all()
    layers[0].selected = True
    layers[2].selected = True

    path = os.path.join(tmpdir, 'layers_folder')

    # Check folder does not exist
    assert not os.path.isdir(path)

    # Write data
    layers.save(path, selected=True, plugin='builtins')

    # Check folder exists
    assert os.path.isdir(path)

    # Check only appropriate files exist
    assert os.path.isfile(os.path.join(path, filenames[0]))
    assert not os.path.isfile(os.path.join(path, filenames[1]))
    assert os.path.isfile(os.path.join(path, filenames[2]))
    assert not os.path.isfile(os.path.join(path, filenames[1]))

    # Check no additional files exist
    assert set(os.listdir(path)) == set([filenames[0], filenames[2]])
    assert set(os.listdir(tmpdir)) == set(['layers_folder'])


# the layers fixture is defined in napari/conftest.py
def test_layers_save_svg(tmpdir, layers):
    """Test saving all layer data to an svg."""
    path = os.path.join(tmpdir, 'layers_file.svg')

    # Check file does not exist
    assert not os.path.isfile(path)

    # Write data
    layers.save(path, plugin='svg')

    # Check file now exists
    assert os.path.isfile(path)


def test_world_extent():
    """Test world extent after adding layers."""
    np.random.seed(0)
    layers = LayerList()

    # Empty data is taken to be 512 x 512
    np.testing.assert_allclose(layers.extent.world[0], (0, 0))
    np.testing.assert_allclose(layers.extent.world[1], (511, 511))
    np.testing.assert_allclose(layers.extent.step, (1, 1))

    # Add one layer
    layer_a = Image(
        np.random.random((6, 10, 15)), scale=(3, 1, 1), translate=(10, 20, 5)
    )
    layers.append(layer_a)
    np.testing.assert_allclose(layer_a.extent.world[0], (10, 20, 5))
    np.testing.assert_allclose(layer_a.extent.world[1], (25, 29, 19))
    np.testing.assert_allclose(layers.extent.world[0], (10, 20, 5))
    np.testing.assert_allclose(layers.extent.world[1], (25, 29, 19))
    np.testing.assert_allclose(layers.extent.step, (3, 1, 1))

    # Add another layer
    layer_b = Image(
        np.random.random((8, 6, 15)), scale=(6, 2, 1), translate=(-5, -10, 10)
    )
    layers.append(layer_b)
    np.testing.assert_allclose(layer_b.extent.world[0], (-5, -10, 10))
    np.testing.assert_allclose(layer_b.extent.world[1], (37, 0, 24))
    np.testing.assert_allclose(layers.extent.world[0], (-5, -10, 5))
    np.testing.assert_allclose(layers.extent.world[1], (37, 29, 24))
    np.testing.assert_allclose(layers.extent.step, (3, 1, 1))


def test_world_extent_mixed_ndim():
    """Test world extent after adding layers of different dimensionality."""
    np.random.seed(0)
    layers = LayerList()

    # Add 3D layer
    layer_a = Image(np.random.random((15, 15, 15)), scale=(4, 12, 2))
    layers.append(layer_a)
    np.testing.assert_allclose(layers.extent.world[1], (56, 168, 28))

    # Add 2D layer
    layer_b = Image(np.random.random((10, 10)), scale=(6, 4))
    layers.append(layer_b)
    np.testing.assert_allclose(layers.extent.world[1], (56, 168, 36))
    np.testing.assert_allclose(layers.extent.step, (4, 6, 2))


def test_world_extent_mixed_flipped():
    """Test world extent after adding data with a flip."""
    # Flipped data results in a negative scale value which should be
    # made positive when taking into consideration for the step size
    # calculation
    np.random.seed(0)
    layers = LayerList()

    layer = Image(
        np.random.random((15, 15)), affine=[[0, 1, 0], [1, 0, 0], [0, 0, 1]]
    )
    layers.append(layer)
    np.testing.assert_allclose(layer.scale, (1, -1))
    np.testing.assert_allclose(layers.extent.step, (1, 1))


def test_ndim():
    """Test world extent after adding layers."""
    np.random.seed(0)
    layers = LayerList()

    assert layers.ndim == 2

    # Add one layer
    layer_a = Image(np.random.random((10, 15)))
    layers.append(layer_a)
    assert layers.ndim == 2

    # Add another layer
    layer_b = Image(np.random.random((8, 6, 15)))
    layers.append(layer_b)
    assert layers.ndim == 3

    # Remove layer
    layers.remove(layer_b)
    assert layers.ndim == 2
