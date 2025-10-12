import os
import datetime
from dotenv import load_dotenv
from livekit import rtc,agents
from livekit.agents import AgentSession, Agent, RoomInputOptions, RoomOutputOptions
from livekit.plugins import (
    google,silero, noise_cancellation,deepgram,elevenlabs)
    # noise_cancellation,  
import random
import os
import datetime
from google.genai import Client
import logging
import asyncio
from prompts import WELCOME_PROMPT, ROOM_TYPES_INFO, MEETING_PROMPT
import re
import pymupdf
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
    meeting_id, 
    
)
from api2 import api

from dbdriver import MeetingDatabase


logger=logging.getLogger("agent")

load_dotenv(dotenv_path="env_example.env")


class HotelReceptionistAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=WELCOME_PROMPT + "\n\n" + ROOM_TYPES_INFO+ "\n\n" + MEETING_PROMPT,
            tools=[
                search_available_rooms,
                check_room_availability,
                get_room_pricing,
                book_room,
                get_room_details,
                suggest_room_for_occasion, 
                calculate_discount,
                get_booking_summary,
                convert_to_pdf
            ]
        )
        self.meeting_db = MeetingDatabase()
    _active_tasks = []



    async def async_handle_byte_stream(self, reader, participant_identity,):
        info = reader.info
        file_bytes=bytes()
        
        
          # Read the stream to a file
        with open(reader.info["name"], mode="wb") as f:
           async for chunk in reader:
               file_bytes += chunk
               
           f.write(file_bytes)
           f.close()
        api(file=reader.info["name"])
        doc = pymupdf.open("C:/Users/Dell/Downloads/Balance-Sheet-Example.pdf") # open a document
        text1= ""
        for page in doc: # iterate the document pages
         text = page.get_text() # get plain text encoded
         text1=text1.join(text)
        chat_ctx = self.chat_ctx.copy()
        chat_ctx.add_message(role="user",content=["here is an balance sheet in an text format . Please answer questions asked by the user based on the information in the pdf.",text1])
        await self.update_chat_ctx(chat_ctx)
        

    def handle_byte_stream(self, reader, participant_identity):
        global _active_tasks
        task = asyncio.create_task(self.async_handle_byte_stream(reader, participant_identity))
        _active_tasks.append(task)
        task.add_done_callback(lambda t: _active_tasks.remove(t))
 
    

    # RAG-aware conversational handler
    async def handle_user_message(self, message: str) -> str:
        text = message.lower().strip()

        # Add PDF as meeting file
        if re.search(r'\b(add|ingest)\b.*\b(pdf)\b', text):
            match = re.search(r"(?:path|file(?:name)?|file):\s*([^\s]+\.pdf)", message, re.IGNORECASE)
            pdf_path = match.group(1) if match else None
            if not pdf_path:
                return "Please specify the PDF file path ('file: yourfile.pdf') to ingest."
            success = self.meeting_db.ingest_pdf_file(pdf_path)
            return f"PDF '{pdf_path}' ingested for retrieval." if success else f"Failed to ingest '{pdf_path}'. Make sure the file exists."

        # Add plain text meeting file
        if re.search(r'\badd\b.*\bmeeting file\b', text):
            match_file = re.search(r"filename\s*[:=]\s*(\S+)", message, re.IGNORECASE)
            match_content = re.search(r"content\s*[:=]\s*(.+)", message, re.IGNORECASE | re.DOTALL)
            if not match_file or not match_content:
                return ("Please specify your 'filename:...' and 'content:...' to add a meeting file.")
            filename = match_file.group(1)
            content = match_content.group(1)
            return self.add_meeting_file(filename, content)

        # Semantic search in meeting files
        if re.search(r'\b(search|find|lookup|show)\b.*\b(meeting file|meeting|transcript|notes)\b', text):
            query_match = re.search(r'(?:about|for|on|:)\s*(.*)', text)
            query = query_match.group(1) if query_match else message
            return self.search_meeting_files(query)

        # Retrieve content of a specific meeting file
        if re.search(r'\b(get|show|retrieve|read)\b.*\b(meeting file|transcript|meeting)\b', text):
            filename_match = re.search(r"filename\s*[:=]\s*(\S+)", message, re.IGNORECASE)
            if not filename_match:
                return "Please specify the filename with 'filename:<filename>'."
            filename = filename_match.group(1)
            return self.retrieve_meeting_file(filename)

        # Delete all meeting files
        if re.search(r'\b(delete|remove|truncate|clear)\b.*(meeting files|transcripts|meetings|database)\b', text):
            return self.truncate_meeting_files()

        # Otherwise, fallback message
        return (
            "I'm here to help you with your meeting files! "
            "You can ask me to add, ingest PDF, search, retrieve, or delete meeting files. "
            "For example: 'Add meeting file filename:notes.txt content:...'"
        )

    def add_meeting_file(self, filename: str, content: str) -> str:
        success = self.meeting_db.add_file(filename, content)
        if success:
            return f"Meeting file '{filename}' added successfully."
        else:
            return f"Failed to add meeting file '{filename}' (maybe already exists)."

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
        if content:
            return content
        else:
            return f"No meeting file found with filename '{filename}'."

    def truncate_meeting_files(self) -> str:
        self.meeting_db.truncate_files()
        return "All meeting files have been deleted successfully."
    
    


  


