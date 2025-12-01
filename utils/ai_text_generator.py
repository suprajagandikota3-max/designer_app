import openai
import os
from typing import List, Optional
import random

def get_ai_suggestions(prompt: str, api_key: Optional[str] = None) -> List[str]:
    """
    Get AI-generated text suggestions based on user prompt
    """
    suggestions = []
    
    # If no API key, return sample suggestions
    if not api_key:
        return get_fallback_suggestions(prompt)
    
    try:
        client = openai.OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a creative copywriter. Generate 5 short, catchy text suggestions for designs."},
                {"role": "user", "content": f"Generate design text about: {prompt}"}
            ],
            max_tokens=100,
            n=5,
            temperature=0.8
        )
        
        suggestions = [choice.message.content.strip() for choice in response.choices]
    
    except Exception as e:
        print(f"AI Error: {e}")
        suggestions = get_fallback_suggestions(prompt)
    
    return suggestions[:5]

def generate_ai_text(prompt: str, api_key: Optional[str] = None) -> str:
    """
    Generate AI analysis or enhancement text
    """
    if not api_key:
        return "Enable AI features with an API key for personalized design analysis."
    
    try:
        client = openai.OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional graphic designer. Provide brief, helpful feedback."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"AI analysis unavailable. Error: {str(e)}"

def get_fallback_suggestions(prompt: str) -> List[str]:
    """
    Provide fallback suggestions when AI is not available
    """
    # Categorized fallback suggestions
    categories = {
        "business": [
            "Innovate. Inspire. Impact.",
            "Excellence in Every Detail",
            "Your Vision, Our Expertise",
            "Building Better Solutions",
            "Quality That Speaks"
        ],
        "creative": [
            "Where Imagination Meets Reality",
            "Colors of Creativity",
            "Design Without Boundaries",
            "Artistic Expression Redefined",
            "Creative Minds, Beautiful Designs"
        ],
        "motivational": [
            "Dream Big. Achieve More.",
            "Your Journey Starts Here",
            "Empower Your Potential",
            "Success by Design",
            "Be Bold. Be Brilliant."
        ],
        "simple": [
            "Clean & Effective",
            "Simple Elegance",
            "Minimal Design, Maximum Impact",
            "Essence of Simplicity",
            "Pure & Purposeful"
        ]
    }
    
    # Try to match category based on prompt keywords
    prompt_lower = prompt.lower()
    
    if any(word in prompt_lower for word in ["business", "corporate", "professional"]):
        return categories["business"]
    elif any(word in prompt_lower for word in ["creative", "art", "design"]):
        return categories["creative"]
    elif any(word in prompt_lower for word in ["motivate", "inspire", "success"]):
        return categories["motivational"]
    else:
        # Return random mix
        all_suggestions = []
        for cat in categories.values():
            all_suggestions.extend(cat)
        return random.sample(all_suggestions, min(5, len(all_suggestions)))
