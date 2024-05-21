import streamlit as st
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import numpy as np
import base64
import os

# Create tabs
tab1, tab2, tab3 = st.tabs(["Home", "About", "Contact"])

# Content for Home Tab
with tab1:
    st.title("Home Page")
    st.write("Welcome to the home page!")

# Content for About Tab
with tab2:
    st.title("About Page")
    st.write("This is the about page.")

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
    Ak = st.sidebar.slider(r'Kite reference area $A_\text{k}$ (m$^{2}$)', 50, 200, 120)
    u1 = st.sidebar.slider(r'Tether linear density $\mu$ (g m$^{-1}$)', 30, 200, 62)
    rho_a = st.sidebar.slider(r'Air density $\rho_\text{a}$ (kg m$^{-3}$)', 0.8, 1.2, 1.13)

    d1 = 0.45
    d2 = 0.15
    Wep =  80
    kpsi = 10.1
    kB = 0.5

    dt=dt1/1000
    u=u1/1000

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
        plt.text(L1_val + 30, 12, f'$L_1 = {L1_val:.0f} \, \\mathrm{{m}}$', ha='left', va='center', fontsize=12, color='black', alpha=0.7)
        plt.text(L2_val + 30, 12, f'$L_2 = {L2_val:.0f} \, \\mathrm{{m}}$', ha='left', va='center', fontsize=12, color='black', alpha=0.7)

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

    st.title("Desmos Graph Embed in Streamlit")

    # Embed the iframe using Streamlit's HTML component
    components.html(f'<iframe src="https://www.desmos.com/calculator/h7aq5hwx0u" width="680" height="500"></iframe>', width=680, height=500)

    st.subheader('Analytical equations used:')

    # Show the static equations as LaTeX
    
    st.markdown(r'Displacement $f(s)$:')
    st.latex(r'f(s) = A e^{-\frac{\beta s}{2c}} \sin\left( \frac{2\pi}{T_t} \left( t - \frac{s}{c} \right) \right)')
    
    st.markdown(r'First spacial derivative $f\'(s)$:')
    st.latex(r'f\'(s) = -A e^{-\frac{\beta s}{2c}} \cdot \frac{1}{c} \sqrt{\left( \frac{\beta}{2} \right)^2 + \left( \frac{2\pi}{T_t} \right)^2} \sin\left( \frac{2\pi}{T_t} \left( t - \frac{s}{c} \right) + \arctan\left( \frac{4\pi}{\beta T_t} \right) \right)')
    
    st.markdown(r'Critical value $\delta(s)$:')
    st.latex(r'\delta(s) = e^{-\frac{\beta s}{2c}} \sin\left( \arctan\left( \frac{4\pi}{\beta T_t} \right) \right)')

    components.html(f'<iframe src="https://www.desmos.com/calculator/worwfdu6lu?embed" width="680" height="400" style="border: 1px solid #ccc" frameborder=0></iframe>', width=680, height=500)

# Content for Contact Tab
with tab3:
    def displayPDF(file):
        # Opening file from file path
        with open(file, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    
        # Embedding PDF in HTML using iframe
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    
        # Displaying File
        st.markdown(pdf_display, unsafe_allow_html=True)

    st.title("Contact Page")
    st.write("This is the contact page.")
    
    # Title of the app
    st.title("PDF Viewer")
    
    # Path to the PDF file
    pdf_path = "Thesis_Interim_Report (2).pdf"
    
    # Check if the file exists
    if os.path.exists(pdf_path):
        displayPDF(pdf_path)
    else:
        st.error(f"File {pdf_path} does not exist.")

    image1 = Image.open("GlobalCoordinates.png")
    st.image(image1, caption='Diagram of global spherical coordinate system $(r_G,\\vartheta_G,\\phi_G)$ used by Argatov.', use_column_width=True)
