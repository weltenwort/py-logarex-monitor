import asyncio
from logging import basicConfig, getLogger
from pathlib import Path
from py_logarex_monitor.commands.monitor_serial import run_monitor_serial
from typing import Optional

import typer

# from .commands.parse_candump import run_parse_candump
# from .commands.monitor_canbus import run_monitor_canbus
from .config import (
    load_configuration_from_file_path,
    load_default_configuration,
)

# from .elster_protocol.register_definitions import (
#     load_default_register_definitions,
#     load_register_definitions_from_file_path,
# )

app = typer.Typer()


@app.command()
def run(
    config_file: Optional[Path] = typer.Option(
        None,
        dir_okay=False,
        exists=True,
    ),
    # register_definition_file: Optional[Path] = typer.Option(
    #     Path(__file__).resolve().parent
    #     / "elster_protocol"
    #     / "register_definitions.toml",
    #     dir_okay=False,
    #     exists=True,
    # ),
    # log_frames: bool = typer.Option(False, "--log-frames"),
    # log_registers: bool = typer.Option(False, "--log-registers"),
):
    basicConfig(level=0)

    logger = getLogger()

    logger.info("Loading configuration...")

    configuration = (
        load_configuration_from_file_path(config_file)
        if config_file
        else load_default_configuration()
    )

    # register_definitions = (
    #     load_register_definitions_from_file_path(register_definition_file)
    #     if register_definition_file
    #     else load_default_register_definitions()
    # )

    asyncio.run(
        run_monitor_serial(
            serial_config=configuration.serial_port, mqtt_config=configuration.mqtt
        )
        # run_monitor_canbus(
        #     can_interface=can_interface,
        #     log_frames=log_frames,
        #     log_registers=log_registers,
        #     mqtt_config=configuration.mqtt,
        #     default_register_configuration=configuration.can_bus.default_register_configuration,
        #     register_configurations=configuration.can_bus.register_configuration,
        #     register_definitions=register_definitions,
        #     sender_id=configuration.can_bus.sender_id,
        # )
    )


# @app.command()
# def parse_candump():
#     asyncio.run(run_parse_candump())
