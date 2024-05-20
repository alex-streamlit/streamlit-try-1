import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

st.title('Hello World App')
st.write('Hello, world!')

# Parameters
CDt = 1.27
m = 180
dt = 0.011
CL = 1
Ak = 120
u = 0.062
d1 = 0.45
d2 = 0.15
Wep = 80
rho_a = 1.13
kpsi = 10.1
kB = 0.5

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

# Streamlit App
st.title('Composite Model for Operational Azimuth Angle $\\phi_{\\mathrm{op}}$')

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
