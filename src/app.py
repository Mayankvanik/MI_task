import gradio as gr
import os
import shutil
from moviepy.editor import *
from transformers import pipeline
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from db import video_history
import subprocess


cmd = "ollama"
LLM = ChatGroq(
    groq_api_key="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",
    model="llama3-70b-8192"
)

prompt = PromptTemplate(
    template="""system
    You are a Categorizer By Tag Agent. You are a master at understanding the meaning of context.

    user
    Conduct a comprehensive analysis of the context and categorize it by tag using the following categories:
        Science - used when the context is about scientific knowledge, research, or summaries of scientific discoveries.
        Artificial Intelligence - used when the context involves AI technologies, machine learning, neural networks, or related advancements.
        Mathematics - used when the context pertains to mathematical theories, problems, solutions, or research.
        Nature - used when the context is about natural phenomena, wildlife, ecosystems, or environmental studies.
        Entertainment - used when the context involves movies, music, games, sports, or other forms of entertainment.
    Output a single category only from the types listed above.
    
    Example: AI is new future of world and revolution.
    Artificial Intelligence

    User context:\n\n{initial_msg}\n\n

    assistant
    """,
    input_variables=["initial_msg"],
)
category_generator = prompt | LLM | StrOutputParser()

pipe = pipeline("automatic-speech-recognition", model="openai/whisper-tiny")

UPLOAD_DIR = "./src/uploaded_videos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

import cv2

def capture_screenshot(video_path, output_image_path):
    # Open the video file
    video_capture = cv2.VideoCapture(video_path)

    # Check if video opened successfully
    if not video_capture.isOpened():
        print("Error: Could not open video.")
        return

    # Get the frames per second (fps) of the video
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        print("Error: Could not get the FPS of the video.")
        return

    # Calculate the frame number at 5 seconds
    frame_number = int(fps * 10)

    # Set the frame position to the frame number
    video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    # Read the frame at the specified position
    success, frame = video_capture.read()
    if not success:
        print("Error: Could not read the frame.")
        return

    # Save the frame as a JPEG image
    cv2.imwrite(output_image_path, frame)

    # Release the video capture object
    video_capture.release()

    print(f"Screenshot saved as {output_image_path}")

def create_dict_and_format(text_summery, output, video_visual):
    # Create the dictionary
    data = {
        "text_summery": text_summery,
        "output": output,
        "video_visual": video_visual
    }

    # Format the dictionary into a string with each key-value pair on a new line
    formatted_string = '\n\n'.join([f"{key}: {value}" for key, value in data.items()])
    return formatted_string

# Function to handle video uploads
def handle_videos(video_path):
    # Extract the filename from the video path
    filename = os.path.basename(video_path)
    target_path = os.path.join(UPLOAD_DIR, filename)
    
    # Copy the uploaded file to the target path
    shutil.copy(video_path, target_path)

    # Load the video file
    video = VideoFileClip(f"D:/ai_work/mindinv/src/uploaded_videos/{filename}")

    
    filename_new = os.path.splitext(filename)[0]
    audio = video.audio
    # Save the audio to a separate file
    audio.write_audiofile(f"D:/ai_work/mindinv/src/audio_files/{filename_new}.wav")
    
    text = pipe(f'D:/ai_work/mindinv/src/audio_files/{filename_new}.wav')
    #Return a success message

    text_summery = text['text']
    output =category_generator.invoke({"initial_msg": text['text']})

    # Usage example
    video_path = f"D:/ai_work/mindinv/src/uploaded_videos/{filename}"
    output_image_path = f"D:/ai_work/mindinv/src/image_files/{filename_new}.jpg"
    capture_screenshot(video_path, output_image_path)

    cmd = "ollama"
    args = ["run", "llava","what is in the image in 20 words?", "D:/ai_work/mindinv/src/image_files/screenshot.jpg"]
    message = subprocess.check_output([cmd] + args).decode('utf-8').splitlines()
    print('>>',message[1:2],'<<<')
    video_visual = message[1:2]
    video_visual = video_visual[0].strip()
    #video_visual ='jdfjidfnidjnfdjis'

    video_history(output,text_summery,video_visual,output_image_path,filename)

    return create_dict_and_format(text_summery, output, video_visual)#data#

 
# Create the Gradio interface
iface = gr.Interface(
    fn=handle_videos, 
    inputs=gr.File(label="Upload Video(s)"), 
    outputs=gr.Textbox(label="Result")
)

# Launch the interface
iface.launch()
