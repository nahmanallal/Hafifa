import logging
from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.exceptions import CsvParseError
from app.services.upload_service import ingest_air_quality_csv
from app.core.logger import LOGGER_NAME

router = APIRouter()
logger = logging.getLogger(LOGGER_NAME)


@router.post("/upload")
async def upload_csv(file: UploadFile = File(...),db: AsyncSession = Depends(get_db),) -> Response:
    logger.info("Received /upload request for file: %s", file.filename)

    content = await file.read()

    try:
        inserted_rows = await ingest_air_quality_csv(file_content=content, db=db)
        logger.info("Upload completed. %d rows inserted", inserted_rows)

    except CsvParseError as exc:
        logger.warning("CSV parsing error: %s",exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    
    except SQLAlchemyError as exc:
        logger.error("Database error during upload: %s", exc)
        raise HTTPException(status_code=500, detail="Database error") from exc

    return Response(content="ok", media_type="text/plain")
