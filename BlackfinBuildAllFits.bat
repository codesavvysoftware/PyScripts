    @echo off
    rem
    @echo.
    call python BlackfinDataRamAsmFaultInjectionTest1.py BlackfinDiag
    call python BlackfinInstructionAsmFaultInjectionTest1.py BlackfinDiag
    call python BlackfinInstructionRamFaultInjectionTest1.py BlackfinDiag
    call python BlackfinRegisterAsmFaultInjectionTest1.py BlackfinDiag
    call python BlackfinTimerFaultInjectionTest1.py BlackfinDiag
    call python BlackfinSchedulerFaultInjectionTest1.py BlackfinDiag
    call python ApexArmDataCacheDiagnosticFaultInjectionTest1.py ApexDiag
    call python ApexArmInstructionCacheDiagnosticFaultInjectionTest1.py ApexDiag
    call python ApexArmInstructionDiagnosticFaultInjectionTest1.py ApexDiag
    call python ApexArmInstructionDiagnosticFaultInjectionTest2.py ApexDiag
    call python ApexArmRegisterDiagnosticFaultInjectionTest1.py ApexDiag
    call python ApexArmRegisterDiagnosticFaultInjectionTest2.py ApexDiag
    call python ApexCompletionTimeDiagnosticFaultInjectionTest1.py ApexDiag
    call python ApexFirmwareBinaryCrcDiagnosticFaultInjectionTest1.py ApexDiag
    call python ApexFirmwareBinaryCrcDiagnosticFaultInjectionTest2.py ApexDiag
    call python ApexInteractiveWatchdogFaultInjectionTest1.py ApexDiag
    call python ApexInternalRamAddressLineDiagnosticFaultInjectionTest1.py ApexDiag
    call python ApexInternalRamAddressLineDiagnosticFaultInjectionTest2.py ApexDiag
    call python ApexInternalRamEccCircuitDiagnosticFaultInjectionTest1.py ApexDiag
    call python ApexInternalRamEccCircuitDiagnosticFaultInjectionTest2.py ApexDiag
    call python ApexInternalRamScrubberDiagnosticFaultInjectionTest1.py ApexDiag
    call python ApexInternalRamShadowFaultInjectionTest1.py ApexDiag
    call python ApexInternalRamShadowFaultInjectionTest2.py ApexDiag
    call python ApexInternalSafeRamDiagnosticFaultInjectionTest1.py ApexDiag
    rem call python ApexStackDiagnosticFaultInjectionTest1.py ApexOS
    rem call python DspStackDiagnosticFaultInjectionTest1.py BlackfinOS
    rem call python DSPInteractiveWatchdogFaultInjectionTest1.py BlackfinOS

