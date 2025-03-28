# AI News Summarizer with Text-to-Speech  

## 📌 Table of Contents  
- [Key Features & Workflow](#key-features--workflow)  
- [Objectives](#objectives)  
- [Tech Stack Used](#tech-stack-used)  
- [Approach & Explorations](#approach--explorations)  
- [Performance Analysis](#performance-analysis)  
- [Setup & Installation](#setup--installation)  
- [Future Enhancements](#future-enhancements)  
- [Need Help?](#need-help)  

---

## 🔥 Key Features & Workflow  

### **1️⃣ News Scraping & Retrieval**  
- Fetch **company-related news articles** from the **New York Times API**.  
- Retrieve up to **10 relevant articles** for processing.  

### **2️⃣ News Summarization**  
- Extract and store **pre-summarized content** directly from the New York Times API.  
- No additional LLM-based summarization is required.  

### **3️⃣ Sentiment Analysis & Insights**  
- Utilize the **Gemini API** for sentiment analysis (**positive, negative, neutral**).  
- Extract **key topics and trends** from summarized articles.  
- Compare sentiment distribution across articles and highlight coverage differences.  

### **4️⃣ Text-to-Speech (TTS) Conversion**  
- Convert the **final sentiment analysis summary** into speech using **gTTS**.  
- Provide an **audio playback** option for better accessibility.  

### **5️⃣ AI-Powered User Interface**  
- Build an interactive and user-friendly **Streamlit** interface to display:  
  - Article summaries  
  - Sentiment analysis results  
  - Key topic insights  
  - Audio summary playback  

### **6️⃣ Backend Development with FastAPI**  
- Implement a **FastAPI backend** to process user requests efficiently.  
- Return structured **JSON responses** for seamless integration.  

---

## 🎯 Objectives  
✅ Automate news retrieval from **trusted sources** (New York Times).  
✅ Provide **instant summarization** without requiring additional ML models.  
✅ Perform **sentiment analysis** to assess news impact.  
✅ Generate **audio summaries** for accessibility.  
✅ Deliver an intuitive **Streamlit-based UI** for better user experience.  

---

## 🛠 Tech Stack Used  

| Component         | Technology Used        |
|------------------|----------------------|
| **Backend**       | FastAPI               |
| **Frontend**      | Streamlit             |
| **Data Retrieval** | New York Times API    |
| **Sentiment Analysis** | Gemini API          |
| **Text-to-Speech** | gTTS                   |
| **Deployment**    | Docker, Hugging Face Spaces |
| **Environment Variables** | python-dotenv    |

---

## 🔍 Approach & Explorations  

1. **Data Retrieval**  
   - Fetch news articles using the **New York Times API** based on a given company name.  

2. **Summarization Strategy**  
   - Directly extract **pre-summarized content** from NY Times instead of using an LLM-based approach.  

3. **Sentiment Analysis**  
   - Use **Gemini API** to determine sentiment polarity (**positive, negative, neutral**).  
   - Compare sentiment trends across different articles.  

4. **Topic Extraction**  
   - Identify key topics from multiple articles.  
   - Compare topic overlap across different news sources.  

5. **Text-to-Speech (TTS) Generation**  
   - Convert the **final sentiment summary** into an **audio format** using gTTS.  

6. **Building a User Interface**  
   - Develop a **clean and interactive UI** using **Streamlit**.  
   - Provide **real-time visualization** of analysis results.  

7. **Backend API Development**  
   - Use **FastAPI** to handle user queries and return structured JSON responses.  

---

## 📊 Performance Analysis  

| Metric               | Result |
|----------------------|--------|
| **Article Fetch Speed** | Fast (<2s per request) |
| **Summarization Accuracy** | High (Uses NYT pre-summarized content) |
| **Sentiment Analysis Speed** | <1s per article |
| **TTS Conversion Speed** | Instant (<1s for short summaries) |
| **User Experience** | Smooth & Interactive |

---

## 🚀 Setup & Installation  

### **Prerequisites**  
- **Docker Desktop** installed  
- **Hugging Face account**  
- **Gemini API key**  

### **1️⃣ Clone the Repository**  
git clone https://github.com/smitshah0208/News-Summarization.git

cd News-Summarization

### **2️⃣ Install Dependencies**
pip install -r requirements.txt

### **3️⃣ Set Up API Keys**
Create a .env file in the root directory.

Add your API keys inside the .env file:

GEMINI_API_KEY=your-gemini-api-key

### **4️⃣ Run the FastAPI Backend**
uvicorn main:app --reload

### **5️⃣ Start the Streamlit Frontend**
streamlit run app.py

🚀 Future Enhancements
🔹 Multi-source News Scraping – Integrate Google News & other APIs for diverse sources.
🔹 More Advanced TTS Models – Use ElevenLabs or Amazon Polly for high-quality speech.
🔹 Personalized Summaries – Allow users to set custom summary lengths.
🔹 Historical Sentiment Trends – Track a company's sentiment over time.
🔹 Translation Support – Provide multi-language support for wider accessibility.

❓ Need Help?
If you face any issues, feel free to open an issue or reach out via:
📧 Email: smitshah0208@gmail.com
