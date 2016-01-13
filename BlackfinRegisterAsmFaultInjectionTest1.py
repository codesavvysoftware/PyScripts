#/////////////////////////////////////////////////////////////////////////////
#/// @file BlackfinRegisterAsmFaultInjectionTest1.py
#///
#/// This Python script verifies Blackfin Register diagnostic works properly
#/// (BlackfinDiagRegistersTest.cpp: BlackfinDiagRegSanityChk()) works properly. 
#/// Blackfin processor registers are tested. 
#/// Fault injection simulates that there is failure with the registers and a  
#/// returns test failed status.
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
    'BlackfinDiagRegister.s': [ \
    # # # # # # # # # # # # # # # # # # # # # # # # #
    '''
    // Start Fault Injection Point 4
    // End Fault Injection Point 4
// Fault Injection Code Start
    cc = r0 < r2;
// Fault Injection Code End
    '''
    ]
}

# Call the procedure to modify and build the test firmware code with the
# above modifications.
faultInjectionUtils.FaultInjectionUtils().ModifyAndBuildFaultInjectionFile(fileModificationsDictionary, __file__)
