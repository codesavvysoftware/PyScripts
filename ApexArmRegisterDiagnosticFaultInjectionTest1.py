#/////////////////////////////////////////////////////////////////////////////
#/// @file ApexArmRegisterDiagnosticFaultInjectionTest1.py
#///
#/// This Python script verifies that Apex register test
#/// (ApexDiagArm.cpp: TestRegister()) works properly.
#/// Register content is moved to another register
#/// (register read operation takes place)
#/// then teq instruction checks of mov was successful,
#/// result of teq is changed to simulate fault. Since there
#/// is no way to force the mov instruction to act wrong,
#/// the teq instruction result is changed.
#///
#/// @if REVISION_HISTORY_INCLUDED
#/// @par Edit History
#/// pgrzywn 30-SEP-2013 Created.
#/// mstasia 03-OCT-2013 Description added.
#/// pszramo 21-OCT-2013 Modified to match updated faultInjectionUtils.
#/// fzembok 05-NOV-2013 Fault injection point fixes.
#/// pszramo 09-DEC-2013 Adjustments after MISRA fixes.
#/// @endif
#///
#/// @par Copyright (c) 2013 Rockwell Automation Technologies, Inc.  All rights reserved.
#///
#/////////////////////////////////////////////////////////////////////////////

import faultInjectionUtils

#------------------------------------------------------------------------------
# Here is the list of files to be modified by this script, along with
# blocks of new code (first two lines of block are start and end text to
# search for and replace between) for each of the modified files.
fileModificationsDictionary = { \
    'ApexDiagArmAsm.s': [ \
    # # # # # # # # # # # # # # # # # # # # # # # # #
    '''
    ;; Start Fault Injection Point 4
    ;; End Fault Injection Point 4
;; Fault Injection Code Start
        BEQ     ArmRegisterR0ReturnFalse
;; Fault Injection Code End
    '''
    ]
}

# Call the procedure to modify and build the test firmware code with the
# above modifications.
faultInjectionUtils.FaultInjectionUtils().ModifyAndBuildFaultInjectionFile(fileModificationsDictionary, __file__)