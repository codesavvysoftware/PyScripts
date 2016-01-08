    @echo off
    rem
    @echo.
    call python BlackfinDataRamAsmFaultInjectionTest1.py
    call python BlackfinInstructionAsmFaultInjectionTest1.py
	call python BlackfinInstructionRamFaultInjectionTest1.py
	call python BlackfinRegisterAsmFaultInjectionTest1.py
	call python BlackfinTimerFaultInjectionTest1.py
	call python BlackfinSchedulerFaultInjectionTest1.py

