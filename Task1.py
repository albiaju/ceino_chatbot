import os
import string
import requests
from dotenv import load_dotenv
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain_openai import ChatOpenAI

load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

chat = ChatOpenAI(
    temperature=0,
    model="gpt-4o",
    api_key=OPENAI_API_KEY
)


memory = ConversationEntityMemory(llm=chat, k=10)

conversation = ConversationChain(
    llm=chat,
    prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
    memory=memory,
    verbose=False
)



def is_weather_query(question: str) -> bool:
    keywords = ["weather", "temperature", "forecast", "rain", "snow", "humidity"]
    return any(word in question.lower() for word in keywords)

def get_weather_response(question: str) -> str:
    tokens = question.lower().split()
    prepositions = ["in", "at", "for","of","on"]
    city = None

    for prep in prepositions:
        if prep in tokens:
            idx = tokens.index(prep)
            if idx + 1 < len(tokens):
                city = tokens[idx + 1].strip(string.punctuation)
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

def generate_chatgpt_response(question: str) -> str:
    try:
        if is_weather_query(question):
            return get_weather_response(question)
        else:
            return conversation.run(question).strip()
    except Exception as e:
        return f"Error generating response: {e}"


if __name__ == "__main__":
    print("Chat with the bot! (Type 'exit' to quit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        answer = generate_chatgpt_response(user_input)
        print("Bot:", answer)