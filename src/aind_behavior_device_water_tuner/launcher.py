from pathlib import Path

import aind_behavior_experiment_launcher.launcher.behavior_launcher as behavior_launcher
from aind_behavior_experiment_launcher import resource_monitor
from aind_behavior_experiment_launcher.apps import BonsaiApp
from aind_behavior_services.session import AindBehaviorSessionModel

from aind_behavior_device_water_tuner.rig import AindBehaviorWaterTunerRig
from aind_behavior_device_water_tuner.task_logic import AindBehaviorWaterTunerTaskLogic


def make_launcher() -> behavior_launcher.BehaviorLauncher:
    data_dir = r"C:/Data"
    srv = behavior_launcher.BehaviorServicesFactoryManager()
    srv.attach_bonsai_app(BonsaiApp(Path(r"./src/main.bonsai")))
    srv.attach_resource_monitor(
        resource_monitor.ResourceMonitor(
            constrains=[
                resource_monitor.available_storage_constraint_factory(data_dir, 2e11),
            ]
        )
    )

    return behavior_launcher.BehaviorLauncher(
        rig_schema_model=AindBehaviorWaterTunerRig,
        session_schema_model=AindBehaviorSessionModel,
        task_logic_schema_model=AindBehaviorWaterTunerTaskLogic,
        data_dir=data_dir,
        config_library_dir=r"\\allen\aind\scratch\AindBehavior.db\AindBehaviorWaterTuner",
        temp_dir=r"./local/.temp",
        allow_dirty=False,
        skip_hardware_validation=False,
        debug_mode=False,
        group_by_subject_log=True,
        services=srv,
        validate_init=True,
    )


def main():
    launcher = make_launcher()
    launcher.main()
    return None


if __name__ == "__main__":
    main()
