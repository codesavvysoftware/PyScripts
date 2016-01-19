#/////////////////////////////////////////////////////////////////////////////
#/// @file LegacyFaultInjectionUtils.py
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
#/// tnhaley  14-JAN-2013 Created.
#/// @endif
#///
#/// @par Copyright (c) 2016 Rockwell Automation Technologies, Inc.  All rights reserved.
#///
#/////////////////////////////////////////////////////////////////////////////

#-----------------------------------------------------------------------------
import ClearCase  # For isCheckedOut, checkout, uncheckout
import os         # For path
import datetime   # For date
import shutil     # For Copy
import msvcrt     # For getch

# Define constants that need to be confirmed/modified at run time.
# The order of projects in ENZTR_PROJECT_NAME and CNZ_PROJECT_NAME is
# important. A specific order is used to make sure that the requirements
# for a later project are built.
ENZTR_PROJECT_NAME = ["Proj_Apex_SIL2", 
                      "Proj_ice2_HV20_BSP", 
					  "Proj_ABOS_VMS", 
					  "Proj_BSP_VMS", 
					  "Proj_Crypto_DKM", 
					  "Proj_VMS_ENzTR", \
                      "Proj_ICE2_ENzTR_VIP", 
					  "Proj_ICE2_ENzTR-Safeboot_VIP", 
					  "Proj_HIP_Safeboot_ENzTR", 
					  "Proj_HIP_ENzTR"]

CNZ_PROJECT_NAME = ["Proj_Apex_Non-SIL2", "Proj_ABOS_VMS", "Proj_BSP_VMS", "Proj_VMS_CNz", "Proj_ICE2_CNzR-Safeboot_VIP", \
                    "Proj_ice2_HV20_BSP", "Proj_HIP_Safeboot_CNzR", "Proj_Apex_SIL2", "Proj_vbi_2_3_0", "Proj_BSP_ICE2_CNzR_PV", \
                    "Proj_ICE2_CNet_VB", "Proj_ICE2_CNzR_VIP", "Proj_HIP_CNzR"]

ENZTR_PRODUCT_NAME = "ENzTR"

CNZ_PRODUCT_NAME                              = "CNz"

ENZTR_MAIN_HIP_PROJECT                        = "Proj_HIP_ENzTR"

CNZ_MAIN_HIP_PROJECT                          = "Proj_HIP_CNzR"

ENZTR_MAIN_VIP_PROJECT_DEFAULT_FOLDER         = "\\LNX\\NetLinxUCS\\Proj_ICE2_ENzTR_VIP\\default"

CNZ_MAIN_VIP_PROJECT_DEFAULT_FOLDER           = "\\LNX\\NetLinxUCS\\Proj_ICE2_CNz_VIP\\default"

ENZTR_PV_BSP_DKM_PARTIAL_IMAGE_OBJECTS_FOLDER = "\\LNX\\Platform\\BSP\\Board\\Ice2_ENzT\\PV\\Proj_ENzTR_PV_BSP_DKM\\ARMARCH7gnu\\Proj_ENzTR_PV_BSP_DKM_partialImage\\NonDebug\\Objects"

CNZ_PV_BSP_DKM_PARTIAL_IMAGE_OBJECTS_FOLDER   = "\\LNX\\Platform\\BSP\\Board\\Ice2_CNz\\PV\\Proj_CNzR_PV_BSP_DKM\\ARMARCH7gnu\\Proj_CNzR_PV_BSP_DKM_partialImage\\NonDebug\\Objects"
                                                "\\LNX\\Platform\\BSP\\Board\\Ice2_CNz\\PV\\Proj_CNzR-Safeboot_PV_BSP_DKM\\ARMARCH7gnu\\Proj_CNzR-Safeboot_PV_BSP_DKM_partialImage\\NonDebug\\Objects"

WRWB_WORKSPACE = "C:\\workspaces\\workspace_diagnostics_fault_injection_testing_3.9.9"

