import streamlit as st
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import numpy as np
import base64
from PIL import Image
from pdf2image import convert_from_path
import os


components.html(f'<iframe src="https://www.desmos.com/calculator/worwfdu6lu?embed" width="680" height="400" style="border: 1px solid #ccc" frameborder=0></iframe>', width=680, height=500)

