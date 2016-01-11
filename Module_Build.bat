rem Build 1756 IO module (Release Mode)
rem Parameters:
rem   1. The path to the Analog VOB
rem   2. The project folder name (within \Analog\NextGen\Blackfin\)
rem   3. The project name to be passed to gmake

set VIEW_PATH=%1
set PROJ_FOLDER_NAME=%2
set PROJ_NAME=%3
set APEX_DEST=%VIEW_PATH%\Analog\NextGen\apex\Release\apexbin.h

rem Double check that the needed library does exist
IF NOT EXIST %APEX_DEST% (
     EXIT 1
)
pushd %VIEW_PATH%\Analog\NextGen\Blackfin\%PROJ_FOLDER_NAME%

"C:\Program Files\Analog Devices\VisualDSP 5.0\gmake-378" %PROJ_NAME%

popd

rem made it to the end, report success

