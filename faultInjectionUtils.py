#/////////////////////////////////////////////////////////////////////////////
#/// @file faultInjectionUtils.py
#///
#/// This script file contains a procedure used to modify firmware files,
#/// typically for injecting faults. A file modification dictionary is passed
#/// in.  The files in the dictionary are checked out and modified and then
#/// the firmware is built.  Finally, the modified files are saved to a
#/// results folder and the checkouts are undone.
#/// 
#/// This file also prints messages to the screen and a log file which is also
#/// saved to a results folder.
#///
#/// Note that this script file requires the cleartool.pyd file to be present
#/// in the \Lib\site-packages\logixToolsPkg subfolder under the computer's
#/// Python folder (for example: C:\Python27\Lib\site-packages\logixToolsPkg).
#/// The cleartool.pyd file to be used can be found at:
#///     http://project.ra.rockwell.com/PWA/ICE2 Platform Development/
#///     Project Documents/Forms/AllItems.aspx?RootFolder=%2fPWA%2f
#///     ICE2 Platform Development%2fProject Documents%2fTeam Information%2f
#///     Tools and Infrastructure Team%2fclearcase&FolderCTID=&View=
#///     {8D8D137C-F7CA-407F-8180-26CD22515E97}
#/// 
#/// @if REVISION_HISTORY_INCLUDED
#/// @par Edit History
#/// wmpeloso 07-OCT-2013 Created.
#/// wmpeloso 13-OCT-2013 Updated per Collaborator code review #26377.
#/// wmpeloso 16-OCT-2013 Removed unneeded extra indent of all BuildModifiedCode() lines.
#/// wmpeloso 03-NOV-2013 Added deletion of old build files to better detect build errors.
#///                      Added ConfigApexDiagnosticsStartupDelay() and MergeDictionaries().
#/// wmpeloso 07-NOV-2013 Removed unused import of defaultdict.
#/// pgrzywn  08-NOV-2013 Added deletion of Apex.bin to force generation of ApexBinary.h.
#/// wmpeloso 03-DEC-2013 Added support for CNz. Incorporated comments from
#///                      Collaborator code review #28106.
#/// abritto  18-DEC-2013 Added special parsing for product-specific filepaths.
#/// wmpeloso 09-JAN-2014 Added undoing of checkouts when this file fails as
#///                      suggested in Collaborator code review #27491.
#/// wmpeloso 10-JAN-2014 Removed unused UndoCheckouts() Keys parameter per
#///                      Collaborator code review #29206.
#/// wmpeloso 13-JAN-2014 Corrected PrintToScreenAndFile() line in
#///                      MakeWorkspace() per Collaborator code review #29206.
#/// wmpeloso 14-JAN-2014 Updated ApexDiagnosticsStartupDelayDictionary to
#///                      reflect changes made per MISRA fixes per
#///                      Collaborator code review #29206. Updated copyright
#///                      year.
#/// wmpeloso 24-JAN-2014 Fix for .replace() call for parsing product-specific
#///                      filepaths. Added comment regarding required
#///                      cleartool.pyd file.
#/// wmpeloso 21-MAY-2014 Modified CNZ_PROJECT_NAME so "Proj_ICE2_CNet_VB" is
#///                      built before "Proj_ICE2_CNzR_VIP" to force a
#///                      necessary .drch file to be generated before the UCS
#///                      DKM is built since it is missing from the UCS DKM's
#///                      drc.makefile (see Lgx00152375 for details).
#/// tnhaley  14-JAN-2016 Modified to accomodate NextGen Apex and Blackfin 
#///                      edits and builds with the existing legacy class. The
#///                      legacy faultInjectionUtils.py was implemented unchanged
#///                      in a separate .py library file:
#///                          LegacyFaultInjectionUtils.py
#///                      The NextGen FaultInjectionUtils class was implement in:
#///                          NextGenFaultInjectionUtils.py
#///                      The scripts that actually implement the editing of the 
#///                      source files for fault injection remain unchanged. 
#///                      Scripts to edit Blackfin files for fault injection were
#///                      developed.  Also the .bat file that call the scripts
#///                      for the legacy fault injection remains unchanged.
#///                      A new .bat file was implemented for NextGen builds.
#///                      The command line has a parameter that tells the 
#///                      FaultInjectionClass for NextGen what build to do.
#/// @endif
#///
#/// @par Copyright (c) 2016 Rockwell Automation Technologies, Inc.  All rights reserved.
#///
#/////////////////////////////////////////////////////////////////////////////

#-----------------------------------------------------------------------------
import sys
import importlib

class FaultInjectionUtils:

    def __init__(self):
        
        if len(sys.argv) == 0 :

            self.FaultInjectInstance = importlib.import_module('LegacyFaultInjectionUtils').FaultInjectionUtils()

        else:

            self.FaultInjectInstance = importlib.import_module('NextGenFaultInjectionUtils').FaultInjectionUtils()

    def ModifyAndBuildFaultInjectionFile(self, fileModificationsDictionary, TestName):
        
		self.FaultInjectInstance.ModifyAndBuildFaultInjectionFile( fileModificationsDictionary, TestName)




