# Weather risk thresholds
RAIN_HIGH_THRESHOLD = 10.0       # mm – spray warning
HUMIDITY_HIGH_THRESHOLD = 80.0  # % – fungal risk
HEAT_HIGH_THRESHOLD = 38.0      # °C – irrigation advice
WIND_HIGH_THRESHOLD = 30.0      # km/h – wind alert

# Fallback disease analysis
FALLBACK_DISEASE_RESPONSE = """
🌿 **Could not connect to AI service. Here are general guidelines:**

**Common Crop Diseases & Organic Remedies:**

🦠 **Fungal Diseases:**
- Spray diluted neem oil (5ml per litre of water) every 7 days
- Apply Jeevamrut (fermented cow-dung solution) to strengthen plant immunity
- Improve air circulation by pruning dense foliage

🐛 **Pest Infestation:**
- Use neem-based sprays (neem cake + water)
- Release beneficial insects like ladybirds
- Plant companion crops like marigold as natural repellent

🍂 **Leaf Spots / Blight:**
- Remove and burn infected leaves immediately
- Apply turmeric + neem paste on affected areas
- Maintain proper drainage to avoid waterlogging

**Prevention:** 
- Regular Jeevamrut application every 15 days
- Crop rotation every season
- Maintain soil health with organic compost
"""

# Fallback weather response
FALLBACK_WEATHER_RESPONSE = """
🌤️ **Weather service temporarily unavailable.**

**General Seasonal Farming Advice:**
- Monitor local weather before any spray applications
- Water plants early morning to reduce evaporation
- Mulch soil to retain moisture during heat waves
- Watch for fungal symptoms during humid periods
"""

# Fallback market response
FALLBACK_MARKET_RESPONSE = """
📊 **Market data analysis temporarily unavailable.**

**General Selling Strategy:**
- Sell within 2–3 days of harvest for best prices
- Consider local mandis and farmer cooperatives
- Organic produce commands 20–30% premium
- Group selling with other farmers improves bargaining power
"""

# Indian states and major cities for weather lookup
INDIAN_CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai",
    "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Lucknow",
    "Nagpur", "Bhopal", "Indore", "Patna", "Chandigarh",
    "Coimbatore", "Visakhapatnam", "Nashik", "Vadodara", "Surat"
]

# Crop categories
CROP_CATEGORIES = [
    "Vegetables", "Fruits", "Grains & Cereals", 
    "Pulses & Legumes", "Spices", "Cash Crops"
]
