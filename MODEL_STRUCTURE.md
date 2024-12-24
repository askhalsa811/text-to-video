# Application Model Structure

This document provides a detailed structure of the video generation application, outlining each file's purpose, key functions, inputs, outputs, and interactions.

## Core Files

### app.py

*   **Purpose:** Main entry point and orchestrator of the video generation process.
*   **Description:** This script takes a topic as input and coordinates the execution of other modules to generate a video.
*   **Inputs:**
    *   Command-line argument: The topic for the video (string).
*   **Outputs:**
    *   A rendered video file named `rendered_video.mp4`.
    *   Prints intermediate results (script, captions, search terms, video URLs) to the console.
*   **Key Functions:**
    *   `if __name__ == "__main__":`
        *   **Inputs:** Command-line arguments.
        *   **Outputs:** Calls various functions in other modules.
        *   Parses command-line arguments (specifically the video topic).
        *   Calls `generate_script` from `utility.script.script_generator.py`.
        *   Calls `asyncio.run(generate_audio(...))` from `utility.audio.audio_generator.py`.
        *   Calls `generate_timed_captions` from `utility.captions.timed_captions_generator.py`.
        *   Calls `getVideoSearchQueriesTimed` from `utility.video.video_search_query_generator.py`.
        *   Calls `generate_video_url` from `utility.video.background_video_generator.py`.
        *   Calls `merge_empty_intervals` from `utility.video.video_search_query_generator.py`.
        *   Calls `get_output_media` from `utility.render.render_engine.py`.

## Utility Modules

### utility/script/script_generator.py

*   **Purpose:** Generates the script for the video based on the input topic using an AI model.
*   **Description:** This module uses either the **OpenAI API** or **Groq API** to generate a concise and engaging script suitable for short-form video content.
*   **Inputs:**
    *   Video topic (string).
*   **Outputs:**
    *   Generated script (string).
*   **Key Functions:**
    *   `generate_script(topic)`:
        *   **Inputs:** Video topic (string).
        *   **Outputs:** Generated script (string).
        *   Utilizes a prompt to instruct the AI model (either OpenAI's GPT-4o or Groq's Mixtral-8x7b-32768/llama3-70b-8192) to generate a script in JSON format.
        *   Returns the generated script extracted from the JSON response.

### utility/audio/audio_generator.py

*   **Purpose:** Converts the generated script into an audio file using a text-to-speech service.
*   **Description:** This module uses the **ElevenLabs API** to synthesize speech from the provided text.
*   **Inputs:**
    *   Script text (string).
    *   Output filename (string).
*   **Outputs:**
    *   Generated audio file (e.g., `audio_tts.mp3`).
*   **Key Functions:**
    *   `generate_audio(text, outputFilename)`:
        *   **Inputs:** Script text (string), output filename (string).
        *   **Outputs:** Saves the generated audio to the specified file.
        *   Uses the ElevenLabs API to generate audio.
        *   Saves the generated audio to the specified file as an MP3.

### utility/captions/timed_captions_generator.py

*   **Purpose:** Generates timed captions for the audio, providing subtitles with precise start and end times.
*   **Description:** This module uses the **whisper\_timestamped library** to perform speech-to-text transcription and obtain word-level timestamps.
*   **Inputs:**
    *   Audio filename (string).
    *   Optional: Whisper model size (string, default: "base").
*   **Outputs:**
    *   A list of timed captions, where each caption is a tuple containing the time interval and the caption text.
*   **Key Functions:**
    *   `generate_timed_captions(audio_filename, model_size="base")`:
        *   **Inputs:** Audio filename (string), optional model size (string).
        *   **Outputs:** A list of timed captions.
        *   Loads the specified Whisper model.
        *   Transcribes the audio file to obtain word-level timestamps.
        *   Calls `getCaptionsWithTime` to format the captions.
        *   Returns a list of timed captions.
    *   `getCaptionsWithTime(whisper_analysis, maxCaptionSize=15, considerPunctuation=False)`:
        *   **Inputs:** Whisper analysis output (dict), optional max caption size (int), optional consider punctuation (bool).
        *   **Outputs:** A list of timed captions.
        *   Groups words into captions and assigns start and end times.
        *   Splits long sentences into multiple captions based on `maxCaptionSize`.

### utility/video/background_video_generator.py

*   **Purpose:** Retrieves relevant background videos from **Pexels API** based on generated search queries.
*   **Description:** This module interacts with the Pexels API to find visually appropriate background footage.
*   **Inputs:**
    *   Timed video search queries (list of lists).
    *   Video server name (string, e.g., "pexel").
