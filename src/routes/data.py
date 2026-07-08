from fastapi import APIRouter, Depends, UploadFile, File, status
from fastapi.responses import JSONResponse
import os
import aiofiles
import logging
from src.helpers.config import get_settings, Settings
from src.controllers import DataController, ProjectController
from src.models.enum.ResponseEnum import ResponseSignal
from .schemes.data1 import ProcessRequest



logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"]
)


@data_router.post("/upload/{project_id}")
async def upload_data(
    project_id: str,
    file: UploadFile = File(...),
    app_settings: Settings = Depends(get_settings)
):
    
    data_controller = DataController()
    is_valid, result_signal = data_controller.validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseSignal.FILE_UPLOAD_FAILED.value}
        )

    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    
    upload_file_path, file_id  = data_controller.generate_unique_filepath(
        original_filename=file.filename,
        project_id=project_id
    )
    
    try:
         async with aiofiles.open(upload_file_path, "wb") as f:
             while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                 await f.write(chunk)
    except Exception as e:
        
        logger.error(f"Error occurred while uploading the file: {e}")    
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": result_signal}
        )
   
            
    return JSONResponse(
           content={
               "signal": result_signal,
               "file_id": file_id,
           }
         )