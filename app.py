import asyncio
import json

import aiohttp.web

from concurrent.futures import ThreadPoolExecutor
# The following module is built by Cython and C code
from distance_wrapper import calculate_distance_cython

# Thread pool for executing Cython/C code
# CPU-bound tasks should be executed in a thread pool
executor = ThreadPoolExecutor(max_workers=4)

async def count_distance(request):
	"""
	POST /count-distance
	Expects JSON body:
	{
		"coordinates": [[lat1, lon1], [lat2, lon2], ...],
		"speed": 50.0  // optional, default 50 km/h
	}
	
	Returns:
	{
		"distance": 123.45,  // in kilometers
		"time": 2.47  // in hours
	}
	"""
	try:
		data = await request.json()
		
		# Validate input
		if 'coordinates' not in data:

			return aiohttp.web.json_response(
				{"error": "Missing required field: coordinates"},
				status=400
			)
		
		coordinates = data['coordinates']

		if not isinstance(coordinates, list) or len(coordinates) < 2:

			return aiohttp.web.json_response(
				{"error": "Coordinates must be an array with at least 2 points"},
				status=400
			)
		
		# Validate each coordinate
		for i, coord in enumerate(coordinates):

			if not isinstance(coord, list) or len(coord) != 2:

				return aiohttp.web.json_response(
					{"error": "Coordinate {} must be [lat, lon]".format(i)},
					status=400
				)

			try:
				float(coord[0])
				float(coord[1])

			except (ValueError, TypeError):

				return aiohttp.web.json_response(
					{"error": "Coordinate {} must contain numeric values".format(i)},
					status=400
				)

		# Get speed (default 50 km/h)
		speed = float(data.get('speed', 50.0))

		if speed <= 0:

			return aiohttp.web.json_response(
				{"error": "Speed must be greater than 0"},
				status=400
			)

		# Run calculation in thread pool (Cython -> C)
		loop = asyncio.get_event_loop()

		distance, time = await loop.run_in_executor(
			executor,
			calculate_distance_cython,
			coordinates,
			speed
		)

		return aiohttp.web.json_response({
			'distance_km': round(distance, 2),
			'time_hours': round(time, 4)
		})
	
	except json.JSONDecodeError:

		return aiohttp.web.json_response(
			{"error": "Invalid JSON"},
			status=400
		)

	except Exception as e:

		return aiohttp.web.json_response(
			{"error": str(e)},
			status=500
		)


def create_app():
	app = aiohttp.web.Application()
	# Add routes (IO-bound tasks should be executed on async loop)
	app.router.add_post('/count-distance', count_distance)

	return app


if __name__ == '__main__':
	app = create_app()
	aiohttp.web.run_app(app, host='0.0.0.0', port=8080)
