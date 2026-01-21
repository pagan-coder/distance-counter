# distutils: language = c
# cython: language_level = 3

from libc.stdlib cimport malloc, free
from cpython.mem cimport PyMem_Malloc, PyMem_Free
cimport cython


cdef extern from "c_lib/distance.h":

	ctypedef struct Point:
		double lat
		double lon
	
	double calculate_total_distance(Point* points, int num_points)
	double calculate_time_from_distance(double distance, double speed)


@cython.boundscheck(False)
@cython.wraparound(False)
def calculate_distance_cython(list coordinates, double speed):
	"""
	Calculate total distance through all points and time based on speed.
	
	Args:
		coordinates: List of [lat, lon] pairs
		speed: Speed in km/h
	
	Returns:
		tuple: (distance in km, time in hours)
	"""
	cdef int num_points = len(coordinates)
	cdef int i
	cdef double distance
	cdef double time
	cdef Point * points

	if num_points < 2:
		return (0.0, 0.0)
	
	# Allocate memory for points
	points = <Point*>PyMem_Malloc(num_points * sizeof(Point))

	if not points:
		raise MemoryError("Failed to allocate memory for points")
	
	try:
		# Fill points array
		for i in range(num_points):

			if len(coordinates[i]) != 2:
				raise ValueError(f"Coordinate {i} must have exactly 2 values [lat, lon]")

			points[i].lat = float(coordinates[i][0])
			points[i].lon = float(coordinates[i][1])
		
		# Calculate distance
		distance = calculate_total_distance(points, num_points)
		
		# Calculate time
		time = calculate_time_from_distance(distance, speed)
		
		return (distance, time)
	
	finally:
		PyMem_Free(points)
