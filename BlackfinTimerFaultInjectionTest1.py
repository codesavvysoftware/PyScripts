#/////////////////////////////////////////////////////////////////////////////
#/// @file BlackfinTimerFaultInjectionTest1.py
#///
#/// This Python script verifies Blackfin Timer diagnostic works properly
#/// (BlackfinDiagTimerTest.cpp: RunTest()) works properly. 
#/// Blackfin system timer is tested. 
#/// Fault injection simulates that there is failure with the timer and a  
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
    'BlackfinDiagTimerTest.cpp': [ \
    # # # # # # # # # # # # # # # # # # # # # # # # #
    '''
    // Start Fault Injection Point 5
    // End Fault Injection Point 5
// Fault Injection Code Start
        m_ElapsedTimeHost = 0;           
// Fault Injection Code End
    '''
    ]
}

# Call the procedure to modify and build the test firmware code with the
# above modifications.
faultInjectionUtils.FaultInjectionUtils().ModifyAndBuildFaultInjectionFile(fileModificationsDictionary, __file__)
