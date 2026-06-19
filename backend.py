import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
from typing import List, Dict

from auth import hash_password, verify_password, create_access_token, decode_access_token

# ── Setup ──────────────────────────────────────────────────
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = Groq(api_key=GROQ_API_KEY)

app = FastAPI(
    title="AI Chatbot API — Full Stack",
    description="FastAPI backend connected to a Streamlit frontend",
    version="3.0.0"
)

# ── CORS — allows Streamlit (different port) to call this API ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # for learning; restrict in real production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── In-memory "databases" ────────────────────────────────────
fake_users_db: Dict[str, dict] = {}
user_chat_history: Dict[str, List[Dict[str, str]]] = {}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# ── Pydantic Models ───────────────────────────────────────────
class UserRegister(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str


# ── Auth Dependency ───────────────────────────────────────────
def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = decode_access_token(token)
        username = payload.get("sub")
        if username is None or username not in fake_users_db:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# ── Routes ────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "Full Stack AI Chatbot API is running"}


@app.post("/register")
def register(user: UserRegister):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already exists")

    fake_users_db[user.username] = {
        "username": user.username,
        "hashed_password": hash_password(user.password)
    }
    user_chat_history[user.username] = []

    return {"message": f"User '{user.username}' registered successfully"}


@app.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    stored_user = fake_users_db.get(form_data.username)

    if not stored_user or not verify_password(form_data.password, stored_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_access_token(data={"sub": form_data.username})
    return TokenResponse(access_token=token)


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, current_user: str = Depends(get_current_user)):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    history = user_chat_history[current_user]
    history.append({"role": "user", "content": request.message})

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=history[-10:],
            max_tokens=1024,
            temperature=0.7
        )
        reply = response.choices[0].message.content
        history.append({"role": "assistant", "content": reply})
        return ChatResponse(reply=reply)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")


@app.get("/history")
def get_history(current_user: str = Depends(get_current_user)):
    return {"username": current_user, "history": user_chat_history[current_user]}


@app.delete("/history")
def clear_history(current_user: str = Depends(get_current_user)):
    user_chat_history[current_user].clear()
    return {"message": "Chat history cleared successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)