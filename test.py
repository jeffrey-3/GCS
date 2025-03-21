import numpy as np
import matplotlib.pyplot as plt

class AltitudeKalmanFilter:
    def __init__(self, dt, process_noise, baro_noise, range_noise):
        """
        Initialize the Kalman filter.
        
        Parameters:
            dt (float): Time step.
            process_noise (np.array): Process noise covariance matrix (3x3).
            baro_noise (float): Barometer measurement noise variance.
            range_noise (float): Rangefinder measurement noise variance.
        """
        # State vector: [altitude, vertical_velocity, terrain_height]
        self.state = np.zeros(3)  # Initial state
        self.covariance = np.eye(3)  # Initial state covariance

        # State transition matrix
        self.F = np.array([
            [1, dt, 0],  # altitude = altitude + velocity * dt
            [0, 1, 0],   # velocity = velocity
            [0, 0, 1]    # terrain_height = terrain_height
        ])

        # Control input matrix (for accelerometer input)
        self.G = np.array([[0.5 * dt**2], [dt], [0]])

        # Process noise covariance matrix
        self.Q = process_noise

        # Measurement noise covariances
        self.R_baro = baro_noise  # Barometer noise
        self.R_range = range_noise  # Rangefinder noise

        # Measurement matrices
        self.H_baro = np.array([[1, 0, 0]])  # Barometer measures altitude
        self.H_range = np.array([[1, 0, -1]])  # Rangefinder measures (altitude - terrain_height)

    def predict(self, acceleration):
        """
        Prediction step of the Kalman filter.
        
        Parameters:
            acceleration (float): Vertical acceleration from the accelerometer (after subtracting gravity).
        """
        # Predict state
        self.state = self.F @ self.state + self.G * acceleration

        # Predict covariance
        self.covariance = self.F @ self.covariance @ self.F.T + self.Q

    def update_baro(self, baro_measurement):
        """
        Update step using the barometer measurement.
        
        Parameters:
            baro_measurement (float): Barometer altitude measurement.
        """
        # Kalman gain
        K = self.covariance @ self.H_baro.T @ np.linalg.inv(
            self.H_baro @ self.covariance @ self.H_baro.T + self.R_baro
        )

        # Update state
        self.state = self.state + K * (baro_measurement - self.H_baro @ self.state)

        # Update covariance
        self.covariance = (np.eye(3) - K @ self.H_baro) @ self.covariance

    def update_range(self, range_measurement):
        """
        Update step using the rangefinder measurement.
        
        Parameters:
            range_measurement (float): Rangefinder height-above-terrain measurement.
        """
        # Kalman gain
        K = self.covariance @ self.H_range.T @ np.linalg.inv(
            self.H_range @ self.covariance @ self.H_range.T + self.R_range
        )

        # Update state
        self.state = self.state + K * (range_measurement - self.H_range @ self.state)

        # Update covariance
        self.covariance = (np.eye(3) - K @ self.H_range) @ self.covariance

    def get_state(self):
        """
        Get the current state estimate.
        
        Returns:
            np.array: [altitude, vertical_velocity, terrain_height]
        """
        return self.state

# Simulation parameters
dt = 0.1  # Time step (s)
num_steps = 100  # Number of time steps to simulate

# Process noise covariance matrix
process_noise = np.diag([0.1, 0.1, 0.01])  # Tune based on system dynamics

# Measurement noise variances
baro_noise = 1.0  # Barometer noise variance
range_noise = 0.1  # Rangefinder noise variance

# Initialize Kalman filter
kf = AltitudeKalmanFilter(dt, process_noise, baro_noise, range_noise)

# True values (for simulation)
true_altitude = 100.0  # True altitude (m)
true_terrain_height = 50.0  # True terrain height (m)
true_vertical_velocity = 0.0  # True vertical velocity (m/s)

# Arrays to store results
time_steps = np.arange(0, num_steps * dt, dt)
estimated_altitudes = []
estimated_velocities = []
estimated_terrain_heights = []
true_altitudes = []
true_terrain_heights = []

# Simulate over time steps
for step in range(num_steps):
    # Simulate true altitude and terrain height changes
    if step > 50:
        true_terrain_height += 0.1  # Terrain height increases after step 50
    true_altitude += true_vertical_velocity * dt

    # Simulate sensor measurements
    baro_measurement = true_altitude + np.random.normal(0, np.sqrt(baro_noise))
    range_measurement = true_altitude - true_terrain_height + np.random.normal(0, np.sqrt(range_noise))

    # Kalman filter steps
    kf.predict(acceleration=0.0)  # Assume no acceleration for simplicity
    kf.update_baro(baro_measurement)
    kf.update_range(range_measurement)

    # Get estimated state
    estimated_state = kf.get_state()

    # Store results
    estimated_altitudes.append(estimated_state[0])
    estimated_velocities.append(estimated_state[1])
    estimated_terrain_heights.append(estimated_state[2])
    true_altitudes.append(true_altitude)
    true_terrain_heights.append(true_terrain_height)

# Plot results
plt.figure(figsize=(12, 8))

# Plot altitude
plt.subplot(3, 1, 1)
plt.plot(time_steps, true_altitudes, label="True Altitude", linestyle="--")
plt.plot(time_steps, estimated_altitudes, label="Estimated Altitude")
plt.xlabel("Time (s)")
plt.ylabel("Altitude (m)")
plt.legend()
plt.title("Altitude Estimation")

# Plot vertical velocity
plt.subplot(3, 1, 2)
plt.plot(time_steps, estimated_velocities, label="Estimated Vertical Velocity")
plt.xlabel("Time (s)")
plt.ylabel("Vertical Velocity (m/s)")
plt.legend()
plt.title("Vertical Velocity Estimation")

# Plot terrain height
plt.subplot(3, 1, 3)
plt.plot(time_steps, true_terrain_heights, label="True Terrain Height", linestyle="--")
plt.plot(time_steps, estimated_terrain_heights, label="Estimated Terrain Height")
plt.xlabel("Time (s)")
plt.ylabel("Terrain Height (m)")
plt.legend()
plt.title("Terrain Height Estimation")

plt.tight_layout()
plt.show()