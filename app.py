import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from src.simulation import ParachuteSimulation
from src.physics import PhysicsCalculator
from utils.input_handler import InputHandler
from utils.graph_utils import GraphUtils

# Page configuration
st.set_page_config(
    page_title="Parachute Physics Simulator",
    page_icon="🪂",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        text-align: center;
        margin-bottom: 2rem;
    }
    .phase-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #374151;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        padding: 0.5rem;
        background-color: #f9fafb;
        border-left: 4px solid #3b82f6;
    }
    .results-container {
        background-color: #f8fafc;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 0.375rem;
        border: 1px solid #d1d5db;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">🪂 Parachute Physics Simulator</h1>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'simulation_complete' not in st.session_state:
        st.session_state.simulation_complete = False
    if 'results' not in st.session_state:
        st.session_state.results = None
    if 'plots_data' not in st.session_state:
        st.session_state.plots_data = None
    
    # Sidebar for phase selection
    with st.sidebar:
        st.header("Simulation Configuration")
        
        # Phase selection
        st.subheader("Select Parachute Phases")
        selected_phases = st.multiselect(
            "Choose phases to simulate:",
            options=["ACS", "Drogue", "Pilot", "Main"],
            help="Select one or more parachute phases to simulate"
        )
        
        if not selected_phases:
            st.warning("Please select at least one parachute phase to continue.")
            return
        
        # Global parameters
        st.subheader("Global Parameters")
        
        col1, col2 = st.columns(2)
        with col1:
            initial_altitude = st.number_input(
                "Initial Altitude (m)",
                min_value=0.0,
                value=None,
                step=100.0,
                key="initial_altitude"
            )
            initial_velocity = st.number_input(
                "Initial Velocity (m/s)",
                min_value=0.0,
                value=None,
                step=10.0,
                key="initial_velocity"
            )
        
        with col2:
            time_step = st.number_input(
                "Time Step (s)",
                min_value=0.001,
                max_value=1.0,
                value=None,
                step=0.001,
                key="time_step"
            )
            descent_angle = st.number_input(
                "Descent Angle (degrees)",
                min_value=0.0,
                max_value=90.0,
                value=None,
                step=1.0,
                key="descent_angle"
            )
    
    # Main content area
    input_handler = InputHandler()
    
    # Phase-specific inputs
    st.header("Phase-Specific Parameters")
    phase_params = input_handler.get_phase_inputs(selected_phases)
    
    # Validation
    global_params = {
        'initial_altitude': initial_altitude,
        'initial_velocity': initial_velocity,
        'time_step': time_step,
        'descent_angle': descent_angle
    }
    
    # Check if all inputs are provided
    all_inputs_valid = input_handler.validate_inputs(global_params, phase_params, selected_phases)
    
    if all_inputs_valid:
        # Run simulation button
        if st.button("🚀 Run Simulation", type="primary", use_container_width=True):
            with st.spinner("Running physics simulation..."):
                try:
                    # Initialize simulation
                    simulation = ParachuteSimulation(global_params, phase_params, selected_phases)
                    
                    # Run simulation
                    results = simulation.run()
                    
                    # Store results in session state
                    st.session_state.results = results
                    st.session_state.simulation_complete = True
                    st.session_state.plots_data = simulation.get_plot_data()
                    
                    st.success("Simulation completed successfully!")
                    
                except Exception as e:
                    st.error(f"Simulation failed: {str(e)}")
                    return
    
    # Display results if simulation is complete
    if st.session_state.simulation_complete and st.session_state.results:
        display_results(st.session_state.results, st.session_state.plots_data)
    
    elif not all_inputs_valid:
        st.info("Please fill in all required parameters to run the simulation.")

def display_results(results, plots_data):
    st.header("Simulation Results")
    
    # Key metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Max Total Drag Force",
            f"{results['max_total_drag_force']:.1f} N"
        )
    
    with col2:
        st.metric(
            "Landing Velocity",
            f"{results['landing_velocity']:.1f} m/s"
        )
    
    with col3:
        st.metric(
            "Total Flight Time",
            f"{results['total_flight_time']:.1f} s"
        )
    
    with col4:
        st.metric(
            "Total Horizontal Range",
            f"{results['total_horizontal_range']:.1f} m"
        )
    
    with col5:
        st.metric(
            "Final Altitude",
            f"{results['final_altitude']:.1f} m"
        )
    
    # Phase-specific results
    if 'phase_results' in results:
        st.subheader("Phase-Specific Results")
        phase_df = pd.DataFrame(results['phase_results'])
        st.dataframe(phase_df, use_container_width=True)
    
    # Plots
    st.header("Simulation Plots")
    
    # Plot selection
    plot_options = st.multiselect(
        "Select plots to display:",
        options=["Force vs Time", "Velocity vs Time", "Altitude vs Time"],
        default=["Force vs Time", "Velocity vs Time", "Altitude vs Time"]
    )
    
    graph_utils = GraphUtils()
    
    for plot_type in plot_options:
        if plot_type == "Force vs Time":
            fig = graph_utils.create_force_plot(plots_data)
            st.plotly_chart(fig, use_container_width=True)
        
        elif plot_type == "Velocity vs Time":
            fig = graph_utils.create_velocity_plot(plots_data)
            st.plotly_chart(fig, use_container_width=True)
        
        elif plot_type == "Altitude vs Time":
            fig = graph_utils.create_altitude_plot(plots_data)
            st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()