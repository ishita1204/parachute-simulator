import numpy as np
from .physics import PhysicsCalculator

class ParachuteSimulation:
    def __init__(self, global_params, phase_params, selected_phases):
        self.global_params = global_params
        self.phase_params = phase_params
        self.selected_phases = selected_phases
        self.physics = PhysicsCalculator()
        
        # Initialize simulation arrays
        self.time = []
        self.altitude = []
        self.velocity = []
        self.total_drag_force = []
        self.phase_drag_forces = {phase: [] for phase in selected_phases}
        self.horizontal_position = []
        
        # Current state
        self.current_time = 0.0
        self.current_altitude = global_params['initial_altitude']
        self.current_velocity = global_params['initial_velocity']
        self.current_horizontal_pos = 0.0
        self.dt = global_params['time_step']
        self.descent_angle_rad = np.radians(global_params['descent_angle'])
        
        # Phase tracking
        self.active_phases = []
        self.deployed_phases = set()
        self.phase_deployment_times = {}
        self.phase_inflation_times = {}
        
    def run(self):
        """Run the complete parachute simulation"""
        
        while self.current_altitude > 0:
            # Check for phase deployments
            self._check_phase_deployments()
            
            # Calculate forces for current time step
            self._calculate_forces()
            
            # Update dynamics
            self._update_dynamics()
            
            # Store data
            self._store_data()
            
            # Advance time
            self.current_time += self.dt
            
            # Safety check
            if self.current_time > 10000:  # 10000 seconds max
                break
        
        return self._compile_results()
    
    def _check_phase_deployments(self):
        """Check if any phases should be deployed at current altitude"""
        for phase in self.selected_phases:
            if phase not in self.deployed_phases:
                deployment_altitude = self.phase_params[phase]['deployment_altitude']
                
                if self.current_altitude <= deployment_altitude:
                    self._deploy_phase(phase)
    
    def _deploy_phase(self, phase):
        """Deploy a specific parachute phase"""
        self.deployed_phases.add(phase)
        self.phase_deployment_times[phase] = self.current_time
        
        # Calculate inflation time
        diameter = self.phase_params[phase]['diameter']
        n_factor = self.phase_params[phase]['inflation_index']
        
        # Use current velocity for inflation time calculation
        inflation_time = self.physics.calculate_inflation_time(
            n_factor, diameter, self.current_velocity
        )
        
        self.phase_inflation_times[phase] = inflation_time
        
        # Add to active phases
        self.active_phases.append({
            'phase': phase,
            'deployment_time': self.current_time,
            'inflation_time': inflation_time,
            'params': self.phase_params[phase]
        })
    
    def _calculate_forces(self):
        """Calculate drag forces for all active phases"""
        total_drag = 0.0
        
        # Reset phase drag forces for current time step
        for phase in self.selected_phases:
            self.phase_drag_forces[phase].append(0.0)
        
        # Calculate drag for each active phase
        for phase_info in self.active_phases:
            phase = phase_info['phase']
            params = phase_info['params']
            
            # Calculate time since deployment
            time_since_deployment = self.current_time - phase_info['deployment_time']
            
            # Calculate drag force
            drag_force = self.physics.calculate_drag_force(
                altitude=self.current_altitude,
                velocity=self.current_velocity,
                diameter=params['diameter'],
                drag_coefficient=params['drag_coefficient'],
                reefing_factor=params['reefing_factor'],
                time_since_deployment=time_since_deployment,
                inflation_time=phase_info['inflation_time']
            )
            
            # Update phase-specific drag
            self.phase_drag_forces[phase][-1] = drag_force
            total_drag += drag_force
        
        self.total_drag_force.append(total_drag)
    
    def _update_dynamics(self):
        """Update altitude, velocity, and horizontal position"""
        # Get current forces
        current_drag = self.total_drag_force[-1] if self.total_drag_force else 0.0
        
        # Calculate mass (assuming constant for now)
        mass = self._get_current_mass()
        
        # Calculate acceleration
        gravity_component = self.physics.g * np.cos(self.descent_angle_rad)
        drag_deceleration = current_drag / mass
        
        # Net acceleration (positive downward)
        net_acceleration = gravity_component - drag_deceleration
        
        # Update velocity (Euler integration)
        self.current_velocity += net_acceleration * self.dt
        
        # Ensure velocity doesn't go negative
        self.current_velocity = max(0, self.current_velocity)
        
        # Update altitude
        altitude_change = self.current_velocity * self.dt
        self.current_altitude -= altitude_change
        
        # Update horizontal position
        horizontal_velocity = self.current_velocity * np.sin(self.descent_angle_rad)
        self.current_horizontal_pos += horizontal_velocity * self.dt
    
    def _get_current_mass(self):
        """Get current mass (simplified - using first deployed phase mass)"""
        if self.active_phases:
            return self.active_phases[0]['params']['payload_mass']
        else:
            # Use mass from first selected phase as default
            first_phase = self.selected_phases[0]
            return self.phase_params[first_phase]['payload_mass']
    
    def _store_data(self):
        """Store current simulation data"""
        self.time.append(self.current_time)
        self.altitude.append(max(0, self.current_altitude))
        self.velocity.append(self.current_velocity)
        self.horizontal_position.append(self.current_horizontal_pos)
    
    def _compile_results(self):
        """Compile simulation results"""
        results = {
            'max_total_drag_force': max(self.total_drag_force) if self.total_drag_force else 0,
            'landing_velocity': self.velocity[-1] if self.velocity else 0,
            'total_flight_time': self.time[-1] if self.time else 0,
            'total_horizontal_range': self.horizontal_position[-1] if self.horizontal_position else 0,
            'final_altitude': self.altitude[-1] if self.altitude else 0,
            'phase_results': []
        }
        
        # Phase-specific results
        for phase in self.selected_phases:
            phase_drag_forces = self.phase_drag_forces[phase]
            max_drag = max(phase_drag_forces) if phase_drag_forces else 0
            
            results['phase_results'].append({
                'Phase': phase,
                'Max Drag Force (N)': f"{max_drag:.1f}",
                'Deployment Time (s)': f"{self.phase_deployment_times.get(phase, 0):.1f}",
                'Inflation Time (s)': f"{self.phase_inflation_times.get(phase, 0):.1f}"
            })
        
        return results
    
    def get_plot_data(self):
        """Get data for plotting"""
        return {
            'time': np.array(self.time),
            'altitude': np.array(self.altitude),
            'velocity': np.array(self.velocity),
            'total_drag_force': np.array(self.total_drag_force),
            'phase_drag_forces': {phase: np.array(forces) for phase, forces in self.phase_drag_forces.items()},
            'horizontal_position': np.array(self.horizontal_position),
            'selected_phases': self.selected_phases
        }