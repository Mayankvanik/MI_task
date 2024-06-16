# # import gradio as gr

# # # Sample video data
# # video_data = [
# #     {"name": "video1.mp4", "tag": "Science", "thumbnail": "D:/ai_work/mindinv/src/uploaded_videos/screenshot.jpg"},
# #     {"name": "video2.mp4", "tag": "Artificial Intelligence","thumbnail": "https://fastly.picsum.photos/id/237/200/300.jpg?hmac=TmmQSbShHz9CdQm0NkEjx1Dyh_Y984R9LpNrpvH2D_U"},
# #     {"name": "video3.mp4", "tag": "Entertainment", "thumbnail": "https://fastly.picsum.photos/id/237/200/300.jpg?hmac=TmmQSbShHz9CdQm0NkEjx1Dyh_Y984R9LpNrpvH2D_U"},
# #     {"name": "video4.mp4", "tag": "Nature", "thumbnail": "https://fastly.picsum.photos/id/237/200/300.jpg?hmac=TmmQSbShHz9CdQm0NkEjx1Dyh_Y984R9LpNrpvH2D_U"},
# #     {"name": "video5.mp4", "tag": "Mathematics", "thumbnail": "https://fastly.picsum.photos/id/237/200/300.jpg?hmac=TmmQSbShHz9CdQm0NkEjx1Dyh_Y984R9LpNrpvH2D_U"},
# # ]


# # # Function to create video blocks
# # def create_video_blocks(video_data):
# #     with gr.Blocks() as demo:
# #         for idx, video in enumerate(video_data):
# #             with gr.Blocks():
# #                 with gr.Row():
# #                     gr.Image(video["thumbnail"], label="Thumbnail", height=200, width=300)
# #                     gr.Textbox(value=video["name"], label="Video Name", interactive=True, min_width=20)
# #                     with gr.Column():
# #                         tag_input = gr.Textbox(value=video["tag"], label="Tag", interactive=True, min_width=20)
# #                         edit_button = gr.Button("Edit Tag")
# #                         edit_button.click(fn=update_tag, inputs=[gr.State(idx), tag_input])
# #     return demo

# # # Gradio interface
# # def display_videos():
# #     with gr.Blocks() as demo:
# #         tag_dropdown = gr.Dropdown(["AI", "science", "math", "nature"], label="Search by tags")
# #         fetch_button = gr.Button("Fetch Videos")
# #         fetch_button.click(fn=create_video_blocks,inputs=tag_dropdown)
       
# #     return demo
# # # Create the Gradio Blocks interface
# # demo = display_videos()
# # demo.launch()


# import gradio as gr

# # Sample video data
# video_data = [
#     {"name": "video1.mp4", "tag": "Science", "thumbnail": "D:/ai_work/mindinv/src/uploaded_videos/screenshot.jpg"},
#     {"name": "video2.mp4", "tag": "Artificial Intelligence", "thumbnail": "https://fastly.picsum.photos/id/237/200/300.jpg?hmac=TmmQSbShHz9CdQm0NkEjx1Dyh_Y984R9LpNrpvH2D_U"},
#     {"name": "video3.mp4", "tag": "Entertainment", "thumbnail": "https://fastly.picsum.photos/id/237/200/300.jpg?hmac=TmmQSbShHz9CdQm0NkEjx1Dyh_Y984R9LpNrpvH2D_U"},
#     {"name": "video4.mp4", "tag": "Nature", "thumbnail": "https://fastly.picsum.photos/id/237/200/300.jpg?hmac=TmmQSbShHz9CdQm0NkEjx1Dyh_Y984R9LpNrpvH2D_U"},
#     {"name": "video5.mp4", "tag": "Mathematics", "thumbnail": "https://fastly.picsum.photos/id/237/200/300.jpg?hmac=TmmQSbShHz9CdQm0NkEjx1Dyh_Y984R9LpNrpvH2D_U"},
# ]

# # Function to filter videos by tag
# def filter_videos(tag):
#     if tag == "All":
#         return video_data
#     return [video for video in video_data if video["tag"] == tag]

