#/////////////////////////////////////////////////////////////////////////////
#/// @file ApexInternalRamAddressLineDiagnosticFaultInjectionTest1.py
#///
#/// This Python script verifies that when two complementary patterns are
#/// inserted into RAM (target addresses differ with one bit) and wrong
#/// values are read back from RAM during address line test,
#/// the test will cause exception. Failure is caused by injection of code
#/// causing these two addresses (r1 and r2 registers) to be equal.
#/// The injection is performed 30 seconds after powerup and it causes
#/// failure during next execution of address line test.
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
    ;Start Fault Injection Point 7
    ;End Fault Injection Point 7
                ;Fault Injection Code Start
                IMPORT  InjectFaultFlag
                ;Fault Injection Code End
    ''',
    # # # # # # # # # # # # # # # # # # # # # # # # #
    '''
    ;Start Fault Injection Point 4
    ;End Fault Injection Point 4
        ;Fault Injection Code Start
        LDR     r6, =InjectFaultFlag
        LDR     r7, [r6]
        CMP     r7, #1
        BNE     WithoutFaultInjection
        ;Simulate that Addr2 is the same as Addr1
        MOV     r2, r1
WithoutFaultInjection
        ;Fault Injection Code End
    '''
    ],
    'ApexDiagRamAddress.cpp': [ \
    # # # # # # # # # # # # # # # # # # # # # # # # #
    '''
    // Start Fault Injection Point 1
    // End Fault Injection Point 1
    // Fault Injection Code Start
    InjectFaultFlag = 0;
    // Fault Injection Code End
    '''
    ],
    'ApexDiagnostic.hpp': [ \
    # # # # # # # # # # # # # # # # # # # # # # # # #
    '''
    // Start Fault Injection Point 1
    // End Fault Injection Point 1
// Fault Injection Code Start
extern UINT32 InjectFaultFlag;
// Fault Injection Code End
    ''',
    # # # # # # # # # # # # # # # # # # # # # # # # #
    '''
    // Start Fault Injection Point 2
    // End Fault Injection Point 2
    // Fault Injection Code Start
    static const UINT32 DGN_FI_DELAY_SEC = 30;
    // Fault Injection Code End
    '''
    ],
    'ApexDiagnostic.cpp': [ \
    # # # # # # # # # # # # # # # # # # # # # # # # #
    '''
    // Start Fault Injection Point 1
    // End Fault Injection Point 1
// Fault Injection Code Start
UINT32 InjectFaultFlag = 0;
// Fault Injection Code End
    ''',
    # # # # # # # # # # # # # # # # # # # # # # # # #
    '''
    // Start Fault Injection Point 2
    // End Fault Injection Point 2
    // Fault Injection Code Start
    if (HI_ApexReg.SystemTime > (DGN_FI_DELAY_SEC * MILLISECONDS_IN_SECOND * MICROSECONDS_IN_MILLISECOND))
    {
        InjectFaultFlag = 1;
    }
    // Fault Injection Code End
    '''
    ]
}

# Call the procedure to modify and build the test firmware code with the
# above modifications.
faultInjectionUtils.FaultInjectionUtils().ModifyAndBuildFaultInjectionFile(fileModificationsDictionary, __file__)