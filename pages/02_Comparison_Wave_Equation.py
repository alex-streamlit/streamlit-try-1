import streamlit as st
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import numpy as np
import base64
from PIL import Image
from pdf2image import convert_from_path
import os


st.set_page_config(page_title="Lost link! Give me a sec", page_icon="🌊", layout="wide")

st.title("Lost link! GFive me a sec")
