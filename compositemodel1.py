import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.header('Composite Model for $\\phi_{\\mathrm{op}}$')
st.subheader('Interactive Plot')

# Sidebar for parameter inputs
st.sidebar.header('System Parameters')

st.markdown(r'Adjust system parameters on the left sidebar. May take a second to update.')

# Parameters with Streamlit sliders
CDt = st.sidebar.slider(r'Tether drag coefficient $C_{D\text{,t}}$', 0.5, 2.0, 1.27)
m = st.sidebar.slider(r'Kite mass $m$ (kg)', 100, 300, 180)
dt1 = st.sidebar.slider(r'Tether diameter $d_\text{t}$ (mm)', 5, 20, 11)
CL = st.sidebar.slider(r'Kite lift coefficient $C_L$', 0.5, 1.5, 1.0)
Ak = st.sidebar.slider(r'Kite reference area $A_\text{k}$ (m)', 50, 200, 120)
u = st.sidebar.slider(r'Tether linear density $\mu$ (kg m$^{-1}$)', 0.04, 0.1, 0.062)
rho_a = st.sidebar.slider(r'Air density $\rho_\text{a}$ (kg m$^{-3}$)', 0.8, 1.2, 1.13)

d1 = 0.45
d2 = 0.15
Wep =  80
kpsi = 10.1
kB =0.5

dt=dt1/1000

# Additional constants
theta_elevation = np.deg2rad(45)  # Assuming an elevation angle of 45 degrees

# Define functions based on the equations
def phi_op1(x, L1):
    return np.arcsin(kpsi * (9 * m / (2 * rho_a * Ak * CL * x * np.cos(theta_elevation)))) * (180 / np.pi)

def phi_op2():
    return (6 / np.pi) * (180 / np.pi) * np.sqrt((u / (rho_a * Ak * CL)) * ((kB * kpsi * (9 * m * dt * CDt / (16 * u * Ak * CL))) ** 2 + 1))

def L1():
    return (-2 * np.pi / (kB * dt * CDt)) * np.sqrt((Ak * CL * u) / (9 * rho_a)) * np.log((d1 ** 2) * ((kB * kpsi * (9 * m * dt * CDt / (16 * u * Ak * CL))) ** 2 + 1))

def L2():
    return (-2 * np.pi / (kB * dt * CDt)) * np.sqrt((Ak * CL * u) / (9 * rho_a)) * np.log((d2 ** 2) * ((kB * kpsi * (9 * m * dt * CDt / (16 * u * Ak * CL))) ** 2 + 1))

# Calculate L1, L2, and phi_op2
L1_val = L1()
L2_val = L2()
phi_op2_val = phi_op2()

# Create arrays for plotting phi_op1
x_values = np.linspace(L1_val / 2, L1_val, 100)
phi_op1_values = phi_op1(x_values, L1_val)

# Create arrays for the transitional domain
x_trans = np.linspace(L1_val, L2_val, 100)
phi_trans = ((phi_op2_val - phi_op1(L1_val, L1_val)) / (L2_val - L1_val)) * (x_trans - L1_val) + phi_op1(L1_val, L1_val)

# Create arrays for the asymptotic domain
x_asymptotic = np.linspace(L2_val, 6000, 100)

