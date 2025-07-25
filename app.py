
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

        # 极小柱状图及字体
        fig_bar, ax_bar = plt.subplots(figsize=(1.25, 1))  # 更小尺寸
        sns.barplot(x=counts.index, y=counts.values, ax=ax_bar)
        ax_bar.set_ylabel("Count", fontsize=3)
        ax_bar.set_xlabel("Sentiment", fontsize=3)
        ax_bar.tick_params(axis='x', labelsize=3)
        ax_bar.tick_params(axis='y', labelsize=3)
        st.pyplot(fig_bar)

        st.subheader("Pie Chart")
        fig1, ax1 = plt.subplots(figsize=(0.625, 0.625))  # 极小饼图
        wedges, texts, autotexts = ax1.pie(
            counts, labels=counts.index, autopct="%1.1f%%", startangle=90, textprops={'fontsize': 3})
        ax1.axis("equal")
        st.pyplot(fig1)

        st.subheader("Word Cloud (Positive & Negative)")
        positive_text = " ".join(df[df["Sentiment"]=="Positive"][review_col].dropna())
        negative_text = " ".join(df[df["Sentiment"]=="Negative"][review_col].dropna())

        col1, col2 = st.columns(2)
        with col1:
            st.write("Positive")
            wc1 = WordCloud(width=200, height=150, background_color="white").generate(positive_text)
            st.image(wc1.to_array())
        with col2:
            st.write("Negative")
            wc2 = WordCloud(width=200, height=150, background_color="white").generate(negative_text)
            st.image(wc2.to_array())
    else:
        st.error("❌ Excel must contain columns named 'Review' and 'Rating'")
