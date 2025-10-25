import os
import asyncio
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import datetime
import re

# Correct LiveKit imports
try:
    from livekit import api
    AccessToken = api.AccessToken
    VideoGrants = api.VideoGrants
except ImportError:
    AccessToken = None
    VideoGrants = None

import jwt

# Import your agent class
from agent import HotelReceptionistAgent

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
logger = logging.getLogger("flask_server")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv(dotenv_path=".env")

# Create single global agent instance
print("Initializing HotelReceptionistAgent...")
try:
    agent_instance = HotelReceptionistAgent()
    print(" Agent initialized successfully!")
except Exception as e:
    print(f" Failed to initialize agent: {e}")
    agent_instance = None

@app.route('/api/agent', methods=['POST'])
def agent_endpoint():
    """Chat endpoint for AI agent"""
    if agent_instance is None:
        return jsonify({'response': 'Agent initialization failed. Please check server logs.'}), 500
    
    data = request.json
    user_message = data.get('message', '')
    logger.info(f"📨 Received message: {user_message}")
    
    try:
        # Use asyncio event loop to run async method
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(agent_instance.handle_user_message(user_message))
        loop.close()
        logger.info(f" Agent response: {response[:100]}...")
        return jsonify({'response': response})
    except Exception as e:
        logger.error(f" Error in agent endpoint: {e}", exc_info=True)
        response = f"Sorry, there was an error processing your message: {str(e)}"
        return jsonify({'response': response}), 500

@app.route('/api/livekit-token', methods=['POST'])
def generate_livekit_token():
    """Generate LiveKit token for video/audio"""
    data = request.json
    identity = data.get("identity", "anonymous")
    room = data.get("room", "default-room")

    api_key = os.environ.get('LIVEKIT_API_KEY')
    api_secret = os.environ.get('LIVEKIT_API_SECRET')
    
    if not api_key or not api_secret:
        logger.error(" LiveKit credentials not found in environment")
        return jsonify({"error": "LiveKit credentials not configured"}), 500

    token = None

    try:
        if AccessToken is not None:
            # Use LiveKit API properly
            token_obj = AccessToken(api_key, api_secret)
            token_obj = token_obj.with_identity(identity).with_name(identity)
            token_obj = token_obj.with_grants(VideoGrants(
                room_join=True,
                room=room,
            ))
            token = token_obj.to_jwt()
        else:
            # Fallback: Manual JWT creation
            payload = {
                "iss": api_key,
                "sub": identity,
                "room": room,
                "exp": int((datetime.datetime.utcnow() + datetime.timedelta(hours=1)).timestamp()),
                "video": {"roomJoin": True, "room": room}
            }
            token = jwt.encode(payload, api_secret, algorithm='HS256')
        
        logger.info(f"🎫 Generated token for identity: {identity}, room: {room}")
        return jsonify({"token": token})
    except Exception as e:
        logger.error(f" Error generating token: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    agent_status = "initialized" if agent_instance else "not initialized"
    return jsonify({
        "status": "ok",
        "message": "Flask server is running",
        "agent_status": agent_status,
        "port": 5000
    })

@app.route('/test', methods=['GET'])
def test_endpoint():
    """Simple test endpoint"""
    return jsonify({
        "message": "Backend is working!",
        "endpoints": {
            "health": "GET /health",
            "test": "GET /test",
            "agent": "POST /api/agent",
            "livekit_token": "POST /api/livekit-token"
        }
    })

if __name__ == "__main__":
    print("=" * 70)
    print(" Starting Flask API Server")
    print("=" * 70)
    print(f" Server URL: http://localhost:5000")
    print(f" Network URL: http://0.0.0.0:5000")
    print("=" * 70)
    print(" Available endpoints:")
    print("   GET  /health             - Health check")
    print("   GET  /test               - Test endpoint")
    print("   POST /api/agent          - Chat with AI agent")
    print("   POST /api/livekit-token  - Get LiveKit token")
    print("=" * 70)
    print(" :")
    print("   - Frontend should connect to: http://localhost:5000")
    print("   - Test health: curl http://localhost:5000/health")
    print("   - Press Ctrl+C to stop the server")
    print("=" * 70)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
