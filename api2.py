from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os
from google.genai import Client
import json
import uvicorn
import dotenv
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
     
       "http://localhost:8080",
   ]
   
   app.add_middleware(
       CORSMiddleware,
       allow_origins=['*'],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   @app.post("/charts/pie")
   async def create_pie_chart():
       # Logic to create a chart
       chart=pdf_parser(prompt="""From the following balance sheet or financial report, extract the major asset components (both current and non-current) along with their values. Output the result in JSON format   for a pie chart. Group similar subcategories under major asset categories if needed. Format the output with 'labels' and 'data' as arrays. Do not include liabilities or equity values.
   
   Example Output Format  (Pie Chart)
   [{"name":"Cash & Cash Equivalents","value":150000},{"name":"Accounts Receivable","value":85000},{"name":"Inventory","value":60000},{"name":"Property, Plant & Equipment","value":220000},{"name":"Intangible Assets","value":40000}]
   """,file=file)
       chart=chart.replace("```"," ").replace("json"," ")
       chart=json.loads(chart)
       
       return chart
   @app.post("/charts/bar")
   async def create_bar_chart():
       # Logic to create a chart
       chart=pdf_parser(prompt="""From the following balance sheet or financial report, extract the values of  Liabilities .
Include both current and non-current components in their totals.
Do not include equity values.

Output the result in JSON format   for a bar chart that shows values of each category of liabilities .


✅ Example Output Format
 [{"name":"Total non-current liabilities","value":150000},{"name":"Accounts Payable","value":85000},{"name":"Short-term Debt","value":60000},{"name":"Long-term Debt","value":220000},{"name":"Deferred Tax Liabilities","value":40000}]""",file=file)
       chart=chart.replace("```"," ").replace("json"," ")
       chart=json.loads(chart)
   
       return chart  
   @app.post("/charts/line")
   async def create_line_chart():
       # Logic to create a chart
       chart=pdf_parser(prompt="""From the following balance sheet or financial report, extract the total shareholders’ equity values over multiple years or reporting periods. Include all components contributing to total equity (e.g., share capital, retained earnings, reserves, accumulated other comprehensive income) summed under total equity for each year.

Output the result in JSON format   for a line chart, showing the evolution of total shareholders’ equity over time.

Use the following structure:

[{"name":2024,"data":350000},{"name":2025,"data":370000},{"name":2026,"data":395000},{"name":2027,"data":420000},{"name":2028,"data":440000}]
""",file=file)
       chart=chart.replace("```"," ").replace("json"," ")
       chart=json.loads(chart)
 
       return chart

   uvicorn.run(app, host="127.0.0.1", port=8000)
if __name__ == "__main__":
       api(file="C:/Users/Dell/OneDrive/Downloads/Balance-Sheet-Example.pdf")
