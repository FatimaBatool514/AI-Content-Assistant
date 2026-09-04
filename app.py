import os
import streamlit as st
from groq import Groq

# Page layout configuration
st.set_page_config(page_title="AI Content Assistant", page_icon="✍️", layout="centered")

st.title("✍️ AI Content Assistant")
st.write("Generate tailored posts, captions, and hashtags in seconds.")

# Sidebar for API key configuration
st.sidebar.header("Configuration")
groq_api_key = st.sidebar.text_input(
    "Groq API Key", 
    type="password", 
    value=st.secrets.get("GROQ_API_KEY", ""),
    help="Get a free key from console.groq.com"
)

# Input controls
col1, col2 = st.columns(2)

with col1:
    content_type = st.selectbox("Content Type", ["Social Media Post", "Article / Blog Summary", "Newsletter Section", "Product Announcement"])
    platform = st.selectbox("Platform", ["LinkedIn", "Twitter / X", "Instagram", "Facebook", "Blog / Website"])
    tone = st.selectbox("Tone of Voice", ["Professional", "Casual & Friendly", "Energetic & Bold", "Educational", "Humorous"])

with col2:
    topic = st.text_input("Topic", placeholder="e.g., Launching a new Python course")
    audience = st.text_input("Target Audience", placeholder="e.g., Beginner programmers, Tech founders")

additional_instructions = st.text_area("Extra Details (Optional)", placeholder="e.g., Include a call to action to sign up on our website.")

# Generate content trigger
if st.button("Generate Content", type="primary", use_container_width=True):
    if not groq_api_key:
        st.error("Please enter your Groq API Key in the sidebar or Streamlit Secrets.")
    elif not topic or not audience:
        st.warning("Please fill in both the Topic and Target Audience fields.")
    else:
        try:
            client = Groq(api_key=groq_api_key)
            
            prompt = f"""
            You are an expert content marketer. Create a complete, publish-ready post based on these specs:
            
            - Content Type: {content_type}
            - Target Platform: {platform}
            - Topic: {topic}
            - Target Audience: {audience}
            - Tone: {tone}
            - Additional Notes: {additional_instructions}

            Format the response clearly into these 3 sections:
            1. **Hook & Caption / Main Content**: Structured specifically for {platform}.
            2. **Call to Action (CTA)**: Encouraging high engagement.
            3. **Hashtags**: 5 to 10 relevant, high-performing hashtags.
            """

            with st.spinner("Generating content via Groq..."):
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=1000
                )
                
                result = response.choices[0].message.content
                
            st.subheader("Generated Output")
            st.markdown(result)
            st.code(result, language="markdown") # Quick copy box
            
        except Exception as e:
            st.error(f"An error occurred: {e}")