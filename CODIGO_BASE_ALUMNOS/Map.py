# Required imports
import numpy as np
from Location import Location
from Boundaries import Boundaries
from Radar import Radar
from tqdm import tqdm

# Constant that avoids setting cells to have an associated cost of zero
EPSILON = 1e-4

class Map:
    """ Class that models the map for the simulation """
    def __init__(self, 
                 boundaries: Boundaries,
                 height:     np.int32, 
                 width:      np.int32, 
                 radars:     np.array=None):
        self.boundaries = boundaries        # Boundaries of the map
        self.height     = height            # Number of coordinates in the y-axis
        self.width      = width             # Number of coordinates int the x-axis
        self.radars     = radars            # List containing the radars (objects)

    def generate_radars(self, n_radars: np.int32) -> None:
        """ Generates n-radars randomly and inserts them into the radars list """
        # Select random coordinates inside the boundaries of the map
        lat_range = np.linspace(start=self.boundaries.min_lat, stop=self.boundaries.max_lat, num=self.height)
        lon_range = np.linspace(start=self.boundaries.min_lon, stop=self.boundaries.max_lon, num=self.width)
        rand_lats = np.random.choice(a=lat_range, size=n_radars, replace=False)
        rand_lons = np.random.choice(a=lon_range, size=n_radars, replace=False)
        self.radars = []        # Initialize 'radars' as an empty list

        # Loop for each radar that must be generated
        for i in range(n_radars):
            # Create a new radar
            new_radar = Radar(location=Location(latitude=rand_lats[i], longitude=rand_lons[i]),
                              transmission_power=np.random.uniform(low=1, high=1000000),
                              antenna_gain=np.random.uniform(low=10, high=50),
                              wavelength=np.random.uniform(low=0.001, high=10.0),
                              cross_section=np.random.uniform(low=0.1, high=10.0),
                              minimum_signal=np.random.uniform(low=1e-10, high=1e-15),
                              total_loss=np.random.randint(low=1, high=10),
                              covariance=None)

            # Insert the new radar
            self.radars.append(new_radar)
        return
    
    def get_radars_locations_numpy(self) -> np.array:
        """ Returns an array with the coordiantes (lat, lon) of each radar registered in the map """
        locations = np.zeros(shape=(len(self.radars), 2), dtype=np.float32)
        for i in range(len(self.radars)):
            locations[i] = self.radars[i].location.to_numpy()
        return locations
    
    def compute_detection_map(self) -> np.array:
        lat_range = np.linspace(self.boundaries.min_lat, self.boundaries.max_lat, self.height)
        lon_range = np.linspace(self.boundaries.min_lon, self.boundaries.max_lon, self.width)
        grid = np.array(np.meshgrid(lat_range, lon_range)).T.reshape(-1, 2).reshape(self.height, self.width, 2)

        # Initialize the detection map with zeros
        detection_map = np.zeros((grid.shape[0], grid.shape[1]), dtype=np.float32)

        # Iterate over each cell in the grid
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                latitude, longitude = grid[i, j]

                # Compute the detection level for each radar and take the maximum
                detection_map[i, j] = max(radar.compute_detection_level(latitude, longitude) for radar in self.radars)

        # Normalize the detection map using MinMax scaling
        detection_min = np.min(detection_map)
        detection_max = np.max(detection_map)
        epsilon = 1e-4  # Small value to avoid zero probabilities

        if detection_max > detection_min:  # Avoid division by zero
            detection_map = ((detection_map - detection_min) / (detection_max - detection_min)) * (
                        1 - epsilon) + epsilon
        else:
            # If all values are the same, set the entire map to epsilon
            detection_map.fill(epsilon)

        return detection_map