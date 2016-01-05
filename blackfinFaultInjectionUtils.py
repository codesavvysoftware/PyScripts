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
#///     Tools and Infrastructure Team%2fClearCase&FolderCTID=&View=
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
#/// @endif
#///
#/// @par Copyright (c) 2014 Rockwell Automation Technologies, Inc.  All rights reserved.
#///
#/////////////////////////////////////////////////////////////////////////////

#-----------------------------------------------------------------------------
#was import ClearCase
import clearcase  # For isCheckedOut, checkout, uncheckout
import os         # For path
import datetime   # For date
import shutil     # For Copy
import msvcrt     # For getch

# Define constants that need to be confirmed/modified at run time.
# The order of projects in ENZTR_PROJECT_NAME and CNZ_PROJECT_NAME is
# important. A specific order is used to make sure that the requirements
# for a later project are built.
#
BLACKFIN_PRODUCT_NAME                            = "BlackfinFIT"

BLACKFIN_MAIN_FOLDER                             = "\\Blackfin\\"

BLACKFIN_PROJECT                                 = "1756IRT8I"

BLACKFIN_DIAG_PATH                               = "\\Common\\Diag"

BLACKFIN_MAKE_CLEAN_CMD                          = "IRT8I_ReleaseDB_clean"

BLACKFIN_MAKE_CMD                                = "IRT8I_ReleaseDB"

# Define constants that should not change.
SEARCH_VOB_STR                                            = "\\FIT"

BUILD_LOG_FILE_NAME                                       = "build.log"

BUILD_RESULTS_FOLDER_NAME                                 = "Build_Results"

BUILD_FILES_FOLDER_NAME                                   = "\\ReleaseDB\\"

