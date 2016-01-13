#/////////////////////////////////////////////////////////////////////////////
#/// @file BlackfinInstructionRamFaultInjectionTest1.py
#///
#/// This Python script verifies Blackfin Instruction Ram diagnostic works properly
#/// (BlackfinDiagInstructionRam.cpp: RunInstructionRamTestIteration()) works properly. 
#/// Instruction RAM bytes are tested by writing preset patterns to RAM. 
#/// Fault injection simulates a failure with Instruction RAM and returns a
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
    'BlackfinDiagInstructionRam.cpp': [ \
    # # # # # # # # # # # # # # # # # # # # # # # # #
    '''
    // Start Fault Injection Point 3
    // End Fault Injection Point 3
// Fault Injection Code Start
       hasError = TRUE;
// Fault Injection Code End
    '''
    ]
}

# Call the procedure to modify and build the test firmware code with the
# above modifications.
faultInjectionUtils.FaultInjectionUtils().ModifyAndBuildFaultInjectionFile(fileModificationsDictionary, __file__)
