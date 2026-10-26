# StarFinder

StarFinder calculates the live altitude and azimuth of a star or Messier object for a selected observing location. It is intended as a building block for telescope-automation projects.

## Features

- Calculates a target's current horizontal coordinates:
  - **Altitude**: angle above or below the horizon.
  - **Azimuth**: compass direction around the horizon.
- Uses the computer's current date and time to calculate the target's live position.
- Looks up targets from the included `Stars.txt` and `Messier.txt` catalogues.
- Looks up observing locations from the included `Cities.txt` database.
- Continuously refreshes the calculated position once per second.

## Requirements

- Python 3
- NumPy

Install NumPy with:

```bash
python3 -m pip install numpy
```

On Windows, you may need to use `py` instead of `python3`.

## Configuration

Before running the program, open `Star_Coord.py` and update the configuration near the bottom of the file:

```python
fname_s = "Stars.txt"      # Use "Messier.txt" for Messier objects
fname_c = "Cities.txt"
target_name = "Vega"       # Must match an entry in the selected catalogue
city = "Athens"
country = "Greece"
```

Use a target name exactly as it appears in the selected catalogue. For example:

- `Vega` when using `Stars.txt`
- `M13` when using `Messier.txt`

The city and country must also match an entry in `Cities.txt`. If a location is not available, add it to the database or update the coordinate lookup before running the program.

## Run

Run the program from the repository directory so it can find the data files:

```bash
python3 Star_Coord.py
```

On Windows, use:

```bash
py Star_Coord.py
```

The terminal will display the target's Greenwich Mean Sidereal Time, altitude, and azimuth. The output is refreshed every second. Press `Ctrl+C` to stop the program.

## Coordinate conventions

- **Altitude** is reported in degrees. Positive values indicate that the object is above the horizon; negative values indicate that it is below the horizon.
- **Azimuth** is reported in degrees, measured around the horizon.
- The program uses the computer's local clock and timezone to determine the current time.

## Included data files

- `Star_Coord.py` — main program and coordinate calculations.
- `Stars.txt` — bright-star catalogue containing right ascension and declination values.
- `Messier.txt` — Messier-object catalogue containing equatorial coordinates and object information.
- `Cities.txt` — city, country, latitude, and longitude data used for observing locations.

## Notes and limitations

- Run the program from the repository root; the script currently uses relative paths for the catalogue files.
- Target and location names are case-sensitive and must match the data files.
- The default values in `Star_Coord.py` are examples. Change them before running if necessary.
- The calculated coordinates are intended for general tracking and telescope-automation experiments. Additional calibration and more precise astronomical corrections may be required for high-precision pointing.
