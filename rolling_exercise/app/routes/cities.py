from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.db.session import get_db
from app.schemas.air_quality import AirQualityMeasurementOut, CityAqiAverageOut
from app.db.models import AirQualityMeasurement
from app.services.cities_service import fetch_best_cities , fetch_by_city, fetch_average_city_aqi

router = APIRouter(prefix="/cities")

@router.get("/best", response_model=list[CityAqiAverageOut])
async def get_best_cities(session: AsyncSession = Depends(get_db)) -> list[CityAqiAverageOut]:
    rows = await fetch_best_cities(session=session, limit=3)
    return [CityAqiAverageOut(city=city, average_aqi=average_aqi) for city, average_aqi in rows]

@router.get("/{city}", response_model=list[AirQualityMeasurementOut])
async def get_city_measurements(city:str ,session: AsyncSession = Depends(get_db))-> list[AirQualityMeasurementOut]:
    measurments = await fetch_by_city(session=session,city=city)

    if not measurments:

        raise HTTPException(status_code=404,detail="unknown city")
    
    return measurments

@router.get("/{city}/average", response_model=CityAqiAverageOut)
async def get_average_city_aqi(city: str,session: AsyncSession = Depends(get_db),) -> CityAqiAverageOut:
    avg_aqi = await fetch_average_city_aqi(session=session, city=city)

    if avg_aqi is None:

        raise HTTPException(status_code=404,detail="no measurements found for this city")

    return CityAqiAverageOut(city=city, average_aqi=avg_aqi)

