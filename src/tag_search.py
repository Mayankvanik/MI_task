import gradio as gr
from db import user_history
import mysql.connector
import pandas as pd

# Mock data for demonstration

def connect_to_database():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="mayankbiker44",
        database="mi_task"   
    )

def display_videos(new_tag):

    mydb = connect_to_database()  # Connect to database
    mycursor = mydb.cursor()
    try:
        sql = '''SELECT video_id ,video_name, video_tag FROM video_data WHERE video_tag = %s'''
        val = (new_tag,)
        mycursor.execute(sql, val)
        video_data = mycursor.fetchall()
        df = pd.DataFrame(video_data, columns=['video_id','Video', 'Category'])
        return df
    except mysql.connector.Error as err:
        print("Error fetching data:", err)
        


# Gradio interface components
with gr.Blocks() as demo:
    category = gr.Dropdown(choices=["Science", "Artificial Intelligence", "Entertainment", "Nature", "Mathematics"], label="Select Animal Category")
    with gr.Tabs():
        with gr.Tab("DataFrame"):
            dataframe_output = gr.DataFrame()
    
    category.change(fn=display_videos, inputs=category, outputs=dataframe_output)

# Launch the interface
demo.launch()