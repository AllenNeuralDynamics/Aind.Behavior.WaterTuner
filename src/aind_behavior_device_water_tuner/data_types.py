from aind_behavior_services.calibration import water_valve as wv
from pydantic import BaseModel

__version__ = "0.1.0"


class ExtensionDataTypes(BaseModel):
    calibration: wv.WaterValveCalibration
