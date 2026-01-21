#include "distance.h"
#include <math.h>

// Haversine formula to calculate distance between two points on Earth
// Returns distance in kilometers
double haversine_distance(Point p1, Point p2) {
	const double R = 6371.0; // Earth radius in kilometers
	double dlat = (p2.lat - p1.lat) * M_PI / 180.0;
	double dlon = (p2.lon - p1.lon) * M_PI / 180.0;
	
	double a = sin(dlat / 2.0) * sin(dlat / 2.0) +
			   cos(p1.lat * M_PI / 180.0) * cos(p2.lat * M_PI / 180.0) *
			   sin(dlon / 2.0) * sin(dlon / 2.0);
	
	double c = 2.0 * atan2(sqrt(a), sqrt(1.0 - a));
	return R * c;
}

// Calculate total distance from first point through all points to last point
double calculate_total_distance(Point * points, int num_points) {

	if (num_points < 2) {
		return 0.0;
	}
	
	double total_distance = 0.0;
	
	for (int i = 0; i < num_points - 1; i++) {
		total_distance += haversine_distance(points[i], points[i + 1]);
	}
	
	return total_distance;
}

// Calculate time from distance and speed
// distance in kilometers, speed in km/h
// Returns time in hours
double calculate_time_from_distance(double distance, double speed) {

	if (speed <= 0.0) {
		return 0.0;
	}

	return distance / speed;
}