WORKBENCH_INSTALLATION_FOLDER                 = "C:\\Rockwell_Work_Bench"

RA_WORKBENCH_VERSION                          = "\\WB_PID_3_9_09"

WORKBENCH_PATH                                = WORKBENCH_INSTALLATION_FOLDER + RA_WORKBENCH_VERSION

WIND_RIVER_HYPERVISOR_FOLDER                  = "\\wrhv-2.0"

WORKBENCH_VERSION                             = "\\workbench-3.3"

VXWORKS_VERSION                               = "vxworks-6.9"

WORKBENCH_ENVIRONMENT_COMMAND                 = "\\wrenv -p"

WORKBENCH_BUILD_COMMAND                       = "\\x86-win32\\bin\\wrws_update.bat -data %s -f 0 -j %s -b build >> \"%s\\%s\" 2>>&1"

HYPERVISOR_VERSION                            = " ICE2_HV_2.0 "

WORKBENCH_MAKE_WORKSPACE_COMMAND              = "cscript /nologo %s\\LNX\\Platform\\Tools\\MakeWorkspace\\MakeWorkspace.wsf %s\\LNX %s %s  >> \"%s\\%s\" 2>>&1"


# Define constants that should not change.
SEARCH_VOB_STR                                            = "\\LogixTests\\"

SOURCE_FOLDERS_ALLOWED_TO_BE_MODIFIED_FILENAME            = "FaultInjectionSrcFoldersAllowedToBeModified.txt"

BUILD_LOG_FILE_NAME                                       = "build.log"

MAKE_WORKSPACE_LOG_FILE_NAME                              = "MakeWorkspace.log"

MAX_NUMBER_OF_SRC_FOLDERS_ALLOWED_TO_BE_MODIFIED          = 100

MAX_NUMBER_OF_SRC_FILES_ALLOWED_TO_BE_MODIFIED            = 100

MAX_NUMBER_OF_FILES_AND_FOLDERS_TO_DELETE_BEFORE_BUILDING = 100

MAX_NUMBER_OF_BUILDS_PER_SCRIPT_PER_PRODUCT_PER_DAY       = 50

BUILD_RESULTS_FOLDER_NAME                                 = "Build Results"

BUILD_FILES_FOLDER_NAME                                   = "\\obj_ice2_wrhv\\"

MAIN_BUILT_BINARY_FILE_NAME                               = "\\system.elf"

PRODUCTS_PATH                                             = "\\LNX\\Products\\"

WORKBENCH_GNU_FOLDER                                      = WORKBENCH_PATH + WIND_RIVER_HYPERVISOR_FOLDER + "\\obj\\lib_wrhv\\arm\\ARMCA9\\gnu"

DIAGNOSTICS_DKM_ARMARCH7GNU_FOLDER                        = "\\LNX\\NetLinxUCS\\Proj_Diagnostics_DKM\\ARMARCH7gnu"

LIB_ICE2_A_FILE                                           = WORKBENCH_GNU_FOLDER + "\\libice2.a"

LIB_ICE2_DIAGNOSTICS_A_FILE                               = WORKBENCH_GNU_FOLDER + "\\libice2diagnostics.a"

OBJ_ICE2_FOLDER                                           = WORKBENCH_GNU_FOLDER + "\\objice2"

OBJ_ICE2_DIAGNOSTICS_FOLDER                               = WORKBENCH_GNU_FOLDER + "\\objice2diagnostics"

APEX_BINARY_H_FILE                                        = "\\LNX\\Platform\\NetLinxUCS\\BSP\\ICE2\\RaSupport\\ApexBinary.h"

APEX_BINARY_FILE                                          = "\\LNX\\Logix\\Engine\\Subsystems\\Apex\\Release\\Apex.bin"

ENZTR_BSP_APEX_IMPL_O_FILE                                = ENZTR_PV_BSP_DKM_PARTIAL_IMAGE_OBJECTS_FOLDER + "\\bsp_ApexImpl.o"

