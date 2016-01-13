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
#/// @endif
#///
#/// @par Copyright (c) 2014 Rockwell Automation Technologies, Inc.  All rights reserved.
#///
#/////////////////////////////////////////////////////////////////////////////

#-----------------------------------------------------------------------------
#was import clearcase
import clearcase  # For isCheckedOut, checkout, uncheckout
import os         # For path
import datetime   # For date
import shutil     # For Copy
import msvcrt     # For getch
import sys
import importlib


# FaultInjectionUtils class
# This class is used to process the fault injection script file.
## Define constants that need to be confirmed/modified at run time.
# The order of projects in ENZTR_PROJECT_NAME and CNZ_PROJECT_NAME is
# important. A specific order is used to make sure that the requirements
# for a later project are built.
#
BLACKFIN_PRODUCT_NAME                            = "BlackfinFIT"

BLACKFIN_PRODUCT_FOLDER                          = "Blackfin"

BLACKFIN_PROJECT_FOLDER                          = "1756IRT8I"

BLACKFIN_BUILD_TYPE_FOLDER                       = "Release"

BLACKFIN_DIAG_PATH                               = "\\Common\\Diag"

BLACKFIN_OS_PATH                                 = "\\Common\\OS"

BLACKFIN_MAKE_CLEAN_CMD                          = "IRT8I_Release_clean"

BLACKFIN_MAKE_CMD                                = "IRT8I_Release"

BLACKFIN_BUILD_SCRIPT                            = "Module_Build.bat"

APEX_PRODUCT_NAME                                = "ApexFIT"

APEX_PRODUCT_FOLDER                              = "apex"

APEX_PROJECT_FOLDER                              = "Release"

APEX_DIAG_PATH                                   = ""

APEX_OS_PATH                                     = "\\OS"

APEX_MAKE_CLEAN_CMD                              = "clean"

APEX_MAKE_CMD                                    = "all"

APEX_BUILD_SCRIPT                                = "APEX2_Build_Test.bat"

# Define constants that should not change.
SEARCH_VOB_STR                                            = "\\FIT"

SEARCH_BRANCH_STR                                         = "\\Analog\NextGen\\FIT"

BUILD_RESULTS_FOLDER_NAME                                 = "Build_Results"

BUILD_FILES_FOLDER_NAME                                   = "\\Release\\"

MAX_NUMBER_OF_SRC_FOLDERS_ALLOWED_TO_BE_MODIFIED          = 100

MAX_NUMBER_OF_SRC_FILES_ALLOWED_TO_BE_MODIFIED            = 100

MAX_NUMBER_OF_FILES_AND_FOLDERS_TO_DELETE_BEFORE_BUILDING = 100

MAX_NUMBER_OF_BUILDS_PER_SCRIPT_PER_PRODUCT_PER_DAY       = 50

