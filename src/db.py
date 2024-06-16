# import gradio as gr
# import os
# import shutil

# # Ensure the directory for uploaded videos exists
# os.makedirs("uploaded_videos", exist_ok=True)

# def upload_and_return(video_file):
#     # Define the target path where the video will be saved
#     # target_path = os.path.join("uploaded_videos", 'abc')
    
#     # # Save the uploaded file to the target path
#     # with open(target_path, "wb") as f:
#     #     shutil.copyfileobj(video_file, f)

#     return 'sucess'

# # Create the Gradio interface
# iface = gr.Interface(
#     fn=upload_and_return,
#     inputs=gr.Video(label="Upload your video"),
#     outputs=gr.Text(label="Download your video")
# )

# # Launch the interface
# iface.launch()


# import ffmpeg

# def extract_audio_from_video(video_path, output_audio_path):
#     """
#     Extracts the audio from an MP4 video file and saves it as an MP3 file.

#     :param video_path: Path to the input video file.
#     :param output_audio_path: Path to save the extracted audio file.
#     """
#     try:
#         (
#             ffmpeg
#             .input(video_path)
#             .output(output_audio_path, format='mp3', acodec='libmp3lame')
#             .run(overwrite_output=True)
#         )
#         return "Audio extraction successful"
#     except ffmpeg.Error as e:
#         print(f"Error: {e}")
#         return "Audio extraction failed"

# # Example usage
# video_path = r"D:/ai_work/mindinv/uploaded_videos/vv.mp4"
# output_audio_path = r"D:/ai_work/mindinv/uploaded_videos/videoplayback_audio.mp3"

# message = extract_audio_from_video(video_path, output_audio_path)
# print(message)

import subprocess
cmd = "ollama"
args = ["run", "llava","what is in the image in 20 words?", "D:/ai_work/mindinv/src/uploaded_videos/screenshot.jpg"]
message = subprocess.check_output([cmd] + args).decode('utf-8').splitlines()
print('>>',message[1:2],'<<<')
mas = message[1:2]
#mas = ' '.join(map(str, mas))
mas = mas[0].strip()


import mysql.connector

def connect_to_database():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="mayankbiker44",
        database="mi_task"   
    )
    
def video_history(video_tag, video_summery,video_visual,output_image_path,filename):
    #return (answer)
    try:
        mydb = connect_to_database()
        mycursor = mydb.cursor()
        sql1 = "INSERT INTO mi_task.video_data (video_tag, video_summery,video_visual,image,video_name) VALUES (%s, %s, %s ,%s ,%s)" 
        val1 = (video_tag, video_summery,video_visual,output_image_path,filename)

        mycursor.execute(sql1, val1)
        mydb.commit()

        return 'yess'

    except Exception as e:
        print('Error checking user existence: ', e)
        return False
    

    
# video_history('text','math',mas)