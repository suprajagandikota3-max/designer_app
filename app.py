import streamlit as st
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(page_title="Designer App", layout="centered")

st.title("🎨 Smart Designer App")
st.subheader("Advanced Text to Image Generator")

# -------- USER INPUTS --------

text = st.text_input("Enter your design text:")

bg_color = st.color_picker("Choose Background Color", "#000000")
text_color = st.color_picker("Choose Text Color", "#FFFFFF")

align = st.selectbox("Text Alignment", ["Left", "Center", "Right"])

width = st.slider("Image Width", 400, 1200, 800)
height = st.slider("Image Height", 300, 800, 500)

# -------- GENERATE DESIGN --------

if st.button("🎨 Generate Design"):
    if text.strip() == "":
        st.warning("Please enter some text!")
    else:
        # Create image
        img = Image.new("RGB", (width, height), color=bg_color)
        draw = ImageDraw.Draw(img)

        font = ImageFont.load_default()

        # ✅ NEW SAFE METHOD (NO ERROR)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Text alignment logic
        if align == "Left":
            x = 20
        elif align == "Center":
            x = (width - text_width) // 2
        else:  # Right
            x = width - text_width - 20

        y = (height - text_height) // 2

        draw.text((x, y), text, fill=text_color, font=font)

        img.save("design.png")

        st.image(img, caption="✅ Your design is ready!")

        with open("design.png", "rb") as file:
            st.download_button(
                label="⬇️ Download Design",
                data=file,
                file_name="my_design.png",
                mime="image/png"
            )

        st.success("🎉 Design Generated Successfully!")
