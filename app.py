import os
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from dotenv import load_dotenv
import urllib.parse

# Load environment variables
load_dotenv()

app = Flask(__name__)

# MongoDB configuration with proper URL encoding
username = urllib.parse.quote_plus(os.getenv("MONGO_USERNAME", "joseph"))
password = urllib.parse.quote_plus(os.getenv("MONGO_PASSWORD", "josephcode"))
MONGO_URI = f"mongodb+srv://{username}:{password}@cluster0.1wjst2q.mongodb.net/survey_db?retryWrites=true&w=majority"

# Connect to MongoDB
try:
    client = MongoClient(MONGO_URI)
    db = client['survey_db']  
    collection = db['responses']  # Collection will be created automatically
    
    # Test connection
    client.admin.command('ping')
    print("✅ Successfully connected to MongoDB Atlas!")
except Exception as e:
    print(f"❌ Failed to connect to MongoDB: {e}")
    raise

@app.route('/', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':
        try:
            data = {
                "age": int(request.form['age']),
                "gender": request.form['gender'],
                "income": float(request.form['income']),
                "expenses": {
                    category: float(request.form.get(category, 0))
                    for category in ['utilities', 'entertainment', 'school_fees', 'shopping', 'healthcare']
                    if request.form.get(category)
                }
            }
            collection.insert_one(data)
            return redirect('/thankyou')
        except Exception as e:
            return f"<h3>Error submitting data: {e}</h3>"

    return render_template('form.html')

@app.route('/thankyou')
def thank_you():
    return "<h2>Thank you for submitting your data!</h2>"

