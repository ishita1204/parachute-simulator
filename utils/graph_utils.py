import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

class GraphUtils:
    def __init__(self):
        self.phase_colors = {
            'ACS': '#ef4444',
            'Drogue': '#f97316',
            'Pilot': '#eab308', 
            'Main': '#22c55e'
        }
    
    def _get_time_tick_spacing(self, max_time):
        """
        Calculate appropriate tick spacing based on total simulation time
        """
        if max_time <= 300:
            return 0.5  # 0.5 second intervals for shorter simulations
        elif max_time <= 1500:
            return 5.0  # 5 second intervals for medium simulations
        else:
            return 10.0  # 10 second intervals for long simulations
    
    def _configure_time_axis(self, fig, plots_data):
        """
        Configure x-axis with fixed linear time ticks
        """
        if len(plots_data['time']) > 0:
            max_time = np.max(plots_data['time'])
            dtick = self._get_time_tick_spacing(max_time)
            
            fig.update_xaxes(
                tickmode='linear',
                tick0=0,
                dtick=dtick
            )
    
    def create_force_plot(self, plots_data):
        """Create Force vs Time plot"""
        fig = go.Figure()
        
        # Add total drag force
        fig.add_trace(go.Scatter(
            x=plots_data['time'],
            y=plots_data['total_drag_force'],
            mode='lines',
            name='Total Drag Force',
            line=dict(color='#1f2937', width=3),
            hovertemplate='<b>Total Drag Force</b><br>Time: %{x:.2f} s<br>Force: %{y:.1f} N<extra></extra>'
        ))
        
        # Add individual phase forces
        for phase in plots_data['selected_phases']:
            if phase in plots_data['phase_drag_forces']:
                phase_forces = plots_data['phase_drag_forces'][phase]
                if len(phase_forces) > 0 and np.max(phase_forces) > 0:
                    fig.add_trace(go.Scatter(
                        x=plots_data['time'],
                        y=phase_forces,
                        mode='lines',
                        name=f'{phase} Drag Force',
                        line=dict(color=self.phase_colors[phase], width=2),
                        hovertemplate=f'<b>{phase} Drag Force</b><br>Time: %{{x:.2f}} s<br>Force: %{{y:.1f}} N<extra></extra>'
                    ))
        
        # Update layout
        fig.update_layout(
            title='Drag Force vs Time',
            xaxis_title='Time (s)',
            yaxis_title='Drag Force (N)',
            hovermode='x unified',
            showlegend=True,
            height=500,
            template='plotly_white'
        )
        
        # Configure fixed linear time axis
        self._configure_time_axis(fig, plots_data)
        
        return fig
    
    def create_velocity_plot(self, plots_data):
        """Create Velocity vs Time plot"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=plots_data['time'],
            y=plots_data['velocity'],
            mode='lines',
            name='Velocity',
            line=dict(color='#3b82f6', width=3),
            fill='tonexty',
            fillcolor='rgba(59, 130, 246, 0.1)',
            hovertemplate='<b>Velocity</b><br>Time: %{x:.2f} s<br>Velocity: %{y:.1f} m/s<extra></extra>'
        ))
        
        fig.update_layout(
            title='Velocity vs Time',
            xaxis_title='Time (s)',
            yaxis_title='Velocity (m/s)',
            hovermode='x unified',
            showlegend=True,
            height=500,
            template='plotly_white'
        )
        
        # Configure fixed linear time axis
        self._configure_time_axis(fig, plots_data)
        
        return fig
    
    def create_altitude_plot(self, plots_data):
        """Create Altitude vs Time plot"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=plots_data['time'],
            y=plots_data['altitude'],
            mode='lines',
            name='Altitude',
            line=dict(color='#10b981', width=3),
            fill='tonexty',
            fillcolor='rgba(16, 185, 129, 0.1)',
            hovertemplate='<b>Altitude</b><br>Time: %{x:.2f} s<br>Altitude: %{y:.1f} m<extra></extra>'
        ))
        
        fig.update_layout(
            title='Altitude vs Time',
            xaxis_title='Time (s)',
            yaxis_title='Altitude (m)',
            hovermode='x unified',
            showlegend=True,
            height=500,
            template='plotly_white'
        )
        
        # Configure fixed linear time axis
        self._configure_time_axis(fig, plots_data)
        
        return fig
    
    def create_trajectory_plot(self, plots_data):
        """Create 2D trajectory plot (altitude vs horizontal distance)"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=plots_data['horizontal_position'],
            y=plots_data['altitude'],
            mode='lines+markers',
            name='Trajectory',
            line=dict(color='#8b5cf6', width=3),
            marker=dict(size=4),
            hovertemplate='<b>Trajectory</b><br>Horizontal: %{x:.1f} m<br>Altitude: %{y:.1f} m<extra></extra>'
        ))
        
        fig.update_layout(
            title='Flight Trajectory',
            xaxis_title='Horizontal Distance (m)',
            yaxis_title='Altitude (m)',
            hovermode='closest',
            showlegend=True,
            height=500,
            template='plotly_white'
        )
        
        return fig
    
    def create_combined_plot(self, plots_data):
        """Create combined plot with multiple subplots"""
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=('Drag Force vs Time', 'Velocity vs Time', 'Altitude vs Time'),
            vertical_spacing=0.08
        )
        
        # Force plot
        fig.add_trace(go.Scatter(
            x=plots_data['time'],
            y=plots_data['total_drag_force'],
            mode='lines',
            name='Total Drag Force',
            line=dict(color='#1f2937', width=2)
        ), row=1, col=1)
        
        # Velocity plot
        fig.add_trace(go.Scatter(
            x=plots_data['time'],
            y=plots_data['velocity'],
            mode='lines',
            name='Velocity',
            line=dict(color='#3b82f6', width=2)
        ), row=2, col=1)
        
        # Altitude plot
        fig.add_trace(go.Scatter(
            x=plots_data['time'],
            y=plots_data['altitude'],
            mode='lines',
            name='Altitude',
            line=dict(color='#10b981', width=2)
        ), row=3, col=1)
        
        fig.update_xaxes(title_text="Time (s)", row=3, col=1)
        fig.update_yaxes(title_text="Force (N)", row=1, col=1)
        fig.update_yaxes(title_text="Velocity (m/s)", row=2, col=1)
        fig.update_yaxes(title_text="Altitude (m)", row=3, col=1)
        
        # Configure fixed linear time axis for all subplots
        if len(plots_data['time']) > 0:
            max_time = np.max(plots_data['time'])
            dtick = self._get_time_tick_spacing(max_time)
            
            fig.update_xaxes(
                tickmode='linear',
                tick0=0,
                dtick=dtick
            )
        
        fig.update_layout(
            height=1000,
            showlegend=False,
            template='plotly_white'
        )
        
        return fig