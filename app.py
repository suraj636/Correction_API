from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = FastAPI()

# MongoDB Atlas connection string
uri = os.getenv("MONGODB_URI")

# Connect to MongoDB Atlas
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["SpeechToText"]
collection = db["Correction_Feedback"]

# Define CORS policy
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Define data models using Pydantic
class Correction(BaseModel):
    selected_words: list[str]
    corrected_sentence: str

# Default route
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Custom API!"}

# Define API endpoints
@app.post("/submit_correction")
async def submit_correction(correction: Correction):
    # Insert data into MongoDB Atlas
    inserted_data = collection.insert_one({
        "selected_words": correction.selected_words,
        "corrected_sentence": correction.corrected_sentence
    })
    return {"message": "Correction submitted successfully", "inserted_id": str(inserted_data.inserted_id)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
