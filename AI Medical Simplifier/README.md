# 🩺 AI Doctor Assistant

An intelligent medical report analysis platform that leverages **OCR**, **Vector Databases**, and **Local LLMs** to help users interpret medical documents with privacy in mind.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-336791?style=for-the-badge&logo=sqlite&logoColor=white)

## 🚀 Overview
The **AI Doctor Assistant** is a Streamlit-based application designed to process complex medical data from ECGs, X-rays, and blood reports. By utilizing **Tesseract OCR** and **pdfplumber**, the app extracts text and uses **ChromaDB** to store medical history for context-aware analysis via a local **Llama 3** model.

### Key Features
* **Multi-Source Extraction:** Processes text from images (PNG, JPG) and PDF documents using OCR and direct text extraction.
* **Local Privacy:** All AI analysis is performed locally via **Ollama**, ensuring sensitive medical data does not leave your machine.
* **Health Signal Status:** An automated logic engine scans for critical keywords (e.g., "ischemic", "abnormal") to provide an immediate visual health status: Positive, Negative, or Inconclusive.
* **Structured AI Diagnosis:** Generates a comprehensive report including disease explanation, observations, diet plans, and motivational support.
* **RAG Integration:** Uses ChromaDB to store and manage extracted report data for retrieval.

---

## 🛠️ Tech Stack
* **Frontend:** Streamlit
* **OCR & PDF Parsing:** Tesseract OCR, Pytesseract, pdfplumber, and pdf2image
* **LLM Framework:** Ollama (Model: `llama3`)
* **Vector Database:** ChromaDB
* **Language:** Python 3.10+

---

## 📋 Prerequisites

1.  **Tesseract OCR:** * Install Tesseract OCR on your system. 
    * The current configuration points to: `C:\Program Files\Tesseract-OCR\tesseract.exe`. Adjust this path in the code if your installation differs.
2.  **Ollama:**
    * Install [Ollama](https://ollama.com).
    * Pull the required model: `ollama pull llama3`.
3.  **Poppler:**
    * Required for `pdf2image` to function correctly.

---

## ⚙️ Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/your-username/ai-doctor-assistant.git](https://github.com/your-username/ai-doctor-assistant.git)
    cd ai-doctor-assistant
    ```

2.  **Install Python Dependencies:**
    ```bash
    pip install streamlit pillow pdfplumber pytesseract requests chromadb pdf2image
    ```

3.  **Configure API Keys:**
    * The project currently uses a specific **ChromaDB Cloud** configuration (API Key and Tenant ID). Update these settings in the code or switch to a local client for private storage.

4.  **Run the App:**
    ```bash
    streamlit run combined_medical_ai.py
    ```

---

## 📖 Usage Guide

### 1. Upload Reports
Upload your ECGs, X-rays, or Blood Reports in the **Upload Reports** tab. The system will automatically extract and store the text in the collection.

### 2. AI Diagnosis
Once analyzed, the **AI Diagnosis** tab provides a structured medical breakdown, including disease details, do’s and don’ts, and a suggested diet plan.

### 3. Health Signal Status
Check the sidebar to see the **Health Signal Status**:
* 🔴 **POSITIVE:** Health abnormality detected; consultation advised.
* 🟢 **NEGATIVE:** No critical issues detected.
* 🟡 **INCONCLUSIVE:** Insufficient or unclear data.

---

## ⚠️ Disclaimer
**This application is for educational purposes only**. The AI-generated insights are not a replacement for professional medical advice, diagnosis, or treatment. Always consult with a licensed healthcare provider for medical concerns.

---

## 🤝 Contributing
Contributions are welcome! If you'd like to improve the OCR accuracy or add new analysis features, please fork the repo and submit a pull request.
