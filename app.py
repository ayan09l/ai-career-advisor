import streamlit as st
import pandas as pd

# -------------------- Page Config --------------------
st.set_page_config(page_title="💼 AI Career Advisor", page_icon="💡", layout="wide")
st.title("💼 AI Career Advisor")
st.markdown("Discover the best career paths based on your *skills* and *interests*.")

# -------------------- Custom CSS for Styling --------------------
st.markdown("""
    <style>
    /* Page background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Card style */
    .career-card {
        padding: 20px;
        margin: 10px 0;
        border-radius: 15px;
        background-color: rgba(255, 255, 255, 0.9);
        border: 1px solid #ddd;
        box-shadow: 2px 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .career-card:hover {
        transform: translateY(-5px);
        box-shadow: 4px 8px 25px rgba(0,0,0,0.2);
    }

    /* Buttons style */
    div.stButton > button:first-child {
        background-color: #1f77b4;
        color: white;
        font-size: 1rem;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5rem 1rem;
    }
    div.stButton > button:first-child:hover {
        background-color: #105288;
        color: #fff;
    }

    /* Download button style */
    div.stDownloadButton > button:first-child {
        background-color: #ff6600;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5rem 1rem;
    }
    div.stDownloadButton > button:first-child:hover {
        background-color: #cc5200;
        color: #fff;
    }
    </style>
""", unsafe_allow_html=True)

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

        # Weighted scoring
        skill_weight = 2
        for res in results:
            res['Weighted Score'] = res['Skill Match'] * skill_weight + res['Interest Match']

        # Sort by weighted score
        results_weighted = sorted(results, key=lambda x: x['Weighted Score'], reverse=True)
        top_careers_weighted = results_weighted[:3]

        # Missing skills resources
        missing_skills_resources = {
            "Python": "📌 Codecademy Python Course",
            "SQL": "📌 Mode Analytics SQL Tutorial",
            "Machine Learning": "📌 Coursera ML Course",
            "Statistics": "📌 Khan Academy Statistics",
            "Java": "📌 Java Programming on Udemy",
            "Algorithms": "📌 GeeksforGeeks Algorithms",
            "Data Structures": "📌 Coursera Data Structures",
            "SEO": "📌 Moz SEO Guide",
            "Content Creation": "📌 HubSpot Academy Content Marketing",
            "Social Media": "📌 Hootsuite Social Media Training",
            "Excel": "📌 Excel Easy Tutorial",
            "Design": "📌 Canva Design School",
            "Figma": "📌 Figma Official Tutorials",
            "Adobe XD": "📌 Adobe XD Learn & Support",
            "Creativity": "📌 Coursera Creative Problem Solving"
        }

        # -------------------- Responsive Top Career Cards with Progress Bars --------------------
        st.subheader("🌟 Career Suggestions")
        num_cols = min(len(top_careers_weighted), 3)
        cols = st.columns(num_cols)
        for i, career in enumerate(top_careers_weighted):
            col = cols[i % num_cols]
            missing_resources = [missing_skills_resources.get(skill, "") for skill in career['Missing Skills']]
            missing_resources = [res for res in missing_resources if res]
            col.markdown(f"""
                <div class="career-card">
                    <h3 style="color:#1f77b4;">{career['Career']}</h3>
                    ✅ <b>Skill Match:</b> {career['Skill Match']}<br>
                    <progress value="{career['Skill Match']}" max="{len(all_skills)}" style="width: 100%; height: 15px;"></progress><br>
                    🎯 <b>Interest Match:</b> {career['Interest Match']}<br>
                    <progress value="{career['Interest Match']}" max="{len(all_interests)}" style="width: 100%; height: 15px;"></progress><br>
                    🌟 <b>Weighted Score:</b> {career['Weighted Score']}<br>
                    <progress value="{career['Weighted Score']}" max="{len(all_skills)*2 + len(all_interests)}" style="width: 100%; height: 15px;"></progress><br>
                    ❌ <b>Missing Skills:</b> {', '.join(career['Missing Skills']) if career['Missing Skills'] else 'None 🎉'}<br>
                    📚 <b>Recommended Resources:</b><br>
                    {"<br>".join(learning_resources.get(career['Career'], []))}<br>
                    📝 <b>Resources for Missing Skills:</b><br>
                    {"<br>".join(missing_resources) if missing_resources else "None 🎉"}
                </div>
            """, unsafe_allow_html=True)

        # -------------------- Enhanced CSV Download --------------------
        for res in results:
            res['Missing Skills Resources'] = ", ".join([missing_skills_resources.get(skill, "") for skill in res['Missing Skills'] if skill in missing_skills_resources])
        df = pd.DataFrame(results)

        csv = df.to_csv(index=False)
        st.download_button(
            "⬇ Download Enhanced Recommendations",
            data=csv,
            file_name="career_suggestions_enhanced.csv",
            mime="text/csv"
        )

        # -------------------- Suggest Next Skills to Learn --------------------
        st.subheader("💡 Suggest Next Skills to Learn")
        all_missing_skills = set(skill for career in results for skill in career['Missing Skills'])
        if all_missing_skills:
            selected_skills_to_learn = st.multiselect("Select skills you want to focus on learning next:", list(all_missing_skills))
            if selected_skills_to_learn:
                st.markdown("### 📚 Resources for Selected Skills")
                for skill in selected_skills_to_learn:
                    res_link = missing_skills_resources.get(skill, "No resource available")
                    st.markdown(f"- {skill}: {res_link}")
        else:
            st.info("Great! You have all the skills for your top career suggestions 🎉")
