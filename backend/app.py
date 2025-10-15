import os
import json
import base64
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import requests

# ✅ Import database helpers safely
try:
    from models import init_db, save_profile, get_profile
except ImportError:
    print("⚠️ models.py not found — using dummy functions")
    def init_db(): pass
    def save_profile(data): pass
    def get_profile(): return {}

# --- Load environment variables ---
load_dotenv()
AI_API_KEY = os.getenv("AI_API_KEY")
AI_API_URL = os.getenv("AI_API_URL")

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
STATIC_FOLDER = os.path.join(BASE_DIR, "build")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Flask setup ---
app = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path='')
CORS(app)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB

# --- Initialize database ---
init_db()

# ================================
# 📌 PROFILE ENDPOINTS
# ================================
@app.route("/api/profile", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        data = request.json
        save_profile(data)
        return jsonify({"status": "ok", "message": "Profile saved successfully"})
    else:
        profile = get_profile()
        return jsonify(profile or {})

# ================================
# 📌 MEAL PLAN GENERATION
# ================================
def estimate_calorie_needs(profile):
    """Estimate daily calorie needs using Mifflin-St Jeor equation."""
    if not profile:
        return 2000

    weight = profile.get("weight_kg", 60)
    height = profile.get("height_cm", 165)
    age = profile.get("age", 25)
    gender = profile.get("gender", "female").lower()
    activity = profile.get("activity_level", "moderate")

    if gender == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    multiplier = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9
    }.get(activity, 1.55)

    return int(bmr * multiplier)

def generate_meal_plan(profile):
    calories = estimate_calorie_needs(profile)
    pref = (profile.get("dietary_pref") or "mixed").lower()

    protein = int(calories * 0.25 / 4)
    carbs = int(calories * 0.45 / 4)
    fats = int(calories * 0.3 / 9)

    base_meals = {
        "breakfast": "Oats with milk/soy + fruit",
        "lunch": "Rice/Chapati + Protein + Salad",
        "snack": "Yogurt/Buttermilk + Nuts",
        "dinner": "Light protein + Vegetables + Small carbs"
    }

    days = []
    for d in range(7):
        meals = base_meals.copy()

        if pref == "vegetarian":
            meals["lunch"] = "Rice/Chapati + Paneer/Legumes + Salad"
            meals["dinner"] = "Lentil soup + Veg stir fry"
        elif pref in ["non-veg", "mixed", "non-vegetarian"]:
            meals["lunch"] = "Rice/Chapati + Chicken/Fish + Salad"
            meals["dinner"] = "Grilled chicken/fish + Vegetables"
        elif pref == "vegan":
            meals["breakfast"] = "Oats with soy milk + fruit"
            meals["lunch"] = "Rice/Chapati + Legumes + Salad"
            meals["snack"] = "Nuts + Fruit"
            meals["dinner"] = "Tofu stir fry + Vegetables"

        days.append({
            "day": f"Day {d + 1}",
            "calories_target": calories,
            "macros": {
                "protein_g": protein,
                "carbs_g": carbs,
                "fat_g": fats
            },
            "meals": meals
        })

    shopping = [
        "Rice / Wheat flour (chapati)",
        "Vegetables (seasonal)",
        "Fruits (bananas, apples)",
        "Legumes (lentils, chickpeas)",
        "Dairy / milk / yogurt",
        "Eggs / Chicken / Fish or Paneer",
        "Nuts (almonds, peanuts)",
        "Cooking oil (olive/groundnut)"
    ]

    return {
        "days": days,
        "shopping_list": shopping,
        "daily_calories": calories,
        "dietary_preference": pref
    }

@app.route("/api/mealplan", methods=["GET"])
def mealplan():
    profile = get_profile()
    plan = generate_meal_plan(profile or {})
    return jsonify(plan)

