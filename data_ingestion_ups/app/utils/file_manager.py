import shutil
from pathlib import Path

from core.logger import logger


INGESTION_DIR = Path("data/ingestion_file")
COMPLETED_DIR = Path("data/completed_file")
FAILED_DIR = Path("data/failed_file")


class FileManager:

    @staticmethod
    def save_uploaded_file(file, filename: str):

        file_path = INGESTION_DIR / filename

        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        logger.info(f"File saved to ingestion folder: {file_path}")

        return str(file_path)

    @staticmethod
    def move_to_completed(file_path: str):

        src = Path(file_path)

        dest = COMPLETED_DIR / src.name

        shutil.move(src, dest)

        logger.info(f"File moved to completed folder: {dest}")

    @staticmethod
    def move_to_failed(file_path: str):

        src = Path(file_path)

        dest = FAILED_DIR / src.name

        shutil.move(src, dest)

        logger.info(f"File moved to failed folder: {dest}")