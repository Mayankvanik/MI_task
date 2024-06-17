import gradio as gr
from db import display_videos
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



# Gradio interface components
with gr.Blocks() as demo:
    category = gr.Dropdown(choices=["Science", "Artificial Intelligence", "Entertainment", "Nature", "Mathematics"], label="Select Animal Category")
    #convert tag list in Dataframe for readable formate
    with gr.Tabs():
        with gr.Tab("DataFrame"):
            dataframe_output = gr.DataFrame()
    
    category.change(fn=display_videos, inputs=category, outputs=dataframe_output)

# Launch the interface
demo.launch()