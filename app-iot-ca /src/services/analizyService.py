from ..database.connection import Datas

async def reporta_data_analizy(identifier: str):
    dadats = await Datas.find['identifier': identifier]
    return dadats