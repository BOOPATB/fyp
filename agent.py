
import os
import datetime
from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions, RoomOutputOptions
from livekit.plugins import google, silero, deepgram, elevenlabs 
from livekit.api import AccessToken,VideoGrants,TrackInfo
import asyncio
import pymupdf
from flask import Flask, request, jsonify
from roomCreation import create_room
from flask_cors import CORS
import threading
from api2 import api
from prompts import WELCOME_PROMPT, ROOM_TYPES_INFO, MEETING_PROMPT
from api import (
    search_available_rooms,
    check_room_availability,
    get_room_pricing,
    book_room,
    get_room_details,
    suggest_room_for_occasion,
    calculate_discount,
    get_booking_summary,
    convert_to_pdf,
)
from dbdriver import MeetingDatabase
import logging
import re

# --- Added for LiveKit JWT token ---


app = Flask(__name__)
CORS(app)
logger = logging.getLogger("agent")

load_dotenv(dotenv_path=".env")

meeting_id = "default_meeting"

class HotelReceptionistAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=WELCOME_PROMPT + "\n\n" + ROOM_TYPES_INFO + "\n\n" + MEETING_PROMPT,
            tools=[
                search_available_rooms,
                check_room_availability,
                get_room_pricing,
                book_room,
                get_room_details,
                suggest_room_for_occasion,
                calculate_discount,
                get_booking_summary,
                convert_to_pdf,
            ]
        )
        self.meeting_db = MeetingDatabase()
    _active_tasks = []

    async def async_handle_byte_stream(self, reader, participant_identity):
        try:
            info = reader.info
            file_bytes = bytes()
            with open(info["name"], mode="wb") as f:
                async for chunk in reader:
                    file_bytes += chunk
                f.write(file_bytes)
            api(file=reader.info["name"])
            doc = pymupdf.open(info["name"])
            text_accum = ""
            for page in doc:
                text = page.get_text()
                text_accum += text

            chat_ctx = self.chat_ctx.copy()
            msg_content = [
                "Here is a balance sheet in text format. Please answer questions asked based on the PDF.",
                text_accum
            ]
            chat_ctx.add_message(role="user", content=msg_content)
            await self.update_chat_ctx(chat_ctx)
        except Exception as e:
            logger.error(f"Error handling byte stream: {e}")

    def handle_byte_stream(self, reader, participant_identity):
        task = asyncio.create_task(self.async_handle_byte_stream(reader, participant_identity))
        self._active_tasks.append(task)
        task.add_done_callback(lambda t: self._active_tasks.remove(t))

    async def handle_user_message(self, message: str) -> str:
        text = message.lower().strip()

        if "add" in text and "pdf" in text:
            match = re.search(r"(?:path|file(?:name)?|file):\s*([^\s]+\.pdf)", message, re.IGNORECASE)
            pdf_path = match.group(1) if match else None
            if not pdf_path:
                return "Please specify the PDF file path ('file: yourfile.pdf') to ingest."
            success = self.meeting_db.ingest_pdf_file(pdf_path)
            return f"PDF '{pdf_path}' ingested for retrieval." if success else f"Failed to ingest '{pdf_path}'."

        if "add" in text and "meeting file" in text:
            match_file = re.search(r"filename\s*[:=]\s*(\S+)", message, re.IGNORECASE)
            match_content = re.search(r"content\s*[:=]\s*(.+)", message, re.IGNORECASE | re.DOTALL)
            if not match_file or not match_content:
                return "Please specify your 'filename:...' and 'content:...' to add a meeting file."
            filename = match_file.group(1)
            content = match_content.group(1)
            return self.add_meeting_file(filename, content)

        if re.search(r'\b(search|find|lookup|show)\b.*\b(meeting file|meeting|transcript|notes)\b', text):
            query_match = re.search(r'(?:about|for|on|:)\s*(.*)', text)
            query = query_match.group(1) if query_match else message
            return self.search_meeting_files(query)

        if re.search(r'\b(get|show|retrieve|read)\b.*\b(meeting file|transcript|meeting)\b', text):
            filename_match = re.search(r"filename\s*[:=]\s*(\S+)", message, re.IGNORECASE)
            if not filename_match:
                return "Please specify the filename with 'filename:<filename>'."
            filename = filename_match.group(1)
            return self.retrieve_meeting_file(filename)

        if re.search(r'\b(delete|remove|truncate|clear)\b.*(meeting files|transcripts|meetings|database)\b', text):
            return self.truncate_meeting_files()

        return (
            "I'm here to assist with your meeting files! "
            "Ask me to add, ingest PDF, search, retrieve, or delete meeting files."
        )

    def add_meeting_file(self, filename: str, content: str) -> str:
        success = self.meeting_db.add_file(filename, content)
        return (
            f"Meeting file '{filename}' added successfully."
            if success else f"Failed to add meeting file '{filename}'."
        )

    def search_meeting_files(self, query: str, top_k: int = 5) -> str:
        results = self.meeting_db.vector_search(query, top_k)
        if not results:
            return "No meeting files found matching your query."
        response = "Meeting files matching your query:\n\n"
        for r in results:
            snippet = r["content"][:200].replace('\n', ' ')
            response += f"- {r['filename']} (Similarity: {r['similarity']:.3f}, Date: {r['created_at']})\n  {snippet}\n"
        return response

    def retrieve_meeting_file(self, filename: str) -> str:
        content = self.meeting_db.retrieve_file_content(filename)
        return content if content else f"No meeting file found with filename '{filename}'."

    def truncate_meeting_files(self) -> str:
        self.meeting_db.truncate_files()
        return "All meeting files have been deleted successfully."