# Plotting function
def plot_graph():
    plt.figure(figsize=(14, 8))

    plt.plot(x_values, phi_op1_values, color='red', linestyle='-', linewidth=2, label='Centripetal domain $\\phi_{\\mathrm{op,1}}$')
    plt.plot(x_asymptotic, [phi_op2_val] * len(x_asymptotic), color='blue', linestyle='-', linewidth=2, label='Asymptotic domain $\\phi_{\\mathrm{op,2}}$')

    plt.plot(x_trans, phi_trans, color='black', linestyle='--', linewidth=2, label='Transitional domain')

    plt.axvline(x=L1_val, color='black', linestyle=(0, (1, 1)), alpha=0.7)
    plt.axvline(x=L2_val, color='black', linestyle=(0, (1, 1)), alpha=0.7)
    plt.text(L1_val + 10, 12, f'$L_1 = {L1_val:.0f} \, \\mathrm{{m}}$', ha='left', va='center', fontsize=12, color='black', alpha=0.7)
    plt.text(L2_val + 10, 12, f'$L_2 = {L2_val:.0f} \, \\mathrm{{m}}$', ha='left', va='center', fontsize=12, color='black', alpha=0.7)

    plt.xlabel('Tether length L (m)', fontsize=14)
    plt.ylabel('Azimuth angle $\\phi$ (°)', fontsize=14)
    plt.title('Composite Model for Operational Azimuth Angle $\\phi_{\\mathrm{op}}$', fontsize=16)
    plt.xlim([0, 5000])
    plt.ylim([0, 14])
    plt.grid(axis='y', which='major', linestyle=':', linewidth=0.5)
    plt.gca().yaxis.set_major_locator(plt.MultipleLocator(1))

    # Adjust the legend
    plt.legend(loc='upper right', fontsize=12)

    st.pyplot(plt)

plot_graph()

st.subheader('Analytical equations used:')


st.markdown(r'Operational azimuth angle in centripetal domain $\phi_\text{op,1}$, where $L < L_1$:')


st.latex(r''' \phi_\text{op,1} = \arcsin{\left(k_{\psi}\frac{9m}{2 \rho_\text{a} A_\text{k} C_L L \cos{\vartheta_\text{op}}}\right)} \cdot \frac{180}{\pi} \text{ (°)} ''')

st.markdown(r'Operational azimuth angle in asymptotic domain $\phi_\text{op,2}$, where $L > L_2$:')

st.latex(r'''  \phi_\text{op,2} =  \frac{6}{\pi}\sqrt{\frac{\mu}{\rho_\text{a} A_\text{k} C_L}\left[\left(k_\beta k_\psi \frac{9 m d_\text{t} C_{D,\text{t}}}{16 \mu A_\text{k} C_L}\right)^2+1\right]}  \cdot \frac{180}{\pi} \text{ (°)} ''')


st.markdown(r'Critical lengths $L_{1,2}$ as a function of $\delta_{1,2}$:')

st.latex(r""" L(\delta) = -\frac{2 \pi}{k_\beta d_\text{t} C_{D,\text{t}}} \sqrt{\frac{ A_\text{k} C_L \mu}{9 \rho_\text{a}}} \ln{\left(\delta^2 \left[ \left( k_\beta k_\psi \frac{ 9 m d_\text{t} C_{D,\text{t}} }{16 \mu A_\text{k} C_L} \right)^2 + 1  \right] \right)} \text{ (m)} """)

st.markdown(r'For $\delta_1 = 0.45$, $\delta_2 = 0.15$.')
st.markdown(r'Where $k_\beta = 0.5$, $k_\psi = 10.1$, and $\vartheta_\text{op} = 45 °$.')



###NEW

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

st.header('Wave Equation')

st.subheader('Interactive animation of wave equation')

st.markdown(r'Interactive animation of solved wave equation for linear daming on a semi-infinite string for the case of light damping. Adjust system parameters on the left sidebar. May be slow: [More responsive interactive animation](https://www.desmos.com/calculator/1qwmfqhaqu?)')

# Sidebar for parameter inputs
st.sidebar.header('System Parameters')

st.markdown("[More responsive interactive animation](https://www.desmos.com/calculator/1qwmfqhaqu?)")



# Set up the sidebar for parameter inputs
st.sidebar.header('System Parameters')

# Define the parameters
beta = st.sidebar.slider(r'Linear damping coefficient $\beta$', 1, 50, 10)
Tt = st.sidebar.slider(r'Time interval $T_t$', 0.5, 2.0, 1.0)
c = st.sidebar.slider(r'Wave propagation velocity $c$', 5, 25, 10)
A = st.sidebar.slider(r'Excitation amplitude $A$', 0.5, 3.0, 1.0)

