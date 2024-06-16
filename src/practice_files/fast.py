from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import os
import shutil

app = FastAPI()

# Ensure the directory for uploaded videos exists
UPLOAD_DIR = "uploaded_videos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_video(file: UploadFile = File(...)):
    # Define the target path where the video will be saved
    target_path = os.path.join(UPLOAD_DIR, file.filename)
    
    # Save the uploaded file to the target path
    with open(target_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Return a success message
    return {"message": "Upload successful", "file_path": target_path}

@app.get("/download/{filename}")
async def download_video(filename: str):
    # Define the path of the file to be downloaded
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    # Check if the file exists
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='application/octet-stream', filename=filename)
    else:
        return {"error": "File not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

