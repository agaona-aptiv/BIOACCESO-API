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
#          Description: Configuration file for the Session management.
#          Enterprise: Condumex
#          SW Developer: Felipe Martinez
#          FILE DESCRIPTION
#          File: Session_ctrl_cfg.py
#          Project: EDT_AccessCTRL
#          Delivery: FIRST DELIVERY
#
#
#########################################################################################

# -----------------------------------------------
#  Imported Modules
# -----------------------------------------------
from enum import Enum


# -----------------------------------------------
#  Exported Type Declarations
# -----------------------------------------------

#  ---------- Security Access Levels ------------
class SecurityLevel(Enum):
    SEC_LEVEL_0 = 0  # No security algorithm associated
    SEC_LEVEL_1 = 1  # Security algorithm 1 associated to manufacturing security
    SEC_LEVEL_2 = 2  # Security algorithm 2 associated to admin security
    SEC_LEVEL_3 = 3  # Security algorithm 3 associated to support security

#  ---------- Supported Sessions ------------
class SessionLevel(Enum):
    SESSION_0 = 0  # Default session - Session not required
    SESSION_1 = 1  # Manufacturing session
    SESSION_2 = 2  # Admin session
    SESSION_3 = 3  # Support session


#########################################################################################
#  File Revision History (top to bottom: first revision to last revision)
#
# Oct-14-2020   Felipe Martinez
#   + DBL_72
#      - Created initial file.
#
#########################################################################################
