import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# Page settings
st.set_page_config(page_title="Designer App", layout="centered")

# App Title
st.title("🎨 Smart Designer App")
st.write("మీ own Poster / Design ని create చేయండి!")

# User Input
text = st.text_input("మీ Design Text Enter చేయండి:")

bg_color = st.color_picker("Background Color ఎంచుకోండి:", "#000000")
text_color = st.color_picker("Text Color ఎంచుకోండి:", "#FFFFFF")

# Button
if st.button("🎯 Generate Design"):

    # Create Image
    img = Image.new("RGB", (600, 400), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Default font
    try:
        font = ImageFont.truetype("arial.ttf", 30)
    except:
        font = ImageFont.load_default()

    # Center Text
    text_width, text_height = draw.textsize(text, font=font)
    x = (600 - text_width) / 2
    y = (400 - text_height) / 2

    draw.text((x, y), text, fill=text_color, font=font)

    # Show Image
    st.image(img, caption="✅ Your Design is Ready!")

    # Download Option
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")

    st.download_button(
        label="⬇️ Download Your Design",
        data=buffer.getvalue(),
        file_name="my_design.png",
        mime="image/png"
    )

    st.success("✅ Design Successfully Created!")
