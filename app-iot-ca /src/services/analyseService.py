from ..database.connection import Data, HistoryOccurrence, DataModel

class AnalyseService:
    async def list_data_analyse():
        data = Data.find()
        return list(data)
    
    async def list_history_occurrence_analyse() -> list:
       return  HistoryOccurrence.find()
    
    async def list_data_model():
        data = DataModel.find()
        return list(data)
    