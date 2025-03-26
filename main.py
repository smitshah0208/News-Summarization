import streamlit as st
import requests
import base64
import plotly.express as px
import pandas as pd

def load_custom_css():
    st.markdown("""
    <style>
    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }
    .stApp {
        background-color: #ffffff;
        font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
        color: #333333;
    }
    .stContainer {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }
    h1 {
        color: #1a3152;
        font-weight: 700;
        text-align: center;
        margin-bottom: 20px;
        font-size: 2.5rem;
    }
    h2 {
        color: #2c4766;
        font-weight: 600;
        margin-top: 20px;
        margin-bottom: 15px;
        border-bottom: 2px solid #4285f4;
        padding-bottom: 10px;
    }
    .stTextInput > div > div > input {
        background-color: #ffffff;
        border: 2px solid #4285f4;
        border-radius: 8px;
        padding: 12px;
        font-size: 1rem;
        color: #333333;
    }
    .stButton > button {
        background-color: #4285f4;
        color: #ffffff;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
    }
    .article-item {
        background-color: #f8fafc;
        border-left: 4px solid #4285f4;
        padding: 15px;
        margin-bottom: 15px;
        border-radius: 8px;
        color: #333333;
    }
    .article-item a {
        color: #4285f4;
    }
    .comparison-item {
        background-color: #f8fafc;
        padding: 15px;
        margin-bottom: 15px;
        border-radius: 8px;
        border-left: 4px solid #34c759;
    }
    .sentiment-text {
        background-color: #f8fafc;
        padding: 15px;
        border-radius: 8px;
        color: #333333;
        font-size: 1.1rem;
        line-height: 1.5;
    }
    </style>
    """, unsafe_allow_html=True)

def display_articles(articles):
    st.markdown("## 📰 News Articles")
    if not articles:
        st.warning("No articles found.")
        return
    
    for article in articles:
        topics = article.get('Topics', [])
        topics_str = ', '.join(topics) if topics else 'No topics available'
        st.markdown(f"""
        <div class="article-item">
            <h3>{article.get('Title', 'Untitled')}</h3>
            <p>{article.get('Summary', 'No summary available')}</p>
            <p><strong>Sentiment:</strong> {article.get('Sentiment', 'N/A')}</p>
            <p><strong>Topics:</strong> {topics_str}</p>
        </div>
        """, unsafe_allow_html=True)

def create_sentiment_chart(sentiment_data):
    df = pd.DataFrame.from_dict(sentiment_data, orient='index', columns=['Count'])
    df.index.name = 'Sentiment'
    df.reset_index(inplace=True)
    
    color_map = {
        'positive': '#34c759',
        'neutral': '#fbbc05',
        'negative': '#ea4335'
    }
    
    fig = px.bar(
        df, 
        x='Sentiment', 
        y='Count', 
        title='Sentiment Distribution',
        color='Sentiment',
        color_discrete_map=color_map,
        text=df['Count']
    )
    
    fig.update_traces(
        textposition='auto',
        textfont=dict(size=18, color='#333333')
    )
    
    fig.update_layout(
        title=dict(
            text='Sentiment Distribution',
            x=0.5,  # Center the title
            xanchor='center',
            font=dict(size=20, color='#333333')
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=14, color='#333333'),
        xaxis_title_font=dict(size=16, color='#333333'),
        yaxis_title_font=dict(size=16, color='#333333'),
        xaxis=dict(
            tickfont=dict(size=14, color='#333333')
        ),
        yaxis=dict(
            tickfont=dict(size=14, color='#333333'),
            side='left'  # Primary Y-axis on the left
        ),
        yaxis2=dict(
            tickfont=dict(size=14, color='#333333'),
            overlaying='y',  # Overlay on the same chart
            side='right',  # Secondary Y-axis on the right
            showgrid=False  # Avoid duplicate grid lines
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_audio(audio_path):
    st.markdown("## 🎧 Audio Summary")
    try:
        with open(audio_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        audio_html = f"""
        <div style="background-color: #f8fafc; padding: 15px; border-radius: 12px;">
            <audio controls style="width:100%">
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        </div>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Audio file not found.")

def display_coverage_differences(differences):
    st.markdown("## 🔍 Coverage Differences")
    if not differences:
        st.warning("No coverage differences available.")
        return
    for diff in differences:
        st.markdown(f"""
        <div class="comparison-item">
            <p><strong>Comparison:</strong> {diff.get('Comparison', 'N/A')}</p>
            <p><strong>Impact:</strong> {diff.get('Impact', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)

def display_topic_overlap(topics):
    st.markdown("## 📋 Topic Analysis")
    if not topics:
        st.warning("No topic analysis available.")
        return
        
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Common Topics")
        common_words = topics.get('common_words_across_pairs', [])
        st.write(", ".join(common_words) if common_words else "No common topics")
    
    with col2:
        st.markdown("### Unique Topics by Article")
        for i, article in enumerate([f"unique_words_in_article_{j+1}" for j in range(10)], 1):
            words = topics.get(article, [])
            if words:
                st.write(f"Article {i}: {', '.join(words) if words else 'No unique topics'}")

def main():
    load_custom_css()
    
    st.markdown("<h1>🌐 Company Media Intelligence</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#666666;'>Comprehensive News Coverage Analysis</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        company_name = st.text_input("Enter Company Name", placeholder="e.g., Tesla")
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        generate_report = st.button("Generate Report", type="primary")
    
    if generate_report and company_name:
        try:
            api_url = f"http://127.0.0.1:8000/report/{company_name}"
            with st.spinner('Fetching Report...'):
                response = requests.get(api_url)
                response.raise_for_status()
                report = response.json()
            
            st.markdown(f"## 📊 Media Analysis: {report.get('Company', company_name).capitalize()}")
            
            create_sentiment_chart(report.get('Comparative Sentiment Score', {}))
            
            st.markdown("## 💡 Overall Sentiment")
            st.markdown(
                f'<div class="sentiment-text">{report.get("Final Sentiment Analysis", "No analysis available")}</div>',
                unsafe_allow_html=True
            )
            
            display_articles(report.get('Articles', []))
            display_coverage_differences(report.get('Coverage Differences', []))
            display_topic_overlap(report.get('Topic Overlap', {}))
            
            if report.get('Audio'):
                display_audio(report['Audio'])
            
        except requests.RequestException as e:
            st.error(f"Error fetching report: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()