'''
Created on October, 2020
@author: Felipe Martinez
'''
#########################################################################################
#  COPYRIGHT 2020
#  \verbatim
#                 This software is copyright protected and proprietary to Condumex.
#                 All other rights remain with Condumex
#
#  \endverbatim
#  LICENSE
#          Module: Proteus
#          Description: Configuration file for the Proteus Handler.
#          Enterprise: Condumex
#          SW Developer: Felipe Martinez
#          FILE DESCRIPTION
#          File: Proteus_Handler_cfg.py
#          Project: EDT_AccessCTRL
#          Delivery: FIRST DELIVERY
#
#
#########################################################################################

# -----------------------------------------------
#  Imported Modules
# -----------------------------------------------
import mod_ProTeUS.cfg.Manufacturing_Services_cfg as man
import mod_ProTeUS.cfg.Specific_Services_cfg as spec

# -----------------------------------------------
#  Exported Type Declarations
# -----------------------------------------------
EXPIRATION_TIME = (60000 * 4)  # 4 Min in Millis

#  ---------- Supported Services ------------
Supported_Services_List = {
    0x10: man.Manufacturing_SubServices_List,
    0x54: spec.Specific_Subservices_List
}

#########################################################################################
#  File Revision History (top to bottom: first revision to last revision)
#
# Oct-14-2020   Felipe Martinez
#   + DBL_72
#      - Created initial file.
#
#########################################################################################
