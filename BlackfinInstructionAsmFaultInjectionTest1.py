#/////////////////////////////////////////////////////////////////////////////
#/// @file BlackfinInstructionAsmFaultInjectionTest1.py
#///
#/// This Python script verifies Blackfin Instruction Test diagnostic works properly
#/// (BlackfinDiagInstructionsTest.cpp: BlackfinDiagInstrTest()) works properly. 
#/// Instructions are tested by executing instructions run as part of the firmware
#/// but not executed by the diagnostic code. 
#/// Fault injection simulates that the instruction fails and returns a 
#/// test failed status.
#///
#/// @if REVISION_HISTORY_INCLUDED
#/// @par Edit History
#/// thaley1 06-JAN-2016 Initial version.
#/// @endif
#///
#/// @par Copyright (c) 2016 Rockwell Automation Technologies, Inc. All rights reserved.
#///
#/////////////////////////////////////////////////////////////////////////////

import faultInjectionUtils

#------------------------------------------------------------------------------
# Here is the list of files to be modified by this script, along with
# blocks of new code (first two lines of block are start and end text to
# search for and replace between) for each of the modified files.
fileModificationsDictionary = { \
    'BlackfinDiagInstruction.s': [ \
    # # # # # # # # # # # # # # # # # # # # # # # # #
    '''
    // Start Fault Injection Point 2
    // End Fault Injection Point 2
// Fault Injection Code Start
  cc = r0 < r1;
// Fault Injection Code End
    '''
    ]
}

# Call the procedure to modify and build the test firmware code with the
# above modifications.
faultInjectionUtils.FaultInjectionUtils().ModifyAndBuildFaultInjectionFile(fileModificationsDictionary, __file__)
