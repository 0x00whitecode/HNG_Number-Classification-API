from fastapi import FastAPI, HTTPException
from typing import List
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Function to check if a number is Armstrong
def is_armstrong(n: int) -> bool:
    digits = [int(digit) for digit in str(n)]
    return n == sum(digit ** len(digits) for digit in digits)

# Function to check if a number is prime
def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Function to fetch fun fact from Numbers API
def get_fun_fact(n: int) -> str:
    response = requests.get(f"http://numbersapi.com/{n}?json")
    if response.status_code == 200:
        return response.json().get('text', 'No fun fact available.')
    else:
        raise HTTPException(status_code=400, detail="Failed to fetch data from the Numbers API.")

# API Endpoint
@app.get("/api/classify-number")
async def classify_number(number: int):
    # Validate if number is an integer
    if not isinstance(number, int):
        raise HTTPException(status_code=400, detail="Invalid input. Please provide a valid integer.")

    # Calculate properties
    is_prime_number = is_prime(number)
    is_armstrong_number = is_armstrong(number)
    parity = "odd" if number % 2 != 0 else "even"
    
    # Prepare properties based on Armstrong and parity
    properties = []
    if is_armstrong_number:
        properties.append("armstrong")
    if parity == "odd":
        properties.append("odd")
    else:
        properties.append("even")

    # Fetch fun fact from Numbers API
    fun_fact = get_fun_fact(number)

    # Prepare the response
    response = {
        "number": number,
        "is_prime": is_prime_number,
        "is_perfect": False,  # This task doesn't include perfect number classification
        "properties": properties,
        "digit_sum": sum(int(digit) for digit in str(number)),
        "fun_fact": fun_fact
    }

    return response
