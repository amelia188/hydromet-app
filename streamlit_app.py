import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc
import math


# App config
st.set_page_config(layout="wide")

# Title
st.title("Hydromet Concepts Explorer")

# Main tabs
tab_infilt, tab_runoff, tab_hydro, tab_evap = st.tabs([
    "🧽 Infiltration", 
    "🌧️ Rainfall-Runoff", 
    "📈 Unit Hydrograph", 
    "☀️ Evapotranspiration"
])


# 1. INFILTRATION TAB
with tab_infilt:
    st.header("Infiltration Models")
    # App description
    st.markdown("""
    Explore different infiltration equations used in hydrometeorology. 
    Adjust parameters interactively to see how they affect infiltration rates.""")
            
    st.subheader("About Infiltration Equations")

    st.markdown("""
    Infiltration equations model how water enters the soil surface. 
    Different models are appropriate for different conditions:

    - **Green-Ampt**: Good for uniform soils with sharp wetting front
    - **Philip's**: Solution to Richards' equation for short times
    - **Horton's**: Empirical, good for initially dry soils
    - **SCS Curve Number**: Empirical method for watershed-scale estimates
                
    Future Expansion Ideas:
    - Richards' equation solver
    - More complex soil layering models
    - Comparison between different equations
    - Real-world case studies
    """)

    equation = st.selectbox(
        "Select Infiltration Equation",
        ["Green-Ampt", "Philip", "Horton", "SCS Curve Number"],
        key="infil_eq"
    )
    

