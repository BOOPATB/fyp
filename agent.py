from dotenv import load_dotenv
from livekit import agents
from livekit.agents import (AgentSession, Agent, RoomInputOptions,RoomOutputOptions,function_tool,)
from livekit import rtc
from livekit.plugins.google import (
   LLM
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

load_dotenv("env_example.env")


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

    



async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
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
            # LiveKit Cloud enhanced noise cancellation
            # - If self-hosting, omit this parameter
            # - For telephony applications, use `BVCTelephony` for best results
            noise_cancellation=noise_cancellation.BVC(),
        ),
        room_output_options=RoomOutputOptions(
            # LiveKit Cloud enhanced noise cancellation
            # - If self-hosting, omit this parameter
            # - For telephony applications, use `BVCTelephony` for best results
            transcription_enabled=True
        )
    )
   
          
    await ctx.connect(auto_subscribe=True)

    await session.generate_reply(
        instructions="Greet the user warmly as a hotel receptionist and offer to help them with room reservations. Mention that you can help them find the perfect room, check availability, and provide special discounts for special occasions."
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint)) 