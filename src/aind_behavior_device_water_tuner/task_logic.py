from typing import Literal

from aind_behavior_services.task_logic import AindBehaviorTaskLogicModel, TaskParameters
from pydantic import Field, PositiveFloat

__version__ = "0.1.0"


class AindBehaviorWaterTunerParameters(TaskParameters):
    valve_open_time: list[PositiveFloat] = Field(
        ...,
        min_length=1,
        description="An array with the times (s) the valve is open during calibration",
    )
    valve_open_interval: float = Field(
        default=0.2,
        description="Time between two consecutive valve openings (s)",
        title="Valve open interval",
        gt=0,
    )
    repeat_count: int = Field(
        default=200,
        ge=1,
        description="Number of times the valve opened per measure valve_open_time entry",
        title="Repeat count",
    )


class AindBehaviorWaterTunerTaskLogic(AindBehaviorTaskLogicModel):
    """WaterTuner operation control model that is used to run a calibration data acquisition workflow"""

    name: str = Field(default="WaterValveCalibrationLogic", title="Task name")
    version: Literal[__version__] = __version__
    task_parameters: AindBehaviorWaterTunerParameters = Field(..., title="Task parameters", validate_default=True)
