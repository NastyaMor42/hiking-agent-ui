import streamlit as st
from openai import OpenAI
import json

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 🎨 RTL FIX אמיתי
st.markdown("""
<style>
html, body, [class*="css"]  {
    direction: rtl;
    text-align: right;
}
.card {
    background-color: #1e1e1e;
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.title("🥾 מתכנן טיולים בישראל")

# 📚 דאטה אמיתי עם אזורים
KNOWN_HIKES = [
    {"name": "נחל כזיב", "area": "צפון"},
    {"name": "הר מירון", "area": "צפון"},
    {"name": "נחל עמוד", "area": "צפון"},
    {"name": "בניאס", "area": "צפון"},
    {"name": "הר תבור", "area": "צפון"},
    {"name": "שמורת החולה", "area": "צפון"},
    {"name": "הר הארבל", "area": "צפון"},

    {"name": "נחל השופט", "area": "מרכז"},
    {"name": "פארק קנדה", "area": "מרכז"},
    {"name": "יער בן שמן", "area": "מרכז"},
    {"name": "נחל אלכסנדר", "area": "מרכז"},
    {"name": "קיסריה", "area": "מרכז"},
    {"name": "אפולוניה", "area": "מרכז"},
    {"name": "חוף פלמחים", "area": "מרכז"},

    {"name": "מצדה", "area": "דרום"},
    {"name": "עין גדי", "area": "דרום"},
    {"name": "נחל דוד", "area": "דרום"},
    {"name": "נחל ערוגות", "area": "דרום"},
    {"name": "מכתש רמון", "area": "דרום"},
    {"name": "עין עבדת", "area": "דרום"},
]

# 🖼️ תמונה יציבה (fallback)
def get_image(name):
    try:
        return f"https://source.unsplash.com/600x400/?{name},israel,nature"
    except:
        return "https://via.placeholder.com/600x400?text=Hiking"

# 🧠 AI רק מתאר (לא בוחר!)
def describe_hike(name):
    prompt = f"""
תאר בקצרה את המסלול: {name}

החזר JSON:
{{
 "duration": "",
 "difficulty": "",
 "description": ""
}}
"""
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(response.choices[0].message.content)

# 🎛️ UI
region = st.selectbox("📍 אזור", ["צפון", "מרכז", "דרום"])

duration = st.selectbox(
    "⏱️ משך",
    ["1-2 שעות", "2-4 שעות", "4-6 שעות", "6+ שעות"]
)

difficulty = st.selectbox("🥵 רמת קושי", ["קל", "בינוני", "קשה"])
dog = st.checkbox("🐶 מתאים לכלבים")

if st.button("🔍 מצא מסלולים"):

    # 🔥 פילטור אמיתי (לא AI)
    filtered = [h for h in KNOWN_HIKES if h["area"] == region]

    if len(filtered) == 0:
        st.error("לא נמצאו מסלולים 😅")
    else:
        selected = filtered[:2]  # פשוט לבינתיים

        for i, hike in enumerate(selected):

            st.markdown('<div class="card">', unsafe_allow_html=True)

            st.subheader(f"🥾 {hike['name']}")

            # 🖼️ תמונה
            st.image(get_image(hike['name']))

            # 🧠 תיאור מה-AI
            try:
                details = describe_hike(hike['name'])

                st.write(f"⏱️ {details['duration']}")
                st.write(f"🥵 {details['difficulty']}")
                st.write(f"📝 {details['description']}")
            except:
                st.write("📝 תיאור לא זמין")

            # 🗺️ מפה
            map_url = f"https://www.google.com/maps?q={hike['name']}&output=embed"
            st.components.v1.iframe(map_url, height=300)

            # 🚗 ניווט
            nav_link = f"https://www.google.com/maps/search/?api=1&query={hike['name']}"
            st.markdown(f"[🚗 נווט למסלול]({nav_link})")

            st.markdown('</div>', unsafe_allow_html=True)