import logging
from typing import List, Dict, Optional, Tuple
from dbdriver import HotelDatabase
from datetime import datetime, timedelta
from livekit.agents import function_tool, RunContext
import os 
from fpdf import FPDF
import random
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
meeting_id = random.randint(100, 999)
# Initialize database
db = HotelDatabase()
def  ingest_text(pdf_path: str) -> None:
    from agent import ingest_pdf_cli 
    ingest_pdf_cli(pdf_path)
@function_tool
async def convert_to_pdf() :
 """Convert a text file to PDF."""
 pdf = FPDF()
 
 pdf.add_page()
 
 pdf.set_font("Arial", size=12)
 logger.info(f"Converting user_speech_log_{meeting_id}.txt to PDF")
 if os.path.exists(f"user_speech_log_{meeting_id}.txt"):
  try:
      
      with open(f"user_speech_log_{meeting_id}.txt", "r") as f:
          
          for line in f:
              
              pdf.multi_cell(0, 10, txt=line, align='L')
  
  
      pdf.output(f"user_speech_log_{meeting_id}.pdf")
      ingest_text(os.path.abspath(f"user_speech_log_{meeting_id}.pdf"))
      logger.info("Successfully converted TXT to PDF.")
 
  except FileNotFoundError:
      print("Error: The file my_file.txt was not found.")
  except Exception as e:
     print(f"An error occurred: {e}")
  
 
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