class FaultInjectionUtils:

    def __init__(self):

        pass

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
        self.TestName = os.path.basename(TestName)

        JustFileName = os.path.splitext(self.TestName)[0]

        # If the test results folder does not already exist, create it.
        if not os.path.exists(BUILD_RESULTS_FOLDER_NAME):
            os.makedirs(BUILD_RESULTS_FOLDER_NAME)

        # Determine the build results sub folder name.
        cwdStr = os.getcwd()
        today = datetime.date.today()

        BuildResultsSubFolderName = cwdStr + "\\" + BUILD_RESULTS_FOLDER_NAME + "\\" + str(today) + "_" + self.ProductName + JustFileName 

        self.BuildResultsSubFolderName = BuildResultsSubFolderName.replace ("-", "_")

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
        LogFilePathAndName = self.BuildResultsSubFolderName + "\\" + JustFileName + ".log"
        self.LogFile = open(LogFilePathAndName,'w')

        # Print a separator line to make screen output easier to read.
        self.PrintToScreenAndFile("-----------------------------------------------------------", True)

        # Print the TestName, self.BuildResultsSubFolderName and LogFilePathAndName.
        self.PrintToScreenAndFile("self.TestName = %s" % self.TestName, True)
        self.PrintToScreenAndFile("self.BuildResultsSubFolderName = %s" % self.BuildResultsSubFolderName, True)
        self.PrintToScreenAndFile("LogFilePathAndName = %s" % LogFilePathAndName, True)

        # Extract the view path from the current working directory.
        vobStrIndex = cwdStr.find(SEARCH_VOB_STR)

        # Search for SEARCH_VOB_STR in the current working directory.
        if vobStrIndex < 0:
            UnexpectedError = "Search VOB string '%s' not in current working directory (%s)" % (SEARCH_VOB_STR, cwdStr)
            self.PrintToScreenAndFile(UnexpectedError, False)
            raise RuntimeError, UnexpectedError

        vobBranchPathIndex = cwdStr.find(SEARCH_BRANCH_STR)
        if vobBranchPathIndex < 0:
            UnexpectedError = "Search VOB string '%s' not in current working directory (%s)" % (vobBranchPathIndex, cwdStr)
            self.PrintToScreenAndFile(UnexpectedError, False)
            raise RuntimeError, UnexpectedError


        # SEARCH_VOB_STR was found so the view path is the current working directory truncated at the VOB string index.
        self.ViewPath = cwdStr[:vobStrIndex]
        self.PrintToScreenAndFile("self.ViewPath = %s" % self.ViewPath, True)
        self.BranchPath = cwdStr[:vobBranchPathIndex]
        self.PrintToScreenAndFile("self.BranchPath = %s" % self.ViewPath, True)

    def IsFileFoundInPath( self, path, filename ):
        isFileFound = False
	    
        FileToEditWithPath = path+"\\"+filename
	    
        if os.path.isfile(FileToEditWithPath):
            isFileFound = True
            self.FileToEditIndex += 1
            self.FileToEditWithPath[self.FileToEditIndex] = FileToEditWithPath
       
        return isFileFound

    #-------------------------------------------------------------------------
    # Check if the file found is in the list of folders allowed to be modified.
    def IsFileFoundInDiagnosticSourceFileFolder(self, filename):
        self.SourceFileName = filename

        return self.IsFileFoundInPath( self.DiagEditPath, filename )

    #-------------------------------------------------------------------------
    # Check if the file found is in the list of folders allowed to be modified.
    def IsFileFoundInAllowedFolders(self, filename):
        productString = "%" + self.ProductName + "%" # for product-specific paths

        for lineIndex in range(0, self.AllowedFolderFileLineCount):
            if len(self.AllowedFolder[lineIndex]) and (self.AllowedFolder[lineIndex][0] != "#") and \
                  (self.AllowedFolder[lineIndex][0] != " "):

                if productString in self.AllowedFolder[lineIndex]:
                    self.AllowedFolder[lineIndex] = self.AllowedFolder[lineIndex].replace("%", "")

                # Determine the file path and confirm that it exists.
                filePath = self.ViewPath + self.AllowedFolder[lineIndex]
	            
                if ( IsFileFoundInPath( filePath, filename ) ):
                    return True
				
        return False

    #-------------------------------------------------------------------------
    # Modify the file as specified in the fault injection script file's dictionary.
    def ModifyFile(self, fileModificationsDictionary, filename, fileNameWithPath):
        self.PrintToScreenAndFile("Modifying file %s" % fileNameWithPath, True)
        fileToEdit = open(fileNameWithPath)
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
                UnexpectedError = "Search pattern '%s' not found in %s" % (patternStart, fileNameWithPath)
                self.PrintToScreenAndFile(UnexpectedError, False)
                raise RuntimeError, UnexpectedError
            try:
                end = text.index(patternEnd, start) + len(patternEnd)
            except ValueError:
                UnexpectedError = "Search pattern '%s' not found in %s" % (patternEnd, fileNameWithPath)
                self.PrintToScreenAndFile(UnexpectedError, False)
                raise RuntimeError, UnexpectedError
            result = text[start:end]
            text = text.replace(result,newblock_woPattern)
        fileToEdit = open(fileNameWithPath,'w')
        fileToEdit.write(text)
        fileToEdit.close()
        self.PrintToScreenAndFile("File %s has been Modified" % fileNameWithPath, True)

    #-------------------------------------------------------------------------
    # Process all of the file names in the fault injection script file's dictionary,
    # check the files out, modify the files and copy the files to the build results folder.
    def ProcessFileModificationsDictionary(self, fileModificationsDictionary):
        self.FileToEditWithPath = range(MAX_NUMBER_OF_SRC_FILES_ALLOWED_TO_BE_MODIFIED)
        filenameArray = range(MAX_NUMBER_OF_SRC_FILES_ALLOWED_TO_BE_MODIFIED)
        self.FileToEditIndex = -1

        # Determine the paths to all of the files to be modified.
        for filename in fileModificationsDictionary.keys():
            self.PrintToScreenAndFile("filename = %s" % filename, True)
            # Check if the file exists in one of the allowed folders. If not, return an error.
            if not self.IsFileFoundInDiagnosticSourceFileFolder(filename):
                UnexpectedError = "File '%s' was not found in any of the allowed folders" % filename
                self.PrintToScreenAndFile(UnexpectedError, False)
                raise RuntimeError, UnexpectedError
            filenameArray[self.FileToEditIndex] = filename
 
        # Loop through all of the files to edit and process each one.
        for self.currentFileToEditIndex in range(0, self.FileToEditIndex + 1):
            # Check if the file is already checked out.
            self.PrintToScreenAndFile("Checking if file %s is already checked out..." % self.FileToEditWithPath[self.currentFileToEditIndex], True)
            if clearcase.isCheckedOut(self.FileToEditWithPath[self.currentFileToEditIndex]):
                UnexpectedError = "File %s already Checked Out!" % self.FileToEditWithPath[self.currentFileToEditIndex]
                self.PrintToScreenAndFile(UnexpectedError, False)
                raise RuntimeError, UnexpectedError
            self.PrintToScreenAndFile("File %s is not already checked out" % self.FileToEditWithPath[self.currentFileToEditIndex], True)

            # Check the file out.
            self.PrintToScreenAndFile("Checking out file %s" % self.FileToEditWithPath[self.currentFileToEditIndex], True)
            if clearcase.checkout(self.FileToEditWithPath[self.currentFileToEditIndex], False, 'Temporary Checkout for Fault Injection Test.') != None:
                UnexpectedError = "Error while trying to checkout file %s!" % self.FileToEditWithPath[self.currentFileToEditIndex]
                self.PrintToScreenAndFile(UnexpectedError, False)
                raise RuntimeError, UnexpectedError
            self.PrintToScreenAndFile("File %s has been checked out." % self.FileToEditWithPath[self.currentFileToEditIndex], True)

            # Modify the file.
            self.ModifyFile(fileModificationsDictionary, filenameArray[self.currentFileToEditIndex], self.FileToEditWithPath[self.currentFileToEditIndex])

            # Copy the modified file to the build results folder.
            self.PrintToScreenAndFile("Copying modified file %s" % self.FileToEditWithPath[self.currentFileToEditIndex], True)
            if shutil.copyfile(self.FileToEditWithPath[self.currentFileToEditIndex], self.BuildResultsSubFolderName + "\\" + filenameArray[self.currentFileToEditIndex] + ".modified") != None:
                UnexpectedError = "Error while trying to copy modified file %s!" % self.FileToEditWithPath[self.currentFileToEditIndex]
                self.PrintToScreenAndFile(UnexpectedError, False)
                raise RuntimeError, UnexpectedError
            self.PrintToScreenAndFile("Modified file %s has been copied as %s" % (self.FileToEditWithPath[self.currentFileToEditIndex], filenameArray[self.currentFileToEditIndex] + ".modified"), True)

    #-------------------------------------------------------------------------
    # Build the modified code.
    def BuildModifiedCode(self):
        #os.chdir(self.PathToBuildImageFrom)

        if os.system(self.CleanBuildCmd) :
            UnexpectedError = "Error while doing a 'clean' build the modified code! "
            self.PrintToScreenAndFile(UnexpectedError, False)
            raise RuntimeError, UnexpectedError

        if os.system(self.BuildExecutableCmd) :
            UnexpectedError = "Error while doing a build the modified code!"
            self.PrintToScreenAndFile(UnexpectedError, False)
            raise RuntimeError, UnexpectedError

        self.PrintToScreenAndFile("Building Modified Firmware...", True)

    #-------------------------------------------------------------------------
    # Copy the product build binary folder to the build results subfolder.
    def CopyBinaryFolder(self):
        TestBuildResultsFolder = self.BuildResultsSubFolderName + BUILD_FILES_FOLDER_NAME
        
        # If a previous binary files folder already exists under the fault injection build results folder, delete it since copytree will fail if it already exists.
        if os.path.exists(TestBuildResultsFolder):
            shutil.rmtree(TestBuildResultsFolder)

        # Copy the binary files folder to the build results folder.
        self.PrintToScreenAndFile("Copying the binary files folder (%s) to the build results folder (%s)." % (self.ResultsOfBuildFolder, TestBuildResultsFolder), True)
        shutil.copytree(self.ResultsOfBuildFolder, TestBuildResultsFolder)
        self.PrintToScreenAndFile("Copy the binary files folder to the build results folder.", True)


    #-----------------------------------------------------------------------------
    # Undo the check out of all of the files in the fault injection script file's
    # dictionary that were checked out.
    def UndoCheckouts(self):
        FailureToUncheckAll = False

        if self.MakeFileWithPath != "" :
            if clearcase.isCheckedOut(self.MakeFileWithPath):
                self.PrintToScreenAndFile("Undoing makefile checkout", True)
                if clearcase.uncheckout(self.MakeFileWithPath):
                    UnexpectedError = "Error while trying to uncheckout makefile"
                    self.PrintToScreenAndFile(UnexpectedError,False)
                    FailureToUncheckAll = True
        
        self.PrintToScreenAndFile("Undoing Checkouts...", True)
        for currentFileToEditIndex in range(0, self.FileToEditIndex + 1):
            if clearcase.isCheckedOut(self.FileToEditWithPath[currentFileToEditIndex]):
                self.PrintToScreenAndFile("Undoing checkout of file %s..." % self.FileToEditWithPath[currentFileToEditIndex], True)
                if clearcase.uncheckout(self.FileToEditWithPath[currentFileToEditIndex], keep = True) != None:
                    UnexpectedError = "Error while trying to uncheckout file %s!" % self.FileToEditWithPath[currentFileToEditIndex]
                    self.PrintToScreenAndFile(UnexpectedError, False)
                    FailureToUncheckAll = True
                else:
                    self.PrintToScreenAndFile("File %s has been unchecked out" % self.FileToEditWithPath[currentFileToEditIndex], True)
        if FailureToUncheckAll == True:
            raise RuntimeError, "Unable to Checkout All Files"
    #-------------------------------------------------------------------------
    # Each fault injection script file calls into this method and passes in a
    # dictionary of the files to be modified by this script as well as the
    # fault injection script file's name.  The dictionary passed in includes
    # the blocks of new code (the first two lines of the block are text to
    # search for) for each of the modified files.
    def ModifyFileBuildFaultInjectionTest(self, fileModificationsDictionary, TestName):
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

        # Use try/except to detect any exceptions that are thrown after one
        # or more files have been checked out so checkouts can be undone
        # before exiting due to the exception.
        try:
            # Process all of the file names in the fault injection script file's dictionary,
            # check the files out, modify the files and copy the files to the build results folder.
            self.ProcessFileModificationsDictionary(fileModificationsDictionary)

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

    def ModifyAndBuildFaultInjectionFile(self, fileModificationsDictionary, TestName):
        makefileModificationsDictionaryRM = { \
			'makefile': [ \
			# # # # # # # # # # # # # # # # # # # # # # # # #
			'''
            # Start Fault Injection Point 1
            # End Fault Injection Point 1
            # Fault Injection Code Start
RM :=cmd /C del /F /Q
            # Fault Injection Code End
		    '''
			]
        }
        makefileModificationsDictionaryDEL = { \
			'makefile':[ \
			# # # # # # # # # # # # # # # # # # # # # # # # # 
			''' 
            # Start Fault Injection Point 2
            # End Fault Injection Point 2
            # Fault Injection Code Start
	-$(RM) ".\\apexbin.h"
	-$(RM) ".\\._2"
	-$(RM) ".\\._4"
	-$(RM) ".\\apex.*"
	-$(RM) ".\\*.bin"
	-$(RM) ".\\OS\\*.o"
	-$(RM) ".\\OS\\*.d"
	-$(RM) ".\\*.o"
	-$(RM) ".\\*.d"
	-$(RM) ".\\ControlBus\\*.o"
	-$(RM) ".\\ControlBus\\*.d"
	-$(RM) ".\\OS\\*.o"
	-$(RM) ".\\OS\\*.d"
	-$(RM) ".\\Utility\\*.o"
	-$(RM) ".\\Utility\\*.d"
            # Fault Injection Code End
		    '''
			]
        }

        if len(sys.argv) != 0 :

            if sys.argv[1] == "BlackfinDiag" :

                self.ProductName = BLACKFIN_PRODUCT_NAME

                self.Init(TestName)

                self.DiagEditPath      = self.ViewPath + "\\" + BLACKFIN_PRODUCT_FOLDER + "\\" + BLACKFIN_DIAG_PATH
		
                self.CleanBuildCmd = ".\\" + BLACKFIN_BUILD_SCRIPT + " " + self.BranchPath + " " + BLACKFIN_PROJECT_FOLDER + " " + BLACKFIN_MAKE_CLEAN_CMD
		
                self.BuildExecutableCmd = ".\\" + BLACKFIN_BUILD_SCRIPT + " " + self.BranchPath + " " + BLACKFIN_PROJECT_FOLDER + " " + BLACKFIN_MAKE_CMD

                self.ResultsOfBuildFolder = self.ViewPath + "\\" + BLACKFIN_PRODUCT_FOLDER + "\\"  + BLACKFIN_PROJECT_FOLDER + "\\" + BLACKFIN_BUILD_TYPE_FOLDER

                self.MakeFileWithPath = ""

            elif sys.argv[1] == "BlackfinOS" :

                self.ProductName = BLACKFIN_PRODUCT_NAME

                self.Init(TestName)

                self.DiagEditPath      = self.ViewPath + "\\" + BLACKFIN_PRODUCT_FOLDER + "\\" + BLACKFIN_OS_PATH
		
                self.CleanBuildCmd = ".\\" + BLACKFIN_BUILD_SCRIPT + " " + self.BranchPath + " " + BLACKFIN_PROJECT_FOLDER + " " + BLACKFIN_MAKE_CLEAN_CMD
		
                self.BuildExecutableCmd = ".\\" + BLACKFIN_BUILD_SCRIPT + " " + self.BranchPath + " " + BLACKFIN_PROJECT_FOLDER + " " + BLACKFIN_MAKE_CMD

                self.ResultsOfBuildFolder = self.ViewPath + "\\" + BLACKFIN_PRODUCT_FOLDER + "\\"  + BLACKFIN_PROJECT_FOLDER + "\\" + BLACKFIN_BUILD_TYPE_FOLDER

                self.MakeFileWithPath = ""


            elif sys.argv[1] == "ApexDiag" :

                self.ProductName = APEX_PRODUCT_NAME 

                self.Init(TestName)

                self.DiagEditPath      = self.ViewPath + "\\" + APEX_PRODUCT_FOLDER + "\\" + APEX_DIAG_PATH

                self.CleanBuildCmd = ".\\" + APEX_BUILD_SCRIPT + " " + self.BranchPath + " " + APEX_MAKE_CLEAN_CMD
		
                self.BuildExecutableCmd = ".\\" + APEX_BUILD_SCRIPT + " " + self.BranchPath + " " + APEX_MAKE_CMD

                self.ResultsOfBuildFolder = self.ViewPath + "\\" + APEX_PRODUCT_FOLDER + "\\"  + APEX_PROJECT_FOLDER

                self.MakeFileWithPath = self.ViewPath + "\\" + APEX_PRODUCT_FOLDER + "\\"  + APEX_PROJECT_FOLDER + "\\makefile"
        
                if clearcase.isCheckedOut(self.MakeFileWithPath):
                    if clearcase.uncheckout(self.MakeFileWithPath, keep = True) != None:
                        UnexpectedError = "Error while trying to uncheckout file %s!" % self.MakeFileWithPath
                        self.PrintToScreenAndFile(UnexpectedError, False)
                        raise RuntimeError, UnexpectedError
                    UnexpectedError = "File %s already Checked Out!" % self.MakeFileWithPath
                    self.PrintToScreenAndFile(UnexpectedError, False)
                    raise RuntimeError, UnexpectedError
                self.PrintToScreenAndFile("File %s is not already checked out" % self.MakeFileWithPath, True)

                # Check the file out.
                self.PrintToScreenAndFile("Checking out file %s" % self.MakeFileWithPath, True)
                if clearcase.checkout(self.MakeFileWithPath, False, 'Temporary Checkout for Fault Injection Test.') != None:
                    UnexpectedError = "Error while trying to checkout file %s!" % self.MakeFileWithPath
                    self.PrintToScreenAndFile(UnexpectedError, False)
                    raise RuntimeError, UnexpectedError
                self.PrintToScreenAndFile("File %s has been checked out." % self.MakeFileWithPath, True)
        
                # Modify the file.
                self.ModifyFile(makefileModificationsDictionaryRM, "makefile", self.MakeFileWithPath)
                self.ModifyFile(makefileModificationsDictionaryDEL, "makefile", self.MakeFileWithPath)

            elif sys.argv[1] == "ApexOS" :

                self.ProductName = APEX_PRODUCT_NAME

                self.Init(TestName)

                self.DiagEditPath      = self.ViewPath + "\\" + APEX_PRODUCT_FOLDER + "\\" + APEX_OS_PATH

                self.CleanBuildCmd = ".\\" + APEX_BUILD_SCRIPT + " " + self.BranchPath + " " + APEX_MAKE_CLEAN_CMD
		
                self.BuildExecutableCmd = ".\\" + APEX_BUILD_SCRIPT + " " + self.BranchPath + " " + APEX_MAKE_CMD

                self.ResultsOfBuildFolder = self.ViewPath + "\\" + APEX_PRODUCT_FOLDER + "\\"  + APEX_PROJECT_FOLDER

                self.MakeFileWithPath = self.ViewPath + "\\" + APEX_PRODUCT_FOLDER + "\\"  + APEX_PROJECT_FOLDER + "\\makefile"
        
                if clearcase.isCheckedOut(self.MakeFileWithPath):
                    if clearcase.uncheckout(self.MakeFileWithPath, keep = True) != None:
                        UnexpectedError = "Error while trying to uncheckout file %s!" % self.MakeFileWithPath
                        self.PrintToScreenAndFile(UnexpectedError, False)
                        raise RuntimeError, UnexpectedError
                    UnexpectedError = "File %s already Checked Out!" % self.MakeFileWithPath
                    self.PrintToScreenAndFile(UnexpectedError, False)
                    raise RuntimeError, UnexpectedError
                self.PrintToScreenAndFile("File %s is not already checked out" % self.MakeFileWithPath, True)

                # Check the file out.
                self.PrintToScreenAndFile("Checking out file %s" % self.MakeFileWithPath, True)
                if clearcase.checkout(self.MakeFileWithPath, False, 'Temporary Checkout for Fault Injection Test.') != None:
                    UnexpectedError = "Error while trying to checkout file %s!" % self.MakeFileWithPath
                    self.PrintToScreenAndFile(UnexpectedError, False)
                    raise RuntimeError, UnexpectedError
                self.PrintToScreenAndFile("File %s has been checked out." % self.MakeFileWithPath, True)
        
                # Modify the file.
                self.ModifyFile(makefileModificationsDictionaryRM, "makefile", self.MakeFileWithPath)
                self.ModifyFile(makefileModificationsDictionaryDEL, "makefile", self.MakeFileWithPath)
            else :

                raise RuntimeError, "Invalid command line arg"
        self.ModifyFileBuildFaultInjectionTest(fileModificationsDictionary, TestName)
    




