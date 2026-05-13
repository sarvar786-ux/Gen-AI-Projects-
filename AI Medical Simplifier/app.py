import streamlit as st
from PIL import Image
import pdfplumber
import pytesseract
import requests
import chromadb
from pdf2image import convert_from_bytes
from chromadb import Client
from chromadb.config import Settings
# ------------------- SET TESSERACT PATH -------------------
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ------------------- SETUP CHROMADB -------------------




client = chromadb.CloudClient(
  api_key='your api_key',
  tenant='your key',
  database='your_database_name'
)
collection = client.get_or_create_collection("your_database_name")


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Doctor Assistant",
    page_icon="🩺",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {background: linear-gradient(135deg, #e0f7fa, #e8f5e9);}
.main {background: linear-gradient(135deg, #ffffff, #f1f8ff); padding:20px; border-radius:12px;}
h1,h2,h3 {color: #0b5394;}
.upload-box {background: linear-gradient(120deg,#e3f2fd,#e8f5e9); padding:20px; border-radius:15px; border:1px solid #cfe2f3;}
.report-box {background: linear-gradient(120deg,#f3e5f5,#e8eaf6); padding:20px; border-radius:15px;}
.chat-box {background: linear-gradient(120deg,#fff3e0,#e0f2f1); padding:20px; border-radius:15px;}
.footer {font-size:12px; color:gray; text-align:center;}
.main {
    background: rgba(255, 255, 255, 0.88);
    padding: 20px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- OLLAMA FUNCTION ----------------
def analyze_with_ollama(text):
    prompt = f"""
You are a medical AI assistant.

Analyze the following medical data and explain clearly:
1. Tell What Exactly the disease is
2. Observations
3. Do's and Don'ts
4. When to consult a doctor
5. Suggested Diet Plan 
6. MOtivate the pateint positively
7. Provide references to credible medical sources
8. Give the nearest doctor consultation centers if possible.
Medical Data:
{text}
"""
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3", "prompt": prompt, "stream": False},
        timeout=300
    )
    return response.json().get("response", "No response from AI")
# ---------------- HEALTH SIGNAL LOGIC ----------------
def get_health_signal(analysis_text):
    text = analysis_text.lower()

    positive_keywords = [
        "ischemic", "abnormal", "disease", "reduced", "irregular",
        "consult a doctor", "critical", "risk"
    ]

    negative_keywords = [
        "normal", "no abnormality", "within normal range",
        "healthy", "stable"
    ]

    if any(word in text for word in positive_keywords):
        return "POSITIVE"
    elif any(word in text for word in negative_keywords):
        return "NEGATIVE"
    else:
        return "INCONCLUSIVE"

# ---------------- SIDEBAR ----------------
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Go to", ["Upload Reports", "AI Diagnosis", "Chat with AI Doctor"])
st.sidebar.markdown("---")

# -------- HEALTH SIGNAL STATUS (LEFT COLUMN) --------
st.sidebar.subheader("🩺 Health Signal Status")

if "analysis" in st.session_state:
    status = get_health_signal(st.session_state["analysis"])

    if status == "POSITIVE":
        st.sidebar.markdown("""
        <div style="background-color:#2b1a1a;
                    padding:12px;
                    border-radius:10px;
                    border-left:6px solid #ff4b4b;">
            <b style="color:#ff4b4b;">🔴 POSITIVE</b><br>
            <span style="color:#ffdada;">
            Health abnormality detected.<br>
            Doctor consultation advised.
            </span>
        </div>
        """, unsafe_allow_html=True)

    elif status == "NEGATIVE":
        st.sidebar.markdown("""
        <div style="background-color:#1a2b1a;
                    padding:12px;
                    border-radius:10px;
                    border-left:6px solid #4bff4b;">
            <b style="color:#4bff4b;">🟢 NEGATIVE</b><br>
            <span style="color:#d9ffd9;">
            No critical issues detected.
            </span>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.sidebar.markdown("""
        <div style="background-color:#2b2a1a;
                    padding:12px;
                    border-radius:10px;
                    border-left:6px solid #ffd84b;">
            <b style="color:#ffd84b;">🟡 INCONCLUSIVE</b><br>
            <span style="color:#fff3c4;">
            Insufficient or unclear data.
            </span>
        </div>
        """, unsafe_allow_html=True)
else:
    st.sidebar.info("Upload & analyze reports to see status")

st.sidebar.markdown("---")
st.sidebar.caption("⚠️ This app is for educational purposes only.")


# ---------------- HEADER ----------------
st.title("🩺 AI Doctor Assistant")
st.caption("Upload medical reports • Get AI insights • Improve health awareness")

# =====================================================
# PAGE 1: UPLOAD REPORTS
# =====================================================
if page == "Upload Reports":
    st.header("📂 Upload Medical Reports")

    extracted_text_all = ""

    with st.container():
        st.markdown('<div class="upload-box">', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            ecg_files = st.file_uploader("Upload ECG(s)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
            xray_files = st.file_uploader("Upload X-ray / Scan(s)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
        with col2:
            report_files = st.file_uploader("Upload PDF Medical Report(s)", type=["pdf"], accept_multiple_files=True)
            blood_files = st.file_uploader("Upload Blood Report(s)", type=["pdf","png","jpg"], accept_multiple_files=True)

        # ---------- PROCESS PDF REPORTS ----------
        if report_files:
            for report in report_files:
                try:
                    with pdfplumber.open(report) as pdf:
                        for page_pdf in pdf.pages:
                            extracted_text_all += page_pdf.extract_text() or ""
                except Exception as e:
                    st.warning(f"pdfplumber failed for {report.name}, using OCR: {e}")
                    try:
                        images = convert_from_bytes(report.read())
                        for img in images:
                            extracted_text_all += "\n" + pytesseract.image_to_string(img)
                    except Exception as e2:
                        st.error(f"OCR failed for {report.name}: {e2}")

        # ---------- PROCESS ECG IMAGES ----------
        if ecg_files:
            for ecg in ecg_files:
                try:
                    image = Image.open(ecg)
                    extracted_text_all += "\n" + pytesseract.image_to_string(image)
                except Exception as e:
                    st.error(f"Error reading ECG {ecg.name}: {e}")

        # ---------- PROCESS X-RAY IMAGES ----------
        if xray_files:
            for xray in xray_files:
                try:
                    image = Image.open(xray)
                    extracted_text_all += "\n" + pytesseract.image_to_string(image)
                except Exception as e:
                    st.error(f"Error reading X-ray {xray.name}: {e}")

        # ---------- PROCESS BLOOD REPORTS ----------
        if blood_files:
            for blood in blood_files:
                try:
                    if blood.type == "application/pdf":
                        try:
                            with pdfplumber.open(blood) as pdf:
                                for page_pdf in pdf.pages:
                                    extracted_text_all += page_pdf.extract_text() or ""
                        except:
                            images = convert_from_bytes(blood.read())
                            for img in images:
                                extracted_text_all += "\n" + pytesseract.image_to_string(img)
                    else:
                        image = Image.open(blood)
                        extracted_text_all += "\n" + pytesseract.image_to_string(image)
                except Exception as e:
                    st.error(f"Error reading Blood Report {blood.name}: {e}")

        # ---------- SHOW AND STORE RESULTS ----------
        if extracted_text_all:
            st.success("All reports processed successfully")
            with st.expander("📄 Extracted Text (Debug)"):
                st.text(extracted_text_all[:4000])

            # Store in ChromaDB
            collection.add(
                documents=[extracted_text_all],
                metadatas=[{"source":"user_uploads"}],
                ids=[str(len(collection.get()["ids"])+1)]
            )

            if st.button("🧠 Analyze Reports"):
                with st.spinner("AI Doctor is analyzing your reports..."):
                    ai_output = analyze_with_ollama(extracted_text_all)
                st.session_state["analysis"] = ai_output
                st.success("Analysis completed! Go to AI Diagnosis tab 👈")

        st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# PAGE 2: AI DIAGNOSIS
# =====================================================
elif page == "AI Diagnosis":
    st.header("🧠 AI Medical Analysis")
    if "analysis" in st.session_state:
        st.markdown('<div class="report-box">', unsafe_allow_html=True)
        st.write(st.session_state["analysis"])
        st.markdown('</div>', unsafe_allow_html=True)
        st.download_button(
            "📥 Download AI Report",
            data=st.session_state["analysis"],
            file_name="ai_medical_report.txt"
        )
    else:
        st.warning("Please upload and analyze reports first.")

# =====================================================
# PAGE 3: CHAT WITH AI
# =====================================================
elif page == "Chat with AI Doctor":
    st.header("💬 Ask Follow-Up Questions")
    with st.container():
        st.markdown('<div class="chat-box">', unsafe_allow_html=True)
        user_question = st.text_input("Ask your health-related question:")
        if st.button("Ask AI Doctor"):
            with st.spinner("AI Doctor is thinking..."):
                response = analyze_with_ollama(user_question)
            st.info("AI Doctor Response")
            st.write(response)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    '<div class="footer">🩺 AI Doctor Assistant • Not a replacement for professional medical advice</div>',
    unsafe_allow_html=True
)
