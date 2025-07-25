
import streamlit as st
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

st.set_page_config(layout="wide")
st.title("📊 Excel-Based Sentiment Dashboard")

uploaded_file = st.file_uploader("Upload an Excel file with customer reviews", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # 自动识别列
    review_col = "Review"
    rating_col = "Rating"

    if review_col in df.columns and rating_col in df.columns:
        def classify_sentiment(score):
            if score >= 4:
                return "Positive"
            elif score == 3:
                return "Neutral"
            else:
                return "Negative"

        df["Sentiment"] = df[rating_col].apply(classify_sentiment)

        st.success("✅ Sentiment classification completed!")

        st.subheader("Sentiment Distribution")
        counts = df["Sentiment"].value_counts()
        st.bar_chart(counts)

        st.subheader("Pie Chart")
        fig1, ax1 = plt.subplots(figsize=(2.5, 2.5))  # 更小的图像尺寸
        ax1.pie(counts, labels=counts.index, autopct="%1.1f%%", startangle=90)
        ax1.axis("equal")
        st.pyplot(fig1)

        st.subheader("Word Cloud (Positive & Negative)")
        positive_text = " ".join(df[df["Sentiment"]=="Positive"][review_col].dropna())
        negative_text = " ".join(df[df["Sentiment"]=="Negative"][review_col].dropna())

        col1, col2 = st.columns(2)
        with col1:
            st.write("Positive")
            wc1 = WordCloud(width=400, height=300, background_color="white").generate(positive_text)
            st.image(wc1.to_array())
        with col2:
            st.write("Negative")
            wc2 = WordCloud(width=400, height=300, background_color="white").generate(negative_text)
            st.image(wc2.to_array())
    else:
        st.error("❌ Excel must contain columns named 'Review' and 'Rating'")
