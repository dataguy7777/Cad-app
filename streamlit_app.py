import streamlit as st
import cadquery as cq
from streamlit_stl_viewer import stl_viewer  # Ensure this matches the actual package name

# Function to generate the quadcopter frame
def create_quadcopter_frame(arm_length, arm_width, body_size, motor_mount_diameter):
    # Base body of the quadcopter
    body = cq.Workplane("XY").box(body_size, body_size, 20)

    # Generate arms
    for i in range(4):
        arm = (cq.Workplane("XY")
               .box(arm_length, arm_width, 10)
               .translate((body_size / 2 + arm_length / 2, 0, 5)))

        # Rotate and position each arm
        arm = arm.rotate((0, 0, 0), (0, 0, 1), i * 90)
        body = body.union(arm)

    # Create motor mounts
    for i in range(4):
        mount = (cq.Workplane("XY")
                 .circle(motor_mount_diameter / 2)
                 .extrude(5)
                 .translate((body_size / 2 + arm_length - motor_mount_diameter, 0, 15)))

        mount = mount.rotate((0, 0, 0), (0, 0, 1), i * 90)
        body = body.union(mount)

    return body

def main():
    st.title('Parametric Quadcopter Frame Generator')

    # UI for parameters
    st.sidebar.header("Quadcopter Parameters")
    arm_length = st.sidebar.slider('Arm Length (mm)', 50, 200, 100, step=1)
    arm_width = st.sidebar.slider('Arm Width (mm)', 5, 20, 10, step=1)
    body_size = st.sidebar.slider('Body Size (mm)', 40, 100, 60, step=1)
    motor_mount_diameter = st.sidebar.slider('Motor Mount Diameter (mm)', 5, 20, 10, step=1)

    # Generate model
    frame = create_quadcopter_frame(arm_length, arm_width, body_size, motor_mount_diameter)

    # Export model as STL
    stl_path = "/tmp/quadcopter_frame.stl"
    frame_val = frame.val()  # Get the underlying CadQuery object
    frame_val.exportStl(stl_path)

    # Display the 3D model in the Streamlit app using STL viewer
    st.header("3D Model Preview")
    stl_viewer(stl_path)

    # Provide a download button for the STL file
    with open(stl_path, "rb") as f:
        st.sidebar.download_button(
            label="Download STL",
            data=f,
            file_name="quadcopter_frame.stl",
            mime="application/octet-stream"
        )

if __name__ == "__main__":
        main()