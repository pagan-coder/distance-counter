# Distance Counter

Aiohttp server with Cython and C integration for calculating distances between geographic coordinates.

It utilizes Python's asyncio loop to quickly serve user requests (IO-bound task) while moving the calculation to a thread and C (CPU-bound task).

## Description

The application provides a REST API endpoint for calculating the total distance between points on Earth using the Haversine formula. The calculation is performed in C code through a Cython wrapper, ensuring high performance.

## Architecture

- **Python (app.py)**: aiohttp server with POST endpoint `/count-distance`
- **Cython (distance_wrapper.pyx)**: Wrapper between Python and C code
- **C (c_lib/distance.c, distance.h)**: Distance calculation using Haversine formula
- **ThreadPool**: Asynchronous request processing with thread pool

## Requirements

- Python 3.7+
- Cython >= 0.29.0
- aiohttp >= 3.8.0
- GCC compiler

## Installation and Build

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Build Cython extension:

```bash
python3 setup.py build_ext --inplace
```

This will create a `distance_wrapper.cpython-*.so` file containing the compiled Cython module.

## Running

Start the server:

```bash
python3 app.py
```

The server will run on `http://0.0.0.0:8080`

## API

### POST /count-distance

Calculates the total distance between points and the time required to travel this distance at a given speed.

**Request body:**
```json
{
    "coordinates": [[lat1, lon1], [lat2, lon2], ...],
    "speed": 80.0
}
```

- `coordinates`: Array of [lat, lon] coordinates (minimum 2 points)
- `speed`: Speed in km/h (optional, default: 50.0 km/h)

**Response:**
```json
{
    "distance": 322.65,
    "time": 4.0332
}
```

- `distance_km`: Total distance in kilometers
- `time_hours`: Time in hours

## Example with multiple points (route)

```bash
curl -X POST http://localhost:8080/count-distance \
  -H "Content-Type: application/json" \
  -d '{
    "coordinates": [
      [50.037778, 13.8725],
      [50.554905, 13.931091],
      [54.676389, 13.437778]
    ],
    "speed": 88.0
  }'
```
