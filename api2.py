from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os
from google.genai import Client
import json
import uvicorn
import dotenv
import re
dotenv.load_dotenv("env_example.env")
def pdf_parser(prompt: str,file: Optional[str])-> str:
    client=Client(api_key=os.getenv("GOOGLE_API_KEY"))
    files=client.files.upload(file=file)
    response= client.models.generate_content(
      model="gemini-2.5-flash",contents=[prompt,files])
    return response.text
def api(file: Optional[str]):
   app=FastAPI()
   origins = [
     
       "http://localhost:3000",
   ]
   
   app.add_middleware(
       CORSMiddleware,
       allow_origins=origins,
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   line_chart =  pdf_parser(prompt="""From the provided balance sheet or financial report, extract the total shareholders’ equity (also known as total equity, stockholders’ equity, or owners’ equity) for each available year or reporting period.

Instructions:
-Identify all components that contribute to total shareholders’ equity — such as:
-Share capital / common stock / paid-in capital
-Retained earnings
-Reserves

Non-controlling interest (if included in total equity line)
Use the "Total Equity" or "Total Shareholders’ Equity" line item as the final summed figure for each period.
If multiple years or periods are present, extract the total equity value for each.
If more than four years are available, select the four years with the highest total equity values.
Format the extracted data in a consistent list of objects suitable for a line chart:

[
  {"x": 2021, "y": 320000},
  {"x": 2022, "y": 345000},
  {"x": 2023, "y": 370000},
  {"x": 2024, "y": 395000}
]

Ensure:
Each x represents the fiscal year (as a number, e.g., 2024).
Each y represents the total shareholders’ equity for that year (as a numeric value).

Output only the  list — no commentary or explanation.""",file=file).replace("```"," ").replace("json"," ")
   bar_chart= pdf_parser(prompt="""From the following balance sheet or financial report, extract only the numeric values of Liabilities, including both current and non-current components.

Extraction Rules:

Identify all relevant liability line items, such as (but not limited to):
-Deferred Tax Liabilities
-Other Non-current Liabilities
-Total Current Liabilities
-Total Non-current Liabilities


From all available categories, choose only 4 of the most important or significant liability categories, typically those with the largest values or most impact.
Do not include any equity values (e.g., share capital, retained earnings, total equity).
Ensure that both current and non-current liabilities are represented within the selected categories.
Present all extracted data in a consistent JSON list format, suitable for visualization in a bar chart.

✅ Output Format:
Return only the JSON list (no commentary, no extra text).

Example:

[
  {"x": "Total Non-current Liabilities", "y": 150000},
  {"x": "Accounts Payable", "y": 85000},
  {"x": "Short-term Debt", "y": 60000},
  {"x": "Long-term Debt", "y": 220000}
]

Output Requirements:

Each object must include:
"x" → liability category name (string)
"y" → numeric value (integer or float)
All numeric values must be extracted directly from the financial report (no estimated or calculated values).

Output should always maintain the same structured format for repeated extractions.""",file=file).replace("```"," ").replace("json"," ")
   pie_chart= pdf_parser(prompt="""From the following balance sheet or financial report, extract the major asset components and their corresponding values.

Extraction Rules:

Include both current and non-current assets.
Identify and group similar subcategories under major asset headings if necessary.

Example grouping:

Combine “Cash,” “Bank Balances,” and “Short-term Investments” into “Cash & Cash Equivalents.”
Combine “Machinery,” “Buildings,” and “Land” into “Property, Plant & Equipment (PPE).”
Focus only on asset categories, not liabilities or equity.
Choose only the 4 most important (highest value or most significant) asset categories.



✅ Output Format:
Return only the JSON list — no commentary, no explanations.
Format for pie chart visualization as follows:

[
  {"x": "Cash & Cash Equivalents", "y": 150000},
  {"x": "Accounts Receivable", "y": 85000},
  {"x": "Inventory", "y": 60000},
  {"x": "Property, Plant & Equipment", "y": 220000}
]

Output Requirements:

"x" → Asset category name (string)
"y" → Numeric value (integer or float)
Only assets — exclude liabilities, equity, and totals unrelated to assets.

Maintain consistent structure across multiple executions to ensure data comparability.
   """,file=file).replace("```"," ").replace("json"," ")
   @app.get("/charts/pie")
   async def create_pie_chart():
       # Logic to create a chart
       chart= pie_chart
       cleaned = re.sub(r'\s+', '', chart)
       proper_json = json.loads(cleaned)
       return {"chart": proper_json}
   
   @app.get("/charts/bar")
   async def create_bar_chart():
       # Logic to create a chart
       chart= bar_chart  
       cleaned = re.sub(r'\s+', '', chart)
       proper_json = json.loads(cleaned)

       return {"chart": proper_json}

   @app.get("/charts/line")
   async def create_line_chart():
       # Logic to create a chart
       chart= line_chart
       cleaned = re.sub(r'\s+', '', chart)
       proper_json = json.loads(cleaned)

       return {"chart": proper_json}

   uvicorn.run(app, host="127.0.0.1", port=8000)
if __name__ == "__main__":
       api(file="C:/Users/Dell/Downloads/FY24_Q1_Consolidated_Financial_Statements.pdf")
