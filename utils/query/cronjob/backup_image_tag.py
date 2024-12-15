import sys
import csv
import os
import asyncio
from pathlib import Path
from sqlalchemy.future import select

sys.path.append(str(Path(__file__).resolve().parents[3]))
from services.postgres.models import ImageTag
from services.postgres.connection import database_connection


async def retrieve_all() -> list:
    async with database_connection(connection_type="async").connect() as session:
        try:
            query = select(ImageTag)
            result = await session.execute(query)
            rows = result.fetchall()
            if not rows:
                print(f"[retrieve_all] No data entry in {ImageTag.__tablename__}!")
                raise ValueError("Data entry not found.")
            return [dict(row._mapping) for row in rows]
        except ValueError:
            raise
        except Exception as e:
            print(f"[retrieve_all] Error retieving all entry: {e}")
            await session.rollback()
            raise ValueError("Invalid database query")
        finally:
            await session.close()


async def save_data(data: list) -> None:
    default_path = Path("/project-utils/backup")
    default_path.mkdir(parents=True, exist_ok=True)

    filename = "backup_image_tag.csv"
    filepath = os.path.join(default_path, filename)

    with open(filepath, mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(data)

    print(f"Data successfully saved to {filepath}")


async def main():
    data = await retrieve_all()
    await save_data(data=data)


asyncio.run(main())
