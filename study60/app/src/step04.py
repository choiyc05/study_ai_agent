from fastapi import APIRouter, HTTPException, Depends
from src.core import get_app_state


router = APIRouter(
  prefix="/step04",
  tags=["step04"],
)