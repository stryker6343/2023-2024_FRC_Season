import math

import commands2
import constants
import conversions
import ctre
import wpilib
import wpimath.controller
import navx
from subsystems.swerve_wheel import SwerveWheel


class SwerveDrive(commands2.SubsystemBase):
    
    def __init__(self) -> None:

        super().__init__()
        # init motors
        self.leftFrontDirection = ctre.TalonFX(constants.kleftFrontDirectionID)
        self.leftFrontSpeed = ctre.TalonFX(constants.kleftFrontSpeedID)

        self.leftRearDirection = ctre.TalonFX(constants.kleftRearDirectionID)
        self.leftRearSpeed = ctre.TalonFX(constants.kleftRearSpeedID)

        self.rightFrontDirection = ctre.TalonFX(constants.krightFrontDirectionID)
        self.rightFrontSpeed = ctre.TalonFX(constants.krightFrontSpeedID)

        self.rightRearDirection = ctre.TalonFX(constants.krightRearDirectionID)
        self.rightRearSpeed = ctre.TalonFX(constants.krightRearSpeedID)

        # fix inverse
        self.leftFrontSpeed.setInverted(True)
        self.leftRearSpeed.setInverted(True)

        self.rightFrontSpeed.setInverted(True)
        self.rightRearSpeed.setInverted(True)

        self.leftFrontDirection.setInverted(False)
        self.leftRearDirection.setInverted(False)

        self.rightFrontDirection.setInverted(False)
        self.rightRearDirection.setInverted(False)

        # init CAN coders
        self.flCANcoder = ctre.CANCoder(constants.kflCANcoderID)
        self.rlCANcoder = ctre.CANCoder(constants.krlCANcoderID)
        self.frCANcoder = ctre.CANCoder(constants.kfrCANcoderID)
        self.rrCANcoder = ctre.CANCoder(constants.krrCANcoderID)

        # init swerve modules
        self.leftFrontSwerveModule = SwerveWheel(self.leftFrontDirection, self.leftFrontSpeed, self.flCANcoder, constants.kflCANoffset, 0.0)
        self.leftRearSwerveModule = SwerveWheel(self.leftRearDirection, self.leftRearSpeed, self.rlCANcoder, constants.krlCANoffset, 0.0)

        self.rightFrontSwerveModule = SwerveWheel(self.rightFrontDirection, self.rightFrontSpeed, self.frCANcoder, constants.kfrCANoffset, 0.0)
        self.rightRearSwerveModule = SwerveWheel(self.rightRearDirection, self.rightRearSpeed, self.rrCANcoder, constants.krrCANoffset, 0.0)

        self.wheels = [self.leftFrontSwerveModule, self.rightFrontSwerveModule, self.leftRearSwerveModule, self.rightRearSwerveModule]

        self.navX = navx.AHRS.create_spi()
        
        self.PDP = wpilib.PowerDistribution(0, wpilib.PowerDistribution.ModuleType.kCTRE)

        self.pidController = wpimath.controller.PIDController(constants.kChargeP, constants.kChargeI, constants.kChargeD)
        self.onChargeStation = False

    def turnWheel(self, module: SwerveWheel, direction: float, magnitude: float):

        self.units = conversions.convertDegreesToTalonFXUnits(direction)

        if magnitude >= 1.0:
            magnitude = 1.0
        elif magnitude <= -1.0:
            magnitude = -1.0

        # find current angle
        currentAngle = conversions.convertTalonFXUnitsToDegrees(module.directionMotor.getSelectedSensorPosition()/constants.ksteeringGearRatio)
        
        if direction < 0:
            opposAngle = direction + 180
            negAngle = 360 + direction
        elif direction > 0:
            opposAngle = direction - 180
            negAngle = direction - 360
            
        else:
            if conversions.sign(direction) == -1:
                opposAngle = -180
                negAngle = 0
            else:
                opposAngle = 180
                negAngle = 0

        # print some stats for debugging
        wpilib.SmartDashboard.putNumber(" Abs Opposite Angle -", opposAngle)
        wpilib.SmartDashboard.putNumber(" Neg Angle -", negAngle)
        # check if the joystick is in use
        if magnitude != 0.0:
            module.turn(constants.ksteeringGearRatio * conversions.convertDegreesToTalonFXUnits(conversions.getclosest(currentAngle, direction, magnitude)[0]))
            module.move(conversions.getclosest(currentAngle, direction, magnitude)[1])

            wpilib.SmartDashboard.putNumber(" Wanted Angle -", direction)
            wpilib.SmartDashboard.putNumber("Given Angle", conversions.getclosest(currentAngle, direction, magnitude)[0])
            wpilib.SmartDashboard.putNumber("Current Angle", currentAngle)

    def translate(self, direction: float, magnitude: float):

        self.turnWheel(self.leftFrontSwerveModule, direction, magnitude)
        self.turnWheel(self.leftRearSwerveModule, direction, magnitude)
        self.turnWheel(self.rightFrontSwerveModule, direction, magnitude)
        self.turnWheel(self.rightRearSwerveModule, direction, magnitude)

    def translateAndTurn(self, translationX: float, translationY: float, rotX: float):

        translationX *= -1
        rotX *= -1

        temp = translationY * math.cos(self.getYaw() * (math.pi / 180)) + translationX * math.sin(self.getYaw() * (math.pi / 180))
        translationX = -translationY * math.sin(self.getYaw() * (math.pi / 180)) + translationX * math.cos(self.getYaw() * (math.pi / 180))
        translationY = temp

        # FOR FUTURE ROBOTICS PEOPLE: These usually would require the rotX to be multiplied by (robotLength or robotWidth / 2). 
        # However, since Larry is a square, we don't use this. I'm leaving the code there just in case someone reads this and uses it.
        robotLength = 1
        robotWidth = 1

        a = translationX - rotX #* (robotLength / 2) 
        b = translationX + rotX #* (robotLength / 2)
        c = translationY - rotX #* (robotWidth / 2)
        d = translationY + rotX #* (robotWidth / 2)

        if constants.kDebug:
            wpilib.SmartDashboard.putString("ABCD", str([a, b, c, d]))

        # Wheel 1 = topRight, Wheel 2 = topLeft, Wheel 3 = bottomLeft, Wheel 4 = bottomRight
        # wheel = [speed, angle]
        roundingAm = 3

        topRight = [math.sqrt(b ** 2 + c ** 2), math.atan2(b, c) * (180/math.pi) + 180]
        topLeft = [math.sqrt(b ** 2 + d ** 2), math.atan2(b, d) * (180/math.pi) + 180]
        bottomLeft = [math.sqrt(a ** 2 + d ** 2), math.atan2(a, d) * (180/math.pi) + 180]
        bottomRight = [math.sqrt(a ** 2 + c ** 2), math.atan2(a, c) * (180/math.pi) + 180]

        new_wheels = [topRight, topLeft, bottomRight, bottomLeft]

        # Check if any wheels have a speed higher than 1. If so, divide all wheels by highest value
        highestSpeed = max(abs(topRight[0]), abs(topLeft[0]), abs(bottomLeft[0]), abs(bottomRight[0]))
        if highestSpeed != 0:
            topRight[0] /= highestSpeed
            topLeft[0] /= highestSpeed
            bottomLeft[0] /= highestSpeed
            bottomRight[0] /= highestSpeed

        runs = 0
        for wheel in self.wheels:
            if abs(new_wheels[runs][1] - wheel.getCurrentAngle()) > 90 and abs(new_wheels[runs][1] - wheel.getCurrentAngle()) < 270:
                new_wheels[runs][1] += 180
                new_wheels[runs][1] %= 360 
                new_wheels[runs][0] *= -1
                if constants.kDebug:
                    wpilib.SmartDashboard.putBoolean("Wheel " + str(runs) + " Reversed?", True)
            elif constants.kDebug:
                wpilib.SmartDashboard.putBoolean("Wheel " + str(runs) + " Reversed?", False)
            runs += 1

        wpilib.SmartDashboard.putString("topRight", str(topRight))
        wpilib.SmartDashboard.putString("topLeft", str(topLeft))
        wpilib.SmartDashboard.putString("bottomLeft", str(bottomLeft))
        wpilib.SmartDashboard.putString("bottomRight", str(bottomRight))

        # Stops robot from moving while no controller values are being returned
        if translationX == 0 and translationY == 0 and rotX == 0:
            self.stopAllMotors()

        self.turnWheel(self.leftFrontSwerveModule, topLeft[1], topLeft[0])
        self.turnWheel(self.rightFrontSwerveModule, topRight[1], topRight[0])
        self.turnWheel(self.leftRearSwerveModule, bottomLeft[1], bottomLeft[0])
        self.turnWheel(self.rightRearSwerveModule, bottomRight[1], bottomRight[0])

    def turnInPlace(self, turnPower: float):

        self.turnWheel(self.leftFrontSwerveModule, 45.0, turnPower)
        self.turnWheel(self.rightFrontSwerveModule, 135.0, turnPower)
        self.turnWheel(self.rightRearSwerveModule, 225.0, turnPower)
        self.turnWheel(self.leftRearSwerveModule, 315.0, turnPower)

    def stopAllMotors(self):

        self.leftFrontSwerveModule.stopAllMotors()
        self.leftRearSwerveModule.stopAllMotors()
        self.rightFrontSwerveModule.stopAllMotors()
        self.rightRearSwerveModule.stopAllMotors()

    def getYaw(self):

        return self.navX.getYaw()
        
    def getPitch(self):

        return self.navX.getPitch()
    
    def flushWheels(self):

        self.turnWheel(self.leftFrontSwerveModule, 0.0, 0.01)
        self.turnWheel(self.leftRearSwerveModule, 0.0, 0.01)
        self.turnWheel(self.rightFrontSwerveModule, 0.0, 0.01)
        self.turnWheel(self.rightRearSwerveModule, 0.0, 0.01)

        self.stopAllMotors()

    def getPosFromOffState(self):

        self.leftFrontSwerveModule.CANtoTalon()
        self.leftRearSwerveModule.CANtoTalon()
        self.rightFrontSwerveModule.CANtoTalon()
        self.rightRearSwerveModule.CANtoTalon()

    def reset(self):

        self.navX.reset()

        self.leftFrontDirection.setSelectedSensorPosition(0.0, constants.kPIDLoopIdx, constants.ktimeoutMs)
        self.leftFrontSpeed.setSelectedSensorPosition(0.0, constants.kPIDLoopIdx, constants.ktimeoutMs)

        self.leftRearDirection.setSelectedSensorPosition(0.0, constants.kPIDLoopIdx, constants.ktimeoutMs)
        self.leftRearSpeed.setSelectedSensorPosition(0.0, constants.kPIDLoopIdx, constants.ktimeoutMs)

        self.rightFrontDirection.setSelectedSensorPosition(0.0, constants.kPIDLoopIdx, constants.ktimeoutMs)
        self.rightFrontSpeed.setSelectedSensorPosition(0.0, constants.kPIDLoopIdx, constants.ktimeoutMs)

        self.rightRearDirection.setSelectedSensorPosition(0.0, constants.kPIDLoopIdx, constants.ktimeoutMs)
        self.rightRearSpeed.setSelectedSensorPosition(0.0, constants.kPIDLoopIdx, constants.ktimeoutMs)
