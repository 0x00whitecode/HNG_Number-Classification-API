from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx  # Use httpx for async requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (Adjust for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to check if a number is prime
def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Function to check if a number is perfect
def is_perfect(n: int) -> bool:
    return sum(i for i in range(1, n) if n % i == 0) == n

# Function to check if a number is an Armstrong number
def is_armstrong(n: int) -> bool:
    digits = [int(digit) for digit in str(n)]
    power = len(digits)
    return sum(digit ** power for digit in digits) == n

# Function to calculate the sum of digits
def digit_sum(n: int) -> int:
    return sum(int(digit) for digit in str(n))

# Function to check if a number is odd or even
def is_odd(n: int) -> bool:
    return n % 2 != 0

# Fetch fun fact from Numbers API (async version)
async def get_fun_fact(n: int) -> str:
    url = f"http://numbersapi.com/{n}?json"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            return response.json().get("text", "No fun fact available.")
        return "No fun fact available."

# API Endpoint
@app.get("/api/classify-number")
async def classify_number(number: int):
    properties = []
    if is_armstrong(number):
        properties.append("armstrong")
    properties.append("odd" if is_odd(number) else "even")

    # Fetch fun fact asynchronously
    fun_fact = await get_fun_fact(number)

    response = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": digit_sum(number),
        "fun_fact": fun_fact
    }

    return response
