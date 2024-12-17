import sys
import asyncio
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))
from utils.query.cronjob.backup import save_data
from services.postgres.models import ModelCard
from utils.query.labels_documentation import retrieve_all


async def backup_model_card():
    data = await retrieve_all(table_model=ModelCard)
    await save_data(data=data, filename="backup_model_card.csv")


asyncio.run(backup_model_card())
