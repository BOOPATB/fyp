import os
import datetime
from dotenv import load_dotenv
from livekit import agents
<<<<<<< HEAD
from livekit.agents import AgentSession, Agent, RoomInputOptions, RoomOutputOptions
from livekit.plugins import (
    gemini,
    # noise_cancellation,  
=======
from livekit.agents import (AgentSession, Agent, RoomInputOptions,RoomOutputOptions,function_tool,)
from livekit import rtc
from livekit.plugins.google import (
   LLM
>>>>>>> 924c612ee04151481c1dbd33d4e748d1660e0ce4
)
from livekit.plugins import noise_cancellation,deepgram,cartesia
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
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
from dbdriver import MeetingDatabase

<<<<<<< HEAD

load_dotenv(env_path="CoreLance/.env")
=======
load_dotenv("env_example.env")
>>>>>>> 924c612ee04151481c1dbd33d4e748d1660e0ce4


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
<<<<<<< HEAD
        llm=gemini.LLM(
              model="gemini-2.5-flash-preview-04-17",
            api_key=GEMINI_API_KEY,
        )
        # Add STT/TTS and noise_cancellation here if you want
=======
        stt=deepgram.STT(
            api_key="afbc8893b9e4f291f1f2a24b4aef77524e35047e",
            
        ),
        llm= LLM(
            model="gemini-2.5-flash-preview-04-17",
            api_key="AIzaSyBaSOX01gr8YMGIR_6UCtnPH1tCXAqYxfo"
        ),
        tts=cartesia.TTS(
            api_key="sk_car_2Gq9PKQuwL7smGS8ZFfi9V",
            voice="en-US-Wavenet-D"
        ),
>>>>>>> 924c612ee04151481c1dbd33d4e748d1660e0ce4
    )

    @session.on("user_input_transcribed")
    def on_transcript(transcript):
        if transcript.is_final:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("user_speech_log.txt", "a") as f:
                f.write(f"[{timestamp}] {transcript.transcript}\n") 
    await session.start(
        room=ctx.room,
        agent=HotelReceptionistAgent(),
        room_input_options=RoomInputOptions(
            # noise_cancellation=noise_cancellation.BVC(),
        ),
        room_output_options=RoomOutputOptions(
<<<<<<< HEAD
=======
            # LiveKit Cloud enhanced noise cancellation
            # - If self-hosting, omit this parameter
            # - For telephony applications, use `BVCTelephony` for best results
>>>>>>> 924c612ee04151481c1dbd33d4e748d1660e0ce4
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
