import streamlit as st
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import numpy as np
import base64
from PIL import Image
from pdf2image import convert_from_path
import os

st.set_page_config(page_title="Linear Damping Wave Equation 🌊", page_icon="❄🌊")
st.markdown("# Linear Damping Wave Equation 🌊")
st.sidebar.markdown("# Linear Damping Wave Equation 🌊")


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
