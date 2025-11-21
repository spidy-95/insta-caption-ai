import os
import base64
import streamlit as st
from openai import OpenAI, RateLimitError

# =========================
# OpenAI client
# =========================

api_key = os.environ.get("OPENAI_API_KEY")
if api_key is None:
    st.error("OPENAI_API_KEY environment variable is not set.")
    st.stop()

client = OpenAI(api_key=api_key)


# =========================
# Helper functions
# =========================

def encode_image_to_base64(file):
    """
    Takes a file-like object (Streamlit upload) and returns a base64 string.
    """
    return base64.b64encode(file.read()).decode("utf-8")


# =========================
# Caption generators
# =========================

def generate_captions_text(description: str, style: str):
    """
    Generate captions from a text description only.
    """
    prompt = f"""
    You are an Instagram caption generator.

    Photo description: {description}
    Caption style: {style}

    Requirements:
    - Generate 5 different caption options
    - Short, aesthetic, Instagram-friendly
    - Add emojis that match the vibe
    - Each caption on its own line
    - No numbering (no 1., 2., etc.)
    """

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            max_output_tokens=120,
        )

        text = response.output_text
        captions = [c.strip() for c in text.split("\n") if c.strip()]
        return captions

    except RateLimitError:
        # Friendly message instead of raw traceback
        raise RuntimeError(
            "Too many requests to the OpenAI API. "
            "Please wait 20–30 seconds and try again."
        )
    except Exception as e:
        # Generic fallback
        raise RuntimeError(f"Something went wrong while generating captions: {e}")


def generate_captions_image(file, style: str):
    """
    Generate captions using BOTH the uploaded image and the requested style.
    """
    # Detect mime type (png / jpeg) from uploaded file
    mime_type = file.type or "image/png"

    # Reset pointer and encode as base64
    file.seek(0)
    b64_image = encode_image_to_base64(file)

    prompt = f"""
    You are an Instagram caption generator.

    Look at the uploaded photo and write captions that match the mood, outfit,
    colors, expressions, and setting.

    IMPORTANT RULES:
    - Do NOT guess the person's religion.
    - Do NOT guess ethnicity.
    - Do NOT assume specific culture, festival, or country.
    - Avoid sensitive or personal assumptions.
    - Focus ONLY on aesthetics, vibes, feelings, colors, and general descriptions.

    Caption style: {style}

    Generate 5 short Instagram-ready captions with emojis.
    Each caption should be on its own line without numbering.
    """

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt},
                        {
                            "type": "input_image",
                            "image_url": f"data:{mime_type};base64,{b64_image}",
                        },
                    ],
                }
            ],
            max_output_tokens=120,
        )

        text = response.output_text
        captions = [c.strip() for c in text.split("\n") if c.strip()]
        return captions

    except RateLimitError:
        raise RuntimeError(
            "Too many requests to the OpenAI API. "
            "Please wait 20–30 seconds and try again."
        )
    except Exception as e:
        raise RuntimeError(f"Something went wrong while generating captions: {e}")


# =========================
# Streamlit UI
# =========================

st.set_page_config(page_title="Insta Caption AI", page_icon="✨")

st.title("✨ Insta Caption AI")
st.write("By Vaswati · Generate aesthetic captions from a description or a photo.")

mode = st.radio("Choose mode:", ["Text description", "Upload photo"])

styles = [
    "aesthetic",
    "funny",
    "gym",
    "emotional",
    "travel",
    "soft girl",
    "baddie",
    "minimal",
]

style = st.selectbox("Caption style:", styles)

if mode == "Text description":
    description = st.text_area(
        "Describe your photo:",
        placeholder="Example: sunset at Lake Michigan with coffee in my hand",
    )

    if st.button("Generate captions"):
        if not description.strip():
            st.warning("Please type something to describe your photo.")
        else:
            try:
                with st.spinner("Thinking of cute captions..."):
                    captions = generate_captions_text(description, style)

                st.subheader("✨ Captions")
                for c in captions:
                    st.write("• " + c)
            except RuntimeError as e:
                st.error(str(e))

else:
    uploaded_file = st.file_uploader(
        "Upload a photo (jpg / jpeg / png):", type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded photo", use_container_width=True)

    if st.button("Generate captions from photo"):
        if uploaded_file is None:
            st.warning("Please upload a photo first.")
        else:
            try:
                with st.spinner("Looking at your photo and writing captions..."):
                    captions = generate_captions_image(uploaded_file, style)

                st.subheader("✨ Captions")
                for c in captions:
                    st.write("• " + c)
            except RuntimeError as e:
                st.error(str(e))
