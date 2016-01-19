#/////////////////////////////////////////////////////////////////////////////
#/// @file ApexInternalRamAddressLineDiagnosticFaultInjectionTest1.py
#///
#/// This Python script verifies that when two complementary patterns are
#/// inserted into RAM (target addresses differ with one bit) and wrong
#/// values are read back from RAM during address line test,
#/// the test will cause exception. Failure is caused by injection of code
#/// causing these two addresses (r1 and r2 registers) to be equal.
#/// The test should fail at power-up.
#///
#/// @if REVISION_HISTORY_INCLUDED
#/// @par Edit History
#/// pgrzywn 30-SEP-2013 Created.
#/// pszramo 21-OCT-2013 Modified to match updated faultInjectionUtils.
#/// mstasia 07-NOV-2013 Description modified.
#/// pszramo 17-DEC-2013 Adjustments after MISRA fixes.
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
    'ApexDiagRAMassy.s': [ \
    # # # # # # # # # # # # # # # # # # # # # # # # #
    '''
    ;Start Fault Injection Point 3
    ;End Fault Injection Point 3
    ;Fault Injection Code Start
        MOV     r2, r1
    ;Fault Injection Code End
    '''
    ]
}

# Call the procedure to modify and build the test firmware code with the
# above modifications.
faultInjectionUtils.FaultInjectionUtils().ModifyAndBuildFaultInjectionFile(fileModificationsDictionary, __file__)