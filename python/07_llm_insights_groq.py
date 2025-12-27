import os
import sqlite3
from groq import Groq

# -------------------------
# CONFIG
# -------------------------

# Make sure you have set this once in PowerShell:
# setx GROQ_API_KEY "your_key_here"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY not found. Please set it using setx GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

# -------------------------
# DATABASE CONNECTION
# -------------------------

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "mindone_dw.db"))

print(f"📂 Database path: {DB_PATH}")
print(f"📂 Database exists: {os.path.exists(DB_PATH)}")

conn = sqlite3.connect(DB_PATH)

# -------------------------
# SQL METRICS
# -------------------------

total_revenue = conn.execute("""
    SELECT ROUND(SUM(revenue), 2) FROM fact_sales
""").fetchone()[0]

total_orders = conn.execute("""
    SELECT COUNT(DISTINCT order_id) FROM fact_sales
""").fetchone()[0]

avg_delivery = conn.execute("""
    SELECT ROUND(AVG(delivery_days), 2) FROM fact_sales
""").fetchone()[0]

conn.close()

# -------------------------
# BUILD PROMPT FOR LLM
# -------------------------

prompt = f"""
You are a senior business analyst.

Here are the key ecommerce metrics:

- Total Revenue: {total_revenue}
- Total Orders: {total_orders}
- Average Delivery Time (days): {avg_delivery}

Tasks:
1. Write 3 clear business insights
2. Write 2 actionable recommendations
3. Keep language executive-friendly
"""

# -------------------------
# CALL GROQ LLM
# -------------------------

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "system", "content": "You analyze business data and give insights."},
        {"role": "user", "content": prompt}
    ]
)

llm_output = response.choices[0].message.content

# -------------------------
# PRINT OUTPUT
# -------------------------

print("\n📊 LLM BUSINESS INSIGHTS (GROQ)\n")
print(llm_output)

# -------------------------
# SAVE OUTPUT FOR POWER BI
# -------------------------

OUTPUT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "llm_business_insights.txt")
)


with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(llm_output)

print(f"\n✅ LLM insights saved to:\n{OUTPUT_PATH}")
