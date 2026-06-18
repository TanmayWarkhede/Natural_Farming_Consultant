🌱 Smart Voice-Based Natural Farming Consultant

An AI-powered assistant designed to support farmers transitioning to natural and organic farming through intelligent, voice-enabled guidance.

It combines AI vision, weather intelligence, market analysis, and conversational assistance into a single unified platform.

✨ Features
🦠 Disease Detection

Farmers can upload crop images to get instant AI-based diagnosis.
The system identifies the crop disease, explains severity in simple language, and suggests organic-only treatments such as neem spray, Jeevamrut, and Panchagavya.
Voice output is supported for accessibility.

🌦 Weather Intelligence

Provides real-time weather data using the Open-Meteo API.
It analyzes temperature, rainfall, humidity, and wind conditions to generate farming risk alerts such as:

Heavy rain → spraying warning
High heat → irrigation guidance
High humidity → fungal disease risk
Strong wind → delay spraying

It also generates AI-powered farming advice with voice output.

📈 Market Intelligence

Tracks prices for 44+ crops across vegetables, fruits, grains, pulses, spices, and cash crops.
Farmers can:

Filter crops by category
View price trends
Get AI-based selling strategies (when to sell, store, or wait for better rates)
🤖 AI Assistant (Krishi Mitra)

A conversational farming expert trained for natural farming guidance.
It answers queries related to:

Organic farming methods
Pest control solutions
Soil improvement techniques
Crop planning

It supports multi-turn conversations and voice responses.

📊 Dashboard

A centralized overview showing:

System health status
Current weather summary
Market snapshot
Daily farming tip
🛠 Tech Stack
Streamlit (Frontend UI)
Google Gemini 2.5 Flash (AI engine for vision + chat)
Open-Meteo API (Weather data, free)
gTTS (Voice output system)
Pandas (Data processing)
SQLite (Optional logging and analytics)
📁 Project Structure

Natural_Farming_Consultant/
├── app.py
├── requirements.txt
├── config/
├── utils/
├── pages/
├── data/
├── assets/
├── database/
├── uploads/
└── reports/

🚀 Installation Steps
1. Clone the repository

Download the project from GitHub and navigate into the folder.

2. Create a virtual environment

Use Python venv to isolate dependencies (recommended for smooth setup).

3. Install dependencies

Install all required Python libraries using the requirements file.

4. Configure API key

Create a .env file and add your Google Gemini API key:
GEMINI_API_KEY=your_api_key_here

5. Run the application

Start the Streamlit app and open it in your browser.

⚙️ Configuration Details
Gemini API key is required (free from Google AI Studio)
Model used: gemini-2.5-flash-preview-05-20
Weather API requires no key (Open-Meteo is free)
📖 How to Use
Disease Detection

Upload a crop image → Click analyze → Get disease details + organic solution + voice output

Weather Module

Enter city name → Get weather conditions → View risk alerts → Receive AI farming advice

Market Module

Browse crop prices → Filter categories → Get AI recommendation on selling strategy

AI Assistant

Ask farming questions → Receive organic farming guidance → Enable voice for hands-free use

🧠 Core System Modules
Gemini Utilities → Handles AI vision, chat, and farming advice generation
Weather Utilities → Fetches weather data and calculates farming risk
Market Utilities → Processes crop prices and market insights
Voice Utilities → Converts AI responses into speech using gTTS
🌾 Supported Crop Categories
Vegetables
Fruits
Grains & Cereals
Pulses & Legumes
Spices
Cash Crops
🧪 Error Handling System

The application is designed to be stable and never crash:

Missing API key → fallback response system
Weather API failure → retry message
No image uploaded → validation warning
Voice system failure → switches to text-only mode
📄 License

This project is released under the MIT License and can be freely used or modified.

🙏 Acknowledgements

Special thanks to:

Google Gemini AI for intelligence engine
Open-Meteo for free weather data
Streamlit for rapid UI development
Indian farming community for inspiration

🌱 Built for Natural Farming & Sustainable Agriculture 🌱
