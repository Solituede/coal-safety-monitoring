from fastapi import APIRouter
from ..database import read_historical_data
from ..safety_calculator import SafetyCalculator
from backend.routes.data_routes import router as data_router
