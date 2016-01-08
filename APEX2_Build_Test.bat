rem Build Apex binary (Release)

set VIEW_PATH=%1

SET MAKE_OPT = %2

pushd %VIEW_PATH%\Analog\NextGen\apex\Release

"C:\Program Files\ARM\bin\win_32-pentium\make" %2

popd
