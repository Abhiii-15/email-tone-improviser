import os
import streamlit as st
import pyperclip
from groq import Groq

# ----------------- API Key -----------------
# Replace with your Groq API key
os.environ["GROQ_API_KEY"] = "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"
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# ----------------- Page Config -----------------
st.set_page_config(page_title="Email Tone Improviser", page_icon="📧", layout="centered")

# ----------------- Styling -----------------
st.markdown("""
<style>
    body { background-color: black; color: white; font-family: Arial, sans-serif; }
    .title { text-align:center; font-size:36px; font-weight:bold; color:#d3d3d3; margin-bottom:15px; }
    .watermark { position:fixed; bottom:10px; left:50%; transform:translateX(-50%); color:#a9a9a9; font-size:12px; }
    textarea, input, .stTextInput, .stTextArea { background-color:#222 !important; color:white !important; }
    .stButton>button { background-color:#00bfff; color:black; font-weight:bold; border-radius:10px; }
    .result-box { border:2px solid #cccccc; padding:15px; border-radius:10px; background-color:#111111; white-space:pre-wrap; }
</style>
""", unsafe_allow_html=True)

# ----------------- Title -----------------
st.markdown("<div class='title'>Email Tone Improviser</div>", unsafe_allow_html=True)

# ----------------- User Input -----------------
email_text = st.text_area("✏️ Paste your email here:", height=200)
tone = st.selectbox("🎯 Select the tone you want:", ["Formal", "Friendly", "Persuasive", "Apologetic", "Enthusiastic"])
make_bullets = st.checkbox("• Convert long paragraphs into concise bullet points")

# ----------------- Tone Instructions -----------------
tone_instructions = {
    "Formal": "Use proper and context fitting salutations (e.g., 'Dear [Name]'), professional vocabulary, complete sentences, and polite closing (e.g., 'Best regards').",
    "Friendly": "Use casual but polite wording, approachable tone, contractions allowed, friendly greetings and closing.",
    "Persuasive": "Use convincing, confident, and motivating language, highlight benefits, encourage action politely.",
    "Apologetic": "Express regret sincerely, polite and empathetic wording, clear acknowledgment of the issue.",
    "Enthusiastic": "Use energetic and positive language, express enthusiasm and excitement, friendly greetings, and upbeat closing."
}

# ----------------- Columns for Buttons -----------------
col_run, col_copy, col_dl = st.columns([1, 1, 1])

# Placeholder for output
result_box = st.empty()
state_key = "improved_email_text"
if state_key not in st.session_state:
    st.session_state[state_key] = ""

# ----------------- Improve Email Action -----------------
with col_run:
    if st.button("✨ Improve Email Tone"):
        if not email_text.strip():
            st.warning("⚠️ Please paste an email first.")
        else:
            with st.spinner("Improvising your email tone…"):
                # System prompt with strict tone enforcement
                system_prompt = f"""
You are an expert email editor.
Rewrite the given email strictly according to the selected tone: {tone}.
Instruction: {tone_instructions[tone]}
Do not change the meaning of the email.
"""
                if make_bullets:
                    system_prompt += " Convert long paragraphs into short, scannable bullet points where appropriate."

                try:
                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",  # faster model
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": email_text}
                        ],
                        max_tokens=400,
                        temperature=0.4
                    )

                    improved_email = response.choices[0].message.content.strip()
                    st.session_state[state_key] = improved_email

                    result_box.markdown("#### ✨ Improved Email")
                    result_box.markdown(f"<div class='result-box'>{improved_email}</div>", unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"❌ Error: {e}")

# ----------------- Copy to Clipboard -----------------
with col_copy:
    if st.button("📋 Copy to Clipboard"):
        improved_email = st.session_state.get(state_key, "")
        if not improved_email:
            st.warning("Nothing to copy yet. Generate an improved email first.")
        else:
            pyperclip.copy(improved_email)
            st.success("📋 Improved email copied to clipboard!")

# ----------------- Download as .txt -----------------
with col_dl:
    improved_email = st.session_state.get(state_key, "")
    st.download_button(
        label="📥 Download .txt",
        data=improved_email if improved_email else "",
        file_name="improved_email.txt",
        disabled=(improved_email == ""),
        help="Generate the email first, then download."
    )

# ----------------- Watermark -----------------
st.markdown("<div class='watermark'>Developed by Abhijnan Raj</div>", unsafe_allow_html=True)
