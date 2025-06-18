

from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import requests
import string

load_dotenv()

from Task1 import generate_chatgpt_response

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str
    user: Union[str, None] = "Anonymous"

def is_weather_query(question: str) -> bool:
    keywords = ["weather", "temperature", "forecast", "rain", "snow", "humidity"]
    return any(word in question.lower() for word in keywords)

def get_weather_response(question: str) -> str:
    tokens = question.lower().split()
    prepositions = ["in", "at", "for"]
    city = None

    for prep in prepositions:
        if prep in tokens:
            idx = tokens.index(prep)
            if idx + 1 < len(tokens):
                raw_city = tokens[idx + 1]
                city = raw_city.translate(str.maketrans('', '', string.punctuation))
                break

    if not city:
        return "Please specify a city for the weather information."

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        res = requests.get(url)
        data = res.json()
        if data.get("cod") != 200:
            return f"Could not get weather data for '{city}'. Please check the city name."

        weather_desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        return f"The weather in {city.title()} is currently {weather_desc} with a temperature of {temp}°C and humidity of {humidity}%."
    except Exception as e:
        return f"Failed to get weather data due to: {e}"

@app.on_event("startup")
async def startup_event():
    print("FastAPI running at http://127.0.0.1:8000")
    print("Swagger: http://127.0.0.1:8000/docs")

@app.get("/")
def read_root():
    return {"message": "Weather + Chatbot API is running."}

@app.get("/chat/{question}")
def get_chat_response(question: str, user: Union[str, None] = None):
    try:
        if is_weather_query(question):
            answer = get_weather_response(question)
        else:
            answer = generate_chatgpt_response(question)
        return {
            "user": user or "Anonymous",
            "question": question,
            "answer": answer
        }
    except Exception as e:
        return {
            "error": str(e),
            "answer": "An error occurred while processing your request."
        }

@app.put("/chat")
def put_chat_response(chat: ChatRequest):
    try:
        if is_weather_query(chat.question):
            answer = get_weather_response(chat.question)
        else:
            answer = generate_chatgpt_response(chat.question)
        return {
            "user": chat.user or "Anonymous",
            "question": chat.question,
            "answer": answer
        }
    except Exception as e:
        return {
            "error": str(e),
            "answer": "An error occurred while processing your request."
        }



