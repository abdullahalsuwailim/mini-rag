from fastapi import APIRouter, Depends, UploadFile, File, status
from fastapi.responses import JSONResponse
import os
import aiofiles

from src.helpers.config import get_settings, Settings
from src.controllers import DataController, ProjectController


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
            content={"signal": result_signal}
        )

    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    
    upload_file_path = os.path.join(
    project_dir_path,
    data_controller.generate_unique_filename(
        original_filename=file.filename
    )
)

    async with aiofiles.open(upload_file_path, "wb") as f:
        while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
            await f.write(chunk)
            
            
    return JSONResponse(
    content={
        "signal": result_signal
          }
         )