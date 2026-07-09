from src.models.BaseDataModel import BaseDataModel
from.db_schemes.DataChunk import DataChunk
from .enum.DataBaseEnum import DataBaseEnum
from pymongo import InsertOne
class ChunkModel(BaseDataModel):
    def __init__(self,db_client: object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]
        
        
    async def create_chunk(self, chunk: DataChunk):
        result = await self.collection.insert_one(
        chunk.model_dump(by_alias=True,exclude_none=True)
        )

        chunk.id = result.inserted_id
        return chunk
    
    async def get_chunks(self, project_id: str):
        result = await self.collection.find.one({
            "_id": project_id
        })
        
        if result is None:
            return None
        
        return DataChunk(**result)
    
    async def insert_many_chunks(self, chunks: list,batch_size: int=1000):
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            
            
            operations = [
                InsertOne(chunk.model_dump(by_alias=True,exclude_none=True))
                for chunk in batch
            ]
            
            await self.collection.bulk_write(operations)
            
            
        return len(chunks)
    
    async def delete_chunks_by_project_id(self, project_id: str):
        result = await self.collection.delete_many(
            {"chunk_project_id": project_id}
        )
        
        return result.deleted_count