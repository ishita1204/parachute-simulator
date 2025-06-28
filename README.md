# 🪂 Parachute Physics Simulator

A comprehensive physics-based parachute simulation tool built with Streamlit. This application allows engineers to simulate parachute deployment systems with multiple phases (ACS, Drogue, Pilot, Main) and analyze their performance through detailed physics calculations.

## Features

- **Multi-Phase Simulation**: Support for ACS, Drogue, Pilot, and Main parachute phases
- **Physics-Accurate Calculations**: 
  - Altitude-dependent air density using ISA model
  - Drag force calculations with reefing effects
  - Inflation time modeling
  - Dynamic trajectory simulation
- **Interactive Visualization**: 
  - Force vs Time plots
  - Velocity vs Time plots  
  - Altitude vs Time plots
  - Phase-specific drag force analysis
- **Modular Design**: Select any combination of parachute phases
- **Input Validation**: Comprehensive parameter validation with helpful guidance
- **Real-time Results**: Immediate simulation results with key metrics

## Quick Start

### Online Deployment (Recommended)

1. **Deploy to Streamlit Cloud**:
   - Fork this repository
   - Connect to [Streamlit Cloud](https://streamlit.io/cloud)
   - Deploy directly from GitHub

2. **Access the Application**:
   - Open the deployed URL
   - Start simulating parachute systems immediately

### Local Development

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd parachute-simulator
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

4. **Open in Browser**:
   - Navigate to `http://localhost:8501`

## Usage Guide

### 1. Select Parachute Phases
- Choose which phases to simulate: ACS, Drogue, Pilot, Main
- You can select any combination (1-4 phases)

### 2. Configure Global Parameters
- **Initial Altitude**: Starting altitude (m)
- **Initial Velocity**: Starting velocity (m/s)  
- **Time Step**: Simulation time step (s)
- **Descent Angle**: Initial descent angle (degrees)

### 3. Set Phase-Specific Parameters
For each selected phase, configure:
- **Diameter**: Parachute diameter (m)
- **Drag Coefficient**: Aerodynamic drag coefficient
- **Deployment Altitude**: Altitude at which phase deploys (m)
- **Inflation Index**: Inflation time factor
- **Payload Mass**: Mass during this phase (kg)
- **Reefing Factor**: Reefing ratio (0-1, where 1 = no reefing)

### 4. Run Simulation
- Click "🚀 Run Simulation" to start
- View real-time results and interactive plots
- Analyze phase-specific performance metrics

## Physics Model

The simulation is based on fundamental aerodynamic principles:

### Drag Force Calculation
```
F_drag = (1/2) × ρ(h) × v² × C_d × A
```
Where:
- `ρ(h)` = altitude-dependent air density
- `v` = velocity
- `C_d` = drag coefficient
- `A` = parachute area

### Air Density (ISA Model)
```
ρ = ρ₀ × (1 - 0.0065 × h / 288.15)^5.2561
```

### Inflation Time
```
t_inflate = n × D / V
```
Where:
- `n` = inflation index
- `D` = diameter
- `V` = velocity at deployment

### Reefing Effects
During inflation, drag force scales linearly from reefed to full capacity:
```
F_effective = F_drag × (reefing_factor + (1 - reefing_factor) × inflation_progress)
```

## Project Structure

```
parachute-simulator/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Documentation
├── src/
│   ├── simulation.py     # Core simulation logic
│   └── physics.py        # Physics calculations
└── utils/
    ├── input_handler.py  # User input management
    └── graph_utils.py    # Plotting utilities
```

## Key Results

The simulation provides:
- **Max Drag Force**: Peak drag force per phase and total
- **Landing Velocity**: Final descent velocity
- **Total Flight Time**: Complete simulation duration
- **Horizontal Range**: Total horizontal distance traveled
- **Phase Analysis**: Detailed breakdown of each phase performance

## Validation

The physics model has been validated against:
- Standard atmospheric models (ISA)
- Parachute engineering principles
- MATLAB reference implementations
- Aerospace industry practices

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For questions, issues, or feature requests:
- Open an issue on GitHub
- Contact the development team
- Check the documentation

---

**Built with ❤️ for the aerospace engineering community**