ENZTR_BSP_APEX_IMPL_D_FILE                                = ENZTR_PV_BSP_DKM_PARTIAL_IMAGE_OBJECTS_FOLDER + "\\bsp_ApexImpl.d"

CNZ_BSP_APEX_IMPL_O_FILE                                  = CNZ_PV_BSP_DKM_PARTIAL_IMAGE_OBJECTS_FOLDER + "\\bsp_ApexImpl.o"

CNZ_BSP_APEX_IMPL_D_FILE                                  = CNZ_PV_BSP_DKM_PARTIAL_IMAGE_OBJECTS_FOLDER + "\\bsp_ApexImpl.d"

NON_VIEW_FILES_AND_FOLDERS_TO_DELETE_BEFORE_BUILDING      = [LIB_ICE2_A_FILE, LIB_ICE2_DIAGNOSTICS_A_FILE, \
                                                             OBJ_ICE2_FOLDER, OBJ_ICE2_DIAGNOSTICS_FOLDER]
CNET_VB_AFX_FILE                                          = "\\LNX\\NetLinxUCS\\CNet_VB\\obj_CNzR_debug\\CNet_VB.axf"

ENZTR_VIEW_FILES_AND_FOLDERS_TO_DELETE_BEFORE_BUILDING    = [PRODUCTS_PATH + ENZTR_MAIN_HIP_PROJECT + BUILD_FILES_FOLDER_NAME,
                                                             ENZTR_MAIN_VIP_PROJECT_DEFAULT_FOLDER, APEX_BINARY_H_FILE, \
                                                             DIAGNOSTICS_DKM_ARMARCH7GNU_FOLDER, ENZTR_BSP_APEX_IMPL_O_FILE, \
                                                             ENZTR_BSP_APEX_IMPL_D_FILE, APEX_BINARY_FILE]

CNZ_VIEW_FILES_AND_FOLDERS_TO_DELETE_BEFORE_BUILDING      = [PRODUCTS_PATH + CNZ_MAIN_HIP_PROJECT + BUILD_FILES_FOLDER_NAME,
                                                             CNZ_MAIN_VIP_PROJECT_DEFAULT_FOLDER, APEX_BINARY_H_FILE, \
                                                             DIAGNOSTICS_DKM_ARMARCH7GNU_FOLDER, CNZ_BSP_APEX_IMPL_O_FILE, \
                                                             CNZ_BSP_APEX_IMPL_D_FILE, APEX_BINARY_FILE, CNET_VB_AFX_FILE]

# Define the dictionary for delaying Apex diagnostics startup.
# An individual diagnostic fault injection script file calls into this file to merge
# with this dictionary to make sure that its diagnostic fault injection testing does not
# fail before ICE2 checks the fault line for Apex2 failures.
ApexDiagnosticsStartupDelayDictionary = {\
    'ApexDiagnostic.cpp': [ \
    # # # # # # # # # # # # # # # # # # # # # # # # # 
    '''
    // Start Fault Injection Point 3
    // End Fault Injection Point 3
    // Fault Injection Code Start
    for ( int DiagIndex = 0; DiagIndex < DGN_NUM_RUNTIME_TESTS; DiagIndex++ )
    {
        DgnList[DiagIndex].triggerValueTimeslice = MsToDgnSlices(30000); // 30 seconds
    }
    // Fault Injection Code End
    '''
    ]
}

