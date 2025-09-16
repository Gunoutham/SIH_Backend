from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from src.db import get_db_connection
import psycopg2 as pg
from psycopg2.extras import RealDictCursor
from typing import List
from src.ai import get_response, SYSTEM_PROMPT


class Login(BaseModel):
    username: str
    password: str

class Register(BaseModel):
    username: str
    email: str
    password: str

class ChatHistory(BaseModel):
    sender: str
    message_text: str

class AskRequest(BaseModel):
    user_input: str
    chat_history: List[ChatHistory]

app = FastAPI()

@app.post('/')
def login(login_cred: Login):
    conn = None
    try:
       conn = get_db_connection()
       with conn.cursor(cursor_factory=RealDictCursor) as cursor:
          cursor.execute("SELECT username, password FROM users WHERE username=%s",(login_cred.username,))

          user_record = cursor.fetchone()

          if not user_record or login_cred.password!=user_record['password']:
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
             )
          
          return {
             'status': 'success'
          }
    except (Exception, pg.DatabaseError) as e:
        if isinstance(e, HTTPException):
            raise e  
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An internal error occurred: {e}"
        )
    finally:
        if conn:
            conn.close()

@app.post('/register')
def register(reg_det: Register):
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM users WHERE username=%s",(reg_det.username,))

            user = cursor.fetchone()
            if user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Username already exists",
                )
            cursor.execute(f"INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",(reg_det.username,reg_det.email,reg_det.password))
            conn.commit()

            return {
                "status": 'success'
            }
    except pg.IntegrityError:
        if conn:
            conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with that username or email already exists (database constraint).",
        )
        
    except (Exception, pg.DatabaseError) as e:
        if conn:
            conn.rollback()
        if isinstance(e, HTTPException):
            raise e  
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An internal error occurred: {e}"
        )
    finally:
        if conn:
            conn.close()

@app.post('/ask')
def ask(req_data: AskRequest):
    history_tuples = []
    for item in req_data.chat_history:
        history_tuples.append((item.sender, item.message_text))
        
    ai_reply = get_response(
        user_input=req_data.user_input,
        chat_history=history_tuples,
        system_prompt=SYSTEM_PROMPT
    )
    
    return {"reply": ai_reply}