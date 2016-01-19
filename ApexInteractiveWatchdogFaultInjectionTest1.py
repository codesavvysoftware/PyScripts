#/////////////////////////////////////////////////////////////////////////////
#/// @file ApexInteractiveWatchdogFaultInjectionTest1.py
#///
#/// This Python script verifies that when code is modified on the Apex2
#/// side (only) to cause Apex2 to stop responding to watchdog requests
#/// from the DSP (while Apex2 continues to service its own hardware watchdog),
#/// the module should fault, based on major non-recoverable fault action
#/// from the DSP, since it has not seen the response from Apex2.
#///
#/// @if REVISION_HISTORY_INCLUDED
#/// @par Edit History
#/// kolat   05-Jan-2016 Created.
#/// @endif
#///
#/// @par Copyright (c) 2016 Rockwell Automation Technologies, Inc.  All rights reserved.
#///
#/////////////////////////////////////////////////////////////////////////////

import faultInjectionUtils

#------------------------------------------------------------------------------
# Here is the list of files to be modified by this script, along with
# blocks of new code (first two lines of block are start and end text to
# search for and replace between) for each of the modified files.
fileModificationsDictionary = { \
    'apxWatchdog.cpp': [ \
    # # # # # # # # # # # # # # # # # # # # # # # # # 
    '''
            // Start Fault Injection Point 1
            // End Fault Injection Point 1
            // Fault Injection Code Start
            // Service the host watchdog for 250 x 50ms scans (12.5s) before stopping
            if ( HI_ApexParam.pWatchdog->parts.asic < 250 )
            {
            	HI_ApexParam.pWatchdog->parts.asic = HI_ApexParam.pWatchdog->parts.host;
            }
            // Fault Injection Code End
    '''
    ]
}

# Call the procedure to modify and build the test firmware code with the
# above modifications.
faultInjectionUtils.FaultInjectionUtils().ModifyAndBuildFaultInjectionFile(fileModificationsDictionary, __file__)