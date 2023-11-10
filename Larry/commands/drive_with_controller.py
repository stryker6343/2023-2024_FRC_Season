import math
import typing

import commands2
import constants
import conversions
import wpilib
from subsystems.swerve_drive import SwerveDrive


class DriveWithController(commands2.CommandBase):
    def __init__(self, swerveDrive: SwerveDrive, x: typing.Callable[[], float], y: typing.Callable[[], float],
                 rightx: typing.Callable[[], float]) -> None:
        
        super().__init__()
        self.drive = swerveDrive
        self.x = x
        self.y = y
        self.rightx = rightx
        self.addRequirements([self.drive])
        self.drive.reset()
        self.drive.getPosFromOffState()

    def initialize(self) -> None:
        
        self.drive.navX.reset()

    def execute(self) -> None:

        translationX = conversions.deadband(self.x(), constants.kdeadband)
        translationY = conversions.deadband(self.y(), constants.kdeadband)
        rotationX = conversions.deadband(self.rightx(), constants.kdeadband)

        self.drive.translateAndTurn(translationX, translationY, rotationX)
        if constants.kDebug:
            wpilib.SmartDashboard.putNumber("translationX", translationX)
            wpilib.SmartDashboard.putNumber("translationY", translationY)
            wpilib.SmartDashboard.putNumber("rotationX", rotationX)

    def end(self, interrupted: bool) -> None:
        
        self.drive.stopAllMotors()

    def isFinished(self) -> bool:
        
        return False