# FaultInjectionUtils class
# This class is used to process the fault injection script file.
class FaultInjectionUtils:

    #-------------------------------------------------------------------------
    # Print a message to both the screen and the specified log file.
    def PrintToScreenAndFile(self, Message, PrintToScreen):
        Message = str(datetime.datetime.now()) + " " + Message + "\n"
        if PrintToScreen:
            # Print the message to the screen.
            print Message

        # Print the message to the log file.
        self.LogFile.write(Message)

    #-------------------------------------------------------------------------
    # Perform all necessary initialization.
    def Init(self, TestName):
        # Get the basename of the TestName
        TestName = os.path.basename(TestName)

        # If the test results folder does not already exist, create it.
        if not os.path.exists(BUILD_RESULTS_FOLDER_NAME):
            os.makedirs(BUILD_RESULTS_FOLDER_NAME)

        # Determine the build results sub folder name.
        cwdStr = os.getcwd()
        today = datetime.date.today()
        self.BuildResultsSubFolderName = cwdStr + "\\" + BUILD_RESULTS_FOLDER_NAME + "\\" + str(today) + "_" + BLACKFIN_PRODUCT_NAME + "_" + TestName

        # If the build results sub folder already exists, rename it with a ".old" or ".old.n" extension.
        if os.path.exists(self.BuildResultsSubFolderName):
            if not os.path.exists(self.BuildResultsSubFolderName + ".old"):
                NewBuildResultsSubFolderName = self.BuildResultsSubFolderName + ".old"
            else:
                FoundOldBuildSubFolderIndex = False
                OldBuildSubFolderIndex = 0
                while (OldBuildSubFolderIndex < MAX_NUMBER_OF_BUILDS_PER_SCRIPT_PER_PRODUCT_PER_DAY - 2 and \
                       not FoundOldBuildSubFolderIndex):
                    OldBuildSubFolderIndex += 1
                    if not os.path.exists(self.BuildResultsSubFolderName + ".old." + str(OldBuildSubFolderIndex)):
                        NewBuildResultsSubFolderName = self.BuildResultsSubFolderName + ".old." + str(OldBuildSubFolderIndex)
                        FoundOldBuildSubFolderIndex = True
                if not FoundOldBuildSubFolderIndex:
                    UnexpectedError = "Already built the maximum number of builds per script per product per day (%s)!" % MAX_NUMBER_OF_BUILDS_PER_SCRIPT_PER_PRODUCT_PER_DAY
                    raise RuntimeError, UnexpectedError
            os.rename(self.BuildResultsSubFolderName, NewBuildResultsSubFolderName)

        # Create the build results sub folder.
        os.makedirs(self.BuildResultsSubFolderName)

        # Determine the log file name and open it.
        LogFilePathAndName = self.BuildResultsSubFolderName + "\\" + TestName + ".log"
        self.LogFile = open(LogFilePathAndName,'w')

        # Print a separator line to make screen output easier to read.
        self.PrintToScreenAndFile("-----------------------------------------------------------", True)

        # Print the TestName, self.BuildResultsSubFolderName and LogFilePathAndName.
        self.PrintToScreenAndFile("TestName = %s" % TestName, True)
        self.PrintToScreenAndFile("self.BuildResultsSubFolderName = %s" % self.BuildResultsSubFolderName, True)
        self.PrintToScreenAndFile("LogFilePathAndName = %s" % LogFilePathAndName, True)

        # Extract the view path from the current working directory.
        vobStrIndex = cwdStr.find(SEARCH_VOB_STR)

        # Search for SEARCH_VOB_STR in the current working directory.
        if vobStrIndex < 0:
            UnexpectedError = "Search VOB string '%s' not in current working directory (%s)" % (SEARCH_VOB_STR, cwdStr)
            self.PrintToScreenAndFile(UnexpectedError, False)
            raise RuntimeError, UnexpectedError

        # SEARCH_VOB_STR was found so the view path is the current working directory truncated at the VOB string index.
        self.ViewPath = cwdStr[:vobStrIndex]
        self.PrintToScreenAndFile("self.ViewPath = %s" % self.ViewPath, True)
        self.BlackfinBuildPath = self.ViewPath + BLACKFIN_MAIN_FOLDER + BLACKFIN_PROJECT
        self.BlackfinDiagEditPath = self.ViewPath + BLACKFIN_MAIN_FOLDER + BLACKFIN_DIAG_PATH

    #-------------------------------------------------------------------------
    # Check if the file found is in the list of folders allowed to be modified.
    def IsFileFoundInBlackfinProjFolder(self, filename):
        isFileFound = False
        self.DiagFileToEditWithPath = self.BlackfinDiagEditPath + "\\" + filename
        if os.path.isfile(self.DiagFileToEditWithPath):
            isFileFound = True

        return isFileFound

    #-------------------------------------------------------------------------
    # Modify the file as specified in the fault injection script file's dictionary.
    def ModifyFile(self, fileModificationsDictionary, filename):
        self.PrintToScreenAndFile("Modifying file %s" % self.DiagFileToEditWithPath, True)
        fileToEdit = open(self.DiagFileToEditWithPath)
        text = fileToEdit.read()
        fileToEdit.close()
        for newblock in fileModificationsDictionary[filename]:
            newblock = newblock.strip()
            patternStart = newblock.split('\n')[0]
            patternEnd   = newblock.split('\n')[1]
            patternEnd   = patternEnd.strip()
            newblock_woPattern = newblock.replace(patternStart,'')
            newblock_woPattern = newblock_woPattern.replace(patternEnd,'')
            newblock_woPattern = newblock_woPattern.strip()
            try:
                start = text.index(patternStart)
            except ValueError:
                UnexpectedError = "Search pattern '%s' not found in %s" % (patternStart, self.DiagFileToEditWithPath)
                self.PrintToScreenAndFile(UnexpectedError, False)
                raise RuntimeError, UnexpectedError
            try:
                end = text.index(patternEnd, start) + len(patternEnd)
            except ValueError:
                UnexpectedError = "Search pattern '%s' not found in %s" % (patternEnd, self.DiagFileToEditWithPath)
                self.PrintToScreenAndFile(UnexpectedError, False)
                raise RuntimeError, UnexpectedError
            result = text[start:end]
            text = text.replace(result,newblock_woPattern)
        fileToEdit = open(self.DiagFileToEditWithPath,'w')
        fileToEdit.write(text)
        fileToEdit.close()
        self.PrintToScreenAndFile("File %s has been Modified" % self.DiagFileToEditWithPath, True)

    #-------------------------------------------------------------------------
    # Process all of the file names in the fault injection script file's dictionary,
    # check the files out, modify the files and copy the files to the build results folder.
    def ProcessBlackfinFileModificationsDict(self, fileModificationsDictionary):

        for filename in fileModificationsDictionary.keys() :
            break
        
        if not self.IsFileFoundInBlackfinProjFolder( filename ):
            UnexpectedError = "File '%s' was not found in any of the allowed folders" % filename
            self.PrintToScreenAndFile(UnexpectedError, False)
            raise RuntimeError, UnexpectedError

        if clearcase.isCheckedOut(self.DiagFileToEditWithPath):
            UnexpectedError = "File %s already Checked Out!" % self.DiagFileToEditWithPath
            self.PrintToScreenAndFile(UnexpectedError, False)
            raise RuntimeError, UnexpectedError
            self.PrintToScreenAndFile("File %s is not already checked out" % self.DiagFileToEditWithPath, True)

        # Check the file out.
        self.PrintToScreenAndFile("Checking out file %s" % self.DiagFileToEditWithPath, True)
        
        if clearcase.checkout(self.DiagFileToEditWithPath, False, 'Temporary Checkout for Fault Injection Test.') != None:
            UnexpectedError = "Error while trying to checkout file %s!" % self.DiagFileToEditWithPath
            self.PrintToScreenAndFile(UnexpectedError, False)
            raise RuntimeError, UnexpectedError
        
        self.PrintToScreenAndFile("File %s has been checked out." % self.DiagFileToEditWithPath, True)
        
		# Modify the file.
        self.ModifyFile(fileModificationsDictionary, filename)

    #-------------------------------------------------------------------------
    # Build the modified code.
    def BuildModifiedCode(self):
        os.chdir(self.BlackfinBuildPath)

        CleanBuildCmd = "make " + BLACKFIN_MAKE_CLEAN_CMD
		
        BuildCmd = "make " + BLACKFIN_MAKE_CMD
		
        if os.system(CleanBuildCmd) :
            UnexpectedError = "Error while doing a 'clean' build the modified code! See %s\\%s for the errors!" % (self.BlackfinBuildPath, BUILD_LOG_FILE_NAME)
            self.PrintToScreenAndFile(UnexpectedError, False)
            raise RuntimeError, UnexpectedError

        if os.system(BuildCmd) :
            UnexpectedError = "Error while doing a build the modified code! See %s\\%s for the errors!" % (self.BlackfinBuildPath, BUILD_LOG_FILE_NAME)
            self.PrintToScreenAndFile(UnexpectedError, False)
            raise RuntimeError, UnexpectedError

        self.PrintToScreenAndFile("Building Modified Firmware...", True)
        self.PrintToScreenAndFile("For details, see build log file %s." % self.BuildResultsSubFolderName + "\\" + BUILD_LOG_FILE_NAME, True)

    #-------------------------------------------------------------------------
    # Copy the product build binary folder to the build results subfolder.
    def CopyBinaryFolder(self):
        TestBuildResultsFolder = self.BuildResultsSubFolderName + BUILD_FILES_FOLDER_NAME
        
        BinaryFolder = self.BlackfinBuildPath + BUILD_FILES_FOLDER_NAME

        # If a previous binary files folder already exists under the fault injection build results folder, delete it since copytree will fail if it already exists.
        if os.path.exists(TestBuildResultsFolder):
            shutil.rmtree(TestBuildResultsFolder)

        # Copy the binary files folder to the build results folder.
        self.PrintToScreenAndFile("Copying the binary files folder (%s) to the build results folder (%s)." % (BinaryFolder, TestBuildResultsFolder), True)
        shutil.copytree(BinaryFolder, TestBuildResultsFolder)
        self.PrintToScreenAndFile("Copy the binary files folder to the build results folder.", True)

    #-----------------------------------------------------------------------------
    # Undo the check out of all of the files in the fault injection script file's
    # dictionary that were checked out.
    def UndoCheckouts(self):
        self.PrintToScreenAndFile("Undoing Checkouts...", True)

        if clearcase.isCheckedOut(self.DiagFileToEditWithPath):
            self.PrintToScreenAndFile("Undoing checkout of file %s..." % self.DiagFileToEditWithPath, True)
            
        if clearcase.uncheckout(self.DiagFileToEditWithPath, keep = True) != None:
            UnexpectedError = "Error while trying to uncheckout file %s!" % self.DiagFileToEditWithPath
            self.PrintToScreenAndFile(UnexpectedError, False)
            raise RuntimeError, UnexpectedError
            
        self.PrintToScreenAndFile("File %s has been unchecked out" % self.DiagFileToEditWithPath, True)

    #-------------------------------------------------------------------------
    # Each fault injection script file calls into this method and passes in a
    # dictionary of the files to be modified by this script as well as the
    # fault injection script file's name.  The dictionary passed in includes
    # the blocks of new code (the first two lines of the block are text to
    # search for) for each of the modified files.
    def ModifyAndBuildFaultInjectionFile(self, fileModificationsDictionary, TestName):
        # Note: To run multiple scripts using a batch file:
        #     1. Check out this file.
        #     2. Comment out the call to self.GetProductSelection() below.
        #     3. Add a line above the call to self.SetProductSpecificSettings()
        #        to hard code the product selection. For example:
        #        "self.ProductSelection = ProductSelectionOptions.Blackfin"
        #     4. Make sure that WRWB_WORKSPACE is set equal to the workspace
        #        path and name to be used above.
        #     5. Comment out the call to self.GetWorkspaceSelection() below.
        #     6. Create a batch file and use "call" for every script file that
        #        is to be run. For example:
        #            call python InteractiveWatchdogFaultInjectionTest1.py
        #            call python InteractiveWatchdogFaultInjectionTest2.py
        #     7. When done, undo the checkout of this file. Do not check these
        #        changes in.

        # Perform all necessary initialization.
        self.Init(TestName)

        # Use try/except to detect any exceptions that are thrown after one
        # or more files have been checked out so checkouts can be undone
        # before exiting due to the exception.
        try:
            # Process all of the file names in the fault injection script file's dictionary,
            # check the files out, modify the files and copy the files to the build results folder.
            self.ProcessBlackfinFileModificationsDict(fileModificationsDictionary)

            # Build the modified code.
            self.BuildModifiedCode()

            # Copy the product build binary folder to the build results subfolder.
            self.CopyBinaryFolder()
            
        except:
            # If an exception was detected, undo all of the checkouts that were
            # made and exit.
            self.PrintToScreenAndFile("Exception detected!", True)
            self.UndoCheckouts()
            raise

        # Undo the file checkouts.
        self.UndoCheckouts()

        # Print a message indicating successful completion.
        self.PrintToScreenAndFile("faultInjectionUtils.FaultInjectionUtils().ModifyAndBuildFaultInjectionFile() completed successfully!", True)