# Define the functions for f(s, t), f'(s, t), and δ(s)
def f(s, t, beta, Tt, c, A):
    return A * np.exp(-beta * s / (2 * c)) * np.sin((2 * np.pi / Tt) * (t - s / c))

def f_prime(s, t, beta, Tt, c, A):
    return -A * np.exp(-beta * s / (2 * c)) * (1 / c) * np.sqrt((beta / 2)**2 + (2 * np.pi / Tt)**2) * np.sin((2 * np.pi / Tt) * (t - s / c) + np.arctan(4 * np.pi / (beta * Tt)))

def delta(s, beta, Tt, c):
    return np.exp(-beta * s / (2 * c)) * np.sin(np.arctan(4 * np.pi / (beta * Tt)))

# Create the figure and axis
fig, ax = plt.subplots()

# Set up the range for s
s_values = np.linspace(0, 10, 500)

# Initialize the lines for f(s, t), f'(s, t), and δ(s)
line_f, = ax.plot([], [], 'r-', label=r'$f(s, t)$')
line_f_prime, = ax.plot([], [], 'b-', label=r"$f'(s, t)$")
line_delta, = ax.plot([], [], 'k--', label=r'$\delta(s)$')

# Set up the plot limits and labels
ax.set_xlim(0, 10)
ax.set_ylim(-1.2*A, 1.2*A)
ax.set_xlabel(r'Position along tether abscissa $s$')
ax.set_ylabel(r'Function output: $f(s,t)$, $f\'(s,t)$, $\delta(s)$')
ax.axhline(0, color='black', linewidth=0.5)
ax.legend()

# Initialize the plot
def init():
    line_f.set_data([], [])
    line_f_prime.set_data([], [])
    line_delta.set_data([], [])
    return line_f, line_f_prime, line_delta

# Animation function
def animate(t):
    y_f = f(s_values, t, beta, Tt, c, A)
    y_f_prime = f_prime(s_values, t, beta, Tt, c, A)
    y_delta = delta(s_values, beta, Tt, c)
    
    line_f.set_data(s_values, y_f)
    line_f_prime.set_data(s_values, y_f_prime)
    line_delta.set_data(s_values, y_delta)
    
    return line_f, line_f_prime, line_delta

# Create the animation
frames = np.linspace(0, Tt, 200)
interval = Tt * 1000 / len(frames)  # Correct interval calculation
ani = animation.FuncAnimation(fig, animate, init_func=init, frames=frames, interval=interval, blit=True)

# Save the animation as a GIF in the current directory
ani.save('animation.gif', writer='pillow')

# Display the animation in Streamlit
st.image('animation.gif')

st.subheader('Analytical equations used:')

# Show the static equations as LaTeX

st.markdown(r'Displacement $f(s)$:')
st.latex(r'f(s) = A e^{-\frac{\beta s}{2c}} \sin\left( \frac{2\pi}{T_t} \left( t - \frac{s}{c} \right) \right)')

st.markdown(r'First spacial derivative $f\'(s)$:')
st.latex(r'f\'(s) = -A e^{-\frac{\beta s}{2c}} \cdot \frac{1}{c} \sqrt{\left( \frac{\beta}{2} \right)^2 + \left( \frac{2\pi}{T_t} \right)^2} \sin\left( \frac{2\pi}{T_t} \left( t - \frac{s}{c} \right) + \arctan\left( \frac{4\pi}{\beta T_t} \right) \right)')

st.markdown(r'Critical value $\delta(s)$:')
st.latex(r'\delta(s) = e^{-\frac{\beta s}{2c}} \sin\left( \arctan\left( \frac{4\pi}{\beta T_t} \right) \right)')
