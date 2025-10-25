# Hotel Reservation Voice AI System

A comprehensive hotel room reservation system with LiveKit voice AI integration, featuring real-time voice interaction, database management, and Excel export functionality.

## Features

- **Voice AI Receptionist**: Real-time voice interaction using LiveKit and OpenAI
- **Room Management**: SQLite database with 8 different room types
- **Special Occasion Discounts**: Automatic discount calculation for honeymoon, birthday, anniversary, etc.
- **Excel Export**: Automatic export of booking data for non-technical staff
- **Function Tools**: AI can access database functions using `@function_tool` decorators

## Room Types & Pricing

1. **Normal Room** - $50-$80 per night
2. **Couple Room** - $80-$120 per night  
3. **2 Beds Room** - $100-$150 per night
4. **4 Beds Room** - $150-$200 per night
5. **Queen Size Room** - $120-$180 per night
6. **Honeymoon Suite** - $200-$300 per night (15% discount)
7. **Deluxe Suite** - $250-$400 per night
8. **Luxury Suite** - $350-$600 per night

## Special Occasion Discounts

- Honeymoon: 15% discount
- Birthday: 10% discount
- Anniversary: 12% discount
- Wedding: 20% discount
- Special celebrations: 8% discount

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file with your credentials:

```bash
# OpenAI API Key for LLM, STT, and TTS
OPENAI_API_KEY=your_openai_api_key_here

# LiveKit Cloud credentials
LIVEKIT_API_KEY=your_livekit_api_key_here
LIVEKIT_API_SECRET=your_livekit_api_secret_here
LIVEKIT_URL=wss://your-livekit-url.livekit.cloud
```

### 3. Download Model Files

```bash
python agent.py download-files
```

## Usage

### Console Mode (Local Testing)

```bash
python agent.py console
```

### Development Mode (LiveKit Cloud)

```bash
python agent.py dev
```

### Agent Playground

Use the LiveKit Agents playground to interact with your voice AI agent.

## File Structure

- `agent.py` - Main LiveKit agent with voice AI integration
- `api.py` - Function tools with `@function_tool` decorators for AI access
- `dbdriver.py` - SQLite database management and operations
- `prompts.py` - Conversation prompts and system instructions
- `requirements.txt` - Python dependencies
- `env_example.txt` - Environment variables template

## AI Function Tools

The AI agent has access to the following functions:

- `search_available_rooms()` - Search rooms by type or get all types
- `check_room_availability()` - Check if a room type is available
- `get_room_pricing()` - Get pricing for a specific room type
- `book_room()` - Book a room for a guest
- `get_room_details()` - Get detailed room information
- `suggest_room_for_occasion()` - Suggest rooms based on occasion and budget
- `calculate_discount()` - Calculate discount for special occasions
- `get_booking_summary()` - Get overall booking statistics

## Database Features

- Automatic room initialization with sample data
- Real-time availability tracking
- Booking history with special occasion tracking
- Automatic Excel export after each booking
- Discount calculation and application

## Logging

All operations are logged with timestamps and operation details for debugging and monitoring.

## Next Steps

1. Set up your LiveKit Cloud account
2. Configure your OpenAI API key
3. Update the `.env` file with your credentials
4. Run the agent in development mode
5. Test voice interactions through the LiveKit playground 