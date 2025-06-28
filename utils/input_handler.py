import streamlit as st

class InputHandler:
    def __init__(self):
        self.phase_colors = {
            'ACS': '#ef4444',
            'Drogue': '#f97316', 
            'Pilot': '#eab308',
            'Main': '#22c55e'
        }
    
    def get_phase_inputs(self, selected_phases):
        """Get input parameters for selected phases"""
        phase_params = {}
        
        for phase in selected_phases:
            st.markdown(f'<div class="phase-header" style="border-left-color: {self.phase_colors[phase]}">{phase} Parachute Parameters</div>', 
                       unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                diameter = st.number_input(
                    f"Diameter (m)",
                    min_value=0.1,
                    value=None,
                    step=0.1,
                    key=f"{phase}_diameter",
                    help=f"Diameter of the {phase} parachute"
                )
                
                drag_coefficient = st.number_input(
                    f"Drag Coefficient (Cd)",
                    min_value=0.1,
                    value=None,
                    step=0.1,
                    key=f"{phase}_cd",
                    help=f"Drag coefficient for {phase} parachute"
                )
            
            with col2:
                deployment_altitude = st.number_input(
                    f"Deployment Altitude (m)",
                    min_value=0.0,
                    value=None,
                    step=100.0,
                    key=f"{phase}_deploy_alt",
                    help=f"Altitude at which {phase} parachute deploys"
                )
                
                inflation_index = st.number_input(
                    f"Inflation Index (n)",
                    min_value=0.1,
                    value=None,
                    step=0.1,
                    key=f"{phase}_inflation_index",
                    help=f"Inflation index for {phase} parachute"
                )
            
            with col3:
                payload_mass = st.number_input(
                    f"Payload Mass (kg)",
                    min_value=1.0,
                    value=None,
                    step=10.0,
                    key=f"{phase}_mass",
                    help=f"Mass of payload for {phase} phase"
                )
                
                reefing_factor = st.number_input(
                    f"Reefing Factor (0-1)",
                    min_value=0.0,
                    max_value=1.0,
                    value=None,
                    step=0.1,
                    key=f"{phase}_reefing",
                    help=f"Reefing factor for {phase} parachute (0 = fully reefed, 1 = no reefing)"
                )
            
            phase_params[phase] = {
                'diameter': diameter,
                'drag_coefficient': drag_coefficient,
                'deployment_altitude': deployment_altitude,
                'inflation_index': inflation_index,
                'payload_mass': payload_mass,
                'reefing_factor': reefing_factor
            }
        
        return phase_params
    
    def validate_inputs(self, global_params, phase_params, selected_phases):
        """Validate that all required inputs are provided"""
        
        # Check global parameters
        for param, value in global_params.items():
            if value is None or value <= 0:
                return False
        
        # Check phase parameters
        for phase in selected_phases:
            if phase not in phase_params:
                return False
            
            for param, value in phase_params[phase].items():
                if value is None or value < 0:
                    return False
                
                # Special validation for reefing factor
                if param == 'reefing_factor' and (value < 0 or value > 1):
                    return False
        
        # Check deployment altitude ordering (if multiple phases)
        if len(selected_phases) > 1:
            deployment_altitudes = []
            for phase in selected_phases:
                deployment_altitudes.append(
                    (phase, phase_params[phase]['deployment_altitude'])
                )
            
            # Sort by deployment altitude (descending)
            deployment_altitudes.sort(key=lambda x: x[1], reverse=True)
            
            # Check if altitudes are in logical order
            phase_order = ['ACS', 'Drogue', 'Pilot', 'Main']
            sorted_phases = [phase for phase, _ in deployment_altitudes]
            
            # Warn if deployment order doesn't match typical sequence
            if sorted_phases != [p for p in phase_order if p in selected_phases]:
                st.warning("⚠️ Deployment altitudes may not follow typical sequence (ACS → Drogue → Pilot → Main)")
        
        return True
    
    def get_phase_info(self, phase):
        """Get information about a specific phase"""
        phase_info = {
            'ACS': {
                'name': 'Attitude Control System',
                'description': 'Small parachute for initial stabilization',
                'typical_diameter': '1-3 m',
                'typical_cd': '0.8-1.2'
            },
            'Drogue': {
                'name': 'Drogue Parachute',
                'description': 'Medium parachute for deceleration',
                'typical_diameter': '3-8 m',
                'typical_cd': '1.0-1.4'
            },
            'Pilot': {
                'name': 'Pilot Parachute',
                'description': 'Parachute to deploy main chute',
                'typical_diameter': '2-5 m',
                'typical_cd': '0.9-1.3'
            },
            'Main': {
                'name': 'Main Parachute',
                'description': 'Primary parachute for landing',
                'typical_diameter': '10-30 m',
                'typical_cd': '1.2-1.8'
            }
        }
        
        return phase_info.get(phase, {})