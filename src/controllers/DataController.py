from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from src.models.enum import ResponseSignal
import re 
import os

class DataController(BaseController):
    
    def __init__(self):
        super().__init__()
        self.size_scale = 1024 * 1024  # Convert MB to bytes
    def validate_uploaded_file(self, file: UploadFile):
        
        if file.content_type not in self.settings.FILE_ALLOWED_TYPES:
            return False,ResponseSignal.FILE_TYPE_NOT_ALLOWED.value
        
        if file.size > self.settings.FILE_MAX_SIZE * self.size_scale:
            return False,ResponseSignal.FILE_TOO_LARGE.value
        
        return True,ResponseSignal.FILE_UPLOAD_SUCCESS.value
    
    def get_file_extension(self, filename: str):
        return filename.split(".")[-1]
    
    def generate_unique_filepath(self, original_filename: str, project_id: str):
         random_key = self.generate_random_string()
         project_path = ProjectController().get_project_path(project_id=project_id)
         
        
         cleaned_filename = self.get_clean_file_name(orig_file_name=original_filename)

         new_file_path = os.path.join(
            project_path,
            f"{random_key}_{cleaned_filename}"
         )
        
         while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(
                project_path,
                f"{random_key}_{cleaned_filename}"
            )
            
         return new_file_path,  f"{random_key}_{cleaned_filename}"      
        
    def get_clean_file_name(self, orig_file_name: str):
        #remove any special characters from the filename eccept for underscores and .
        clean_filename = re.sub(r'[^\w\.]', '', orig_file_name.strip())
        
        #replace any spaces with underscores
        clean_filename = clean_filename.replace(' ', '_')
        
        
        return clean_filename