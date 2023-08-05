from os import path
import pytest
import numpy as np


from tests.helpers.utils import load_csv, verify_points, basic_polylidar_verification, verify_all_polygons_are_valid, load_npy
from polylidar import extractPlanesAndPolygons, extractPolygons, extractPolygonsAndTimings


def test_building1(benchmark, building1, basic_params):
    benchmark(extractPlanesAndPolygons, building1, **basic_params)


def test_building2(benchmark, building2, basic_params):
    benchmark(extractPlanesAndPolygons, building2, **basic_params)


def test_100k_array_lmax(benchmark, np_100K_array, params_lmax):
    benchmark(extractPolygons, np_100K_array, **params_lmax)

def test_100k_array_3d_lmax(benchmark, np_100K_array_3d, params_lmax):
    benchmark(extractPolygons, np_100K_array_3d, **params_lmax)

def test_clusters(benchmark, cluster_groups):
    """
    Will benchmark clusters AND check that python overhead is less than 3ms (ussually <1 ms)
    """
    points = cluster_groups['points']
    polylidar_kwargs = cluster_groups['polylidar_kwargs']
    _, timings = benchmark(extractPolygonsAndTimings, points, **polylidar_kwargs)
    cpp_timing = np.sum(timings) / 1000.0 # Actuall c++ timing
    median_benchmark = benchmark.stats.stats.median # python benchmark timing
    assert cpp_timing == pytest.approx(median_benchmark, abs=0.003)
    