# ProductSelection class
# This class is used for obtaining the product selection from user input.
class ProductSelectionOptions:
    NoProduct, ENzTR, CNz, Exit = range(4)

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
        self.BuildResultsSubFolderName = cwdStr + "\\" + BUILD_RESULTS_FOLDER_NAME + "\\" + str(today) + " " + self.ProductName + " " + TestName

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

        # Initialize the workspace variable.
        self.Workspace = WRWB_WORKSPACE

        # Read and save all of the allowed source code folders from the text file.
        self.AllowedFolder = range(MAX_NUMBER_OF_SRC_FOLDERS_ALLOWED_TO_BE_MODIFIED)
        allowedFoldersFile = open(SOURCE_FOLDERS_ALLOWED_TO_BE_MODIFIED_FILENAME)
        self.AllowedFolderFileLineCount = 0;
        for line in allowedFoldersFile.readlines():
            self.AllowedFolder[self.AllowedFolderFileLineCount] = line.strip()
            self.AllowedFolderFileLineCount += 1
        allowedFoldersFile.close()

        # Create the array of old files and folders to be deleted before building.
        self.FilesAndFoldersToDeleteBeforeBuilding = range(MAX_NUMBER_OF_FILES_AND_FOLDERS_TO_DELETE_BEFORE_BUILDING)
        for i in range(len(self.ViewFilesAndFoldersToDeleteBeforeBuilding)):
            self.FilesAndFoldersToDeleteBeforeBuilding[i] = self.ViewPath + self.ViewFilesAndFoldersToDeleteBeforeBuilding[i]

        for j in range(len(NON_VIEW_FILES_AND_FOLDERS_TO_DELETE_BEFORE_BUILDING)):
            self.FilesAndFoldersToDeleteBeforeBuilding[i + j + 1] = NON_VIEW_FILES_AND_FOLDERS_TO_DELETE_BEFORE_BUILDING[j]

        self.FilesAndFoldersToDeleteBeforeBuilding[i + j + 2] = self.BuildResultsSubFolderName + "\\" + BUILD_LOG_FILE_NAME

        self.NumberOfFilesAndFoldersToDelete = len(self.ViewFilesAndFoldersToDeleteBeforeBuilding) + len(NON_VIEW_FILES_AND_FOLDERS_TO_DELETE_BEFORE_BUILDING) + 1

    #-------------------------------------------------------------------------
    # Check if the file found is in the list of folders allowed to be modified.
    def IsFileFoundInAllowedFolders(self, filename):
        isFileFound = False
        productString = "%" + self.ProductName + "%" # for product-specific paths

        for lineIndex in range(0, self.AllowedFolderFileLineCount):
            if len(self.AllowedFolder[lineIndex]) and (self.AllowedFolder[lineIndex][0] != "#") and \
                  (self.AllowedFolder[lineIndex][0] != " "):

                if productString in self.AllowedFolder[lineIndex]:
                    self.AllowedFolder[lineIndex] = self.AllowedFolder[lineIndex].replace("%", "")

                # Determine the file path and confirm that it exists.
                filePath = self.ViewPath + self.AllowedFolder[lineIndex] + "\\" + filename
                if os.path.isfile(filePath):
                    isFileFound = True
                    self.FileToEditIndex += 1
                    self.FileToEditWithPath[self.FileToEditIndex] = filePath
                    break

        return isFileFound

    #-------------------------------------------------------------------------
    # Modify the file as specified in the fault injection script file's dictionary.
    def ModifyFile(self, fileModificationsDictionary, filename):
        self.PrintToScreenAndFile("Modifying file %s" % self.FileToEditWithPath[self.currentFileToEditIndex], True)
        fileToEdit = open(self.FileToEditWithPath[self.currentFileToEditIndex])
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
                UnexpectedError = "Search pattern '%s' not found in %s" % (patternStart, self.FileToEditWithPath[self.currentFileToEditIndex])
                self.PrintToScreenAndFile(UnexpectedError, False)
                raise RuntimeError, UnexpectedError
            try:
                end = text.index(patternEnd, start) + len(patternEnd)
            except ValueError:
                UnexpectedError = "Search pattern '%s' not found in %s" % (patternEnd, self.FileToEditWithPath[self.currentFileToEditIndex])
                self.PrintToScreenAndFile(UnexpectedError, False)
                raise RuntimeError, UnexpectedError
            result = text[start:end]
            text = text.replace(result,newblock_woPattern)
        fileToEdit = open(self.FileToEditWithPath[self.currentFileToEditIndex],'w')
        fileToEdit.write(text)
        fileToEdit.close()
        self.PrintToScreenAndFile("File %s has been Modified" % self.FileToEditWithPath[self.currentFileToEditIndex], True)

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
            if not self.IsFileFoundInAllowedFolders(filename):
                UnexpectedError = "File '%s' was not found in any of the allowed folders" % filename
                self.PrintToScreenAndFile(UnexpectedError, False)
                raise RuntimeError, UnexpectedError
            filenameArray[self.FileToEditIndex] = filename

        # Loop through all of the files to edit and process each one.
        for self.currentFileToEditIndex in range(0, self.FileToEditIndex + 1):
            # Check if the file is already checked out.
            self.PrintToScreenAndFile("Checking if file %s is already checked out..." % self.FileToEditWithPath[self.currentFileToEditIndex], True)
            if ClearCase.isCheckedOut(self.FileToEditWithPath[self.currentFileToEditIndex]):
                UnexpectedError = "File %s already Checked Out!" % self.FileToEditWithPath[self.currentFileToEditIndex]
                self.PrintToScreenAndFile(UnexpectedError, False)
                raise RuntimeError, UnexpectedError
            self.PrintToScreenAndFile("File %s is not already checked out" % self.FileToEditWithPath[self.currentFileToEditIndex], True)

            # Check the file out.
            self.PrintToScreenAndFile("Checking out file %s" % self.FileToEditWithPath[self.currentFileToEditIndex], True)
            if ClearCase.checkout(self.FileToEditWithPath[self.currentFileToEditIndex], False, 'Temporary Checkout for Fault Injection Test.') != None:
                UnexpectedError = "Error while trying to checkout file %s!" % self.FileToEditWithPath[self.currentFileToEditIndex]
                self.PrintToScreenAndFile(UnexpectedError, False)
                raise RuntimeError, UnexpectedError
            self.PrintToScreenAndFile("File %s has been checked out." % self.FileToEditWithPath[self.currentFileToEditIndex], True)

            # Modify the file.
            self.ModifyFile(fileModificationsDictionary, filenameArray[self.currentFileToEditIndex])

            # Copy the modified file to the build results folder.
            self.PrintToScreenAndFile("Copying modified file %s" % self.FileToEditWithPath[self.currentFileToEditIndex], True)
            if shutil.copy(self.FileToEditWithPath[self.currentFileToEditIndex], self.BuildResultsSubFolderName + "\\" + filenameArray[self.currentFileToEditIndex] + ".modified") != None:
                UnexpectedError = "Error while trying to copy modified file %s!" % self.FileToEditWithPath[self.currentFileToEditIndex]
                self.PrintToScreenAndFile(UnexpectedError, False)
                raise RuntimeError, UnexpectedError
            self.PrintToScreenAndFile("Modified file %s has been copied as %s" % (self.FileToEditWithPath[self.currentFileToEditIndex], filenameArray[self.currentFileToEditIndex] + ".modified"), True)

    #-----------------------------------------------------------------------------
    # Get the desired workspace selection.
    def GetWorkspaceSelection(self):
        IsValidUseDefaultSelection = False
        while (not IsValidUseDefaultSelection):
            self.PrintToScreenAndFile ("Do you want to use the default workspace (%s)? (y/n (or x to exit))" % self.Workspace, True)
            c = msvcrt.getch()
            self.PrintToScreenAndFile( c, True)
            if c == 'x' or c == 'X':
                UnexpectedError = "The program exited due to user request! The program did NOT complete successfully!"
                self.PrintToScreenAndFile(UnexpectedError, False)
                raise RuntimeError, UnexpectedError
            if c == 'y' or c == 'Y' or c == 'n' or c == 'N':
                IsValidUseDefaultSelection = True
            else:
                self.PrintToScreenAndFile("Invalid entry.", True)

        if c == 'n' or c == 'N':
            IsValidWorkspaceSelection = False
            while (not IsValidWorkspaceSelection):
                InputString = raw_input("Enter the workspace path and name to be used ('x' to exit):")
                if InputString == "x" or InputString == "X":
                    UnexpectedError = "The program exited due to user request! The program did NOT complete successfully!"
                    self.PrintToScreenAndFile(UnexpectedError, False)
                    raise RuntimeError, UnexpectedError
                elif InputString != "":
                    self.Workspace = InputString
                    IsValidWorkspaceSelection = True
        self.PrintToScreenAndFile ("self.Workspace = %s" % self.Workspace, True)

    #-------------------------------------------------------------------------
    # If the workspace does not already exist, make it.
    def MakeWorkspace(self):
        if not os.path.exists(self.Workspace):
            IsValidMakeWorkspaceSelection = False
            while (not IsValidMakeWorkspaceSelection):
                self.PrintToScreenAndFile("Workspace %s was not found, make workspace now? (y or x to exit)" % self.Workspace, True)
                c = msvcrt.getch()
                print c
                if c == 'x' or c == 'X':
                    UnexpectedError = "The program exited due to user request! The program did NOT complete successfully!"
                    raise RuntimeError, UnexpectedError
                if c == 'y' or c == 'Y':
                    IsValidMakeWorkspaceSelection = True
                else:
                    print("Invalid entry.")
            self.PrintToScreenAndFile("Making workspace %s..." % self.Workspace, True)
            if os.system((WORKBENCH_PATH + WORKBENCH_ENVIRONMENT_COMMAND + " " + VXWORKS_VERSION + " " + WORKBENCH_MAKE_WORKSPACE_COMMAND \
               % (self.ViewPath, self.ViewPath, HYPERVISOR_VERSION, self.Workspace, self.BuildResultsSubFolderName, MAKE_WORKSPACE_LOG_FILE_NAME))):
                UnexpectedError = "Error while making the workspace! See %s\\%s for the errors!" % (self.BuildResultsSubFolderName, BUILD_LOG_FILE_NAME)
                self.PrintToScreenAndFile(UnexpectedError, False)
                raise RuntimeError, UnexpectedError
            self.PrintToScreenAndFile("Workspace %s has been successfully created." % self.Workspace, True)
        else:
            self.PrintToScreenAndFile("Workspace %s already exists so no need to create it." % self.Workspace, True)

        # If the workspace folder does not exist, return an error.
        if not os.path.exists(self.Workspace):
            UnexpectedError = "Workspace folder (%s) does not exist!" % self.Workspace
            self.PrintToScreenAndFile(UnexpectedError, False)
            raise RuntimeError, UnexpectedError

    #-------------------------------------------------------------------------
    # Build the modified code.
    def BuildModifiedCode(self):
        self.PrintToScreenAndFile("Building Modified Firmware...", True)
        self.PrintToScreenAndFile("For details, see build log file %s." % self.BuildResultsSubFolderName + "\\" + BUILD_LOG_FILE_NAME, True)

        # Delete the old files and folders to be deleted before building.
        for k in range(self.NumberOfFilesAndFoldersToDelete):
            if os.path.exists(self.FilesAndFoldersToDeleteBeforeBuilding[k]):
                try:
                    # If it is a directory, use shutil.rmtree(). Otherwise, use os.remove().
                    if os.path.isdir(self.FilesAndFoldersToDeleteBeforeBuilding[k]):
                        shutil.rmtree(self.FilesAndFoldersToDeleteBeforeBuilding[k])
                    else:
                        os.remove(self.FilesAndFoldersToDeleteBeforeBuilding[k])
                except:
                    pass

        # Perform the build.
        for i in range(len(self.ProjectName)):
            if os.system((WORKBENCH_PATH + WORKBENCH_ENVIRONMENT_COMMAND + " " + VXWORKS_VERSION + " " + WORKBENCH_PATH + WORKBENCH_VERSION + WORKBENCH_BUILD_COMMAND \
                          % (self.Workspace, self.ProjectName[i], self.BuildResultsSubFolderName, BUILD_LOG_FILE_NAME))):
                UnexpectedError = "Error while building the modified code! See %s\\%s for the errors!" % (self.BuildResultsSubFolderName, BUILD_LOG_FILE_NAME)
                self.PrintToScreenAndFile(UnexpectedError, False)
                raise RuntimeError, UnexpectedError

        # If the product build main binary file does not exist under the product build folder, return an error.
        if not os.path.exists(self.ViewPath + PRODUCTS_PATH + self.MainHipProject + BUILD_FILES_FOLDER_NAME + MAIN_BUILT_BINARY_FILE_NAME):
            UnexpectedError = "Build Failed! Product build main binary file (%s) does not exist!" \
            % (self.ViewPath + PRODUCTS_PATH + self.MainHipProject + BUILD_FILES_FOLDER_NAME + MAIN_BUILT_BINARY_FILE_NAME)
            self.PrintToScreenAndFile(UnexpectedError, False)
            raise RuntimeError, UnexpectedError

        self.PrintToScreenAndFile("Finished Building Modified Firmware Successfully.", True)

    #-------------------------------------------------------------------------
    # Copy the product build binary folder to the build results subfolder.
    def CopyBinaryFolder(self):
        # If a previous binary files folder already exists under the fault injection build results folder, delete it since copytree will fail if it already exists.
        if os.path.exists(self.BuildResultsSubFolderName + BUILD_FILES_FOLDER_NAME):
            shutil.rmtree(self.BuildResultsSubFolderName + BUILD_FILES_FOLDER_NAME)

        # Copy the binary files folder to the build results folder.
        self.PrintToScreenAndFile("Copying the binary files folder (%s) to the build results folder (%s)." % (self.ViewPath + PRODUCTS_PATH + self.MainHipProject + BUILD_FILES_FOLDER_NAME, self.BuildResultsSubFolderName + BUILD_FILES_FOLDER_NAME), True)
        shutil.copytree(self.ViewPath + PRODUCTS_PATH + self.MainHipProject + BUILD_FILES_FOLDER_NAME, self.BuildResultsSubFolderName + BUILD_FILES_FOLDER_NAME)
        self.PrintToScreenAndFile("Copy the binary files folder to the build results folder.", True)

    #-----------------------------------------------------------------------------
    # Undo the check out of all of the files in the fault injection script file's
    # dictionary that were checked out.
    def UndoCheckouts(self):
        self.PrintToScreenAndFile("Undoing Checkouts...", True)
        for currentFileToEditIndex in range(0, self.FileToEditIndex + 1):
            if ClearCase.isCheckedOut(self.FileToEditWithPath[currentFileToEditIndex]):
                self.PrintToScreenAndFile("Undoing checkout of file %s..." % self.FileToEditWithPath[currentFileToEditIndex], True)
                if ClearCase.uncheckout(self.FileToEditWithPath[currentFileToEditIndex], keep = True) != None:
                    UnexpectedError = "Error while trying to uncheckout file %s!" % self.FileToEditWithPath[currentFileToEditIndex]
                    self.PrintToScreenAndFile(UnexpectedError, False)
                    raise RuntimeError, UnexpectedError
                self.PrintToScreenAndFile("File %s has been unchecked out" % self.FileToEditWithPath[currentFileToEditIndex], True)

    #-----------------------------------------------------------------------------
    # Merge the specified dictionaries into a new dictionary.
    # Note that this method is needed instead of just using the existing
    # dictionary .update() method in order to properly handle repeated keys (the
    # case where multiple dictionaries being merged contain the same key (file
    # name)). The .update() method just replaces the contents of the repeated key
    # in the first dictionary with the contents of the repeated key from the
    # second dictionary so the contents of the repeated key in the first
    # dictionary is lost.
    # Returns the new dictionary.
    def MergeDictionaries(self, dictionary1, dictionary2):
        mergedDictionary = dictionary1.copy()
        for key in dictionary2:
            if key in mergedDictionary:
                mergedDictionary[key].extend(dictionary2[key])
            else:
                mergedDictionary[key] = dictionary2[key]
        return mergedDictionary

    #-----------------------------------------------------------------------------
    # Configure the Apex diagnositc startup delay.
    # This is done to make sure that no diagnostic fault injection tests
    # fail before ICE2 starts checking the fault line for Apex2 failures.
    # Some diagnostic fault injection tests were failing before then which
    # caused ICE2 to fail for the wrong reason during those tests.
    # This method is called only from diagnostic fault injection test files
    # that would otherwise fail in that manner. This method is not called
    # from within this file.
    def ConfigApexDiagnosticsStartupDelay(self, fileModificationsDictionary):
        mergedDictionary = self.MergeDictionaries(fileModificationsDictionary, ApexDiagnosticsStartupDelayDictionary)
        return mergedDictionary

    #-----------------------------------------------------------------------------
    # Get the desired product selection.
    def GetProductSelection(self):
        ValidProductSelection = False
        while (not ValidProductSelection):
            print ("Please select the product that you are running this script for (or 3 to exit):")
            print ("     %s. ENzTR" % str(ProductSelectionOptions.ENzTR))
            print ("     %s. CNz" % str(ProductSelectionOptions.CNz))
            print ("     %s. Exit" % str(ProductSelectionOptions.Exit))
            print("Enter selection here: "),
            c = msvcrt.getch()
            try:
                self.ProductSelection = int(c)
            except:
                self.ProductSelection = 0
            print(self.ProductSelection)

            # If the selection was valid, set the flag to true and continue. Otherwise, print message and try again.
            if (self.ProductSelection > ProductSelectionOptions.NoProduct) and (self.ProductSelection < ProductSelectionOptions.Exit + 1):
                ValidProductSelection = True
            else:
                print("Invalid entry.")

        if self.ProductSelection == ProductSelectionOptions.Exit:
            UnexpectedError = "The program exited due to user request! The program did NOT complete successfully!"
            raise RuntimeError, UnexpectedError

    #-----------------------------------------------------------------------------
    # Set the product specific settings based on the product selection.
    def SetProductSpecificSettings(self):
        if self.ProductSelection == ProductSelectionOptions.ENzTR:
            self.ProductName = ENZTR_PRODUCT_NAME
            self.ProjectName = ENZTR_PROJECT_NAME
            self.MainHipProject = ENZTR_MAIN_HIP_PROJECT
            self.ViewFilesAndFoldersToDeleteBeforeBuilding = ENZTR_VIEW_FILES_AND_FOLDERS_TO_DELETE_BEFORE_BUILDING

        elif self.ProductSelection == ProductSelectionOptions.CNz:
            self.ProductName = CNZ_PRODUCT_NAME
            self.ProjectName = CNZ_PROJECT_NAME
            self.MainHipProject = CNZ_MAIN_HIP_PROJECT
            self.ViewFilesAndFoldersToDeleteBeforeBuilding = CNZ_VIEW_FILES_AND_FOLDERS_TO_DELETE_BEFORE_BUILDING

        else:
            UnexpectedError = "Invalid product selection value (%s)!" % self.ProductSelection
            raise RuntimeError, UnexpectedError

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
        #        "self.ProductSelection = ProductSelectionOptions.ENzTR"
        #     4. Make sure that WRWB_WORKSPACE is set equal to the workspace
        #        path and name to be used above.
        #     5. Comment out the call to self.GetWorkspaceSelection() below.
        #     6. Create a batch file and use "call" for every script file that
        #        is to be run. For example:
        #            call python InteractiveWatchdogFaultInjectionTest1.py
        #            call python InteractiveWatchdogFaultInjectionTest2.py
        #     7. When done, undo the checkout of this file. Do not check these
        #        changes in.

        # Get the product selection.
        self.GetProductSelection()

        # Set the product specific settings based on the product selection from the user.
        self.SetProductSpecificSettings()

        # Perform all necessary initialization.
        self.Init(TestName)

        # Get the workspace selection.
        self.GetWorkspaceSelection()

        # Create the workspace.
        self.MakeWorkspace()

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