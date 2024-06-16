import gradio as gr

# Mock data for demonstration



video_data = [
    {"name": "video1.mp4", "tag": "Science", "thumbnail": "D:/ai_work/mindinv/src/uploaded_videos/screenshot.jpg"},
    {"name": "video2.mp4", "tag": "Artificial Intelligence","thumbnail": "https://fastly.picsum.photos/id/237/200/300.jpg?hmac=TmmQSbShHz9CdQm0NkEjx1Dyh_Y984R9LpNrpvH2D_U"},
    {"name": "video3.mp4", "tag": "Entertainment", "thumbnail": "https://fastly.picsum.photos/id/237/200/300.jpg?hmac=TmmQSbShHz9CdQm0NkEjx1Dyh_Y984R9LpNrpvH2D_U"},
    {"name": "video4.mp4", "tag": "Nature", "thumbnail": "https://fastly.picsum.photos/id/237/200/300.jpg?hmac=TmmQSbShHz9CdQm0NkEjx1Dyh_Y984R9LpNrpvH2D_U"},
    {"name": "video5.mp4", "tag": "Mathematics", "thumbnail": "https://fastly.picsum.photos/id/237/200/300.jpg?hmac=TmmQSbShHz9CdQm0NkEjx1Dyh_Y984R9LpNrpvH2D_U"},
]

def update_tag(index, new_tag):
    video_data[index]["tag"] = new_tag
    return f"Tag for {video_data[index]['name']} updated to {new_tag}"

def display_videos():
    with gr.Blocks() as demo:
        for idx, video in enumerate(video_data):
            with gr.Blocks():
                with gr.Row():
                    gr.Image(video["thumbnail"], label="Thumbnail", height=200, width=300)
                    gr.Textbox(value=video["name"], label="Video Name", interactive=True, min_width=20)
                    with gr.Column():
                        tag_input = gr.Textbox(value=video["tag"], label="Tag", interactive=True, min_width=20)
                        edit_button = gr.Button("Edit Tag")
                        edit_button.click(fn=update_tag, inputs=[gr.State(idx), tag_input])
    return demo
# Create the Gradio Blocks interface
demo = display_videos()
demo.launch()