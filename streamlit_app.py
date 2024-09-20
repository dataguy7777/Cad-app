import streamlit as st
import os
import base64

# Import SolidPython modules
from solid import text as solid_text, linear_extrude, cube, translate, scad_render

# Function to generate the 3D model using SolidPython and save as a .scad file
def generate_solidpython_model(input_text, font, size, height, thickness, output_dir="output_solidpython"):
    """
    Generates a 3D model using SolidPython and saves it as a .scad file.

    Args:
        input_text (str): The text to extrude into 3D.
        font (str): The font to use for the text.
        size (float): The size of the text.
        height (float): The extrusion height of the text.
        thickness (float): The thickness of the base.
        output_dir (str): The directory to save the .scad file.

    Returns:
        str: The path to the generated .scad file.
    """
    # Create text object
    txt = linear_extrude(height=height)(
        solid_text(input_text, size=size, font=font)
    )
    # Create base
    base = cube([size * len(input_text) * 0.6, size, thickness])
    # Combine text and base
    model = txt + translate([0, 0, thickness])(base)

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    scad_file = os.path.join(output_dir, "text_model.scad")

    # Render the model to SCAD format and write it to the file
    with open(scad_file, 'w') as f:
        f.write(scad_render(model))

    return scad_file

# Function to generate a download link for the .scad file
def get_download_link(file_path, file_name, mime_type):
    """
    Generates a download link for a given file.

    Args:
        file_path (str): The path to the file.
        file_name (str): The name of the file.
        mime_type (str): The MIME type of the file.

    Returns:
        str: HTML anchor link for downloading the file.
    """
    with open(file_path, "rb") as f:
        bytes_data = f.read()
    b64 = base64.b64encode(bytes_data).decode()
    href = f'<a href="data:{mime_type};base64,{b64}" download="{file_name}">Download {file_name}</a>'
    return href

# Main Streamlit app
def main():
    st.set_page_config(page_title="Text to 3D CAD Generator", layout="wide")
    st.title("📄 Text to 3D CAD File Generator")

    # Sidebar Navigation
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Go to", ["Home", "SolidPython (OpenSCAD)", "Blender (bpy API)", "FreeCAD"])

    if app_mode == "Home":
        st.header("Welcome to the Text to 3D CAD File Generator")
        st.write("""
        This application allows you to input text and generate corresponding 3D CAD files using different 3D modeling libraries. 
        Select a library from the sidebar to get started.

        ### Supported Libraries:
        - **SolidPython (OpenSCAD)**
        - **Blender (`bpy` API)**
        - **FreeCAD**

        **Note**: Integration with Blender and FreeCAD requires additional setup and is beyond the scope of this example.
        """)

    elif app_mode == "SolidPython (OpenSCAD)":
        st.header("SolidPython (OpenSCAD) - Text to 3D Model")
        st.markdown("""
        SolidPython is a Python interface for OpenSCAD, enabling script-based 3D modeling.
        """)

        # Input Form
        with st.form("solidpython_form"):
            input_text = st.text_input("Enter Text", "Hello World")
            font = st.text_input("Font", "Liberation Sans")
            size = st.number_input("Size", min_value=1, max_value=100, value=10)
            height = st.number_input("Height (Extrusion Depth)", min_value=1, max_value=100, value=5)
            thickness = st.number_input("Base Thickness", min_value=1, max_value=100, value=2)
            submit = st.form_submit_button("Generate 3D Model")

        if submit:
            with st.spinner("Generating 3D model..."):
                scad_file = generate_solidpython_model(input_text, font, size, height, thickness)
            st.success("3D model generated successfully!")

            # Provide Download Link
            file_name = os.path.basename(scad_file)
            mime_type = "application/scad"
            download_link = get_download_link(scad_file, file_name, mime_type)
            st.markdown(download_link, unsafe_allow_html=True)

            # Optionally, provide a link to open in OpenSCAD
            st.markdown("""
            **Next Steps:**
            1. Download and install [OpenSCAD](https://www.openscad.org/downloads.html) if you haven't already.
            2. Open the downloaded `.scad` file in OpenSCAD.
            3. Press `F5` to preview and `F6` to render.
            4. Export to other formats like `.stl` if needed.
            """)

    elif app_mode == "Blender (bpy API)":
        st.header("Blender (`bpy` API) - Text to 3D Model")
        st.markdown("""
        Blender is a powerful open-source 3D creation suite. This section would utilize Blender's Python API (`bpy`) to generate 3D models.
        
        **Important Note**: Integrating Blender with Streamlit requires running Blender in the background and executing scripts externally. This is complex and not covered in this example.
        """)

        st.info("""
        **To Implement Blender Integration:**

        1. **Run Blender in Background Mode**:
        
           You can execute Blender scripts in the background using command-line operations. For example:

           ```bash
           blender --background --python generate_blender_model.py -- "Hello World"
           ```

        2. **Create a Separate Blender Script**:
        
           Write a Python script (`generate_blender_model.py`) that uses the `bpy` API to generate the model based on input arguments.

        3. **Integrate with Streamlit**:
        
           Use Python's `subprocess` module within Streamlit to call the Blender script. After generation, provide a download link for the exported file.

        4. **Security and Performance**:
        
           Ensure that running external scripts does not pose security risks. Handle file paths and user inputs carefully.

        **Example Workflow**:
        
        - User inputs text in Streamlit.
        - Streamlit calls Blender in the background with the input text.
        - Blender script generates the 3D model and exports it (e.g., as `.stl`).
        - Streamlit provides a download link for the exported file.
        """)

    elif app_mode == "FreeCAD":
        st.header("FreeCAD - Text to 3D Model")
        st.markdown("""
        FreeCAD is an open-source parametric 3D CAD modeler. This section would use FreeCAD's Python API to generate 3D models.
        
        **Important Note**: Integrating FreeCAD with Streamlit requires running FreeCAD scripts externally or using its API in a way that's not straightforward. This is complex and not covered in this example.
        """)

        st.info("""
        **To Implement FreeCAD Integration:**

        1. **Create a FreeCAD Script**:
        
           Write a Python script (`generate_freecad_model.py`) that uses FreeCAD's API to create the model based on input parameters.

        2. **Run the Script Externally**:
        
           Execute the FreeCAD script from Streamlit using Python's `subprocess` module.

        3. **Export the Model**:
        
           The FreeCAD script should export the generated model to a standard format like `.stl` or `.step`.

        4. **Provide Download Link**:
        
           After generation, Streamlit can offer the exported file for download.

        5. **Handle Dependencies**:
        
           Ensure that FreeCAD is installed on the server where Streamlit is running, and that the Python environment can access FreeCAD's modules.

        **Example Workflow**:
        
        - User inputs text in Streamlit.
        - Streamlit calls the FreeCAD script with the input text.
        - FreeCAD script generates the 3D model and exports it.
        - Streamlit provides a download link for the exported file.
        """)

if __name__ == "__main__":
    main()