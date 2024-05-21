def displayPDF(file):
  # Convert PDF to a list of image objects
  images = convert_from_path(file, dpi=300)  # Increase dpi for better quality
  for i, image in enumerate(images):
      # Save the image in a temporary file
      image_path = f"temp_page_{i}.png"
      image.save(image_path, 'PNG')
      # Display the image
      st.image(image_path)

st.title("Contact Page")
st.write("This is the contact page.")

# Title of the PDF viewer
st.subheader("PDF Viewer")

# Path to the PDF file
pdf_path = "Thesis_Interim_Report (2).pdf"

# Check if the file exists
if os.path.exists(pdf_path):
    displayPDF(pdf_path)
else:
    st.error(f"File {pdf_path} does not exist.")

# Displaying images
image1 = Image.open("GlobalCoordinates.png")
st.image(image1, caption='Diagram of global spherical coordinate system $(r_G,\\vartheta_G,\\phi_G)$ used by Argatov.', use_column_width=True)

