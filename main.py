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

# Function to check if the number is prime
def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


# Function to check if the number is perfect
def is_perfect(n: int) -> bool:
    divisors_sum = sum(i for i in range(1, n) if n % i == 0)
    return divisors_sum == n


# Function to check if the number is Armstrong
def is_armstrong(n: int) -> bool:
    digits = [int(digit) for digit in str(n)]
    power = len(digits)
    return sum(digit ** power for digit in digits) == n


# Function to calculate the sum of digits
def digit_sum(n: int) -> int:
    return sum(int(digit) for digit in str(n))


# Function to check if the number is odd or even
def is_odd(n: int) -> bool:
    return n % 2 != 0


# Fetch fun fact from Numbers API
def get_fun_fact(n: int) -> str:
    response = requests.get(f"http://numbersapi.com/{n}?json")
    if response.status_code == 200:
        return response.json().get("text", "")
    else:
        return "No fun fact available."


# API Endpoint
@app.get("/api/classify-number")
async def classify_number(number: int):
    # Validate if number is an integer
    if not isinstance(number, int):
        raise HTTPException(status_code=400, detail="Invalid input. Please provide a valid integer.")

    # Check for properties
    properties = []
    if is_armstrong(number):
        properties.append("armstrong")
    if is_odd(number):
        properties.append("odd")
    else:
        properties.append("even")

    # Prepare the response
    response = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": digit_sum(number),
        "fun_fact": get_fun_fact(number)
    }

    return response
