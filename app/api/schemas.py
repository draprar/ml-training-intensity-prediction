from pydantic import BaseModel, ConfigDict

class InputData(BaseModel):
    Avg_HR: float
    Max_HR: float
    Distance: float = 0
    Steps: float = 0
    Avg_Stress: float = 0
    Stress_Change: float = 0
    Total_Reps: float = 0
    Total_Poses: float = 0
    Activity_Type: str
    day_of_week: int
    hour: int

    model_config = ConfigDict(
            json_schema_extra = {
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
                    "hour": 12
                }
            }
        )