import logging
from typing import List, Dict, Optional, Tuple
from dbdriver import HotelDatabase
from datetime import datetime, timedelta
from livekit.agents import function_tool, RunContext
import os 
import random
from google.genai import Client
from playwright.async_api import async_playwright

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
meeting_id = random.randint(1, 999)

# Ensure unique meeting_id for each session
if os.path.exists(f"user_speech_log_{meeting_id}.txt"):
    meeting_id=random.randint(1, 999)

# Initialize database
db = HotelDatabase()
# initialize google genai client

def  ingest_text(pdf_path: str) -> None:
    from agent import ingest_pdf_cli 
    ingest_pdf_cli(pdf_path)
    
@function_tool
async def convert_to_pdf() :
 """Convert a text file to PDF."""
 client=Client(api_key=os.getenv("GOOGLE_API_KEY"))

 if os.path.exists(f"user_speech_log_{meeting_id}.txt"):
      logger.info(f"Converting user_speech_log_{meeting_id}.txt to PDF")
      file=client.files.upload(file=f"user_speech_log_{meeting_id}.txt")
      logger.info(f"summarizing file:{file}")
      response= client.models.generate_content(
      model="gemini-2.5-flash",contents=["""You are a professional meeting summarizer. Convert the following file into a concise,
        structured meeting summary in valid HTML only.

        Required HTML structure and fields:
        - <h1>Meeting Summary</h1>
        - Date (Month DD, YYYY) 
        - Time (start – end with timezone if present)
        - Location
        - Attendees (ul)
        - Agenda (ol)
        - Discussion Points (ul)
        - Decisions Made (ol)
        - Action Items (table with columns: Owner | Task | Due Date | Notes)
        - Next Meeting

        Rules:
        • Output only HTML — no commentary or extra text.  
        • If data missing, show "Not provided".  
        • Dates normalized to "Month DD, YYYY". Times to 12-hour AM/PM.  
        • Action item missing due date → "TBD".  
        • Keep bullets one short sentence (8–20 words).  
        • Make HTML semantic and readable; minimal inline CSS allowed.
        • Use '&minus;' for dashes in time ranges.
        • Use 16px for <p> and <li> tags.
        • Center the <h1> title.

        Example output:
        <h1 style="text-align: center;">Meeting Summary</h1>
        <p style="font-size: 16px;"><strong>Date:</strong> July 31, 2025</p>
        <p style="font-size: 16px;"><strong>Time:</strong> 9:13 PM &minus; 9:13 PM</p>
        <p style="font-size: 16px;"><strong>Location:</strong> Zoom</p>
        <h2>Attendees</h2>
        <ul>
          <li style="font-size: 16px;">Not provided</li>
        </ul>
        <h2>Agenda</h2>
        <ol>
          <li style="font-size: 16px;">Not provided</li>
        </ol>
        <h2>Discussion Points</h2>
        <ul>
          <li style="font-size: 16px;">The meeting opened with brief greetings and was immediately ended after some initial confusion.</li>
        </ul>
        <h2>Decisions Made</h2>
        <ol>
          <li style="font-size: 16px;">Not provided</li>
        </ol>
        <h2>Action Items</h2>
        <table style="width:100%; border-collapse: collapse;">
          <thead>
            <tr style="background-color:#f2f2f2;">
              <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Owner</th>
              <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Task</th>
              <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Due Date</th>
              <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Notes</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td colspan="4" style="border: 1px solid #ddd; padding: 8px; font-size: 16px;">No action items were assigned.</td>
            </tr>
          </tbody>
        </table>
        <h2>Next Meeting</h2>
        <p style="font-size: 16px;">Not provided</p>
 
        """,file])

      new_response=response.text.replace('```'," ").replace('html'," ")
      with open(f"user_speech_log_{meeting_id}.html", "w") as f:
        f.write(new_response)
        path_to_file=os.path.abspath(f"user_speech_log_{meeting_id}.html") if os.path.exists(f"user_speech_log_{meeting_id}.html") else None
      async with async_playwright() as p:
        # Launch Chromium in headless mode 
        browser = await p.chromium.launch()
        page = await browser.new_page()
        

        # Load the local HTML file
        await page.goto(f"file:///{path_to_file}")

        # Generate PDF
        await page.pdf(
            path=f"meeting_summary_{meeting_id}.pdf",
            format="A4",
            margin={"top": "20mm", "bottom": "20mm", "left": "15mm", "right": "15mm"},
            print_background=False
        )

        await browser.close()

      ingest_text(pdf_path=os.path.abspath(f"meeting_summary_{meeting_id}.pdf"))
      logger.info("Successfully converted TXT to PDF.")
 else:
        logger.error(f"File user_speech_log_{meeting_id}.html does not exist.")

