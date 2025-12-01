import streamlit as st
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(page_title="Designer App", layout="centered")

st.title("🎨 Smart Designer App")
st.subheader("Advanced Text to Image Generator")

# -------- USER CONTROLS --------

text = st.text_input("Enter your design text:")

font_size = st.slider("Select Font Size", 20, 100, 40)

align = st.selectbox("Text Alignment", ["Left", "Center", "Right"])

bg_color = st.color_picker("Background Color", "#000000")
text_color = st.color_picker("Text Color", "#FFFFFF")

width = st.slider("Image Width", 400, 1200, 800)
height = st.slider("Image Height", 300, 800, 500)

# -------- GENERATE DESIGN --------

if st.button("🎨 Generate Design"):
    if text.strip() == "":
        st.warning("Please enter some text first!")
    else:
        img = Image.new("RGB", (width, height), color=bg_color)
        draw = ImageDraw.Draw(img)

        font = ImageFont.load_default()

        text_width, text_height = draw.textsize(text, font=font)

        if align == "Left":
            x = 20
        elif align == "Center":
            x = (width - text_width) // 2
        else:  # Right
            x = width - text_width - 20

        y = (height - text_height) // 2

        draw.text((x, y), text, fill=text_color, font=font)

        img.save("design.png")

        st.image(img, caption="✅ Your advanced design is ready!")

        with open("design.png", "rb") as file:
            st.download_button(
                label="⬇️ Download Design",
                data=file,
                file_name="my_advanced_design.png",
                mime="image/png"
            )

        st.success("🎉 Design Generated Successfully!")
