from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.air_quality import AirQualityMeasurementOut
from app.services.alerts_service import fetch_alerts, fetch_alerts_by_city

router = APIRouter()


@router.get("/alerts", response_model=list[AirQualityMeasurementOut])
async def get_alerts(db: AsyncSession = Depends(get_db)) -> list[AirQualityMeasurementOut]:
    return await fetch_alerts(db=db)


@router.get("/alerts/city/{city}", response_model=list[AirQualityMeasurementOut])
async def get_alerts_by_city(city: str,db: AsyncSession = Depends(get_db),) -> list[AirQualityMeasurementOut]:
    return await fetch_alerts_by_city(db=db, city=city)
