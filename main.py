from fastapi import FastAPI, Body
import openai
import os
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS setup (allowing all origins for now)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to your frontend domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set OpenAI key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/describe/")
async def describe_food(data: dict = Body(...)):
    food = data.get("food")

    prompt = (
        f"Give a short JSON response with these fields about '{food}':\n"
        f"- name\n"
        f"- calories per 100g or per piece\n"
        f"- protein (in grams)\n"
        f"- carbs (in grams)\n"
        f"- fat (in grams)\n"
        f"- one-line health benefit.\n"
        f"Respond only with valid JSON."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )
        result = response.choices[0].message["content"].strip()
        return json.loads(result)
    except Exception as e:
        return {"error": "Failed to get AI response", "detail": str(e)}
