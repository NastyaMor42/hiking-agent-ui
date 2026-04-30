import streamlit as st
from openai import OpenAI
import json

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 🎨 RTL + עיצוב
st.markdown("""
<style>
body {
    direction: RTL;
    text-align: right;
}
.card {
    background-color: #f7f7f7;
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.title("🥾 מתכנן טיולים בישראל")

# 📚 דאטה
KNOWN_HIKES = [
    {"name": "נחל כזיב", "area": "צפון"},
    {"name": "הר מירון", "area": "צפון"},
    {"name": "נחל עמוד", "area": "צפון"},
    {"name": "שמורת הבניאס", "area": "צפון"},
    {"name": "הר תבור", "area": "צפון"},
    {"name": "מצדה", "area": "דרום"},
    {"name": "נחל דוד", "area": "דרום"},
    {"name": "עין גדי", "area": "דרום"},
    {"name": "נחל השופט", "area": "מרכז"},
    {"name": "פארק קנדה", "area": "מרכז"},
]

# 🖼️ תמונות
def get_image(query):
    return f"https://source.unsplash.com/600x400/?{query},hiking,israel"

# 🧠 שלב 1 — Planning
def plan_hike(preferences):
    prompt = f"""
אתה סוכן חכם לתכנון טיולים.

העדפות:
{preferences}

שלבים:
1. הבן מה המשתמש רוצה
2. החלט:
   - האם לבחור מתוך רשימה קיימת
   - או לחפש משהו חדש

ענה JSON בלבד:
{{
  "use_known_hikes": true,
  "reason": "",
  "search_query": ""
}}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(response.choices[0].message.content)

# 🧠 שלב 2 — Agent
def run_agent(preferences):
    plan = plan_hike(preferences)

    if plan["use_known_hikes"]:
        source = [h["name"] for h in KNOWN_HIKES]
    else:
        source = plan["search_query"]

    prompt = f"""
אתה מתכנן טיולים בישראל.

השתמש במקור:
{source}

העדפות:
{preferences}

החזר 2 מסלולים בפורמט JSON:

[
  {{
    "name": "",
    "duration": "",
    "difficulty": "",
    "description": ""
  }}
]

ענה רק JSON.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# 🎛️ UI
region = st.selectbox("📍 אזור", ["צפון", "מרכז", "דרום"])
duration = st.slider("⏱️ משך (שעות)", 1, 8, 3)
difficulty = st.selectbox("🥵 רמת קושי", ["קל", "בינוני", "קשה"])
dog = st.checkbox("🐶 מתאים לכלבים")
view = st.selectbox("🌄 סוג נוף", ["הרים", "יער", "מים"])

if st.button("🔍 מצא מסלולים"):
    prefs = f"""
    אזור: {region}
    משך: {duration} שעות
    קושי: {difficulty}
    עם כלב: {dog}
    נוף: {view}
    """

    result = run_agent(prefs)

    try:
        hikes = json.loads(result)

        for i, hike in enumerate(hikes):
            st.markdown('<div class="card">', unsafe_allow_html=True)

            st.subheader(f"🥾 {hike['name']}")

            # 🖼️ תמונה
            st.image(get_image(hike['name']))

            st.write(f"⏱️ משך: {hike['duration']}")
            st.write(f"🥵 קושי: {hike['difficulty']}")
            st.write(f"📝 {hike['description']}")

            # 🗺️ מפה
            map_url = f"https://www.google.com/maps?q={hike['name']}&output=embed"
            st.components.v1.iframe(map_url, height=300)

            # 🚗 ניווט
            nav_link = f"https://www.google.com/maps/search/?api=1&query={hike['name']}"
            st.markdown(f"[🚗 נווט למסלול]({nav_link})")

            st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error("בעיה בפענוח 😅")
        st.write(result)