#/////////////////////////////////////////////////////////////////////////////
#/// @file BlackfinDataRamAsmFaultInjectionTest1.py
#///
#/// This Python script verifies Blackfin Data Ram diagnostic works properly
#/// (BlackfinDiagDataRam.cpp: TestAByte()) works properly. 
#/// RAM bytes are tested by writing preset patterns to RAM. 
#/// Fault injection simulates that RAM fails and returns
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
    'BlackfinDataRamTestByte.s': [ \
    # # # # # # # # # # # # # # # # # # # # # # # # #
    '''
    // Start Fault Injection Point 1
    // End Fault Injection Point 1
// Fault Injection Code Start
  cc = r0 < r4;
// Fault Injection Code End
    '''
    ]
}

# Call the procedure to modify and build the test firmware code with the
# above modifications.
faultInjectionUtils.FaultInjectionUtils().ModifyAndBuildFaultInjectionFile(fileModificationsDictionary, __file__)