# ================================
# 📌 IMAGE ANALYSIS ENDPOINT (Gemini Vision)
# ================================
@app.route("/api/analyze_image", methods=["POST"])
def analyze_image():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    f = request.files["image"]
    if f.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    filename = secure_filename(f.filename)
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    f.save(path)

    try:
        from PIL import Image
        img = Image.open(path)
        width, height = img.size
    except Exception:
        width = height = 0

    if AI_API_KEY and AI_API_URL:
        try:
            with open(path, "rb") as img_file:
                image_data = base64.b64encode(img_file.read()).decode('utf-8')

            mime_type = "image/jpeg"
            if filename.lower().endswith(".png"):
                mime_type = "image/png"
            elif filename.lower().endswith(".webp"):
                mime_type = "image/webp"

            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={AI_API_KEY}"

            payload = {
                "contents": [{
                    "parts": [
                        {"text": "Analyze this food image and return JSON of food items with nutritional info."},
                        {"inline_data": {"mime_type": mime_type, "data": image_data}}
                    ]
                }]
            }

            headers = {"Content-Type": "application/json"}
            resp = requests.post(url, json=payload, headers=headers, timeout=30)
            resp.raise_for_status()
            result = resp.json()
            ai_text = result["candidates"][0]["content"]["parts"][0]["text"]

            return jsonify({
                "width": width,
                "height": height,
                "ai_analysis": ai_text,
                "raw_response": result
            })
        except Exception as e:
            print(f"AI API Error: {str(e)}")
            return jsonify({
                "error": "AI service error",
                "detail": str(e),
                "fallback": True,
                "mock_data": get_mock_nutrition_data(width, height)
            }), 500
    else:
        return jsonify(get_mock_nutrition_data(width, height))

def get_mock_nutrition_data(width, height):
    return {
        "width": width,
        "height": height,
        "items_detected": [
            {"name": "rice", "estimated_grams": 150},
            {"name": "chicken", "estimated_grams": 100},
            {"name": "vegetables", "estimated_grams": 80}
        ],
        "nutrition_estimate": {
            "calories": 550,
            "protein_g": 35,
            "carbs_g": 65,
            "fat_g": 12
        },
        "note": "⚠️ Mock estimate only. Configure AI_API_KEY in .env for real AI analysis."
    }

# ================================
# 📌 CHAT ENDPOINT (Gemini)
# ================================
@app.route("/api/chat", methods=["POST"])
def chat():
    body = request.json or {}
    user_msg = body.get("message", "")

    if not user_msg:
        return jsonify({"error": "No message provided"}), 400

    if AI_API_KEY and AI_API_URL:
        try:
            profile = get_profile()
            context = ""
            if profile:
                context = f"\nUser Profile: {profile.get('age')} yrs, {profile.get('gender')}, {profile.get('weight_kg')}kg, Activity: {profile.get('activity_level')}"

            prompt = f"You are a nutrition and fitness assistant.{context}\n\nUser: {user_msg}"

            url = f"{AI_API_URL}?key={AI_API_KEY}"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            headers = {"Content-Type": "application/json"}

            resp = requests.post(url, json=payload, headers=headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            reply = data["candidates"][0]["content"]["parts"][0]["text"]

            return jsonify({"reply": reply, "source": "gemini-ai"})
        except Exception as e:
            print(f"Chat AI Error: {str(e)}")
            return jsonify({"reply": f"⚠️ AI service unavailable. Error: {str(e)}", "fallback": True}), 500
    else:
        return jsonify({
            "reply": "💬 I can help with meal planning, calorie estimates, and workouts. Configure AI_API_KEY in .env for full AI features.",
            "source": "fallback"
        })

# ================================
# 📌 HEALTH CHECK
# ================================
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "ai_configured": bool(AI_API_KEY and AI_API_URL),
        "database": "connected" if get_profile() is not None else "not configured"
    })

# ================================
# 📌 SERVE FRONTEND (MUST BE LAST)
# ================================
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(STATIC_FOLDER, path)):
        return send_from_directory(STATIC_FOLDER, path)
    elif os.path.exists(os.path.join(STATIC_FOLDER, 'index.html')):
        return send_from_directory(STATIC_FOLDER, 'index.html')
    else:
        return jsonify({
            "message": "✅ Flask backend is running successfully!",
            "available_endpoints": [
                "/api/health",
                "/api/profile",
                "/api/mealplan",
                "/api/analyze_image",
                "/api/chat"
            ],
            "ai_configured": bool(AI_API_KEY and AI_API_URL),
            "note": "Build your React frontend with 'npm run build' and place it in backend/build"
        })

# ================================
# 📌 RUN SERVER
# ================================
if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Starting Flask Backend Server")
    print("=" * 50)
    print(f"✅ AI API Key: {'Configured ✓' if AI_API_KEY else '❌ NOT CONFIGURED'}")
    print(f"✅ AI API URL: {'Configured ✓' if AI_API_URL else '❌ NOT CONFIGURED'}")
    print(f"✅ Frontend: {'Found (build/) ✓' if os.path.exists(STATIC_FOLDER) else 'Not found (API only mode)'}")
    print(f"✅ Database: {'Initialized ✓' if get_profile() is not None else 'Not configured'}")
    print("=" * 50)
    print("📍 Server running at: http://localhost:5000")
    print("📍 API endpoints at: http://localhost:5000/api/")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=True)
