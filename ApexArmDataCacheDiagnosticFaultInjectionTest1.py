# /////////////////////////////////////////////////////////////////////////////
# /// @file ApexArmDataCacheDiagnosticFaultInjectionTest1.py
# ///
# /// This Python script verifies that Apex cache test
# /// (ApexDiagArmCache.cpp: DgnArmCachePowerUp()) works properly.
# /// Data cache BIST is executed and returns its result.
# /// Fault injection simulates that BIST returned
# /// data cache test failed status.
# ///
# /// @if REVISION_HISTORY_INCLUDED
# /// @par Edit History
# /// fzembok 05-NOV-2013 Fault injection point fixes.
# /// pszramo 07-NOV-2013 Adjusted point number (there are two points one
# ///                     after another in the injected file).
# /// pszramo 09-DEC-2013 Adjustments after MISRA fixes.
# /// @endif
# ///
# /// @par Copyright (c) 2013 Rockwell Automation Technologies, Inc. All rights reserved.
# ///
# /////////////////////////////////////////////////////////////////////////////

import faultInjectionUtils

# ------------------------------------------------------------------------------
# Here is the list of files to be modified by this script, along with
# blocks of new code (first two lines of block are start and end text to
# search for and replace between) for each of the modified files.
fileModificationsDictionary = {
    'ApexDiagArmCacheAsm.s': [
        # # # # # # # # # # # # # # # # # # # # # # # # #
        '''
    ;; Start Fault Injection Point 1
    ;; End Fault Injection Point 1
;; Fault Injection Code Start
    MOV     r0, #DATA_CACHE_BIST_FAILED
;; Fault Injection Code End
    '''
    ]
}

# Call the procedure to modify and build the test firmware code with the
# above modifications.
faultInjectionUtils.FaultInjectionUtils().ModifyAndBuildFaultInjectionFile(fileModificationsDictionary, __file__)
