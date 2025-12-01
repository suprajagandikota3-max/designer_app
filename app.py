import streamlit as st
import random
from PIL import Image, ImageDraw, ImageFont
import io
import base64
from utils.ai_text_generator import generate_ai_text, get_ai_suggestions

# Page configuration
st.set_page_config(
    page_title="Smart Designer App",
    page_icon="🎨",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4A00E0;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        color: #8E2DE2;
        font-size: 1.5rem;
        margin-top: 2rem;
    }
    .design-card {
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 25px;
        font-weight: bold;
    }
    .ai-suggestion {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        cursor: pointer;
        transition: transform 0.3s;
    }
    .ai-suggestion:hover {
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 class='main-header'>🎨 Smart Designer Pro</h1>", unsafe_allow_html=True)
st.markdown("### AI-Powered Design Generator with Text Enhancement")

# Sidebar for settings
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    
    # API Key input (optional)
    api_key = st.text_input("OpenAI API Key (optional for AI features):", type="password")
    if api_key:
        st.session_state.api_key = api_key
        st.success("API Key saved!")
    
    st.markdown("---")
    st.markdown("### 🎯 Quick Presets")
    
    # Quick design templates
    template = st.selectbox(
        "Choose a template:",
        ["Custom", "Social Media Post", "Business Card", "Flyer", "Website Banner"]
    )
    
    # AI Enhancement Level
    ai_level = st.slider(
        "AI Enhancement Level:",
        min_value=0,
        max_value=5,
        value=2,
        help="0: No AI, 5: Full AI creativity"
    )
    
    st.markdown("---")
    st.markdown("### 📊 Stats")
    if 'design_count' not in st.session_state:
        st.session_state.design_count = 0
    st.metric("Designs Created", st.session_state.design_count)

# Main layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("<h2 class='sub-header'>✍️ Design Configuration</h2>", unsafe_allow_html=True)
    
    # Text input with AI suggestions
    st.markdown("### Text Content")
    
    # AI Text Generation Section
    with st.expander("🤖 AI Text Assistant", expanded=True):
        text_prompt = st.text_area(
            "Describe what text you want:",
            placeholder="E.g., 'A catchy slogan for a coffee shop' or 'Professional tagline for tech startup'"
        )
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("✨ Generate Suggestions", key="gen_suggestions"):
                if text_prompt:
                    with st.spinner("AI is thinking..."):
                        suggestions = get_ai_suggestions(text_prompt, st.session_state.get('api_key', None))
                        st.session_state.suggestions = suggestions
                else:
                    st.warning("Please enter a description first!")
        
        with col_b:
            if st.button("🔄 Random Suggestion", key="random_suggest"):
                sample_suggestions = [
                    "Innovate. Design. Inspire.",
                    "Quality Meets Creativity",
                    "Elevate Your Brand Presence",
                    "Simple Elegance, Lasting Impact",
                    "Where Ideas Become Reality"
                ]
                st.session_state.suggestions = sample_suggestions
    
    # Display AI suggestions
    if 'suggestions' in st.session_state and st.session_state.suggestions:
        st.markdown("### 💡 AI Suggestions")
        for i, suggestion in enumerate(st.session_state.suggestions[:3]):
            if st.button(suggestion, key=f"sug_{i}", help="Click to use this text"):
                st.session_state.selected_text = suggestion
    
    # Text input with auto-suggestion
    design_text = st.text_area(
        "Enter your design text:",
        value=st.session_state.get('selected_text', 'NKJHJHJHJHJH'),
        height=100,
        key="design_text"
    )
    
    # Design controls
    col1a, col1b = st.columns(2)
    
    with col1a:
        font_size = st.slider("Select Font Size:", 20, 120, 48)
        text_alignment = st.selectbox(
            "Text Alignment:",
            ["Left", "Center", "Right"],
            index=0
        )
    
    with col1b:
        background_color = st.color_picker("Choose Background Color:", "#FFFFFF")
        text_color = st.color_picker("Choose Text Color:", "#000000")
    
    # Advanced options
    with st.expander("🎨 Advanced Options"):
        col_adv1, col_adv2 = st.columns(2)
        with col_adv1:
            font_style = st.selectbox(
                "Font Style:",
                ["Arial", "Helvetica", "Times New Roman", "Courier", "Georgia", "Verdana"]
            )
            add_shadow = st.checkbox("Add Text Shadow", value=False)
        
        with col_adv2:
            padding = st.slider("Padding:", 10, 100, 20)
            opacity = st.slider("Text Opacity:", 50, 100, 100)
    
    # Generate button
    generate_btn = st.button("🚀 Generate Design", type="primary", use_container_width=True)

with col2:
    st.markdown("<h2 class='sub-header'>🎨 Design Preview</h2>", unsafe_allow_html=True)
    
    # Preview area
    preview_container = st.container()
    
    with preview_container:
        if generate_btn and design_text:
            # Create image
            width = 600
            height = 400
            
            # Create image with background
            img = Image.new('RGB', (width, height), color=background_color)
            draw = ImageDraw.Draw(img)
            
            try:
                # Try to load font, fallback to default
                try:
                    font = ImageFont.truetype(font_style.lower().replace(" ", "") + ".ttf", font_size)
                except:
                    font = ImageFont.load_default()
                
                # Calculate text position based on alignment
                text_bbox = draw.textbbox((0, 0), design_text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                
                x = padding
                if text_alignment == "Center":
                    x = (width - text_width) / 2
                elif text_alignment == "Right":
                    x = width - text_width - padding
                
                y = (height - text_height) / 2
                
                # Add shadow if enabled
                if add_shadow:
                    shadow_color = tuple(max(0, c-50) for c in ImageColor.getrgb(text_color))
                    draw.text((x+2, y+2), design_text, font=font, fill=shadow_color)
                
                # Draw main text
                draw.text((x, y), design_text, font=font, fill=text_color)
                
                # Convert PIL Image to bytes for Streamlit
                img_bytes = io.BytesIO()
                img.save(img_bytes, format='PNG')
                img_bytes.seek(0)
                
                # Display image
                st.image(img_bytes, caption="Your Generated Design", use_column_width=True)
                
                # Download button
                st.download_button(
                    label="📥 Download Design",
                    data=img_bytes,
                    file_name="smart_design.png",
                    mime="image/png"
                )
                
                # Increment counter
                st.session_state.design_count += 1
                
                # Show AI enhancements if level > 0
                if ai_level > 0:
                    with st.expander("🤖 AI Design Analysis", expanded=True):
                        st.success("AI Enhancement Applied!")
                        ai_feedback = generate_ai_text(
                            f"Analyze this design: Text='{design_text}', Colors: bg={background_color}, text={text_color}, Font Size={font_size}",
                            st.session_state.get('api_key', None)
                        )
                        st.write(ai_feedback)
                
            except Exception as e:
                st.error(f"Error generating design: {str(e)}")
        
        else:
            # Placeholder image
            placeholder = Image.new('RGB', (600, 400), color='#f0f2f6')
            draw = ImageDraw.Draw(placeholder)
            st.image(placeholder, caption="Design preview will appear here", use_column_width=True)
            
            # Instructions
            st.markdown("""
            <div class='design-card'>
            <h3>💡 Quick Tips:</h3>
            <ul>
                <li>Use the AI Assistant to generate creative text</li>
                <li>Try different color combinations</li>
                <li>Adjust font size for better readability</li>
                <li>Use templates for quick designs</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
col_f1, col_f2, col_f3 = st.columns(3)
with col_f2:
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "✨ <b>Smart Designer Pro</b> - Powered by AI & Streamlit<br>"
        "Create stunning designs with intelligent text suggestions"
        "</div>",
        unsafe_allow_html=True
    )

# Session state initialization
if 'suggestions' not in st.session_state:
    st.session_state.suggestions = []
if 'selected_text' not in st.session_state:
    st.session_state.selected_text = ""
