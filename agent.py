import os
import datetime
from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions, RoomOutputOptions
from livekit.plugins import (
    google,silero, noise_cancellation,deepgram,elevenlabs)
    # noise_cancellation,  
import random
import os
import datetime

import asyncio
from prompts import WELCOME_PROMPT, ROOM_TYPES_INFO
from api import (
    search_available_rooms,
    check_room_availability,
    get_room_pricing,
    book_room,
    get_room_details,
    suggest_room_for_occasion,
    calculate_discount,
    get_booking_summary
)

from dbdriver import MeetingDatabase



load_dotenv(dotenv_path="env_example.env")



class HotelReceptionistAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=WELCOME_PROMPT + "\n\n" + ROOM_TYPES_INFO,
            tools=[
                search_available_rooms,
                check_room_availability,
                get_room_pricing,
                book_room,
                get_room_details,
                suggest_room_for_occasion, 
                calculate_discount,
                get_booking_summary,
            ]
        )
        self.meeting_db = MeetingDatabase()

    # ------ MEETING DATABASE METHODS ------

    def add_meeting_file(self, filename: str, content: str) -> str:
        """Add a new meeting file to the meeting database."""
        success = self.meeting_db.add_file(filename, content)
        if success:
            return f"Meeting file '{filename}' added successfully."
        else:
            return f"Failed to add meeting file '{filename}' (maybe already exists)."

    def search_meeting_files(self, query: str, top_k: int = 5) -> str:
        """Semantic vector search in meeting files."""
        results = self.meeting_db.vector_search(query, top_k)
        if not results:
            return "No meeting files found matching your query."
        response = "Meeting files matching your query:\n\n"
        for r in results:
            snippet = r["content"][:200].replace('\n', ' ')
            response += f"- {r['filename']} (Similarity: {r['similarity']:.3f}, Date: {r['created_at']})\n  {snippet}\n"
        return response

    def retrieve_meeting_file(self, filename: str) -> str:
        """Retrieve the full content of a meeting file."""
        content = self.meeting_db.retrieve_file_content(filename)
        if content:
            return content
        else:
            return f"No meeting file found with filename '{filename}'."

    def truncate_meeting_files(self) -> str:
        """Delete all meeting files (admin/debug use)."""
        self.meeting_db.truncate_files()
        return "All meeting files have been deleted successfully."


    



async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        stt=deepgram.STT(
            api_key=os.getenv("DEEPGRAM_API_KEY"),
            
        ),
        llm= google.LLM(
            model="gemini-2.5-flash",
            api_key=os.getenv("GOOGLE_API_KEY")
        ),
        tts=elevenlabs.TTS(
            api_key=os.getenv("ELEVENLABS_API_KEY"),
           voice_id="ODq5zmih8GrVes37Dizd",
          model="eleven_multilingual_v2"
   ),
        
        vad =silero.VAD.load()
    )
    meeting_id = random.randint(100, 999)
    @session.on("user_input_transcribed")
    def on_transcript(transcript):
        if transcript.is_final:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(f"user_speech_log_{meeting_id}.txt", "a") as f:
                f.write(f"[{timestamp}] {transcript.transcript}\n")
    with open(f"user_speech_log_{meeting_id}.txt", "r") as f:
       content=f.readlines()
       session.agent.add_meeting_file(f"user_speech_log_{meeting_id}.txt", "".join(content))

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

    await session.generate_reply(
        instructions="Greet the user warmly as a hotel receptionist and offer to help them with room reservations. "
                     "Mention that you can help them find the perfect room, check availability, and provide special discounts for special occasions."
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


if __name__ == "__main__":
    import sys

   
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_add_meeting_file()
    else:
        agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