async def entrypoint(ctx: agents.JobContext):
    global meeting_id
    session = AgentSession(
        stt=deepgram.STT(
            api_key=os.getenv("DEEPGRAM_API_KEY"),
            
        ),
        llm= google.LLM(
            model="gemini-2.0-flash",
            api_key=os.getenv("GOOGLE_API_KEY")
        ),
        tts=deepgram.TTS(
            api_key=os.getenv("DEEPGRAM_API_KEY"),
        ),

        vad=silero.VAD.load()
    )
    
    # creating an empty file for the meeting log
    try:
        with open(f"user_speech_log_{meeting_id}.txt", "x") as file:
            pass  # No content is written, creating an empty file
        print(f"File 'user_speech_log_{meeting_id} .txt' created successfully.")
    except FileExistsError:
     print("File 'my_new_file.txt' already exists.")  # Create or clear the log file
    
  
    @session.on("user_input_transcribed")
    def on_transcript(transcript):
        if transcript.is_final:
            logger.info(f"File created for {meeting_id}")
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(f"user_speech_log_{meeting_id}.txt", "a") as f:
                f.write(f"[{timestamp}] {transcript.transcript}\n")
            # rag_response =  HotelReceptionistAgent.handle_user_message(message=transcript)
            # session.send_message(rag_response)


    await session.start(
        room=ctx.room,
        agent=HotelReceptionistAgent(),
        room_input_options=RoomInputOptions(
            # noise_cancellation=noise_cancellation.BVC(),
        ),
        room_output_options=RoomOutputOptions(
            
            transcription_enabled=True
        )
    )
    
    await ctx.connect(auto_subscribe=True)
    ctx.room.register_byte_stream_handler(topic="pdf_upload", handler=HotelReceptionistAgent().handle_byte_stream)
    await session.generate_reply(
        instructions='''Greet the user warmly as a hotel receptionist and offer to help them with room reservations. 
                     Mention that you can help them find the perfect room, check availability, and provide special discounts for special occasions.
                   '''
    )

def test_add_meeting_file():
    """
    Simple helper function to test adding a file to MeetingDatabase from main.py.
    """
    agent = HotelReceptionistAgent()


    test_filename = "example_meeting.txt"
    test_content = "This is a test meeting transcript about hotel management and AI assistant development."

    print("Adding meeting file...")
    result = agent.add_meeting_file(test_filename, test_content)
    print(result)

    print("\nRetrieving the same file content...")
    retrieved_content = agent.retrieve_meeting_file(test_filename)
    print(retrieved_content if retrieved_content else "(File content not found)")

def ingest_pdf_cli(agent: HotelReceptionistAgent, pdf_path: str):
    print(f"Ingesting PDF: {pdf_path}")
    result = agent.meeting_db.ingest_pdf_file(pdf_path)
    print(
        f"PDF '{pdf_path}' ingested for retrieval." if result
        else f"Failed to ingest '{pdf_path}'. Make sure the file exists."
    )            
#as the cli thingy isnt needed now for manual testing
# if __name__ == "__main__":
#     import sys
#     agent = HotelReceptionistAgent()
#     if len(sys.argv) > 2 and sys.argv[1] == "ingest_pdf":
#         path = sys.argv[2]
#         ingest_pdf_cli(agent, path)
#     elif len(sys.argv) > 1 and sys.argv[1] == "test":
#         test_add_meeting_file()
#     else:
#         agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))

