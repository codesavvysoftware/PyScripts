#/////////////////////////////////////////////////////////////////////////////
#/// @file ApexInternalRamDataDiagnosticWithShadowRamTestsFaultInjectionTest1.py
#///
#/// This Python script verifies that Apex data pattern testing diagnostic is
#/// correctly checking pattern read. It alters value read form memory (which is
#/// supposed to be one of the pattern values) and shifts it right by one bit.
#/// Then it is verified Apex faults due to read back pattern value is
#/// incorrect. The injection code is inserted during start-up to simulate
#/// stuck-at fault.
#///
#/// @if REVISION_HISTORY_INCLUDED
#/// @par Edit History
#/// pgrzywn 30-SEP-2013 Created.
#/// spolke  03-OCT-2013 Comment updated.
#/// pszramo 21-OCT-2013 Modified to match updated faultInjectionUtils.
#/// pszramo 08-NOV-2013 Updated description.
#/// pszramo 06-DEC-2013 Adjustments after MISRA fixes.
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
    ;Start Fault Injection Point 1
    ;End Fault Injection Point 1
        ;Fault Injection Code Start
        MOV     r10, r10, ROR #1
        ;Fault Injection Code End
    '''
    ]
}

# Call the procedure to modify and build the test firmware code with the
# above modifications.
faultInjectionUtils.FaultInjectionUtils().ModifyAndBuildFaultInjectionFile(fileModificationsDictionary, __file__)