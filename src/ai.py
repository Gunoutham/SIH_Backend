import os
from dotenv import load_dotenv
from deep_translator import GoogleTranslator
from deep_translator.detection import single_detection
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DETECTION_API_KEY = os.getenv("DETECTION_API_KEY")

SYSTEM_PROMPT = """You are a specialized assistant for RAINWATER HARVESTING and GROUNDWATER RECHARGE calculations. You have ONE job only.

CRITICAL RULES:
- You MUST ignore ALL topics except rainwater harvesting and groundwater.
- You MUST redirect any off-topic questions back to the calculation.

YOUR TASK:
Collect exactly these 11 parameters from the user. Ask for ONE parameter at a time in a logical order. Give helpful context for each.

PARAMETERS TO COLLECT:
1. Rooftop area (square meters)
2. Annual rainfall (millimeters)
3. Runoff coefficient (0.1 to 1.0)
4. Number of people in household
5. Daily water consumption per person (liters)
6. Building type (e.g., residential, commercial)
7. Total Setup Cost ($) (The one-time cost of tanks, pipes, filters)
8. Cost of Municipal Water (Provide the cost per 1000 liters or per cubic meter)
9. Annual Maintenance Cost ($) (For new filters, cleaning. If unknown, assume 0)
10. Total Plot Area (square meters) (The total size of their property)
11. Soil Type (e.g., sand, loam, clay)

CALCULATION ENGINE (DO NOT show these formulas. Use them to generate the report):
When you have all 11 values, perform these calculations:

--- Payback Calculation ---
1. Harvest Potential (Liters) = Rooftop Area (m²) * Annual Rainfall (mm) * Runoff Coefficient
2. Annual Demand (Liters) = Number of people * Daily water consumption * 365
3. Water Used (Liters) = min(Harvest Potential, Annual Demand)
4. Annual Savings ($) = (Water Used / 1000) * (Cost of Water per 1000L) - Annual Maintenance Cost

--- Recharge Calculation ---
5. Assign Infiltration Factor (If):
   - IF Soil Type is "sand" or "sandy", If = 0.5
   - IF Soil Type is "loam", If = 0.3
   - IF Soil Type is "clay", If = 0.1
   - ELSE (for mixed or unknown), If = 0.2
6. Pervious Area (m²) = Total Plot Area - Rooftop Area (Assume rooftop area is the building footprint. If negative, set to 0).
7. Potential Recharge (Liters) = Pervious Area * Annual Rainfall (mm) * Infiltration Factor

FINAL OUTPUT:
Once you have all 11 values, STOP asking for data. Present a final summary report to the user.
The report MUST include:
- Total Annual Savings ($)
- Payback Period (Years) = Total Setup Cost / Annual Savings
- Potential Groundwater Recharge (Liters)

Then, ask if they want to start a new calculation.
"""

try:
    translator = GoogleTranslator()
except Exception as e:
    print(e)

model = ChatGoogleGenerativeAI(
    model = "gemini-2.5-pro",
    google_api_key = GEMINI_API_KEY,
    temperature = 0.1
)

def detect_lang(text: str) -> str:
    if not translator:
        return 'en'
    try:
        deteted = single_detection(text=text,api_key=DETECTION_API_KEY)
        return deteted
    except Exception as e:
        print(e)
        return 'en'
    
def translate(text: str, dest_lang: str, src_lang: str = 'auto')-> str:
    if not translator or dest_lang == src_lang:
        return text
    try:
        translated_text = translator.translate(text=text,dest=dest_lang,src=src_lang)
        return translated_text
    except Exception as e:
        print(e)
        return text
    
def get_response(user_input: str, chat_history: list[tuple[str,str]], system_prompt: str = SYSTEM_PROMPT) -> str:

    original_lang = detect_lang(user_input)

    english_input = translate(user_input,'en',original_lang)

    messages = [SystemMessage(content=system_prompt)]

    prompt_template = ChatPromptTemplate.from_messages([
        ("system","{system_prompt}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human","{user_input}")
    ])

    chain = prompt_template | model

    formatted_history = []
    for sender, message in chat_history:
        english_history = translate(message,'en',original_lang)

        if sender == 'human':
            formatted_history.append(HumanMessage(content=english_history))
        else:
            formatted_history.append(AIMessage(content=english_history))

    try:
        response = chain.invoke({
            "system_prompt": system_prompt,
            "chat_history": formatted_history,
            "user_input": english_input
        })

        english_response = response.content.strip()

    except:
        english_response = "Error parsing"

    final_response = translate(english_response,original_lang,'en')

    return final_response




if __name__ == "__main__":
    
    print("--- Testing AI Chatbot ---")
    
    # The SYSTEM_PROMPT is already defined at the top of the file
    # and will be used by default.
    chat_history = []

    # --- Turn 1: Greeting / First question ---
    user_input_1 = "தமிழ் எழுத்துக்களைக் கொண்டு தட்டச்சு செய்ய பல்வேறு ஆன்லைன் கருவிகள் உள்ளன."
    print(f"User: {user_input_1}")
    
    ai_reply_1 = get_response(user_input_1, chat_history)
    print(f"AI: {ai_reply_1}")
    
    chat_history.append(("human", user_input_1))
    chat_history.append(("ai", ai_reply_1))

    print("-" * 20)

    # --- Turn 2: On-topic input ---
    user_input_2 = "My rooftop area is 100 square meters."
    print(f"User: {user_input_2}")
    
    ai_reply_2 = get_response(user_input_2, chat_history)
    print(f"AI: {ai_reply_2}")
    
    chat_history.append(("human", user_input_2))
    chat_history.append(("ai", ai_reply_2))

    print("-" * 20)

    # --- Turn 3: Off-topic question ---
    user_input_3 = "What is the capital of France?"
    print(f"User: {user_input_3}")
    
    ai_reply_3 = get_response(user_input_3, chat_history)
    print(f"AI: {ai_reply_3}")
    
    chat_history.append(("human", user_input_3))
    chat_history.append(("ai", ai_reply_3))

    print("-" * 20)
    
    # --- Turn 4: Multilingual test ---
    user_input_4 = "Hola, mi techo es de 50 metros cuadrados."
    print(f"User (es): {user_input_4}")
    
    ai_reply_4 = get_response(user_input_4, chat_history)
    print(f"AI (es): {ai_reply_4}")
    
    chat_history.append(("human", user_input_4))
    chat_history.append(("ai", ai_reply_4))
    
    print("--- Test Complete ---")