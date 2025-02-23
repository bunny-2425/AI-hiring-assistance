import streamlit as st
import bcrypt
import os
import time
from pymongo import MongoClient
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["talent_scout"]
users_collection = db["users"]
candidates_collection = db["candidates"]

# Set Streamlit Page Config
st.set_page_config(page_title="AI Hiring Assistant", page_icon="🤖", layout="centered")

# Custom CSS Styling
st.markdown(
    """
    <style>
        .login-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 90vh;
        }
        .login-box {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        .stButton>button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            font-size: 18px;
            padding: 10px;
            border-radius: 5px;
        }
        .title-with-logo {
            display: flex;
            align-items: center;
        }
        .title-with-logo img {
            width: 24px; /* Adjust the size as needed */
            height: 24px; /* Adjust the size as needed */
            margin-right: 10px;
        }
        .logout-button {
            position: absolute;
            top: 10px;
            right: 10px;
            background-color: #f44336;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------- AUTHENTICATION FUNCTIONS ----------------------
def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode("utf-8"), stored_password)

def navigate(page):
    st.session_state.page = page
    st.rerun()

# Initialize Session State Variables
if "page" not in st.session_state:
    st.session_state.page = "login"
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "current_step" not in st.session_state:
    st.session_state.current_step = 1
if "candidate_data" not in st.session_state:
    st.session_state.candidate_data = {}
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# ---------------------- LOGIN PAGE ----------------------
if st.session_state.page == "login" and not st.session_state.authenticated:
    st.markdown("<div class='login-container'><div class='login-box'>", unsafe_allow_html=True)
    st.title("🔒 Welcome to TalentScout")
    st.subheader("Please login to continue")

    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")

    if st.button("Login"):
        user = users_collection.find_one({"username": username})
        if user and verify_password(user["password"], password):
            st.success("✅ Login successful! Redirecting...")
            st.session_state.authenticated = True
            st.session_state.user_id = user["username"]  # Set user ID
            time.sleep(1)
            navigate("main")
        else:
            st.error("❌ Invalid username or password")

    if st.button("Create Account"):
        navigate("register")

    st.markdown("</div></div>", unsafe_allow_html=True)

# ---------------------- REGISTRATION PAGE ----------------------
elif st.session_state.page == "register":
    st.markdown("<div class='login-container'><div class='login-box'>", unsafe_allow_html=True)
    st.title("📝 Register New User")
    
    new_username = st.text_input("👤 Choose a Username")
    new_password = st.text_input("🔑 Choose a Password", type="password")

    if st.button("Register"):
        if users_collection.find_one({"username": new_username}):
            st.error("❌ Username already exists! Choose a different one.")
        else:
            hashed_pw = hash_password(new_password)
            users_collection.insert_one({"username": new_username, "password": hashed_pw})
            st.success("✅ Registration successful! Please login.")
            time.sleep(1)
            navigate("login")

    if st.button("Back to Login"):
        navigate("login")

    st.markdown("</div></div>", unsafe_allow_html=True)

# ---------------------- MAIN DASHBOARD ----------------------
elif st.session_state.page == "main":
    if not st.session_state.authenticated:
        st.error("❌ Unauthorized Access! Please log in first.")
        time.sleep(1)
        navigate("login")

    # Logout Button
    st.markdown(
        """
        <button class="logout-button" onclick="window.location.href='/logout'">Logout</button>
        """,
        unsafe_allow_html=True
    )

    # Sidebar with Branding and Navigation
    try:
        logo = Image.open("E:/chatbot llma/main logo.png")
        logo = logo.resize((190, 150))
        st.sidebar.image(logo, use_column_width=False)
    except Exception as e:
        st.sidebar.error(f"Error loading logo: {e}")

    st.sidebar.title("🚀 TalentScout - AI Hiring Assistant")
    st.sidebar.markdown("Your intelligent assistant for tech hiring.")

    if st.sidebar.button("Step 1"):
        st.session_state.current_step = 1
    if st.sidebar.button("Step 2"):
        st.session_state.current_step = 2
    if st.sidebar.button("Step 3"):
        st.session_state.current_step = 3

    # Greeting message in rainbow color text
    rainbow_text = """
    <h1 style="background: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet);
                -webkit-background-clip: text;
                color: transparent;">
        Hello, {username}!
    </h1>
    """.format(username=st.session_state.user_id)
    st.markdown(rainbow_text, unsafe_allow_html=True)
    
    # ---------------------- STEP 1: PERSONAL DETAILS ----------------------
    if st.session_state.current_step == 1:
        st.title("🤖 TalentScout - AI Hiring Assistant")
        st.header("📌 Step 1: Enter Your Details")
        
        name = st.text_input("👤 Full Name *")
        email = st.text_input("📧 Email Address")
        phone = st.text_input("📞 Phone Number")
        
        # Manual input for years of experience and slider update
        experience_input = st.text_input("📆 Years of Experience *", value=str(st.session_state.candidate_data.get("experience", 2)))
        try:
            experience = int(experience_input)
        except ValueError:
            experience = 2  # Default value if input is not a valid integer

        experience_slider = st.slider("📆 Years of Experience", 0, 20, experience)
        if experience_slider != experience:
            experience = experience_slider
            experience_input = str(experience_slider)

        position = st.text_input("💼 Desired Position")
        location = st.text_input("🌍 Current Location")

        if st.button("Save & Continue"):
            candidate = {"name": name, "email": email, "phone": phone, "experience": experience, "position": position, "location": location}
            candidates_collection.insert_one(candidate)
            st.session_state.candidate_data.update(candidate)
            st.session_state.current_step = 2
            st.rerun()

    # ---------------------- STEP 2: TECH STACK ----------------------
    elif st.session_state.current_step == 2:
        st.title("🔧 Select Your Tech Stack")

        tech_options = [
        "Python", "Django", "Flask", "React", "Angular", "Vue.js", "JavaScript", "Node.js", "Ruby on Rails", 
        "Java", "Kotlin", "Swift", "C#", "C++", "PHP", "Go", "R", "Scala", "Rust", "Perl", "HTML", "CSS", "SQL", 
        "MongoDB", "PostgreSQL", "MySQL", "SQLite", "Microsoft SQL Server", "Oracle", "TensorFlow", "PyTorch", 
        "Keras", "OpenCV", "Scikit-learn", "Docker", "Kubernetes", "AWS", "Azure", "Google Cloud", "DevOps", 
        "Jenkins", "Git", "GitHub", "GitLab", "Jira", "Apache Kafka", "RabbitMQ", "Redis", "Terraform", "Ansible", 
        "Salesforce", "Tableau", "Power BI", "Selenium", "Jupyter", "Hadoop", "Spark", "BigQuery", "Flutter", 
        "Xamarin", "Unity", "TensorFlow Lite", "FastAPI", "Spring Boot"
    ]

        tech_stack = st.multiselect("🔧 Select Technologies *", tech_options, default=st.session_state.candidate_data.get("tech_stack", []))

        if st.button("Save & Continue"):
            if not tech_stack:
                st.error("Please select at least one technology in your tech stack.")
            else:
                st.session_state.candidate_data["tech_stack"] = tech_stack
                st.session_state.current_step = 3
                st.rerun()

    # ---------------------- STEP 3: AI SCREENING ----------------------
    elif st.session_state.current_step == 3:
        logo_path = "E:/chatbot llma/AI logo.png"
        col1, col2 = st.columns([2, 11])  # Adjust the column ratio if needed
        with col1:
            st.image(logo_path, width=90)  # Adjust width as needed
        with col2:
            st.title("AI Chatbot Screening")

        user_input = st.text_input("💡 Type your response:")
        
        if st.button("Ask AI"):
            with st.spinner("Analyzing..."):
                st.write("This is where the AI response will be displayed.")

    # ---------------------- STEP 4: AI CHATBOT WITH RAG & CHROMADB ----------------------
    elif st.session_state.current_step == 4:
        st.title("🤖 AI Chatbot with RAG & ChromaDB")
        with st.form("document_form"):
            doc_text = st.text_area("Enter Document Text")
            doc_id = st.text_input("Document ID")
            submit_doc = st.form_submit_button("Store Document")
            
            if submit_doc:
                try:
                    store_document_with_embedding(doc_id, doc_text)
                    st.success("✅ Document stored successfully!")
                except Exception as e:
                    st.error(f"Error storing document: {e}")

        query = st.text_input("💬 Ask a question")
        if st.button("Get Answer"):
            st.write("This is where the AI response will be displayed.")

    # Sidebar Display of Collected Data
    st.sidebar.markdown("---")
    st.sidebar.subheader("Candidate Data:")
    st.sidebar.write(st.session_state.candidate_data)

# Security Headers
st.markdown(
    """
    <meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self' data:; script-src 'self'; style-src 'self' 'unsafe-inline'">
    <meta http-equiv="X-Frame-Options" content="DENY">
    """,
    unsafe_allow_html=True
)

# Ensure HTTPS
if not st.session_state.get("https_warning_shown", False):
    if os.environ.get("X-Forwarded-Proto", "http") != "https":
        st.warning("You are not using HTTPS. Please ensure your connection is secure.")
        st.session_state.https_warning_shown = True