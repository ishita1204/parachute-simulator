import numpy as np

class PhysicsCalculator:
    def __init__(self):
        # Physical constants
        self.g = 9.81  # gravity (m/s^2)
        self.rho0 = 1.225  # sea-level air density (kg/m^3)
        self.T0 = 288.15  # sea-level temperature (K)
        self.L = 0.0065  # temperature lapse rate (K/m)
        
    def calculate_air_density(self, altitude):
        """
        Calculate air density at given altitude using ISA model
        rho = rho0 * (1 - 0.0065 * h / 288.15) ^ 5.2561
        """
        if altitude < 0:
            altitude = 0
        
        temperature_ratio = 1 - (self.L * altitude / self.T0)
        
        if temperature_ratio <= 0:
            return 0.001  # Minimum density for very high altitudes
        
        density = self.rho0 * (temperature_ratio ** 5.2561)
        return max(density, 0.001)  # Ensure positive density
    
    def calculate_drag_force(self, altitude, velocity, diameter, drag_coefficient, 
                           reefing_factor, time_since_deployment, inflation_time):
        """
        Calculate drag force: F_d = (1/2) * ρ(h) * v^2 * C_d * A
        Includes reefing effects during inflation
        """
        if velocity <= 0:
            return 0
        
        # Calculate air density at current altitude
        rho = self.calculate_air_density(altitude)
        
        # Calculate parachute area
        area = np.pi * (diameter / 2) ** 2
        
        # Base drag force
        base_drag = 0.5 * rho * velocity**2 * drag_coefficient * area
        
        # Apply reefing effects during inflation
        if time_since_deployment < inflation_time:
            # Linear scaling from reefed to full drag during inflation
            inflation_progress = time_since_deployment / inflation_time
            effective_drag_coefficient = (reefing_factor + 
                                        (1 - reefing_factor) * inflation_progress)
            drag_force = base_drag * effective_drag_coefficient
        else:
            # Full drag after inflation
            drag_force = base_drag
        
        return drag_force
    
    def calculate_inflation_time(self, n_factor, diameter, velocity):
        """
        Calculate inflation time: t_inflate = n * D / V
        """
        if velocity <= 0:
            return 0
        
        inflation_time = n_factor * diameter / velocity
        return max(inflation_time, 0.1)  # Minimum inflation time
    
    def calculate_terminal_velocity(self, mass, diameter, drag_coefficient, altitude):
        """
        Calculate terminal velocity: v_terminal = sqrt(2*m*g / (ρ*C_d*A))
        """
        rho = self.calculate_air_density(altitude)
        area = np.pi * (diameter / 2) ** 2
        
        if rho <= 0 or drag_coefficient <= 0 or area <= 0:
            return 0
        
        terminal_velocity = np.sqrt(2 * mass * self.g / (rho * drag_coefficient * area))
        return terminal_velocity
    
    def calculate_trajectory_with_wind(self, velocity, angle, wind_speed, wind_direction):
        """
        Calculate trajectory components with wind effects
        """
        # Velocity components
        v_vertical = velocity * np.cos(np.radians(angle))
        v_horizontal = velocity * np.sin(np.radians(angle))
        
        # Add wind effect
        v_horizontal_total = v_horizontal + wind_speed * np.cos(np.radians(wind_direction))
        
        return v_vertical, v_horizontal_total
    
    def calculate_reynolds_number(self, velocity, diameter, altitude):
        """
        Calculate Reynolds number for parachute flow
        """
        rho = self.calculate_air_density(altitude)
        
        # Dynamic viscosity (approximate for air)
        mu = 1.81e-5  # kg/(m*s) at sea level
        
        if mu <= 0:
            return 0
        
        reynolds = rho * velocity * diameter / mu
        return reynolds
    
    def calculate_drag_coefficient_correction(self, reynolds_number):
        """
        Apply Reynolds number correction to drag coefficient
        """
        # Simplified correction - in practice this would be more complex
        if reynolds_number < 1000:
            return 0.8  # Low Reynolds number correction
        else:
            return 1.0  # High Reynolds number (typical for parachutes)