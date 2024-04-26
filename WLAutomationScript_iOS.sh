#!/bin/bash

initialLoad() {
    print_success() {
        name=$1
        echo -e "${GREEN}$name${NC}"
    }
    
    print_error() {
        name=$1
        echo -e "${RED}$name${NC}"
    }
    
    print_warrning() {
        name=$1
        echo -e "${YELLOW}$name${NC}"
    }
}
initialLoad



GIT_TOKEN="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"
REPOSITORY="https://$GIT_TOKEN@github.com/elitesoftsysadmin/Whitelabel_Automation_POC.git"
GIT_BRANCH="WhiteLabelTesting" #"master"
WORKSPACE="$HOME/Desktop/WL_Automation/Respository/Project"

loadGit() {
    git clone "$REPOSITORY" "$WORKSPACE"
    cd "$WORKSPACE"  # Change to the workspace directory
    git checkout "$GIT_BRANCH"
    git branch
}
loadGit

sleep 2
cd $WORKSPACE

# Define color variables
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

cleanup(){
    git reset
    git stash
    git stash drop
    git checkout $GIT_BRANCH
    
    echo "GIT RESET FINISHED AND SWITCHED TO MASTER BRANCH"
}

removeExistBranch() {
    branchName=$1
    echo "GIT BRANCHES"
    
    # list of origin branches (remote branches)
    git branch -r
    
    echo " Deleting Branch ..."
    # Remove the remote branch
    git push origin --delete $branchName
}



update() {
    # Split the branch name from the json file name
    file=`basename $1 .json`
    branchName=$(echo $file|awk -F_ '{print $NF}')
    
    removeExistBranch $branchName
    echo "$branchName New Branch Creating ..."
    git checkout $branchName || git checkout -b $branchName
    
    print_error "GIT BRANCHES"
    git branch -r
    
    print_warrning "REPLACING BEGIN ..."
    python3 updateDetailsIOS.py $1
    print_success "REPLACING FINISHED"
    
    git add $WORKSPACE
    git commit -m "Update Modification $1"
    git push origin $branchName
    echo "Current Branch Name: $branchName"
    
    print_warrning "BUILD PROCESSES BEGIN ..."
    cleanBuild $branchName
    archive $branchName
    exportDevelopmentBuild $branchName
    exportBuild $branchName
#    uploadBuild $branchName
    print_success "BUILD PROCESSES FINISHED"
    cleanup
}

cleanBuild() {
    name=$1
    
    xcodebuild -workspace EliteConnect.xcworkspace -scheme EliteConnect clean build -allowProvisioningUpdates
    print_success "$name: BUILD CLEANING FINISHED"
}

archive() {
    name=$1
    
    rm -r "$HOME/Desktop/WL_Automation/IPA_Exported/Archive"
    
    # Define variables
    workspace="EliteConnect.xcworkspace"
    scheme="EliteConnect"
    configuration="Release"
    archivePath="$HOME/Desktop/WL_Automation/IPA_Exported/Archive/$name/EliteConnect.xcarchive"
    
    xcodebuild archive -workspace "$workspace" -scheme "$scheme" -configuration "$configuration" -archivePath "$archivePath" -allowProvisioningUpdates
    
    print_success "$name - BUILD ARCHIVIING FINISHED"
}

exportDevelopmentBuild() {
    name=$1
    
    archiveDirectoryPath="$HOME/Desktop/WL_Automation/IPA_Exported/Archive/$name/EliteConnect.xcarchive"
    exportDirectoryPath="$HOME/Desktop/WL_Automation/IPA_Exported/Development/$name"
    
    xcodebuild -exportArchive -allowProvisioningUpdates -archivePath "$archiveDirectoryPath" -exportPath "$exportDirectoryPath" -exportOptionsPlist ExportOptions2.plist
    
    print_success "$name - BUILD DEVELOPMENT EXPORT FINISHED"
}

exportBuild() {
    name=$1
    
    archiveDirectoryPath="$HOME/Desktop/WL_Automation/IPA_Exported/Archive/$name/EliteConnect.xcarchive"
    exportDirectoryPath="$HOME/Desktop/WL_Automation/IPA_Exported/AppStore/$name"
    
    xcodebuild -exportArchive -allowProvisioningUpdates -archivePath "$archiveDirectoryPath" -exportPath "$exportDirectoryPath" -exportOptionsPlist ExportOptions.plist
    
    print_success "$name - BUILD APP STORE EXPORT FINISHED"
}

uploadBuild() {
    name=$1
    
    filePath="$HOME/Desktop/WL_Automation/Branch_Script_JSON/$name/app_parameter_ios_$name.json"
    username_key="Username"
    password_key="Password"
    
    jqPath="/opt/homebrew/bin/jq"
    username=$($jqPath -r .$username_key $filePath)
    password=$($jqPath -r .$password_key $filePath)
    
    print_warrning "Apple Developer Username: $username and Password: $password From File Path: $filePath"
    
    
    xcrun altool --upload-app --type ios --file "$HOME/Desktop/WL_Automation/IPA_Exported/AppStore/$name/EliteConnect.ipa" --username $username --password $password
    
    print_success "$name - BUILD APP STORE UPLOADING FINISHED"
    
}

jsonDirectoryPath="$HOME/Desktop/WL_Automation/Branch_Script_JSON/*"
for directory in $jsonDirectoryPath
do

dirname=$(basename "$directory")
json_files=("$directory"/*.json)
file="${json_files[0]}"
print_warrning "File Name JSON: $file"

cd $WORKSPACE
update $file
pwd
done




