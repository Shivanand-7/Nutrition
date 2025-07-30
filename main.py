from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

app = FastAPI()

TOGETHER_API_KEY = "9b2956bac531938a6c543c3e98eb5bf975f6f64db60536c03ca05db95fbb63b1"
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"  # Good, fast model

class FoodRequest(BaseModel):
    item_name: str

@app.post("/describe/")
def describe_food(request: FoodRequest):
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    Give a short nutrition description for the food item: {request.item_name}.
    Include:
    - Calories per 100g
    - One-line health benefit
    - Macronutrients (protein, carbs, fats) in g per 100g
    Format:
    Food: <name>
    Calories: <value> kcal
    Benefit: <one line>
    Protein: <value>g, Carbs: <value>g, Fat: <value>g
    """

    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a nutrition expert."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 200
    }

    try:
        response = requests.post(TOGETHER_API_URL, headers=headers, json=body)
        response.raise_for_status()
        output = response.json()
        message = output['choices'][0]['message']['content']
        return {"result": message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
