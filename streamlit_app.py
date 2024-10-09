import streamlit as st
from jupyter_cadquery import show
import cadquery as cq

def create_quadcopter_frame(arm_length, arm_width, body_size):
    # Base body of the quadcopter
    body = cq.Workplane("XY").box(body_size, body_size, 20)

    # Generate arms
    for i in range(4):
        arm = (cq.Workplane("XY")
               .box(arm_length, arm_width, 10)
               .translate((body_size/2 + arm_length/2, 0, 5)))

        # Rotate and position each arm
        arm = arm.rotate((0, 0, 0), (0, 0, 1), i*90)
        body = body.union(arm)

    # Create motor mounts
    for i in range(4):
        mount = (cq.Workplane("XY")
                 .circle(10)
                 .extrude(5)
                 .translate((body_size/2 + arm_length - 10, 0, 15)))

        mount = mount.rotate((0, 0, 0), (0, 0, 1), i*90)
        body = body.union(mount)

    return body

def main():
    st.title('Parametric Quadcopter Frame Generator')

    # UI for parameters
    arm_length = st.sidebar.slider('Arm Length', 50, 200, 100)
    arm_width = st.sidebar.slider('Arm Width', 5, 20, 10)
    body_size = st.sidebar.slider('Body Size', 40, 100, 60)

    # Generate model
    frame = create_quadcopter_frame(arm_length, arm_width, body_size)
    frame_display = show(frame, axes=True, grid=True, ortho=True, tools=False)
    
    # Render the 3D model viewer
    st.write(frame_display)

if __name__ == "__main__":
    main()