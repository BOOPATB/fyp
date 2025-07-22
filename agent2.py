import os

os.environ["LIVEKIT_API_HOST"] = "https://meeting-summarizer-eqgbe5iq.livekit.cloud"

os.environ["LIVEKIT_HOST"] = "wss://meeting-summarizer-eqgbe5iq.livekit.cloud"
os.environ["LIVEKIT_API_KEY"] = "APINtxAW9TyWRyn"
os.environ["LIVEKIT_API_SECRET"] = "yn7iXyjuFc4MeJgBUlHdyrtAKoSsLkIwjxuCxQWzxae"
os.environ["GEMINI_API_KEY"] = "AIzaSyBPzDfG9raYthzW616e0iTmWDzBklSimeY"
os.environ["DEEPGRAM_API_KEY"] = "0e6a958d84d35dd479ab3395223b260f0fb39412"

print("LIVEKIT_HOST is:", os.environ["LIVEKIT_HOST"])
print("LIVEKIT_API_HOST is:", os.environ["LIVEKIT_API_HOST"])


from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import deepgram
import google.generativeai as genai
import asyncio


genai.configure(api_key=os.environ["GEMINI_API_KEY"])


class MeetingSummarizerAgent(Agent):
    def __init__(self):
        super().__init__(instructions=(
            "You are a meeting assistant. Listen, transcribe with speaker labels, and summarize the meeting at the end."
        ))
        self.transcripts = []

    async def on_transcription(self, segment, participant):
        self.transcripts.append({
            "speaker": participant.identity if participant else "unknown",
            "text": segment.text,
        })

    async def on_end(self):
        meeting_transcript = "\n".join(
            f"{t['speaker']}: {t['text']}" for t in self.transcripts
        )
        summary_prompt = (
            "Summarize the following meeting transcript, focusing on key decisions, action items, and important discussions:\n\n"
            + meeting_transcript
        )
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(summary_prompt)
        summary = response.text if hasattr(response, "text") else str(response)
        print("==== MEETING SUMMARY ====")
        print(summary)
        print("=========================")


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        stt=deepgram.STT(
            api_key=os.environ["DEEPGRAM_API_KEY"],
            diarization=True  
        ),
    )
    agent = MeetingSummarizerAgent()

    await session.start(
        room=ctx.room,
        agent=agent,
        room_input_options=RoomInputOptions(
            # noise_cancellation=noise_cancellation.BVC(),
        ),
    )
    await ctx.connect()
    await session.generate_reply(
        instructions="Hello! I am your AI meeting assistant. I'll transcribe what everyone says and provide a meeting summary at the end."
    )

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
