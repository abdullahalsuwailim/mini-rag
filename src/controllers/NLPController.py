from .BaseController import BaseController
from src.models.db_schemes import Project , DataChunk
from src.stores.LLM.LLMEnums import DocumentTypeEnum
from typing import List
import json

class NLPController(BaseController):
    def __init__(self,vectordb_client , generation_client , embedding_client):
        super().__init__()
        
        self.vectordb_client = vectordb_client
        self.generation_client = generation_client
        self.embedding_client = embedding_client
        
    def creat_collection_name(self, project_id: str):
        return f"collection_{project_id}".strip()
    
    def reset_vector_db_collection(self,Project):    
        collection_name = self.creat_collection_name(project_id=Project.project_id)
        self.vectordb_client.delete_collection(collection_name=collection_name)
        
    def get_vector_db_collection_info(self,Project: Project):
        collection_name = self.creat_collection_name(project_id=Project.project_id)
        collection_info = self.vectordb_client.get_collection_info(collection_name=collection_name)
        
        return json.loads(
            json.dumps(collection_info, default=lambda x: x.__dict__)
        )
    
    def index_into_vector_db(self,Project: Project , chunks: list[DataChunk],
                              chunk_ids: list[int],
                               do_reset : bool = False):
        
        #step1: get collection name
        
        collection_name = self.creat_collection_name(project_id=Project.project_id)
        
        #step2: manage items
        text = [ c.chunk_text for c in chunks]
        metadata = [ c.chunk_metadata for c in chunks]
        vectors = [
            self.embedding_client.embed_text(text=text,
                                             document_type=DocumentTypeEnum.DOCUMENT.value)
            for text in text
        ]
        
        #step3: create collection if not exists
        _ = self.vectordb_client.create_collection(
            collection_name=collection_name,
            embedding_size=self.embedding_client.embedding_size,
            do_reset=do_reset,
        )
        #step4: insert into vector db
        is_inserted = self.vectordb_client.insert_many(
            collection_name=collection_name,
            texts=text,
            vectors=vectors,
            metadata=metadata,
            record_ids=chunk_ids,
        )
        
        return is_inserted
    
    def search_vector_db_collection(self,Project: Project , text: str , limit: int = 5):
        
        
        #step1: get collection name
        
        collection_name = self.creat_collection_name(project_id=Project.project_id)
        #step2 : get text embedding vector
        vector = self.embedding_client.embed_text(
            text=text,
            document_type=DocumentTypeEnum.QUERY.value
        )
        if not vector or len(vector) == 0:
            return False
           
        #step3 : do semantic search
        results = self.vectordb_client.search_by_vector(
            collection_name=collection_name,
            vector=vector,
            limit=limit
        )
        
        if not results:
            return False
        
        return json.loads(
            json.dumps(results, default=lambda x: x.__dict__)
        )
        