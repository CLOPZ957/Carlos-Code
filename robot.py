
#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import wpilib
import wpilib.drive
import rev

kY = 4 #Y Button
kX = 3 #X Button
kB = 2 #B Button
kA = 1 #A Button
kLB = 5 #LB Button
kRB = 6 #RB Button
kBack = 7 #Back Button
kStart = 8 #Start Button
kRT = 9 #Right Trigger Button

class MyRobot(wpilib.TimedRobot):
    """Main robot class"""

    def robotInit(self):
        """Robot-wide initialization code should go here"""


        self.joystick = wpilib.XboxController(0)
        
        self.lf_motor = wpilib.PWMSparkMax(4) 
        self.lr_motor = wpilib.PWMSparkMax(3)
        self.rf_motor = wpilib.PWMSparkMax(9)
        self.rr_motor = wpilib.PWMSparkMax(2)

        l_motor = wpilib.MotorControllerGroup(self.lf_motor, self.lr_motor)
        r_motor = wpilib.MotorControllerGroup(self.rf_motor, self.rr_motor)

        l_motor.setInverted(True)

        self.drive = wpilib.drive.DifferentialDrive(l_motor, r_motor)

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.timer.restart()

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""

        # Drive for two seconds
        if self.timer.get() < 2.0:
            # Drive forwards half speed, make sure to turn input squaring off
            self.robotDrive.arcadeDrive(0.5, 0, squareInputs=False)
        else:
            self.robotDrive.stopMotor()  # Stop robot

    def teleopPeriodic(self):
        """Called when operation control mode is enabled"""
         #TEST THIS LATER (MOVEMENT ADJUSTMENTS)
        #drive motors
        rightTrigger = self.joystick.getRightTriggerAxis()    #New (test) code
        #RightY = self.joystick.getRightY()    #original code
        LeftX = self.joystick.getLeftX()
        leftTrigger = self.joystick.getLeftTriggerAxis()
        # print(f"RightY: {RightY} - LeftY: {LeftY}")

        #exponential movement
        if(rightTrigger > 0):
            rightTrigger = (rightTrigger**-4)*-1
        else:
            rightTrigger = (rightTrigger**4)

        if(leftTrigger > 0):
            rightTrigger = (rightTrigger**0)
        else:
            rightTrigger = (rightTrigger**4)*-1

        if(rightTrigger == 0):
            leftTrigger = (leftTrigger**4)*-1
        else:
            leftTrigger = (leftTrigger**4)*1
        
        if(LeftX < 0):
            LeftX = (LeftX**4)*-1
        else:
            LeftX = (LeftX**4)

        rightTrigger = rightTrigger *1.5        
        leftTrigger = leftTrigger *.9  
        LeftX = LeftX *.9     
        #this makes it turn slower
        if((rightTrigger < 0.1 and rightTrigger > -0.1) and (LeftX >= 0.5 or LeftX <= -0.5)):
            LeftX = LeftX * 0.66
        elif((LeftX < 0.1 and LeftX > -0.1) and (rightTrigger >= 0.5 or rightTrigger <=-0.5)):
            rightTrigger = rightTrigger * 0.66
        print(f"rightTrigger: {rightTrigger} - LeftX: {LeftX}")

        if((leftTrigger < 0.1 and leftTrigger > -0.1) and (LeftX >= 0.5 or LeftX <= -0.5)):
            LeftX = LeftX * 0.66
        elif((LeftX < 0.1 and LeftX > -0.1) and (leftTrigger >= 0.5 or leftTrigger <=-0.5)):
            leftTrigger = leftTrigger * 0.66
        print(f"leftTrigger: {leftTrigger} - LeftX: {LeftX}")

        self.drive.arcadeDrive(rightTrigger, LeftX, leftTrigger) # new arcade input

    def disabledInit(self) -> None:
        # This just makes sure that our simulation code knows that the motor is off
        self.lf_motor.set(0)
        self.lr_motor.set(0)
        self.rf_motor.set(0)
        self.rr_motor.set(0)
