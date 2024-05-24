"""
    Motor Tester control code
"""

import wpilib
import wpilib.drive

from phoenix6.controls import DutyCycleOut
from phoenix6.hardware import TalonFX
from phoenix6.configs.talon_fx_configs import InvertedValue, NeutralModeValue, TalonFXConfiguration


SPEED = 0.3


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        self.upper_left_motor = TalonFX(16)
        self.lower_left_motor = TalonFX(17)
        self.upper_right_motor = TalonFX(18)
        self.lower_right_motor = TalonFX(19)

        clockwise_config = TalonFXConfiguration()
        clockwise_config.motor_output.with_neutral_mode(NeutralModeValue.COAST)
        clockwise_config.feedback.sensor_to_mechanism_ratio = 1
        clockwise_config.inverted = 1

        # counter_clockwise_config = TalonFXConfiguration()
        # counter_clockwise_config.motor_output.with_neutral_mode(NeutralModeValue.COAST)
        # counter_clockwise_config.feedback.sensor_to_mechanism_ratio = 1
        # counter_clockwise_config.inverted = 0

        self.upper_left_motor.configurator.apply(clockwise_config)
        self.lower_left_motor.configurator.apply(clockwise_config)
        self.upper_right_motor.configurator.apply(clockwise_config)
        self.lower_right_motor.configurator.apply(clockwise_config)

        self.upper_left_request = DutyCycleOut(0.0)
        self.upper_right_request = DutyCycleOut(0.0)
        self.lower_left_request = DutyCycleOut(0.0)
        self.lower_right_request = DutyCycleOut(0.0)

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.upper_left_motor.set_control(self.upper_left_request.with_output(-SPEED))
        self.lower_left_motor.set_control(self.lower_left_request.with_output(SPEED))
        self.upper_right_motor.set_control(self.upper_right_request.with_output(SPEED))
        self.lower_right_motor.set_control(self.lower_right_request.with_output(-SPEED))

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        pass

    def disabledInit(self):
        """This function is called at the end of autonomous mode."""
        self.upper_left_motor.set_control(self.upper_left_request.with_output(0.0))
        self.lower_left_motor.set_control(self.lower_left_request.with_output(0.0))
        self.upper_right_motor.set_control(self.upper_right_request.with_output(0.0))
        self.lower_right_motor.set_control(self.lower_right_request.with_output(0.0))

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        pass


if __name__ == "__main__":
    wpilib.run(MyRobot)
