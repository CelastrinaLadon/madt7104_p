# 🎉 Joinzy - จอยซี่!

**Joinzy** is a Streamlit web app that allows users to create, search, and join parties for shared activities like board games, events, or hangouts — complete with user login, party listings, and chat assistant support.

---

## 🚀 Features

- 🔐 User authentication (register, login, logout with cookies)
- 📝 Create and manage your own parties
- 🔍 Search and filter parties by activity, location, and name
- 🎉 View party details and join or leave parties
- 🤖 Chat assistant powered by Gemini to help users search or create parties
- 📍 Location + activity pricing model support (via `location_activities`)

---

## 🏗️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: SQLAlchemy (with PostgreSQL)
- **Database Models**: UUID primary keys for Users, Parties, Activities, Locations
- **Session State**: Streamlit + CookieManager
- **AI Assistant**: Google Vertex AI Gemini (optional)

---

## 🧱 Project Structure

.
├── models/
│   ├── db.py                # SQLAlchemy engine and Base
│   ├── auth.py              # User model
│   ├── party.py             # Party & PartyPlayer models
│   ├── activities.py        # Activity model
│   └── location.py          # Location and LocationActivities
│
├── views/
│   ├── auth.py              # Login logic
│   ├── register.py          # Registration form
│   ├── create_party.py      # Create party form
│   ├── search_party.py      # Search + Party detail
│   ├── my_parties.py        # User's parties view
│   └── joinzy_assistant.py  # Chat assistant UI
│
├── utils/
│   └── session.py           # Session helpers
│
├── requirements.txt
└── README.md

---

## 💾 How to Run Locally

1. **Clone this repo:**
   ```bash
   git clone https://github.com/yourusername/joinzy.git
   cd joinzy
   ```

2. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up `.streamlit/secrets.toml` with your PostgreSQL URL:**
   ```toml
   [database]
   url = "postgresql://user:password@host:port/dbname"
   ```

4. **Run the app:**
   ```bash
   streamlit run app.py
   ```

> ℹ️ If you're deploying to Streamlit Cloud, make sure to:
> - Replace `psycopg2` with `psycopg2-binary` in `requirements.txt`
> - Set your secrets in the Streamlit Cloud dashboard

---

## 📌 Notes

- Query parameters are accessed via `st.query_params` (Streamlit 1.31+)
- All IDs are UUIDs (as `String`) to avoid integer/char FK mismatches
- Host automatically joins their own party when it's created

---

## 🧠 Future Ideas

- 🎯 Invite links for private parties
- 📅 Calendar view for upcoming parties
- 📲 Mobile-first layout