# # Function to create video blocks
# def create_video_blocks(tag):
#     filtered_videos = filter_videos(tag)
#     video_blocks = []
#     for video in filtered_videos:
#         with gr.Blocks() as block:
#             with gr.Row():
#                 gr.Image(video["thumbnail"], label="Thumbnail", height=200, width=300)
#                 gr.Textbox(value=video["name"], label="Video Name", interactive=True, min_width=20)
#                 with gr.Column():
#                     tag_input = gr.Textbox(value=video["tag"], label="Tag", interactive=True, min_width=20)
#                     edit_button = gr.Button("Edit Tag")
#                     # Placeholder function call for edit button
#                     edit_button.click(fn=lambda x, y: None, inputs=[gr.State(video["name"]), tag_input])
#             video_blocks.append(block)
#     return video_blocks

# # Gradio interface
# def display_videos():
#     with gr.Blocks() as demo:
#         tag_dropdown = gr.Dropdown(["All", "Science", "Artificial Intelligence", "Entertainment", "Nature", "Mathematics"], label="Search by tags")
#         fetch_button = gr.Button("Fetch Videos")
#         video_output = gr.Row()
        
#         def update_video_blocks(tag):
#             blocks = create_video_blocks(tag)
#             return gr.Row.update(children=blocks)
        
#         fetch_button.click(fn=update_video_blocks, inputs=tag_dropdown, outputs=update_video_blocks)
        
#         with gr.Column():
#             tag_dropdown
#             fetch_button
#             video_output

#     return demo

# # Create the Gradio Blocks interface
# demo = display_videos()
# demo.launch()







# demo = gr.Interface(
#     display_videos,[gr.Dropdown(["Science", "Artificial Intelligence", "Entertainment", "Nature", "Mathematics"])],
#     "text"
# )


# import gradio as gr
# import mysql.connector

# def connect_to_database():
#     try:
#         mydb = mysql.connector.connect(
#             host="127.0.0.1",
#             user="root",
#             password="mayankbiker44",
#             database="mi_task"
#         )
#     except mysql.connector.Error as err:
#         print("Error connecting to database:", err)
#         return None  # Indicate failure to connect
#     return mydb

# def display_videos(new_tag):

#     mydb = connect_to_database()  # Connect to database
#     mycursor = mydb.cursor()
#     try:
#         sql = '''SELECT video_name, video_tag, image FROM video_data WHERE video_tag = %s'''
#         val = (new_tag,)
#         mycursor.execute(sql, val)
#         video_data = mycursor.fetchall()
#         return video_data
#     except mysql.connector.Error as err:
#         print("Error fetching data:", err)
#         mydb.close()  # Close connection on error
#         return gr.Label("Error fetching video data.")  # Inform user of data fetching error

# with gr.Blocks() as demo:

#     input=gr.Dropdown(["Science", "Artificial Intelligence", "Entertainment", "Nature", "Mathematics"])
#     submit_button = gr.Button("Submit")
    
#     video_data= display_videos()
#     for video in video_data:
#         with gr.Blocks():
#             output =gr.Image(video[2], label="Thumbnail", height=200, width=300),gr.Textbox(value=video[0], label="Video Name", interactive=True, min_width=20),gr.Textbox(value=video[1], label="Tag", interactive=True, min_width=20)

    
#     submit_button.click(
#         fn=display_videos,
#         inputs=input,
#         outputs=[output]
#         )

# if __name__ == "__main__":
#     demo.launch()


import gradio as gr

# Data containing animal types and names
data = [
    {"type": "dog", "name": "Rover"},
    {"type": "dog", "name": "Buddy"},
    {"type": "dog", "name": "Charlie"},
    {"type": "cat", "name": "Mittens"},
    {"type": "cat", "name": "Whiskers"},
    {"type": "cat", "name": "Shadow"}
]

# Function to filter and return names based on selected category
def get_animal_names(category):
    #return [animal["name"] for animal in data if animal["type"] == category]
    anima = [[animal["type"], animal["name"]] for animal in data if animal["type"] == category]

    with gr.Blocks() as den:
        for id in anima:
            with gr.Row():
                gr.Textbox(id[0])
                gr.Textbox(id[1])
    return den

# Gradio interface components
with gr.Blocks() as demo:
    category = gr.Dropdown(choices=["dog", "cat"], label="Select Animal Category")
    names = gr.Textbox(label="Names", interactive=False)
    
    # for i in names:
    #     with gr.Row():
    #         gr.Textbox(i[0])
    #         gr.Textbox(i[1])

    category.change(fn=get_animal_names, inputs=category, outputs=names)#

# Launch the interface
demo.launch()