# Main content area
if equation == "Green-Ampt":
    st.header("Green-Ampt Infiltration Model")
    st.markdown("""
    The Green-Ampt model describes infiltration into soils based on:
    - Soil properties
    - Initial moisture content
    - Surface ponding
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        Ks = st.slider("Saturated Hydraulic Conductivity (Ks) [cm/hr]", 0.1, 10.0, 1.0, 0.1)
        psi = st.slider("Soil Matric Potential at Wetting Front (ψ) [cm]", 5.0, 50.0, 20.0, 1.0)
        theta_i = st.slider("Initial Water Content (θi) [cm³/cm³]", 0.1, 0.5, 0.2, 0.01)
        theta_s = st.slider("Saturated Water Content (θs) [cm³/cm³]", 0.3, 0.6, 0.5, 0.01)
    
    # Calculate delta_theta
    delta_theta = theta_s - theta_i
    
    # Time array
    time = np.linspace(0.1, 24, 100)  # hours
    
    # Green-Ampt calculations
    F = Ks * time  # Initial approximation
    # More accurate calculation would involve solving implicitly
    infiltration_rate = Ks * (1 + (psi * delta_theta) / F)
    cumulative_infiltration = F
    
    # Plotting
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Infiltration rate plot
    ax1.plot(time, infiltration_rate)
    ax1.set_title('Infiltration Rate vs Time')
    ax1.set_xlabel('Time (hr)')
    ax1.set_ylabel('Infiltration Rate (cm/hr)')
    ax1.grid(True)
    
    # Cumulative infiltration plot
    ax2.plot(time, cumulative_infiltration)
    ax2.set_title('Cumulative Infiltration vs Time')
    ax2.set_xlabel('Time (hr)')
    ax2.set_ylabel('Cumulative Infiltration (cm)')
    ax2.grid(True)
    
    st.pyplot(fig)
    
    # Equation display
    st.latex(r'''
    f(t) = K_s \left(1 + \frac{\psi \Delta\theta}{F(t)}\right)
    ''')
    st.latex(r'''
    F(t) = K_s t + \psi \Delta\theta \ln\left(1 + \frac{F(t)}{\psi \Delta\theta}\right)
    ''')
    
    st.markdown("""
    **Where:**
    - \( f(t) \) = infiltration rate at time t [cm/hr]
    - \( F(t) \) = cumulative infiltration at time t [cm]
    - \( K_s \) = saturated hydraulic conductivity [cm/hr]
    - \( \psi \) = soil matric potential at wetting front [cm]
    - \( \Delta\theta = \theta_s - \theta_i \) = water content difference
    - \( \theta_s \) = saturated water content [cm³/cm³]
    - \( \theta_i \) = initial water content [cm³/cm³]
    """)

elif equation == "Philip":
    st.header("Philip's Infiltration Equation")
    st.markdown("""
    Philip's equation is a two-term approximation solution to Richards' equation.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        S = st.slider("Sorptivity (S) [cm/hr⁰.⁵]", 0.1, 5.0, 1.0, 0.1)
        K = st.slider("Hydraulic Conductivity (K) [cm/hr]", 0.1, 10.0, 1.0, 0.1)
    
    # Time array
    time = np.linspace(0.1, 24, 100)  # hours
    
    # Philip's equation calculations
    infiltration_rate = 0.5 * S * time**(-0.5) + K
    cumulative_infiltration = S * np.sqrt(time) + K * time
    
    # Plotting
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Infiltration rate plot
    ax1.plot(time, infiltration_rate)
    ax1.set_title('Infiltration Rate vs Time')
    ax1.set_xlabel('Time (hr)')
    ax1.set_ylabel('Infiltration Rate (cm/hr)')
    ax1.grid(True)
    
    # Cumulative infiltration plot
    ax2.plot(time, cumulative_infiltration)
    ax2.set_title('Cumulative Infiltration vs Time')
    ax2.set_xlabel('Time (hr)')
    ax2.set_ylabel('Cumulative Infiltration (cm)')
    ax2.grid(True)
    
    st.pyplot(fig)
    
    # Equation display
    st.latex(r'''
    f(t) = \frac{1}{2}St^{-1/2} + K
    ''')
    st.latex(r'''
    F(t) = St^{1/2} + Kt
    ''')
    
    st.markdown("""
    **Where:**
    - \( f(t) \) = infiltration rate at time t [cm/hr]
    - \( F(t) \) = cumulative infiltration at time t [cm]
    - \( S \) = sorptivity [cm/hr⁰.⁵]
    - \( K \) = hydraulic conductivity [cm/hr]
    """)

elif equation == "Horton":
    st.header("Horton's Infiltration Equation")
    st.markdown("""
    Horton's equation describes exponential decay of infiltration rate.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        f0 = st.slider("Initial Infiltration Rate (f₀) [cm/hr]", 0.1, 20.0, 10.0, 0.1)
        fc = st.slider("Final Infiltration Rate (fc) [cm/hr]", 0.01, 5.0, 1.0, 0.01)
        k = st.slider("Decay Coefficient (k) [1/hr]", 0.1, 5.0, 1.0, 0.1)
    
    # Time array
    time = np.linspace(0, 24, 100)  # hours
    
    # Horton's equation calculations
    infiltration_rate = fc + (f0 - fc) * np.exp(-k * time)
    # Numerical integration for cumulative infiltration
    cumulative_infiltration = np.zeros_like(time)
    for i in range(1, len(time)):
        dt = time[i] - time[i-1]
        cumulative_infiltration[i] = cumulative_infiltration[i-1] + infiltration_rate[i] * dt
    
    # Plotting
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Infiltration rate plot
    ax1.plot(time, infiltration_rate)
    ax1.set_title('Infiltration Rate vs Time')
    ax1.set_xlabel('Time (hr)')
    ax1.set_ylabel('Infiltration Rate (cm/hr)')
    ax1.grid(True)
    
    # Cumulative infiltration plot
    ax2.plot(time, cumulative_infiltration)
    ax2.set_title('Cumulative Infiltration vs Time')
    ax2.set_xlabel('Time (hr)')
    ax2.set_ylabel('Cumulative Infiltration (cm)')
    ax2.grid(True)
    
    st.pyplot(fig)
    
    # Equation display
    st.latex(r'''
    f(t) = f_c + (f_0 - f_c)e^{-kt}
    ''')
    
    st.markdown("""
    **Where:**
    - \( f(t) \) = infiltration rate at time t [cm/hr]
    - \( f_0 \) = initial infiltration rate [cm/hr]
    - \( f_c \) = final/constant infiltration rate [cm/hr]
    - \( k \) = decay coefficient [1/hr]
    """)

elif equation == "SCS Curve Number":
    st.header("SCS Curve Number Method for Runoff Estimation")
    st.markdown("""
    The SCS Curve Number method estimates runoff from rainfall using a curve number.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        P = st.slider("Rainfall (P) [cm]", 0.1, 20.0, 5.0, 0.1)
        CN = st.slider("Curve Number (CN)", 30, 100, 70, 1)
        Ia_ratio = st.slider("Initial Abstraction Ratio (Ia/S)", 0.05, 0.3, 0.2, 0.01)
    
    # SCS calculations
    S = (25400 / CN) - 254  # mm
    S = S / 10  # convert to cm
    Ia = Ia_ratio * S
    
    # Calculate runoff
    if P > Ia:
        Q = (P - Ia)**2 / (P - Ia + S)
    else:
        Q = 0
    
    # Potential maximum retention after runoff begins
    F = S * (P - Ia) / (P - Ia + S)
    
    # Infiltration = P - Q
    infiltration = P - Q
    
    # Display results
    st.subheader("Results")
    st.write(f"- Potential Maximum Retention (S): {S:.2f} cm")
    st.write(f"- Initial Abstraction (Ia): {Ia:.2f} cm")
    st.write(f"- Cumulative Infiltration: {infiltration:.2f} cm")
    st.write(f"- Runoff (Q): {Q:.2f} cm")
    
    # Equation display
    st.latex(r'''
    Q = \begin{cases}
    \frac{(P - I_a)^2}{P - I_a + S} & \text{if } P > I_a \\
    0 & \text{otherwise}
    \end{cases}
    ''')
    st.latex(r'''
    S = \frac{25400}{CN} - 254 \text{ (mm)} = \frac{2540}{CN} - 25.4 \text{ (cm)}
    ''')
    st.latex(r'''
    I_a \approx 0.2S \text{ (typically)}
    ''')
    
    st.markdown("""
    **Where:**
    - \( Q \) = runoff [cm]
    - \( P \) = rainfall [cm]
    - \( I_a \) = initial abstraction [cm]
    - \( S \) = potential maximum retention after runoff begins [cm]
    - \( CN \) = curve number (0-100)
    """)


'''
# 2. RAINFALL-RUNOFF TAB  
with tab_runoff:
    st.header("Rainfall-Runoff Relationships")
    model = st.selectbox(
        "Select Model:",
        ["SCS Method", "Rational Method", "Time-Area"],
        key="runoff_model"
    )
    
    if model == "SCS Method":
        # SCS implementation
        pass
    # Other models...

# 3. UNIT HYDROGRAPH TAB
with tab_hydro:
    st.header("Unit Hydrograph Theory")
    st.write("Explore linear system response to rainfall")
    
    # Could implement:
    # - Synthetic unit hydrographs
    # - Convolution operations
    # - Time-area diagrams

# 4. EVAPOTRANSPIRATION TAB
with tab_evap:
    st.header("Evapotranspiration Models")
    et_model = st.selectbox(
        "Select ET Model:",
        ["Penman-Monteith", "Hargreaves", "Priestley-Taylor"],
        key="et_model"
    )
    
    if et_model == "Penman-Monteith":
        # PM implementation
        pass
    # Other models...
'''