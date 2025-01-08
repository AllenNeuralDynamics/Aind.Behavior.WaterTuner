import datetime
import os

from aind_behavior_services.session import AindBehaviorSessionModel

from aind_behavior_device_water_tuner.rig import AindBehaviorWaterTunerRig
from aind_behavior_device_water_tuner.task_logic import (
    AindBehaviorWaterTunerParameters,
    AindBehaviorWaterTunerTaskLogic,
)


def mock_session() -> AindBehaviorSessionModel:
    """Generates a mock AindBehaviorSessionModel model"""
    return AindBehaviorSessionModel(
        date=datetime.datetime.now(tz=datetime.timezone.utc),
        experiment="AindBehaviorWaterTuner",
        root_path="c://",
        subject="test",
        notes="test session",
        experiment_version="0.0.0",
        allow_dirty_repo=True,
        skip_hardware_validation=False,
        experimenter=["Foo", "Bar"],
    )


def mock_rig() -> AindBehaviorWaterTunerRig:
    return AindBehaviorWaterTunerRig(
        rig_name="test_rig",
    )


def mock_task_logic() -> AindBehaviorWaterTunerTaskLogic:
    return AindBehaviorWaterTunerTaskLogic(task_parameters=AindBehaviorWaterTunerParameters())


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
