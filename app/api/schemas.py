from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class InputData(BaseModel):
    Avg_HR: float = Field(..., ge=30, le=240)
    Max_HR: float = Field(..., ge=30, le=260)
    Distance: float = Field(default=0, ge=0, le=300)
    Steps: float = Field(default=0, ge=0, le=200_000)
    Avg_Stress: float = Field(default=0, ge=0, le=100)
    Stress_Change: float = Field(default=0, ge=-100, le=100)
    Total_Reps: float = Field(default=0, ge=0, le=100_000)
    Total_Poses: float = Field(default=0, ge=0, le=100_000)
    Activity_Type: Literal["Walking", "Yoga", "Strength", "Cardio"]
    day_of_week: int = Field(..., ge=0, le=6)
    hour: int = Field(..., ge=0, le=23)

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "Avg_HR": 120.0,
                "Max_HR": 150.0,
                "Distance": 5.0,
                "Steps": 4000,
                "Avg_Stress": 0.0,
                "Stress_Change": 0.0,
                "Total_Reps": 0,
                "Total_Poses": 0,
                "Activity_Type": "Walking",
                "day_of_week": 2,
                "hour": 12,
            }
        },
    )
