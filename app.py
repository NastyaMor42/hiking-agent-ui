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

# 📚 דאטה אמיתי (אפשר להרחיב בעתיד)
KNOWN_HIKES = [
    {"name": "נחל כזיב", "area": "צפון", "query": "נחל כזיב"},
    {"name": "הר מירון", "area": "צפון", "query": "הר מירון"},
    {"name": "נחל עמוד", "area": "צפון", "query": "נחל עמוד"},
    {"name": "מצדה", "area": "דרום", "query": "מצדה"},
    {"name": "נחל דוד", "area": "דרום", "query": "נחל דוד"},
    {"name": "עין גדי", "area": "דרום", "query": "עין גדי"},
    {"name": "שמורת הבניאס", "area": "צפון", "query": "בניאס"},
    {"name": "הר תבור", "area": "צפון", "query": "הר תבור"},
    {"name": "נחל השופט", "area": "מרכז", "query": "נחל השופט"},
    {"name": "פארק קנדה", "area": "מרכז", "query": "פארק קנדה"},
]

# 🖼️ תמונות
def get_image(query):
    return f"https://source.unsplash.com/600x400/?{query},hiking,israel"

# 🧠 Agent
def run_agent(preferences):
    prompt = f"""
אתה מתכנן טיולים בישראל.

בחר רק מתוך הרשימה:
{[h['name'] for h in KNOWN_HIKES]}

אל תמציא מסלולים.

העדפות:
{preferences}

החזר 2 מסלולים בפורמט JSON בלבד:

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

        for hike in hikes:
            st.markdown('<div class="card">', unsafe_allow_html=True)

            st.subheader(f"🥾 {hike['name']}")

            # 🖼️ תמונה
            st.image(get_image(hike['name']))

            st.write(f"⏱️ משך: {hike['duration']}")
            st.write(f"🥵 קושי: {hike['difficulty']}")
            st.write(f"📝 {hike['description']}")

            # 🗺️ מפה (embed!)
            map_query = hike['name']
            map_url = f"https://www.google.com/maps?q={map_query}&output=embed"

            st.markdown("### 🗺️ מיקום:")
            st.components.v1.iframe(map_url, height=300)

            # 🚗 ניווט
            nav_link = f"https://www.google.com/maps/search/?api=1&query={map_query}"
            st.markdown(f"[🚗 נווט למסלול]({nav_link})")

            st.markdown('</div>', unsafe_allow_html=True)

    except:
        st.error("בעיה בפענוח 😅")
        st.write(result)

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

ענה JSON:
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

def run_agent(preferences):
    plan = plan_hike(preferences)

    if plan["use_known_hikes"]:
        source = [h["name"] for h in KNOWN_HIKES]
    else:
        source = plan["search_query"]

    prompt = f"""
תכנן 2 טיולים לפי:

{preferences}

השתמש במקור:
{source}

ענה JSON כמו קודם
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

if st.button("🔍 מצא מסלולים"):
    result = run_agent(prefs)