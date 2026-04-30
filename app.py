import streamlit as st
from openai import OpenAI
import json

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 🎨 RTL
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

# 📚 30+ מסלולים
KNOWN_HIKES = [
    {"name": "נחל כזיב", "area": "צפון", "type": "נחל"},
    {"name": "הר מירון", "area": "צפון", "type": "הר"},
    {"name": "נחל עמוד", "area": "צפון", "type": "נחל"},
    {"name": "בניאס", "area": "צפון", "type": "מים"},
    {"name": "הר תבור", "area": "צפון", "type": "הר"},
    {"name": "נחל שניר", "area": "צפון", "type": "מים"},
    {"name": "מצוקי דרגות", "area": "דרום", "type": "מדבר"},
    {"name": "מצדה", "area": "דרום", "type": "עתיקות"},
    {"name": "עין גדי", "area": "דרום", "type": "מים"},
    {"name": "נחל דוד", "area": "דרום", "type": "מים"},
    {"name": "נחל ערוגות", "area": "דרום", "type": "מים"},
    {"name": "הר סדום", "area": "דרום", "type": "מדבר"},
    {"name": "נחל השופט", "area": "מרכז", "type": "נחל"},
    {"name": "פארק קנדה", "area": "מרכז", "type": "יער"},
    {"name": "יער בן שמן", "area": "מרכז", "type": "יער"},
    {"name": "נחל אלכסנדר", "area": "מרכז", "type": "נחל"},
    {"name": "חוף דור הבונים", "area": "צפון", "type": "ים"},
    {"name": "חוף אכזיב", "area": "צפון", "type": "ים"},
    {"name": "חוף פלמחים", "area": "מרכז", "type": "ים"},
    {"name": "קיסריה", "area": "מרכז", "type": "עתיקות"},
    {"name": "גן לאומי אפולוניה", "area": "מרכז", "type": "עתיקות"},
    {"name": "שמורת החולה", "area": "צפון", "type": "טבע"},
    {"name": "עין אפק", "area": "צפון", "type": "מים"},
    {"name": "הר בנטל", "area": "צפון", "type": "תצפית"},
    {"name": "הר הארבל", "area": "צפון", "type": "תצפית"},
    {"name": "נחל פרת", "area": "מרכז", "type": "מדבר"},
    {"name": "מכתש רמון", "area": "דרום", "type": "מדבר"},
    {"name": "עין עבדת", "area": "דרום", "type": "מים"},
    {"name": "תל עזקה", "area": "מרכז", "type": "תצפית"},
    {"name": "הר הכרמל", "area": "צפון", "type": "יער"},
]

# 🖼️ תמונה
def get_image(query):
    return f"https://source.unsplash.com/600x400/?{query},israel,hiking"

# 🧠 planning
def plan_hike(preferences):
    prompt = f"""
אתה סוכן חכם לתכנון טיולים.

העדפות:
{preferences}

החלט:
- האם להשתמש ברשימה
- או לחפש חופשי

ענה JSON:
{{
  "use_known_hikes": true,
  "search_query": ""
}}
"""
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(response.choices[0].message.content)

# 🧠 agent
def run_agent(preferences):
    plan = plan_hike(preferences)

    if plan["use_known_hikes"]:
        source = [h["name"] for h in KNOWN_HIKES]
    else:
        source = plan["search_query"]

    prompt = f"""
תכנן 2 טיולים בישראל.

מקור:
{source}

העדפות:
{preferences}

ענה JSON:
[
  {{
    "name": "",
    "duration": "",
    "difficulty": "",
    "description": ""
  }}
]
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# 🎛️ UI
region = st.selectbox("📍 אזור", ["צפון", "מרכז", "דרום"])

duration = st.selectbox(
    "⏱️ משך",
    ["1-2 שעות", "2-4 שעות", "4-6 שעות", "6+ שעות"]
)

difficulty = st.selectbox("🥵 רמת קושי", ["קל", "בינוני", "קשה"])
dog = st.checkbox("🐶 מתאים לכלבים")
view = st.selectbox("🌄 סוג נוף", ["הרים", "יער", "ים", "מדבר", "מים"])

if st.button("🔍 מצא מסלולים"):
    prefs = f"""
    אזור: {region}
    משך: {duration}
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
            st.image(get_image(hike['name']))

            st.write(f"⏱️ {hike['duration']}")
            st.write(f"🥵 {hike['difficulty']}")
            st.write(f"📝 {hike['description']}")

            map_url = f"https://www.google.com/maps?q={hike['name']}&output=embed"
            st.components.v1.iframe(map_url, height=300)

            nav_link = f"https://www.google.com/maps/search/?api=1&query={hike['name']}"
            st.markdown(f"[🚗 נווט למסלול]({nav_link})")

            st.markdown('</div>', unsafe_allow_html=True)

    except:
        st.error("בעיה בפענוח 😅")
        st.write(result)