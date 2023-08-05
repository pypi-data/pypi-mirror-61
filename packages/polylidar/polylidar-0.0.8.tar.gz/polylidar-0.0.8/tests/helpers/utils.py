from os import path
import pytest
import numpy as np

from shapely.geometry import Polygon
from polylidar import extractPlanesAndPolygons, extractPolygons

DIR_NAME =path.dirname(path.dirname(__file__))
FIXTURES_DIR = path.join(DIR_NAME, 'fixtures')

def get_poly_coords(outline, points):
    return [get_point(pi, points) for pi in outline]

def get_point(pi, points):
    return [points[pi, 0], points[pi, 1]]

def load_csv(file):
    return np.loadtxt(path.join(FIXTURES_DIR, file), delimiter=',', dtype=np.float64, skiprows=1)

def load_npy(file):
    return np.load(path.join(FIXTURES_DIR, file))

def verify_points(data, n_cols=2):
    assert isinstance(data, np.ndarray)
    assert data.shape[1] == n_cols

def basic_polylidar_verification(points, delaunay, planes, polygons):
    # make sure delaunay has the correct number of points
    assert points.shape[0] == np.array(delaunay.coords).shape[0]
    # make sure that some planes were extracted
    assert len(planes) > 0
    # make sure that some polygons were extracted
    assert len(polygons) > 0

def verify_all_polygons_are_valid(polygons, points):
    for poly in polygons:
        verify_valid_polygon(poly, points)

def verify_valid_polygon(poly, points):
    shell_coords = get_poly_coords(poly.shell, points)
    hole_coords = [get_poly_coords(hole, points) for hole in poly.holes]
    # Verify polygon outer shell
    shapelyPoly = Polygon(shell=shell_coords)
    assert shapelyPoly.is_valid
    # Verify polygon outer shell and holes
    shapelyPoly = Polygon(shell=shell_coords, holes=hole_coords)
#     if not shapelyPoly.is_valid:
#         np.save("scratch/error_{}.npy".format(points.shape[0]), points)
    assert shapelyPoly.is_valid

def verify_all(points, polylidar_kwargs):
    delaunay, planes, polygons = extractPlanesAndPolygons(points, **polylidar_kwargs)
    # Basic test to ensure no obvious errors occurred
    basic_polylidar_verification(points, delaunay, planes, polygons)
    # Ensure that the polygons returned are valid
    verify_all_polygons_are_valid(polygons, points)
    # Ensure that all polygons are as expected
    # Test just polygon extraction
    polygons = extractPolygons(points, **polylidar_kwargs)
    # Ensure that the polygons returned are valid
    verify_all_polygons_are_valid(polygons, points)