*   **Outputs:**
    *   A list of timed video URLs.
*   **Key Functions:**
    *   `search_videos(query_string, orientation_landscape=True)`:
        *   **Inputs:** Search query string (string), optional orientation (bool).
        *   **Outputs:** JSON response from the Pexels API.
        *   Uses the Pexels API to search for videos matching the query.
        *   Returns the JSON response from the Pexels API.
    *   `getBestVideo(query_string, orientation_landscape=True, used_vids=[])`:
        *   **Inputs:** Search query (string), orientation (bool), list of used video links (list).
        *   **Outputs:** URL of the best matching video (string) or None.
        *   Filters the search results to find videos with a 16:9 aspect ratio and a duration close to 15 seconds.
        *   Avoids using the same video multiple times.
        *   Returns the URL of the best matching video.
    *   `generate_video_url(timed_video_searches, video_server)`:
        *   **Inputs:** List of timed search queries (list), video server name (string).
        *   **Outputs:** A list of timed video URLs (list).
        *   Iterates through the search queries and calls `getBestVideo` to find a suitable video for each segment.
        *   Returns a list of timed video URLs.

### utility/render/render_engine.py

*   **Purpose:** Combines the generated audio, captions, and background videos into the final rendered video.
*   **Description:** This module uses the **moviepy library** for video editing and composition and the **requests library** for downloading video files.
*   **Inputs:**
    *   Path to the audio file (string).
    *   Timed captions (list of lists).
    *   Background video data (list of lists containing time intervals and video URLs).
    *   Video server name (string).
*   **Outputs:**
    *   A rendered video file named `rendered_video.mp4`.
*   **Key Functions:**
    *   `download_file(url, filename)`:
        *   **Inputs:** Video URL (string), local filename (string).
        *   **Outputs:** Downloads the video file to the specified filename.
        *   Downloads a file from a given URL using the `requests` library.
    *   `search_program(program_name)`:
        *   **Inputs:** Program name (string).
        *   **Outputs:** Path to the program (string) or None.
        *   Searches for the path of a given program using `where` (Windows) or `which` (Linux/macOS).
    *   `get_program_path(program_name)`:
        *   **Inputs:** Program name (string).
        *   **Outputs:** Path to the program (string) or None.
        *   Gets the path of a given program.
    *   `get_output_media(audio_file_path, timed_captions, background_video_data, video_server)`:
        *   **Inputs:** Audio file path (string), timed captions (list), background video data (list), video server name (string).
        *   **Outputs:** Writes the final video to `rendered_video.mp4`.
        *   Downloads background videos.
        *   Creates `VideoFileClip` objects for background videos and sets their start and end times using `moviepy`.
        *   Creates `TextClip` objects for captions and sets their timing and appearance using `moviepy`.
        *   Combines video and text clips using `moviepy.CompositeVideoClip`.
        *   Adds audio using `moviepy.AudioFileClip` and `moviepy.CompositeAudioClip`.
        *   Writes the final video to `rendered_video.mp4`.

### utility/video/video_search_query_generator.py

*   **Purpose:** Generates search queries for background videos based on the video script and timed captions using an AI model.
*   **Description:** This module uses either the **OpenAI API** or **Groq API** to extract relevant keywords for searching background footage.
*   **Inputs:**
    *   Video script (string).
    *   Timed captions (list of lists).
*   **Outputs:**
    *   A list of timed search queries (list of lists).
*   **Key Functions:**
    *   `getVideoSearchQueriesTimed(script, captions_timed)`:
        *   **Inputs:** Video script (string), timed captions (list).
        *   **Outputs:** A list of timed search queries (list).
        *   Utilizes a prompt to instruct the AI model (either OpenAI's GPT-4o or Groq's Llama3-70b-8192) to generate relevant search queries for each time segment.
        *   Returns a list of timed search queries.
    *   `call_OpenAI(script, captions_timed)`:
        *   **Inputs:** Video script (string), timed captions (list).
        *   **Outputs:** Raw text response from the OpenAI or Groq API.
        *   Makes the API call to OpenAI or Groq to generate the search queries.
    *   `merge_empty_intervals(segments)`:
        *   **Inputs:** A list of timed video segments with potential None URLs (list).
        *   **Outputs:** A list of timed video segments with merged intervals (list).
        *   Merges consecutive time intervals where no search terms were generated, attempting to fill gaps with the previous valid video segment.

This structure provides a comprehensive overview of the application's components and their functionalities, including inputs, outputs, and the libraries/APIs used.