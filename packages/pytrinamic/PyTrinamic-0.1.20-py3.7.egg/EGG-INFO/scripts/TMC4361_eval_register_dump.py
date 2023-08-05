#!/usr/bin/env python3
'''
Dump all register values of the TMC4361 IC.

The connection to a Landungsbrücke is established over USB. TMCL commands are
used for communicating with the IC.

Created on 07.11.2019

@author: JM
'''
import PyTrinamic
from PyTrinamic.connections.ConnectionManager import ConnectionManager
from PyTrinamic.evalboards.TMC4361_eval import TMC4361_eval

PyTrinamic.showInfo()

connectionManager = ConnectionManager()
myInterface = connectionManager.connect()
TMC4361 = TMC4361_eval(myInterface)

print("GENERAL_CONF:                             0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.GENERAL_CONF)))
print("REFERENCE_CONF:                           0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.REFERENCE_CONF)))
print("START_CONF:                               0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.START_CONF)))
print("INPUT_FILT_CONF:                          0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.INPUT_FILT_CONF)))
print("SPI_OUT_CONF:                             0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.SPI_OUT_CONF)))
print("CURRENT_CONF:                             0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.CURRENT_CONF)))
print("SCALE_VALUES:                             0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.SCALE_VALUES)))
print("ENC_IN_CONF:                              0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.ENC_IN_CONF)))
print("ENC_IN_DATA:                              0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.ENC_IN_DATA)))
print("ENC_OUT_DATA:                             0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.ENC_OUT_DATA)))
print("STEP_CONF:                                0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.STEP_CONF)))
print("SPI_STATUS_SELECTION:                     0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.SPI_STATUS_SELECTION)))
print("EVENT_CLEAR_CONF:                         0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.EVENT_CLEAR_CONF)))
print("INTR_CONF:                                0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.INTR_CONF)))
print("EVENTS:                                   0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.EVENTS)))
print("STATUS:                                   0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.STATUS)))
print("STP_LENGTH_ADD__DIR_SETUP_TIME:           0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.STP_LENGTH_ADD__DIR_SETUP_TIME)))
print("START_OUT_ADD:                            0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.START_OUT_ADD)))
print("GEAR_RATIO:                               0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.GEAR_RATIO)))
print("START_DELAY:                              0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.START_DELAY)))
print("CLK_GATING_DELAY:                         0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.CLK_GATING_DELAY)))
print("STDBY_DELAY:                              0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.STDBY_DELAY)))
print("FREEWHEEL_DELAY:                          0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.FREEWHEEL_DELAY)))
print("VDRV_SCALE_LIMIT__PWM_VMAX:               0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.VDRV_SCALE_LIMIT__PWM_VMAX)))
print("UP_SCALE_DELAY__CL_UPSCALE_DELAY:         0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.UP_SCALE_DELAY__CL_UPSCALE_DELAY)))
print("HOLD_SCALE_DELAY__CL_DNSCALE_DELAY:       0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.HOLD_SCALE_DELAY__CL_DNSCALE_DELAY)))
print("DRV_SCALE_DELAY:                          0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.DRV_SCALE_DELAY)))
print("BOOST_TIME:                               0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.BOOST_TIME)))
print("CL_ANGLES:                                0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.CL_ANGLES)))
print("SPI_SWITCH_VEL__DAC_ADDR:                 0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.SPI_SWITCH_VEL__DAC_ADDR)))
print("HOME_SAFETY_MARGIN:                       0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.HOME_SAFETY_MARGIN)))
print("PWM_FREQ__CHOPSYNC_DIV:                   0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.PWM_FREQ__CHOPSYNC_DIV)))
print("RAMPMODE:                                 0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.RAMPMODE)))
print("XACTUAL:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.XACTUAL)))
print("VACTUAL:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.VACTUAL)))
print("AACTUAL:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.AACTUAL)))
print("VMAX:                                     0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.VMAX)))
print("VSTART:                                   0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.VSTART)))
print("VSTOP:                                    0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.VSTOP)))
print("VBREAK:                                   0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.VBREAK)))
print("AMAX:                                     0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.AMAX)))
print("DMAX:                                     0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.DMAX)))
print("ASTART:                                   0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.ASTART)))
print("DFINAL:                                   0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.DFINAL)))
print("DSTOP:                                    0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.DSTOP)))
print("BOW1:                                     0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.BOW1)))
print("BOW2:                                     0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.BOW2)))
print("BOW3:                                     0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.BOW3)))
print("BOW4:                                     0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.BOW4)))
print("CLK_FREQ:                                 0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.CLK_FREQ)))
print("POS_COMP:                                 0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.POS_COMP)))
print("VIRT_STOP_LEFT:                           0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.VIRT_STOP_LEFT)))
print("VIRT_STOP_RIGHT:                          0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.VIRT_STOP_RIGHT)))
print("X_HOME:                                   0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.X_HOME)))
print("X_LATCH__REV_CNT__X_RANGE:                0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.X_LATCH__REV_CNT__X_RANGE)))
print("XTARGET:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.XTARGET)))
print("X_PIPE0:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.X_PIPE0)))
print("X_PIPE1:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.X_PIPE1)))
print("X_PIPE2:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.X_PIPE2)))
print("X_PIPE3:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.X_PIPE3)))
print("X_PIPE4:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.X_PIPE4)))
print("X_PIPE5:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.X_PIPE5)))
print("X_PIPE6:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.X_PIPE6)))
print("X_PIPE7:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.X_PIPE7)))
print("SH_REG0:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.SH_REG0)))
print("SH_REG0:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.SH_REG0)))
print("SH_REG0:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.SH_REG0)))
print("SH_REG0:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.SH_REG0)))
print("SH_REG0:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.SH_REG0)))
print("SH_REG0:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.SH_REG0)))
print("SH_REG0:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.SH_REG0)))
print("SH_REG0:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.SH_REG0)))
print("SH_REG0:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.SH_REG0)))
print("SH_REG0:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.SH_REG0)))
print("SH_REG0:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.SH_REG0)))
print("SH_REG0:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.SH_REG0)))
print("SH_REG0:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.SH_REG0)))
print("SH_REG0:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.SH_REG0)))
print("Freeze_Registers:                         0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.Freeze_Registers)))
print("ENC_POS:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.ENC_POS)))
print("ENC_LATCH__ENC_RESET_VAL:                 0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.ENC_LATCH__ENC_RESET_VAL)))
print("ENC_POS_DEV__CL_TR_TOLERANCE:             0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.ENC_POS_DEV__CL_TR_TOLERANCE)))
print("ENC_POS_DEV_TOL:                          0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.ENC_POS_DEV_TOL)))
print("ENC_IN_RES__ENC_CONST:                    0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.ENC_IN_RES__ENC_CONST)))
print("ENC_OUT_RES:                              0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.ENC_OUT_RES)))
print("SER_CLK_IN_HIGH__LOW:                     0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.SER_CLK_IN_HIGH__LOW)))
print("SSI_IN_CLK_DELAY__SSI_IN_WTIME:           0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.SSI_IN_CLK_DELAY__SSI_IN_WTIME)))
print("SER_PTIME:                                0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.SER_PTIME)))
print("CL_OFFSET:                                0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.CL_OFFSET)))
print("PID_VEL__PID_P__CL_VMAX_CALC_P:           0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.PID_VEL__PID_P__CL_VMAX_CALC_P)))
print("PID_ISUM_RD__PID_I__CL_VMAX_CALC_I:       0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.PID_ISUM_RD__PID_I__CL_VMAX_CALC_I)))
print("PID_D__CL_DELTA_P:                        0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.PID_D__CL_DELTA_P)))
print("PID_E__PID_I_CLIP__PID_D_CLKDIV:          0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.PID_E__PID_I_CLIP__PID_D_CLKDIV)))
print("PID_DV_CLIP:                              0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.PID_DV_CLIP)))
print("PID_TOLERANCE__CL_TOLERANCE:              0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.PID_TOLERANCE__CL_TOLERANCE)))
print("FS_VEL__DC_VEL__CL_VMIN_EMF:              0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.FS_VEL__DC_VEL__CL_VMIN_EMF)))
print("DC_TIME__DC_SG__DC_BLKTIME__CL_VADD_EMF:  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.DC_TIME__DC_SG__DC_BLKTIME__CL_VADD_EMF)))
print("DC_LSPTM__ENC_VEL_ZERO:                   0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.DC_LSPTM__ENC_VEL_ZERO)))
print("ENC_VMEAN__SER_ENC_VARIATION__CL_CYCLE:   0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.ENC_VMEAN__SER_ENC_VARIATION__CL_CYCLE)))
print("V_ENC:                                    0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.V_ENC)))
print("V_ENC_MEAN:                               0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.V_ENC_MEAN)))
print("VSTALL_LIMIT:                             0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.VSTALL_LIMIT)))
print("ADDR_TO_ENC:                              0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.ADDR_TO_ENC)))
print("DATA_TO_ENC:                              0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.DATA_TO_ENC)))
print("ADDR_FROM_ENC:                            0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.ADDR_FROM_ENC)))
print("DATA_FROM_ENC:                            0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.DATA_FROM_ENC)))
print("COVER_LOW:                                0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.COVER_LOW)))
print("COVER_HIGH__POLLING_REG:                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.COVER_HIGH__POLLING_REG)))
print("COVER_DRV_LOW:                            0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.COVER_DRV_LOW)))
print("COVER_DRV_HIGH:                           0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.COVER_DRV_HIGH)))
print("MSLUT_0:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.MSLUT_0)))
print("MSLUT_1:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.MSLUT_1)))
print("MSLUT_2:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.MSLUT_2)))
print("MSLUT_3:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.MSLUT_3)))
print("MSLUT_4:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.MSLUT_4)))
print("MSLUT_5:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.MSLUT_5)))
print("MSLUT_6:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.MSLUT_6)))
print("MSLUT_7:                                  0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.MSLUT_7)))
print("MSLUTSEL:                                 0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.MSLUTSEL)))
print("MSCNT:                                    0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.MSCNT)))
print("CURRENTA__B:                              0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.CURRENTA__B)))
print("CURRENTA__B_SPI:                          0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.CURRENTA__B_SPI)))
print("SCALE_PARAM__CIRCULAR_DEC:                0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.SCALE_PARAM__CIRCULAR_DEC)))
print("ENC_COMP_:                                0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.ENC_COMP_)))
print("START_SIN__DAC_OFFSET:                    0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.START_SIN__DAC_OFFSET)))
print("VERSION_NO:                               0x{0:08X}".format(TMC4361.readRegister(TMC4361.registers.VERSION_NO)))

myInterface.close()