# --- SINGLE GLOBAL AGENT INSTANCE ---
agent_instance = HotelReceptionistAgent()

@app.route('/api/agent', methods=['POST'])
def agent_endpoint():
    data = request.json
    user_message = data.get('message', '')
    try:
        # Use asyncio event loop to run the async method in sync Flask context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(agent_instance.handle_user_message(user_message))
        loop.close()
    except Exception as e:
          logger.error(f"Error in agent endpoint: {e}")
          response = "Sorry, there was an internal error with the agent."
    return jsonify({'response': response})


@app.route('/getToken')
def getToken():
  token = AccessToken(os.getenv('LIVEKIT_API_KEY'), os.getenv('LIVEKIT_API_SECRET')) \
    .with_identity("max") \
    .with_name("akash") \
    .with_grants(VideoGrants(
        room_join=True,
        room="myroom",
        can_publish=True,
        can_subscribe=True,
    ))

  return {"token": token.to_jwt()}

class RunAPI(threading.Thread):
    def __init__(self,host='127.0.0.1', port=7000):
        super().__init__()
        self.host=host  
        self.port=port
        
    def run(self):
        from waitress import serve
        serve(app, host=self.host, port=self.port)

async def entrypoint(ctx: agents.JobContext):
    global meeting_id

    RunAPI().start()
    session = AgentSession(
        stt=deepgram.STT(api_key=os.getenv("DEEPGRAM_API_KEY")),
        llm=google.LLM(model="gemini-2.0-flash", api_key=os.getenv("GOOGLE_API_KEY")),
        tts=deepgram.TTS(api_key=os.getenv("DEEPGRAM_API_KEY")),
        vad=silero.VAD.load()
    )

    try:
        with open(f"user_speech_log_{meeting_id}.txt", "x") as file:
            pass
        print(f"File 'user_speech_log_{meeting_id}.txt' created successfully.")
    except FileExistsError:
        print(f"File 'user_speech_log_{meeting_id}.txt' already exists.")

    @session.on("user_input_transcribed")
    def on_transcript(transcript):
        if transcript.is_final:
            logger.info(f"File created for {meeting_id}")
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(f"user_speech_log_{meeting_id}.txt", "a") as f:
                f.write(f"[{timestamp}] {transcript.transcript}\n")

    agent = agent_instance

    await session.start(
        room=ctx.room,
        agent=agent,
        room_input_options=RoomInputOptions(),
        room_output_options=RoomOutputOptions(transcription_enabled=True),
    )

    await ctx.connect(auto_subscribe=True)
    ctx.room.register_byte_stream_handler(
        topic="pdf_upload",
        handler=agent.handle_byte_stream
    )

    await session.generate_reply(
        instructions="""Greet the user warmly as a hotel receptionist and offer to help them with room reservations. 
                        Mention that you can help them find the perfect room, check availability, and provide special discounts."""
    )
    RunAPI().join()
if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))