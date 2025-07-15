from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    noise_cancellation,
)
from livekit.plugins import google
from promts import AGENT_INSTRUCTION, SESSION_INSTRUCTION
from tools import (
    open_website,
    get_weather,
    open_default_browser,
    play_music,
    play_youtube_music,
    search_web,
    open_file_explorer,
)

load_dotenv()


class Assistant(Agent):
    def __init__(self, tools=None) -> None:
        super().__init__(
            instructions=AGENT_INSTRUCTION,
            llm=google.beta.realtime.RealtimeModel(
                voice="charon"),
            tools=tools or [],
        )


async def entrypoint(ctx: agents.JobContext):
    tools = [
        open_default_browser,
        get_weather,
        open_website,
        play_music,
        play_youtube_music,
        search_web,
        open_file_explorer,
    ]
    assistant = Assistant(tools=tools)

    session = AgentSession()

    await session.start(
        room=ctx.room,
        agent=assistant,
        room_input_options=RoomInputOptions(
            video_enabled=True,
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await ctx.connect()

    await session.generate_reply(
        instructions=SESSION_INSTRUCTION
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
