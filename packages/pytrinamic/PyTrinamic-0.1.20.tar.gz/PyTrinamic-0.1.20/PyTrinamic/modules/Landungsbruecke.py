'''
Created on 20.12.2019

@author: JM
'''

#import ?

#from ?

class Landungsbruecke():

    def __init__(self, connection):

    drvClass = driverControllers[id] # DriverController Class ID
    mcClasss = motionControllers[id] # MotionController Class ID

        if mcClass:
            MC = mcClass(myInterface)
        
        # -> assign correct MC/DRV
        if (id == ...)
            MC = TMC5130_Eval(connection)
        else if id == ...:
            MC = TMC4671_Eval(connection)
        else if id == ...:

            MC = TMC4361A_Eval(connection)


    GP_VitalSignsErrorMask  = 1
    GP_DriversEnable        = 2
    GP_DebugMode            = 3
    GP_BoardAssignment      = 4
    GP_HWID                 = 5
    GP_PinState             = 6