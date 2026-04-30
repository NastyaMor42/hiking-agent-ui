import streamlit as st
from openai import OpenAI
import os

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def run_agent(preferences):
    prompt = f"""
אתה מתכנן טיולים חכם בישראל.

העדפות:
{preferences}

החזר 2 מסלולים.

לכל מסלול:
- שם
- אזור
- משך זמן
- רמת קושי
- למה מתאים
- לינק ניווט בפורמט:
https://www.google.com/maps/search/?api=1&query=NAME

ענה בעברית ובפורמט ברור.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


st.title("🥾 מתכנן טיולים בישראל")

region = st.selectbox("אזור", ["צפון", "מרכז", "דרום"])
duration = st.slider("משך (שעות)", 1, 8, 3)
difficulty = st.selectbox("רמת קושי", ["קל", "בינוני", "קשה"])
dog = st.checkbox("עם כלב 🐶")
view = st.selectbox("סוג נוף", ["הרים", "יער", "ים"])

if st.button("מצא מסלולים"):
    prefs = f"""
אזור: {region}
משך: {duration} שעות
קושי: {difficulty}
עם כלב: {dog}
נוף: {view}
"""

    result = run_agent(prefs)

    st.subheader("תוצאות")
    st.write(result)