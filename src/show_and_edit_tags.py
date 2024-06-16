import gradio as gr
from db import user_history
import mysql.connector

# Mock data for demonstration
video_new01 = user_history()

def user_history():
    try:
        mydb = connect_to_database()
        mycursor = mydb.cursor()

        sql =  f"""SELECT video_name,video_tag,image FROM mi_task.video_data"""
        mycursor.execute(sql)
        result = mycursor.fetchall()
        return  result 

    except Exception as e:
        print('Error checking user existence: ', e)
        return False
    
def connect_to_database():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="mayankbiker44",
        database="mi_task"   
    )

def fetch_video_data():
    video_new = user_history()
    return video_new
   
def update_tag(index, new_tag):
    try:
        mydb = connect_to_database()
        mycursor = mydb.cursor()
        sql2 = '''UPDATE mi_task.video_data SET video_tag = %s WHERE video_name = %s'''
        val2 = (new_tag, video_new01[index][0])
        mycursor.execute(sql2, val2)
        mydb.commit()

    except Exception as e:
        print('Error updating tag: ', e)
        return False

def display_videos():
    with gr.Blocks() as demo:
        video_new = user_history() 
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
