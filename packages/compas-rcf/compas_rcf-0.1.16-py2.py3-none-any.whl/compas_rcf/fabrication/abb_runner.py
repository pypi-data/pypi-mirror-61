"""Fabrication runner for Rapid Clay Fabrication project for fullscale structure.

Run from command line using :code:`python -m compas_rcf.fabrication.abb_rcf_runner`
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import sys
from datetime import datetime
from os import path

from colorama import Fore
from colorama import Style
from colorama import init
from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Vector
from compas_fab.backends.ros import RosClient
from compas_rrc import AbbClient
from compas_rrc import CustomInstruction
from compas_rrc import MoveToFrame
from compas_rrc import MoveToJoints
from compas_rrc import PrintText
from compas_rrc import SetAcceleration
from compas_rrc import SetDigital
from compas_rrc import SetMaxSpeed
from compas_rrc import SetTool
from compas_rrc import SetWorkObject
from compas_rrc import WaitTime

from compas_rcf import __version__
from compas_rcf.fabrication.conf import abb_rcf_conf_template
from compas_rcf.fabrication.conf import fabrication_conf
from compas_rcf.utils.util_funcs import get_offset_frame
from compas_rcf.utils import ui
from compas_rcf.utils.json_ import load_bullets

if sys.version_info[0] < 2:
    raise Exception("This module requires Python 3")
else:
    import questionary

ROBOT_CONTROL_FOLDER_DRIVE = "G:\\Shared drives\\2020_MAS\\T2_P1\\02_Groups\\Phase2\\rcf_fabrication\\02_robot_control"  # noqa E501

DEFAULT_CONF_DIR = path.join(ROBOT_CONTROL_FOLDER_DRIVE, "05_fabrication_confs")
DEFAULT_JSON_DIR = path.join(ROBOT_CONTROL_FOLDER_DRIVE, "04_fabrication_data_jsons")
DEFAULT_LOG_DIR = path.join(ROBOT_CONTROL_FOLDER_DRIVE, "06_fabrication_logs")

# Define external axis, will not be used but required in move cmds
EXTERNAL_AXIS_DUMMY: list = []


def get_picking_frame(bullet_height):
    """Get next picking frame.

    Parameters
    ----------
    bullet_height : float
        Height of bullet to pick up

    Returns
    -------
    `class`:compas.geometry.Frame
    """
    # TODO: Set up a grid to pick from
    picking_frame = Frame(Point(0, 0, 0), Vector(0, 1, 0), Vector(1, 0, 0))

    # TODO: Make the pressing at picking more configurable
    return get_offset_frame(picking_frame, bullet_height * 0.95)


def send_grip_release(client, do_state):
    """Grip or release using RCF tool, either in simulation or on real robot.

    If script target is real robot this will set the digital output on the robot,
    and if the target is virtual robot it will use RobotStudio code to visualize
    clay bullet gripping and releasing

    Parameters
    ----------
    client : :class:`compas_rrc.AbbClient`
    do_state : int (0 or 1)
        Value to set DO to
    """
    if CONF.target == "real":
        client.send(WaitTime(CONF.tool.wait_before_io))
        client.send(SetDigital(CONF.tool.io_needles_pin, do_state))
        client.send(WaitTime(CONF.tool.wait_after_io))
    else:
        # Custom instruction can grip a bullet in RobotStudio
        # note the tool tip must touch the bullet
        if do_state == CONF.tool.grip_state:
            client.send(CustomInstruction("r_A057_RS_ToolGrip"))
        else:
            client.send(CustomInstruction("r_A057_RS_ToolRelease"))

    logging.debug(
        "Signal sent to {}".format(
            "grip" if do_state == CONF.tool.grip_state else "release"
        )
    )


def initial_setup(client):
    """Pre fabrication setup, speed, acceleration, tool, work object and initial pose.

    Parameters
    ----------
    client : :class:`compas_rrc.AbbClient`
    """

    send_grip_release(client, CONF.tool.release_state)

    client.send(SetTool(CONF.tool.tool_name))
    logging.debug("Tool {} set.".format(CONF.tool.tool_name))
    client.send(SetWorkObject(CONF.wobjs.placing_wobj_name))
    logging.debug("Work object {} set.")

    # Set Acceleration
    client.send(SetAcceleration(CONF.speed_values.accel, CONF.speed_values.accel_ramp))
    logging.debug("Acceleration values set.")

    # Set Max Speed
    client.send(
        SetMaxSpeed(CONF.speed_values.speed_override, CONF.speed_values.speed_max_tcp)
    )
    logging.debug("Speed set.")

    # Initial configuration
    client.send(
        MoveToJoints(
            CONF.safe_joint_positions.start,
            EXTERNAL_AXIS_DUMMY,
            CONF.movement.speed_travel,
            CONF.movement.zone_travel,
        )
    )
    logging.debug("Sent move to safe joint position")


def shutdown_procedure(client):
    """Post fabrication procedure, end pose and closing and termination of client.

    Parameters
    ----------
    client : :class:`compas_rrc.AbbClient`
    """
    send_grip_release(client, CONF.tool.release_state)

    client.send(
        MoveToJoints(
            CONF.safe_joint_positions.end,
            EXTERNAL_AXIS_DUMMY,
            CONF.movement.speed_travel,
            CONF.movement.zone_travel,
        )
    )

    client.send_and_wait(PrintText("Finished"))

    # Close client
    client.close()
    client.terminate()


def get_settings():
    """Print and prompts user for changes to default configuration.

    Parameters
    ----------
    target_select : str ('real' or 'virtual')
        Target for script, either virtual robot controller or real. From argparse.
    """
    init(autoreset=True)

    load_or_default = questionary.select(
        "Load config or use default?", choices=["Default", "Load"], default="Default"
    ).ask()

    if load_or_default == "Load":
        conf_file = ui.open_file_dialog(
            initial_dir=DEFAULT_CONF_DIR, file_type=("YAML files", "*.yaml")
        )
        fabrication_conf.set_file(conf_file)
        logging.info("Configuration loaded from {}".format(conf_file))
    else:
        fabrication_conf.read(defaults=True, user=False)
        logging.info("Default configuration loaded from package")

    # At this point the conf is considered set, if changes needs to happen after
    # this point CONF needs to be set again. There's probably a better way though.
    global CONF
    CONF = fabrication_conf.get(abb_rcf_conf_template)

    if CONF.target is None:
        question = questionary.select(
            "Target?", choices=["Virtual robot", "Real robot"], default="Virtual robot"
        ).ask()
        CONF.target = "real" if question == "Real robot" else "virtual"

    logging.info("Target is {} controller.".format(CONF.target.upper()))

    print(Fore.CYAN + Style.BRIGHT + "Configuration")

    ui.print_conf_w_colors(fabrication_conf)

    conf_ok = questionary.confirm("Configuration correct?").ask()
    if not conf_ok:
        logging.critical("Program exited because user didn't confirm config")
        print("Exiting.")
        sys.exit()


def send_picking(client, picking_frame):
    """Send movement and IO instructions to pick up a clay bullet.

    Parameters
    ----------
    client : :class:`compas_rrc.AbbClient`
    picking_frame : compas.geometry.Frame
        Target frame to pick up bullet
    """
    if CONF.target == "virtual":
        # Custom instruction create a clay bullet in RobotStudio
        # TODO: Create bullet at picking point
        client.send(CustomInstruction("r_A057_RS_Create_Bullet"))

    # change work object before picking
    client.send(SetWorkObject(CONF.wobjs.picking_wobj_name))

    # pick bullet
    offset_picking = get_offset_frame(picking_frame, CONF.movement.offset_distance)

    client.send(
        MoveToFrame(
            offset_picking, CONF.movement.speed_travel, CONF.movement.zone_travel
        )
    )

    client.send_and_wait(
        MoveToFrame(picking_frame, CONF.movement.speed_picking, CONF.movement.zone_pick)
    )
    # TODO: Try compress bullet a little bit before picking

    send_grip_release(client, CONF.tool.grip_state)

    client.send(
        MoveToFrame(
            offset_picking, CONF.movement.speed_travel, CONF.movement.zone_travel
        )
    )


def send_placing(client, bullet):
    """Send movement and IO instructions to place a clay bullet.

    Parameters
    ----------
    client : :class:`compas_rrc.AbbClient`
    picking_frame : compas.geometry.Frame
        Target frame to pick up bullet
    """

    logging.debug("Location frame: {}".format(bullet.location))

    # change work object before placing
    client.send(SetWorkObject(CONF.wobjs.placing_wobj_name))

    # add offset placing plane to pre and post frames

    top_bullet_frame = get_offset_frame(bullet.location, bullet.height)
    offset_placement = get_offset_frame(top_bullet_frame, CONF.movement.offset_distance)

    # Safe pos then vertical offset
    for frame in bullet.trajectory_to:
        client.send(
            MoveToFrame(frame, CONF.movement.speed_travel, CONF.movement.zone_travel)
        )

    client.send(
        MoveToFrame(
            offset_placement, CONF.movement.speed_travel, CONF.movement.zone_travel
        )
    )
    client.send(
        MoveToFrame(
            top_bullet_frame, CONF.movement.speed_placing, CONF.movement.zone_place
        )
    )

    send_grip_release(client, CONF.tool.release_state)

    client.send_and_wait(
        MoveToFrame(
            bullet.placement_frame,
            CONF.movement.speed_placing,
            CONF.movement.zone_place,
        )
    )

    client.send(
        MoveToFrame(
            offset_placement, CONF.movement.speed_travel, CONF.movement.zone_travel
        )
    )

    # offset placement frame then safety frame
    for frame in bullet.trajectory_from:
        client.send(
            MoveToFrame(frame, CONF.movement.speed_travel, CONF.movement.zone_travel)
        )


def abb_run(cmd_line_args):
    """Fabrication runner, sets conf, reads json input and runs fabrication process."""
    print("\ncompas_rfc abb runner\n")

    fabrication_conf.set_args(cmd_line_args)

    timestamp_file = datetime.now().strftime("%Y%m%d-%H.%M.log")
    log_file = path.join(DEFAULT_LOG_DIR, timestamp_file)

    handlers = [logging.FileHandler(log_file, mode="a")]

    if fabrication_conf["verbose"]:
        handlers += [logging.StreamHandler(sys.stdout)]

    logging.basicConfig(
        level=logging.DEBUG if fabrication_conf["debug"] else logging.INFO,
        format="%(asctime)s:%(levelname)s:%(funcName)s:%(message)s",
        handlers=handlers,
    )

    logging.info("compas_rcf version: {}".format(__version__))
    logging.debug("argparse input: {}".format(cmd_line_args))
    logging.debug("config after set_args: {}".format(fabrication_conf))

    get_settings()
    logging.info("Fabrication configuration:\n{}".format(fabrication_conf.dump()))

    json_path = ui.open_file_dialog(initial_dir=DEFAULT_JSON_DIR)
    logging.info("Fabrication data read from: {}".format(json_path))

    clay_bullets = load_bullets(json_path)
    logging.info("{} items in clay_bullets.".format(len(clay_bullets)))

    # Create Ros Client
    ros = RosClient()

    # Create ABB Client
    abb = AbbClient(ros)
    abb.run()
    logging.debug("Connected to controller")

    # Set speed, accel, tool, wobj and move to start pos
    initial_setup(abb)

    for i, bullet in enumerate(clay_bullets):
        logging.info("Bullet {} with id {}".format(i, bullet.id))

        picking_frame = get_picking_frame(bullet.height)
        logging.debug("Picking frame: {}".format(picking_frame))

        # Pick bullet
        send_picking(abb, picking_frame)

        # Place bullet
        send_placing(abb, bullet)

    logging.info("Finished program with {} bullets.".format(len(clay_bullets)))
    shutdown_procedure(abb)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--target",
        choices=["real", "virtual"],
        help="Set fabrication runner target.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Prints logging messages to console.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Add DEBUG level messages to logfile, and print them on console if --verbose is set.",  # noqa E501
    )

    args = parser.parse_args()

    abb_run(args)
