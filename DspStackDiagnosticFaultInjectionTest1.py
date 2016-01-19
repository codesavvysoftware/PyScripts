#/////////////////////////////////////////////////////////////////////////////
#/// @file DspStackDiagnosticFaultInjectionTest1.py
#///
#/// This Python script modifies one of the Stack Cookie values.  When the
#/// Stack is checked it should find this bad value and assert.
#///
#/// @if REVISION_HISTORY_INCLUDED
#/// @par Edit History
#/// kolat   08-Jan-2016 Created.
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
    'Os_iotk.c': [ \
    # # # # # # # # # # # # # # # # # # # # # # # # # 
    '''
      /* Start Fault Injection Point 2 */
      /* End Fault Injection Point 2 */
      /* Fault Injection Code Start */
      *temp_stack_ptr = STACK_COOKIE_VALUE - 1;
      /* Fault Injection Code End */
    '''
    ]
}

# Call the procedure to modify and build the test firmware code with the
# above modifications.
faultInjectionUtils.FaultInjectionUtils().ModifyAndBuildFaultInjectionFile(fileModificationsDictionary, __file__)
