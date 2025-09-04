import streamlit as st
import pandas as pd

st.set_page_config(page_title="💼 AI Career Advisor", page_icon="💡", layout="wide")
st.title("💼 AI Career Advisor")
st.markdown("Discover the best career paths based on your *skills* and *interests*.")

# -------------------- Sample Career Database --------------------
career_db = [
    {
        "career": "Data Scientist",
        "skills": ["Python", "Machine Learning", "Statistics", "SQL"],
        "interests": ["AI", "Data Analysis"]
    },
    {
        "career": "Digital Marketer",
        "skills": ["SEO", "Content Creation", "Social Media", "Analytics"],
        "interests": ["Marketing", "Social Media"]
    },
    {
        "career": "Software Engineer",
        "skills": ["Python", "Java", "Algorithms", "Data Structures"],
        "interests": ["Programming", "Tech"]
    },
    {
        "career": "Business Analyst",
        "skills": ["Excel", "Data Analysis", "Communication", "SQL"],
        "interests": ["Business", "Analytics"]
    },
    {
        "career": "UI/UX Designer",
        "skills": ["Design", "Figma", "Creativity", "Adobe XD"],
        "interests": ["Design", "Creativity"]
    }
]

# -------------------- Learning Resources --------------------
learning_resources = {
    "Data Scientist": [
        "📌 Kaggle: Python & ML",
        "📌 Coursera: Data Science Specialization",
        "📌 YouTube: StatQuest"
    ],
    "Digital Marketer": [
        "📌 Google Digital Garage",
        "📌 HubSpot Academy",
        "📌 Coursera: Marketing Analytics"
    ],
    "Software Engineer": [
        "📌 LeetCode: Algorithms",
        "📌 CS50 Harvard",
        "📌 GeeksforGeeks"
    ],
    "Business Analyst": [
        "📌 Excel for Data Analysis - Coursera",
        "📌 SQL for Business - Udemy",
        "📌 Google Data Analytics Certificate"
    ],
    "UI/UX Designer": [
        "📌 Figma Tutorials",
        "📌 Coursera: UI/UX Design",
        "📌 Adobe XD Free Guide"
    ]
}

# -------------------- User Input --------------------
st.subheader("🛠 Select Your Skills")
all_skills = list({skill for career in career_db for skill in career["skills"]})
user_skills = st.multiselect("Choose skills you have:", all_skills)

st.subheader("🎯 Select Your Interests")
all_interests = list({interest for career in career_db for interest in career["interests"]})
user_interests = st.multiselect("Choose interests you have:", all_interests)

# -------------------- Career Recommendation --------------------
if st.button("🚀 Get Career Suggestions"):
    if not user_skills and not user_interests:
        st.warning("Please select at least one skill or interest.")
    else:
        results = []
        for career in career_db:
            skill_score = len(set(user_skills) & set(career["skills"]))
            interest_score = len(set(user_interests) & set(career["interests"]))
            total_score = skill_score + interest_score
            results.append({
                "Career": career["career"],
                "Skill Match": skill_score,
                "Interest Match": interest_score,
                "Total Score": total_score,
                "Missing Skills": list(set(career["skills"]) - set(user_skills))
            })

        # Sort by score
        results = sorted(results, key=lambda x: x["Total Score"], reverse=True)
        df = pd.DataFrame(results)

        # -------------------- Show Top 3 Careers as Cards --------------------
        st.subheader("✨ Top Career Suggestions For You")
        top_careers = results[:3]

        for career in top_careers:
            st.markdown(f"""
                <div style="padding:15px; margin:10px 0; border-radius:10px; background-color:#f9f9f9; border:1px solid #ddd;">
                    <h3 style="color:#ff6600;">{career['Career']}</h3>
                    ✅ <b>Skill Match:</b> {career['Skill Match']}<br>
                    🎯 <b>Interest Match:</b> {career['Interest Match']}<br>
                    ⭐ <b>Total Score:</b> {career['Total Score']}<br>
                    ❌ <b>Missing Skills:</b> {', '.join(career['Missing Skills']) if career['Missing Skills'] else 'None 🎉'}<br>
                    📚 <b>Recommended Resources:</b><br>
                    {"<br>".join(learning_resources.get(career['Career'], []))}
                </div>
            """, unsafe_allow_html=True)

        # -------------------- Download Button --------------------
        csv = df.to_csv(index=False)
        st.download_button(
            "⬇ Download All Recommendations",
            data=csv,
            file_name="career_suggestions.csv",
            mime="text/csv"
        )