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
    
    def generate_unique_filename(self, original_filename: str):
         random_key = self.generate_random_string()
         file_extension = self.get_file_extension(original_filename)
         return f"{random_key}.{file_extension}"
        
         while os.path.exists(new_file_path):
            random_key = self.generate_random_string() 
            new_file_path = os.path.join(
                project_path,
                random_key + "_" + clean_filename
                 )
            
            return new_file_path        
        
    def get_clean_file_name(self, orig_file_name: str):
        #remove any special characters from the filename eccept for underscores and .
        clean_filename = re.sub(r'[^\w\.]', '', orig_file_name.strip())
        
        #replace any spaces with underscores
        clean_filename = clean_filename.replace(' ', '_')
        
        
        return clean_filename