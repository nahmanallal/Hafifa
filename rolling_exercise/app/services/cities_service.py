from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import AirQualityMeasurement 
import logging
from app.core.logger import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

async def fetch_best_cities(*, db: AsyncSession, limit: int) -> list[tuple[str, float]]:
    logger.info("Fetching best cities (limit=%d)", limit)

    average_aqi = func.avg(AirQualityMeasurement.aqi).label("average_aqi")
    stmt = (select(AirQualityMeasurement.city, average_aqi).group_by(AirQualityMeasurement.city).order_by(average_aqi.asc(), AirQualityMeasurement.city.asc()).limit(limit))
    result = await db.execute(stmt)
    rows = result.all()

    logger.info("Best cities fetched: %d results", len(rows))
    return rows

async def fetch_by_city(*, db: AsyncSession, city: str) -> list[AirQualityMeasurement]:
    logger.info("Fetching measurements for city=%s", city)

    stmt = select(AirQualityMeasurement).where(AirQualityMeasurement.city == city)
    result = await db.execute(stmt)
    rows = result.scalars().all()
    logger.info("City=%s: %d rows", city, len(rows))
    return rows


async def fetch_average_city_aqi(*,city:str, db:AsyncSession)-> float | None:
    logger.info("Computing average AQI for city=%s", city)
    stmt = select(func.avg(AirQualityMeasurement.aqi)).where(AirQualityMeasurement.city==city)
    result = await db.execute(stmt)
    return result.scalar()
    
