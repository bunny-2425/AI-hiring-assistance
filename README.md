# AI-hiring-assistance

# TalentScout - AI Hiring Assistant

## Overview
TalentScout is an AI-powered hiring assistant built with Streamlit and MongoDB. It provides a seamless experience for recruiters and job seekers by streamlining the hiring process through authentication, AI screening, and technical evaluations.

## Features
- **User Authentication:** Secure login and registration system with password hashing.
- **Candidate Data Storage:** Store candidate details including personal information, tech stack, and preferences.
- **AI Screening:** Interactive chatbot for candidate screening and evaluation.
- **RAG-based AI Chatbot:** AI-driven question-answering system using Retrieval-Augmented Generation (RAG) with ChromaDB.
- **Streamlit UI:** Intuitive and responsive interface with custom styling.

## Tech Stack
- **Frontend & Backend:** Streamlit
- **Database:** MongoDB (Atlas)
- **AI & ML:** GroqCloud, ChromaDB
- **Authentication:** bcrypt for password hashing
- **Environment Management:** dotenv for environment variables
- **Image Processing:** PIL for logo handling

## Installation
### Prerequisites
- Python 3.8+
- MongoDB Atlas account
- Streamlit installed

### Steps to Run the Application
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/talent-scout.git
   cd talent-scout
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Create a `.env` file and set the MongoDB URI:
   ```sh
   MONGO_URI=your_mongodb_connection_string
   ```
4. Run the Streamlit app:
   ```sh
   streamlit run app.py
   ```

## Usage
1. **Login/Register:** Users need to authenticate using their credentials.
2. **Fill Candidate Details:** Provide personal information, experience, and desired job role.
3. **Select Tech Stack:** Choose relevant technologies from a predefined list.
4. **AI Screening:** Interact with the AI-powered chatbot for automated screening.
5. **AI Chatbot with RAG:** Ask domain-related queries and get intelligent responses.

## Project Structure
```
📂 talent-scout
├── app.py               # Main Streamlit application
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
├── assets/              # Logos and images
├── README.md            # Project documentation
└── modules/             # Additional backend logic
```

## Future Enhancements
- Integration with job boards for automated resume parsing.
- AI-driven job recommendations based on skills.
- Admin dashboard for recruiters.
- Cloud deployment for accessibility.

## License
This project is licensed under the MIT License.

## Contact
For any queries or contributions, reach out to omunde2016@gmail.com .
