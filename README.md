# 🔗 Full Stack AI Chatbot — Frontend + Backend Connected

> My first real full-stack application. A Streamlit frontend  
> talking to a secured FastAPI backend over HTTP, with JWT  
> authentication flowing through the entire system.  
> Day 19 of my 4-month AI Engineering journey.

---

## 🌱 Why I Built This

Days 17–18 gave me a solid backend with authentication.  
But it only lived inside `/docs` — nobody could actually use it like a real application.

Day 19 closed that gap.

Now there's a real frontend UI where users can:
- Register
- Log in
- Store authentication tokens
- Send authenticated chat requests
- Log out securely

This project helped me understand how real frontend and backend systems communicate in production-style applications.

---

## 💭 Thought Process

To make this work like a real-world app, I needed:

- A proper login and registration UI
- JWT token storage after authentication
- Automatic token handling on every request
- Backend protection for authenticated routes
- CORS support for frontend/backend communication
- Session handling and logout functionality

---

## 🛠️ Features

### ✅ Authentication System
- User Registration
- User Login
- JWT Token Authentication
- Password Hashing with bcrypt
- Protected API Routes

### ✅ Frontend Functionality
- Streamlit-based UI
- Session-based login persistence
- Chat interface
- Logout system
- Real-time API communication

### ✅ Backend Functionality
- FastAPI REST API
- JWT verification middleware
- Secure password handling
- Groq LLM integration
- Auth-protected chatbot endpoint

---

## ⚙️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.12 | Core Programming Language |
| FastAPI | Backend REST API |
| Streamlit | Frontend UI |
| Requests | HTTP Communication |
| python-jose | JWT Creation & Verification |
| passlib + bcrypt | Secure Password Hashing |
| Groq API (LLaMA 3.3 70B) | AI Response Generation |
| CORS Middleware | Cross-Origin Communication |

---

## 📂 Project Structure

```bash
day19-fullstack/
│
├── backend.py
├── frontend.py
├── requirements.txt
├── .env
└── README.md
```

---

## 🚀 How to Run Locally

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/PrashikSawant/day19-fullstack.git

cd day19-fullstack
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Create a `.env` File

```env
GROQ_API_KEY=your_groq_api_key_here

SECRET_KEY=your_random_secret_key_here
```

---

### 4️⃣ Run the Backend (Terminal 1)

```bash
uvicorn backend:app --reload
```

Backend runs on:

```bash
http://localhost:8000
```

---

### 5️⃣ Run the Frontend (Terminal 2)

```bash
streamlit run frontend.py
```

Frontend runs on:

```bash
http://localhost:8501
```

---

## 🔌 System Architecture

```text
┌──────────────────┐         ┌───────────────────┐
│                  │         │                   │
│   Streamlit UI   │ ──────► │  FastAPI Backend  │
│ localhost:8501   │ ◄────── │ localhost:8000    │
│                  │         │                   │
└──────────────────┘         └───────────────────┘
         │                             │
         │                             │
         ▼                             ▼
 Stores JWT Token              Verifies JWT Token
 session_state                 Calls Groq API
```

---

## 📚 What I Learned

### 🔹 Frontend + Backend Integration
- How applications communicate over HTTP
- Sending requests using the `requests` library
- Handling JSON responses

### 🔹 Authentication
- JWT token generation and verification
- Protected routes in FastAPI
- Authorization headers
- Secure password hashing

### 🔹 Streamlit State Management
- Using `st.session_state`
- Persisting login sessions
- Managing authentication flow

### 🔹 Web Security Concepts
- Understanding CORS
- Cross-origin communication
- Why browsers block different ports by default

### 🔹 API Design
- Difference between:
  - JSON Requests
  - Form-data Requests
- Login flow vs authenticated chat requests

---

## 🧪 Example Flow

```text
User Registers
      ↓
User Logs In
      ↓
Backend Generates JWT
      ↓
Frontend Stores Token
      ↓
Chat Requests Send Authorization Header
      ↓
Backend Verifies Token
      ↓
AI Response Returned
```

---

## 🗺️ Roadmap

### ✅ Day 19
- Full Stack Frontend + Backend Connection

### 🔜 Day 20
- Rate Limiting
- Usage Tracking

### 🔜 Day 21
- Full Stack Deployment

### 🔜 Day 22
- AI Tool Calling (Calculator Function Calling)

---

## 👨‍💻 About Me

I’m **Prashik Sawant** — an aspiring AI Engineer currently on a  
4-month intensive journey to become job-ready in Generative AI Engineering.

I’m building projects daily to learn:
- Backend Engineering
- AI Integration
- APIs
- Authentication Systems
- Full Stack Development
- LLM Applications

---

## 🔗 Connect With Me

- LinkedIn: [Prashik Sawant](https://www.linkedin.com/in/prashik-sawant-ds/)
- GitHub: [PrashikSawant](https://github.com/PrashikSawant)

---

## ⭐ Project Status

✅ Completed — Day 19

---

## 📜 License

This project is open-source and available under the MIT License.
