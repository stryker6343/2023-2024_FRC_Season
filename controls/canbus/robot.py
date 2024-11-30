"""
    Motor Tester control code
"""

import wpilib
import wpilib.drive

import phoenix5


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        self.timer = wpilib.Timer()
        self.can = wpilib.CAN(1)

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.timer.reset()
        self.timer.start()

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        self.can.writePacket(b"x\01x\23x\45x\67", 1)

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        pass


if __name__ == "__main__":
    wpilib.run(MyRobot)
