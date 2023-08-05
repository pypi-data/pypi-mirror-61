import time
import logging
import numpy as np

from operator import attrgetter

from .parts import LeftArm, RightArm, Head


logger = logging.getLogger(__name__)


class Reachy(object):
    def __init__(self,
                 left_arm=None,
                 right_arm=None,
                 head=None):

        self._parts = []

        if left_arm is not None:
            if not isinstance(left_arm, LeftArm):
                raise ValueError('"left_arm" must be a LeftArm or None!')
            self._parts.append(left_arm)
            if left_arm.hand is not None:
                self._parts.append(left_arm.hand)
        self.left_arm = left_arm

        if right_arm is not None:
            if not isinstance(right_arm, RightArm):
                raise ValueError('"right_arm" must be a RightArm or None!')
            self._parts.append(right_arm)
            if right_arm.hand is not None:
                self._parts.append(right_arm.hand)
        self.right_arm = right_arm

        if head is not None:
            if not isinstance(head, Head):
                raise ValueError('"head" must be a Head or None!')
            self._parts.append(head)
        self.head = head

        logger.info(
            'Connected to reachy',
            extra={
                'parts': [p.name for p in self.parts],
            }
        )

    def close(self):
        logger.info(
            'Closing connection with reachy',
            extra={
                'parts': [p.name for p in self.parts],
            }
        )
        for p in self.parts:
            p.teardown()

    @property
    def parts(self):
        return self._parts

    @property
    def motors(self):
        return sum([p.motors for p in self.parts], [])

    def goto(self,
             goal_positions, duration,
             starting_point='present_position',
             wait=False, interpolation_mode='linear'):

        for i, (motor_name, goal_pos) in enumerate(goal_positions.items()):
            last = wait and (i == len(goal_positions) - 1)

            motor = attrgetter(motor_name)(self)
            motor.goto(goal_pos, duration, starting_point,
                       wait=last, interpolation_mode=interpolation_mode)

    def need_cooldown(self, temperature_limit=50):
        """ Check if Reachy needs to cool down.

        Parameters
        ----------
        temperature_limit : int, optional
                            Temperature limit (in °C) for each motor.

        Returns
        -------
        bool
            Whether or not you should let the robot cool down

        """

        motor_temperature = np.array([
            m.temperature for m in self.motors
        ])
        logger.info(
            'Checking Reachy motors temperature',
            extra={
                'temperatures': {
                    m.name: m.temperature for m in self.motors
                }
            }
        )
        return np.any(motor_temperature > temperature_limit)

    def wait_for_cooldown(self, rest_position, goto_rest_duration=5, lower_temperature=45):
        """ Wait for the robot to lower its temperature.

        The robot will first go to the specified rest position and then, it will turn all motors compliant.
        Finally, it will wait until the temperature of each motor goes below the lower_temperature parameters.

        .. note:: The robot will stay compliant at the end of the function call.
                  It is up to you, to put it back in the desired position.

        Parameters
        ----------
        rest_position: dict
                       the desired rest position for the robot
        goto_rest_duration: float
                            time in seconds to reach the rest position
        lower_temeprature: int
                           lower temperature threshold (in °C) to be reached by all motors before the end of cool down

        """
        self.goto(
            goal_positions=rest_position,
            duration=goto_rest_duration,
            wait=True,
        )

        for m in self.motors:
            m.compliant = True

        while True:
            motor_temperature = np.array([
                m.temperature for m in self.motors
            ])

            logger.warning(
                'Motors cooling down...',
                extra={
                    'temperatures': {
                        m.name: m.temperature for m in self.motors
                    }
                },
            )

            if np.all(motor_temperature < lower_temperature):
                break

            time.sleep(30)
