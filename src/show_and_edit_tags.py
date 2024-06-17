import gradio as gr
from db import user_history,connect_to_database
import mysql.connector

#data for demonstration fetch from sql
video_new = user_history()
    
def fetch_video_data():
    video_new = user_history()
    return video_new

#use video_new  for index search so write here db query
def update_tag(index, new_tag):
    try:
        mydb = connect_to_database()
        mycursor = mydb.cursor()
        sql2 = '''UPDATE mi_task.video_data SET video_tag = %s WHERE video_name = %s'''
        val2 = (new_tag, video_new[index][0])
        mycursor.execute(sql2, val2)
        mydb.commit()

    except Exception as e:
        print('Error updating tag: ', e)
        return False

#show List of user data in component and edit tag feild
def display_videos():
    with gr.Blocks() as demo: 
        for idx, video in enumerate(video_new):
            with gr.Blocks():
                refress_button = gr.Button("refresh")
                refress_button.click(fn=user_history)
                with gr.Row():
                    gr.Image(video[2], label="Thumbnail", height=200, width=300)
                    gr.Textbox(value=video[0], label="Video Name", interactive=True, min_width=20)
                    with gr.Column():
                        tag_input = gr.Textbox(value=video[1], label="Tag", interactive=True, min_width=20)
                        edit_button = gr.Button("Edit Tag")
                        edit_button.click(fn=update_tag, inputs=[gr.State(idx), tag_input], outputs=[])
    return demo

# Create the Gradio Blocks interface
demo = display_videos()
demo.launch()
