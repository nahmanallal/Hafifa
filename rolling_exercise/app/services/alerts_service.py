from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants.config import settings
from app.db.models import AirQualityMeasurement
import logging
from app.core.logger import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

async def fetch_alerts(*, db: AsyncSession) -> list[AirQualityMeasurement]:
    logger.info("Fetching alerts (threshold=%s)", settings.alert_aqi_threshold)
    stmt = select(AirQualityMeasurement).where(AirQualityMeasurement.aqi > settings.alert_aqi_threshold)
    result = await db.execute(stmt)
    rows = result.scalars().all()
    logger.info("Alerts fetched: %d rows",len(rows))
    return rows


async def fetch_alerts_by_city(*, db: AsyncSession, city: str) -> list[AirQualityMeasurement]:
    logger.info("Fetching alerts for city=%s", city)
    stmt = select(AirQualityMeasurement).where(AirQualityMeasurement.aqi > settings.alert_aqi_threshold,AirQualityMeasurement.city == city,)
    result = await db.execute(stmt)
    rows = result.scalars().all()
    logger.info("Alerts for city=%s: %d rows", city, len(rows))
    return rows
