import os
import uuid
import asyncio
from dotenv import load_dotenv
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

if not ELEVENLABS_API_KEY:
    raise ValueError("ELEVENLABS_API_KEY environment variable not set")

client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
)

async def generate_audio(text: str, outputFilename: str):
    """
    Converts text to speech using ElevenLabs API and saves the output as an MP3 file.

    Args:
        text (str): The text to convert to speech.
        outputFilename (str): The path to save the audio file.
    """
    response = await client.text_to_speech.convert(
        voice_id="pNInz6obpgDQGcFmaJgB",  # Adam pre-made voice
        optimize_streaming_latency=0,
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2",  # use the turbo model for low latency
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

    with open(outputFilename, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"A new audio file was saved successfully at {outputFilename}")

if __name__ == "__main__":
    asyncio.run(generate_audio("Hello, world! This is a test of the ElevenLabs API.", "elevenlabs_test.mp3"))
