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
       chart=pdf_parser(prompt="""From the following balance sheet or financial report, extract the major asset components (both current and non-current) along with their values. Output the result in JSON format compatible with Chart.js for a pie chart. Group similar subcategories under major asset categories if needed. Format the output with 'labels' and 'data' as arrays. Do not include liabilities or equity values.
   
   Example Output Format for Chart.js (Pie Chart)
   {
     "type": "pie",
     "data": {
       "labels": [
         "Cash & Cash Equivalents",
         "Accounts Receivable",
         "Inventory",
         "Property, Plant & Equipment",
         "Intangible Assets"
       ],
       "datasets": [
         {
           "label": "Asset Breakdown",
           "data": [150000, 85000, 60000, 220000, 40000],
           "backgroundColor": [
             "#36A2EB",
             "#FF6384",
             "#FFCE56",
             "#4BC0C0",
             "#9966FF"
           ]
         }
       ]
     }
   }""",file=file)
       chart=chart.replace("```"," ").replace("json"," ")
       chart=json.loads(chart)
       
       return chart
   @app.post("/charts/bar")
   async def create_bar_chart():
       # Logic to create a chart
       chart=pdf_parser(prompt="""From the following balance sheet or financial report, extract the total values of Assets and Liabilities for each reporting period (e.g., yearly or quarterly).
Include both current and non-current components in their respective totals.
Do not include equity values.

Output the result in JSON format compatible with Chart.js for a bar chart that compares total assets vs total liabilities over time.

If multiple years or periods exist, show them in "labels"; otherwise, show a single-period comparison.

✅ Example Output Format
{
  "type": "bar",
  "data": {
    "labels": ["2021", "2022", "2023", "2024", "2025"],
    "datasets": [
      {
        "label": "Total Assets",
        "data": [520000, 560000, 590000, 625000, 660000],
        "backgroundColor": "#36A2EB"
      },
      {
        "label": "Total Liabilities",
        "data": [310000, 330000, 350000, 370000, 390000],
        "backgroundColor": "#FF6384"
      }
    ]
  },
  "options": {
    "responsive": true,
    "plugins": {
      "title": {
        "display": true,
        "text": "Assets vs Liabilities Over Time"
      },
      "legend": {
        "position": "top"
      }
    },
    "scales": {
      "y": {
        "beginAtZero": true,
        "title": {
          "display": true,
          "text": "Amount (in USD)"
        }
      },
      "x": {
        "title": {
          "display": true,
          "text": "Fiscal Year"
        }
      }
    }
  }
}""",file=file)
       chart=chart.replace("```"," ").replace("json"," ")
       chart=json.loads(chart)
   
       return chart  
   @app.post("/charts/line")
   async def create_line_chart():
       # Logic to create a chart
       chart=pdf_parser(prompt="""From the following balance sheet or financial report, extract the total shareholders’ equity values over multiple years or reporting periods. Include all components contributing to total equity (e.g., share capital, retained earnings, reserves, accumulated other comprehensive income) summed under total equity for each year.

Output the result in JSON format compatible with Chart.js for a line chart, showing the evolution of total shareholders’ equity over time.

Use the following structure:

{
  "type": "line",
  "data": {
    "labels": ["2021", "2022", "2023", "2024", "2025"],
    "datasets": [
      {
        "label": "Total Shareholders' Equity",
        "data": [350000, 370000, 395000, 420000, 440000],
        "borderColor": "#36A2EB",
        "backgroundColor": "rgba(54,162,235,0.2)",
        "fill": true,
        "tension": 0.4,
        "pointRadius": 5,
        "pointBackgroundColor": "#36A2EB"
      }
    ]
  }
}
""",file=file)
       chart=chart.replace("```"," ").replace("json"," ")
       chart=json.loads(chart)
   
       return chart  
     
   uvicorn.run(app, host="127.0.0.1", port=3000)
