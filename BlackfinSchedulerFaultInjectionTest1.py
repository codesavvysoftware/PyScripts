#/////////////////////////////////////////////////////////////////////////////
#/// @file BlackfinSchedulerFaultInjectionTest1.py
#///
#/// This Python script verifies Blackfin Scheduler diagnostic works properly
#/// (DiagnosticScheduler.cpp: DetermineCurrentSchedulerState()) works properly. 
#/// Blackfin scheduler is tested. 
#/// Fault injection simulates that there is failure with the scheduler and a  
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
    'DiagnosticScheduler.cpp': [ \
    # # # # # # # # # # # # # # # # # # # # # # # # #
    '''
    // Start Fault Injection Point 6
    // End Fault Injection Point 6
// Fault Injection Code Start
                m_CurrentSchedulerState = MAX_PERIOD_EXPIRED_INCOMPLETE_TESTING;          
// Fault Injection Code End
    '''
    ],
    'BlackfinDiagRuntime.cpp': [ \
    # # # # # # # # # # # # # # # # # # # # # # # # #
    '''
    // Start Fault Injection Point 7
    // End Fault Injection Point 7
// Fault Injection Code Start
            static const UINT32 PERIOD_FOR_ALL_DIAGNOSTICS_COMPLETED_MS     = 60 * 1000; // 1 minute
//WithoutFaultInjection
//            static const UINT32 PERIOD_FOR_ALL_DIAGNOSTICS_COMPLETED_MS     = 4 * 60 * 60 * 1000; // 4 hours for now, number of milleseconds in 4 hours
// Fault Injection Code End
    '''
    ]
}

# Call the procedure to modify and build the test firmware code with the
# above modifications.
faultInjectionUtils.FaultInjectionUtils().ModifyAndBuildFaultInjectionFile(fileModificationsDictionary, __file__)
