#/////////////////////////////////////////////////////////////////////////////
#/// @file ApexInternalRamScrubberDiagnosticFaultInjectionTest1.py
#///
#/// This Python script verifies that Apex scrubber diagnostic is correctly
#/// faulting when scrubbing fails. It does it in two steps. First it modifies
#/// value of read ECC register to point to an error in first data memory
#/// address. After this value should be scrubbed. Than the second step is
#/// performed. Read ECC register value is once again modified to the same value
#/// as in first step - signalling error in first data memory cell.
#/// Then it is verified Apex faults due to uncorrectable ECC error.
#///
#/// @if REVISION_HISTORY_INCLUDED
#/// @par Edit History
#/// pgrzywn 30-SEP-2013 Created.
#/// spolke  03-OCT-2013 Comment updated.
#/// pszramo 21-OCT-2013 Modified to match updated faultInjectionUtils.
#/// pszramo 13-DEC-2013 Adjustments after MISRA fixes.
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
    ;Start Fault Injection Point 5
    ;End Fault Injection Point 5
        ;Fault Injection Code Start
        MOV     r1, #0
        ORR     r1, r1, #DGN_ECC_ERR_MASK_SINGLE
        ;Fault Injection Code End
    ''',
    # # # # # # # # # # # # # # # # # # # # # # # # #
    '''
    ;Start Fault Injection Point 6
    ;End Fault Injection Point 6
        ;Fault Injection Code Start
        MOV     r1, #0
        ORR     r1, r1, #DGN_ECC_ERR_MASK_SINGLE
        ;Fault Injection Code End
    '''
    ]
}

# Call the procedure to modify and build the test firmware code with the
# above modifications.
faultInjectionUtils.FaultInjectionUtils().ModifyAndBuildFaultInjectionFile(fileModificationsDictionary, __file__)