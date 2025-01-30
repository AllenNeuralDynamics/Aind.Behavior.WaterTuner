import datetime
import os

from aind_behavior_services import rig
from aind_behavior_services.calibration import aind_manipulator
from aind_behavior_services.calibration.aind_manipulator import (
    AindManipulatorCalibration,
    AindManipulatorCalibrationInput,
    AindManipulatorCalibrationOutput,
    Axis,
    AxisConfiguration,
    ManipulatorPosition,
)
from aind_behavior_services.session import AindBehaviorSessionModel

from aind_behavior_device_water_tuner.rig import AindBehaviorWaterTunerRig, SerialScale
from aind_behavior_device_water_tuner.task_logic import (
    AindBehaviorWaterTunerParameters,
    AindBehaviorWaterTunerTaskLogic,
)


def mock_session() -> AindBehaviorSessionModel:
    """Generates a mock AindBehaviorSessionModel model"""
    return AindBehaviorSessionModel(
        date=datetime.datetime.now(tz=datetime.timezone.utc),
        experiment="AindBehaviorWaterTuner",
        root_path="c://Data",
        subject="test",
        notes="test session",
        experiment_version="0.0.0",
        allow_dirty_repo=True,
        skip_hardware_validation=False,
        experimenter=["Foo", "Bar"],
    )


def mock_rig() -> AindBehaviorWaterTunerRig:
    manipulator_calibration = AindManipulatorCalibration(
        output=AindManipulatorCalibrationOutput(),
        input=AindManipulatorCalibrationInput(
            full_step_to_mm=(ManipulatorPosition(x=0.010, y1=0.010, y2=0.010, z=0.010)),
            axis_configuration=[
                AxisConfiguration(axis=Axis.Y1, min_limit=-1, max_limit=15000),
                AxisConfiguration(axis=Axis.Y2, min_limit=-1, max_limit=15000),
                AxisConfiguration(axis=Axis.X, min_limit=-1, max_limit=15000),
                AxisConfiguration(axis=Axis.Z, min_limit=-1, max_limit=15000),
            ],
            homing_order=[Axis.Y1, Axis.Y2, Axis.X, Axis.Z],
            initial_position=ManipulatorPosition(y1=0, y2=0, x=0, z=0),
        ),
    )

    return AindBehaviorWaterTunerRig(
        rig_name="testrig",
        harp_behavior=rig.HarpBehavior(port_name="COM3"),
        harp_clock_generator=rig.HarpClockGenerator(port_name="COM17"),
        manipulator=aind_manipulator.AindManipulatorDevice(port_name="COM10", calibration=manipulator_calibration),
        scale=SerialScale(port_name="COM12"),
    )


def mock_task_logic() -> AindBehaviorWaterTunerTaskLogic:
    return AindBehaviorWaterTunerTaskLogic(
        task_parameters=AindBehaviorWaterTunerParameters(
            repeat_count=200, valve_open_interval=0.2, valve_open_time=list(range(0.02, 0.1, 0.02))
        )
    )


def main(path_seed: str = "./local/{schema}.json"):
    example_session = mock_session()
    example_rig = mock_rig()
    example_task_logic = mock_task_logic()

    os.makedirs(os.path.dirname(path_seed), exist_ok=True)

    for model in [example_task_logic, example_session, example_rig]:
        with open(path_seed.format(schema=model.__class__.__name__), "w", encoding="utf-8") as f:
            f.write(model.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
