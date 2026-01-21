#ifndef DISTANCE_H
#define DISTANCE_H

typedef struct {
	double lat;
	double lon;
} Point;

double calculate_total_distance(Point* points, int num_points);
double calculate_time_from_distance(double distance, double speed);

#endif

