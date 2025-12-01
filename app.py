import streamlit as st
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(page_title="Designer App", layout="centered")

st.title("🎨 Smart Designer App")
st.subheader("Text to Beautiful Image Generator")

# User input
text = st.text_input("Enter the text for your design:")

bg_color = st.color_picker("Choose Background Color:", "#000000")
text_color = st.color_picker("Choose Text Color:", "#FFFFFF")

if st.button("🎨 Generate Design"):
    if text == "":
        st.error("⚠️ Please enter some text!")
    else:
        # Create Image
        img = Image.new("RGB", (800, 500), color=bg_color)
        draw = ImageDraw.Draw(img)

        # Default font
        font = ImageFont.load_default()

        # Add text to image
        draw.text((100, 220), text, fill=text_color, font=font)

        # Save Image
        img.save("design.png")

        # Show Image in App
        st.image(img, caption="✅ Your design is ready!")

        # Download Button
        with open("design.png", "rb") as file:
            st.download_button(
                label="⬇️ Download Design",
                data=file,
                file_name="my_design.png",
                mime="image/png"
            )

        st.success("🎉 Design Successfully Created!")