@function_tool()
async def search_available_rooms(
    context: RunContext,
    room_type: str = None
) -> Dict:
    """
    Search for available rooms by type or get all room types.
    
    Args:
        room_type: Specific room type to search for (optional). If not provided, returns all room types.
        
    Returns:
        Dictionary containing available rooms information or all room types with counts.
    """
    logger.info(f"API: Searching for available rooms - type: {room_type}")
    
    if room_type:
        rooms = db.get_available_rooms_by_type(room_type)
        return {
            "success": True,
            "room_type": room_type,
            "available_count": len(rooms),
            "rooms": rooms
        }
    else:
        room_types = db.get_all_room_types()
        return {
            "success": True,
            "total_room_types": len(room_types),
            "room_types": room_types
        }

@function_tool()
async def check_room_availability(
    context: RunContext,
    room_type: str
) -> Dict:
    """
    Check if a specific room type is available.
    
    Args:
        room_type: Room type to check availability for.
        
    Returns:
        Dictionary containing availability status and details.
    """
    logger.info(f"API: Checking availability for {room_type}")
    
    rooms = db.get_available_rooms_by_type(room_type)
    is_available = len(rooms) > 0
    
    return {
        "success": True,
        "room_type": room_type,
        "is_available": is_available,
        "available_count": len(rooms),
        "rooms": rooms if is_available else []
    }

@function_tool()
async def get_room_pricing(
    context: RunContext,
    room_type: str
) -> Dict:
    """
    Get pricing information for a specific room type.
    
    Args:
        room_type: Room type to get pricing for.
        
    Returns:
        Dictionary containing pricing information including min/max prices and availability.
    """
    logger.info(f"API: Getting pricing for {room_type}")
    
    room_types = db.get_all_room_types()
    for rt in room_types:
        if rt['room_type'].lower() == room_type.lower():
            return {
                "success": True,
                "room_type": rt['room_type'],
                "min_price": rt['min_price'],
                "max_price": rt['max_price'],
                "available_rooms": rt['available_rooms']
            }
    
    return {
        "success": False,
        "error": f"Room type '{room_type}' not found"
    }

@function_tool()
async def book_room(
    context: RunContext,
    room_id: int,
    guest_name: str,
    check_in_date: str,
    check_out_date: str,
    special_occasion: str = None
) -> Dict:
    """
    Book a specific room for a guest.
    
    Args:
        room_id: ID of the room to book.
        guest_name: Name of the guest.
        check_in_date: Check-in date (YYYY-MM-DD format).
        check_out_date: Check-out date (YYYY-MM-DD format).
        special_occasion: Special occasion for potential discount (optional).
        
    Returns:
        Dictionary containing booking result with success status, message, and final price.
    """
    logger.info(f"API: Booking room {room_id} for {guest_name}")
    
    success, message, final_price = db.book_room(
        room_id, guest_name, check_in_date, check_out_date, special_occasion
    )
    
    if success:
        # Export to Excel after successful booking
        db.export_to_excel()
        logger.info("API: Booking successful, exported to Excel")
    
    return {
        "success": success,
        "message": message,
        "final_price": final_price,
        "room_id": room_id,
        "guest_name": guest_name
    }

@function_tool()
async def get_room_details(
    context: RunContext,
    room_id: int
) -> Dict:
    """
    Get detailed information about a specific room.
    
    Args:
        room_id: ID of the room to get details for.
        
    Returns:
        Dictionary containing detailed room information including status, pricing, and occupancy.
    """
    logger.info(f"API: Getting details for room {room_id}")
    
    room_status = db.get_room_status(room_id)
    if room_status:
        return {
            "success": True,
            "room": room_status
        }
    else:
        return {
            "success": False,
            "error": f"Room {room_id} not found"
        }

@function_tool()
async def suggest_room_for_occasion(
    context: RunContext,
    occasion: str,
    budget: float = None
) -> Dict:
    """
    Suggest appropriate room types based on occasion and budget.
    
    Args:
        occasion: Special occasion (e.g., honeymoon, birthday, anniversary).
        budget: Maximum budget in dollars (optional).
        
    Returns:
        Dictionary containing suggested rooms that match the occasion and budget.
    """
    logger.info(f"API: Suggesting rooms for {occasion} with budget {budget}")
    
    room_types = db.get_all_room_types()
    suggestions = []
    
    for rt in room_types:
        if rt['available_rooms'] > 0:
            # Check if within budget
            if budget is None or rt['max_price'] <= budget:
                suggestions.append({
                    "room_type": rt['room_type'],
                    "max_price": rt['max_price'],
                    "available_rooms": rt['available_rooms'],
                    "suitable_for": occasion
                })
    
    # Sort by price (lowest first)
    suggestions.sort(key=lambda x: x['max_price'])
    
    return {
        "success": True,
        "occasion": occasion,
        "budget": budget,
        "suggestions": suggestions[:3]  # Top 3 suggestions
    }

@function_tool()
async def calculate_discount(
    context: RunContext,
    room_type: str,
    occasion: str
) -> Dict:
    """
    Calculate potential discount for a room type and occasion.
    
    Args:
        room_type: Room type to calculate discount for.
        occasion: Special occasion for discount calculation.
        
    Returns:
        Dictionary containing discount information including original price, discount amount, and final price.
    """
    logger.info(f"API: Calculating discount for {room_type} - {occasion}")
    
    room_types = db.get_all_room_types()
    for rt in room_types:
        if rt['room_type'].lower() == room_type.lower():
            # Calculate discount percentage
            discount_percentage = db._calculate_discount(occasion)
            max_price = rt['max_price']
            discount_amount = max_price * (discount_percentage / 100)
            final_price = max_price - discount_amount
            
            return {
                "success": True,
                "room_type": rt['room_type'],
                "original_price": max_price,
                "discount_percentage": discount_percentage,
                "discount_amount": discount_amount,
                "final_price": final_price,
                "occasion": occasion
            }
    
    return {
        "success": False,
        "error": f"Room type '{room_type}' not found"
    }

@function_tool()
async def get_booking_summary(
    context: RunContext
) -> Dict:
    """
    Get a summary of all bookings and room status.
    
    Returns:
        Dictionary containing booking summary with total rooms, available rooms, occupied rooms, and occupancy rate.
    """
    logger.info("API: Getting booking summary")
    
    room_types = db.get_all_room_types()
    total_rooms = sum(rt['total_rooms'] for rt in room_types)
    total_available = sum(rt['available_rooms'] for rt in room_types)
    total_occupied = total_rooms - total_available
    
    return {
        "success": True,
        "summary": {
            "total_rooms": total_rooms,
            "available_rooms": total_available,
            "occupied_rooms": total_occupied,
            "occupancy_rate": (total_occupied / total_rooms * 100) if total_rooms > 0 else 0
        },
        "room_types": room_types
    } 