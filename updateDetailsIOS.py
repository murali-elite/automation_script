#/usr/bin/python
import json
import os
import shutil
import zipfile
from importlib import reload

import re
import requests
import configparser
import sys
import wget
from pathlib import Path
from shutil import rmtree

def removedirectory(path):
    for path in Path(path).glob("**/*"):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            rmtree(path)

reload(sys)  # Reload does the trick!
#sys.setdefaultencoding('UTF8')

#config = configparser.RawConfigParser()
#config.read('config.properties')
#amazonapikey=config.get('AmazonSection', 'amazonapikeyvalue');
#teamid=config.get('Apple', 'teamid');
#basebundleid=config.get('Apple', 'basebundleid');
#bundleid=config.get('Apple', 'bundleid');
#contentbundleid=config.get('Apple', 'contentbundleid');

base_path = "~/Desktop/WL_Automation/Branch_Script_JSON"

team_id = "X22YF6M8C9"
app_name = "Elite Connect"
bundle_id = "com.elite.EliteConnect"

build_version_number = "23.4.2"
build_number = "1"

#notification_content_version_number = "1"
#notification_service_version_number = "1"

notification_content_bundle_id = "com.elite.NotificationContent"
notification_service_bundle_id = "com.elite.NotificationService"


def copydir(source, dest):
    """Copy a directory structure overwriting existing files"""
    for root, dirs, files in os.walk(source):
        if not os.path.isdir(root):
            os.makedirs(root)
        
        for file in files:
            rel_path = root.replace(source, '').lstrip(os.sep)
            dest_path = os.path.join(dest, rel_path)
            
            if not os.path.isdir(dest_path):
                os.makedirs(dest_path)
            
            shutil.copyfile(os.path.join(root, file), os.path.join(dest_path, file))


# FROM LOCAL PATH
def update_apple_teamID(newValue):
    print("Update Apple TeamID...")
    
    filePath = "EliteConnect.xcodeproj/project.pbxproj"
    
    fin = open(filePath, "rt")
    data = fin.read()
    
    # Replace the content with the .json file
    data = data.replace(team_id, newValue)
    fin.close()
    
    ## Write content to the file
    fin = open(filePath, "wt")
    fin.write(data)
    fin.close()
    
def update_app_name(newValue):
    print("Updating AppName ...")
    filePath = "EliteConnect.xcodeproj/project.pbxproj"
    fin = open(filePath, "rt")
    data = fin.read()
    ## Replace the content with the parameters.json
    data = data.replace(app_name, newValue)
    fin.close()
    ## Write content to the file
    fin = open(filePath, "wt")
    fin.write(data)
    fin.close()

def update_applicationID(newValue):
    print("Update Apple Bundle Identifier ...")
    
    filePath = "EliteConnect.xcodeproj/project.pbxproj"
    
    fin = open(filePath, "rt")
    data = fin.read()
    
    # Replace the content with the .json file
    data = data.replace(bundle_id, newValue)
    fin.close()
    
    ## Write content to the file
    fin = open(filePath, "wt")
    fin.write(data)
    fin.close()

def replace_info_file(source_path):
    print("Replacing Info.plist ....")
    
    # Expand the tilde to the absolute path
    full_soure_path = base_path + source_path
    file_path = os.path.expanduser(full_soure_path)
    
    # Replace local file
    destination_path = "EliteConnect/Info.plist"
    shutil.copy2(file_path, destination_path)

#def UpdateBuild(newValue):
#    print("Updating Build Version ...")
#
#    filePath = "EliteConnect/Info.plist"
#
#    fin = open(filePath, "rt")
#    data = fin.read()
#
#    # Replace the content with the parameters.json
#    data = data.replace("7", newValue)
#    fin.close()
#
#    ## Write content to the file
#    fin = open(filePath, "wt")
#    fin.write(data)
#    fin.close()
    
def update_project_build_number(newValue):
    project_file_path = "EliteConnect.xcodeproj/project.pbxproj"
    with open(project_file_path, 'r') as file:
        project_content = file.read()

    # Define the pattern to find the CURRENT_PROJECT_VERSION
    pattern = re.compile(r'CURRENT_PROJECT_VERSION = (\d+);')

    # Search for the pattern in the project content
    match = pattern.search(project_content)

    if match:
        # Update the version with the new one
        updated_content = pattern.sub(f'CURRENT_PROJECT_VERSION = {newValue};', project_content)

        # Write the updated content back to the file
        with open(project_file_path, 'w') as file:
            file.write(updated_content)
        print(f'Successfully updated build number to {newValue}')
    else:
        print('Failed to find CURRENT_PROJECT_VERSION in the project file')

def update_project_version_number(newValue):
    project_file_path = "EliteConnect.xcodeproj/project.pbxproj"
    with open(project_file_path, 'r') as file:
        project_content = file.read()

    # Define the pattern to find the CURRENT_PROJECT_VERSION
    pattern = re.compile(r'MARKETING_VERSION\s*=\s*([0-9.]+);')

    # Search for the pattern in the project content
    match = pattern.search(project_content)

    if match:
        # Update the version with the new one
        updated_content = pattern.sub(f'MARKETING_VERSION = {newValue};', project_content)

        # Write the updated content back to the file
        with open(project_file_path, 'w') as file:
            file.write(updated_content)
        print(f'Successfully updated version number to {newValue}')
    else:
        print('Failed to find MARKETING_VERSION in the project file')


def replace_resource(source_path):
    print("Replacing Resource Directory ....")
    
    # Destination path for replacing file
    destination_path = "EliteConnect/Resources"
    
    # Expand the tilde to the absolute path
    full_soure_path = base_path + source_path
    file_path = os.path.expanduser(full_soure_path)
    
    # Remove the destination directory and its contents
    shutil.rmtree(destination_path, ignore_errors=True)
    
    # Copy the entire source directory to the destination
    shutil.copytree(file_path, destination_path)

def replace_assets(source_path):
    print("Replacing Assets ....")
    
    # Destination path for replacing file
    destination_path = "EliteConnect/Assets.xcassets"
    
    # Expand the tilde to the absolute path
    full_soure_path = base_path + source_path
    file_path = os.path.expanduser(full_soure_path)
    
    # Remove the destination directory and its contents
    shutil.rmtree(destination_path, ignore_errors=True)
    
    # Copy the entire source directory to the destination
    shutil.copytree(file_path, destination_path)
    
def replace_assets_primary_color(source_path):
    print("Update Assetes Primary Color ...")
        
    # Expand the tilde to the absolute path
    file_path = os.path.expanduser(source_path)
    
    # Replace local file
    destination_path = "EliteConnect/Assets.xcassets/22.3.0/AppColor/Primary.colorset/Contents.json"
    shutil.copy2(file_path, destination_path)
    
    

# ExportOption.plist for export build
def update_export_option_plist(newValue):
    print("Updating Export Option Plist Distribution file ...")
    
    filePath = "ExportOptions.plist"
    
    fin = open(filePath, "rt")
    data = fin.read()
    
    # Replace the content with the parameters.json
    data = data.replace(team_id, newValue)
    fin.close()
    
    ## Write content to the file
    fin = open(filePath, "wt")
    fin.write(data)
    fin.close()

def update_export_option_adHoc_plist(newValue):
    print("Updating Export Option2 Plist Ad-Hoc file ...")
    
    filePath = "ExportOptions2.plist"
    
    fin = open(filePath, "rt")
    data = fin.read()
    
    # Replace the content with the parameters.json
    data = data.replace(team_id, newValue)
    fin.close()
    
    ## Write content to the file
    fin = open(filePath, "wt")
    fin.write(data)
    fin.close()


def update_notification_serviceID(newValue):
    print("Updating Notification Service ID ...")
    
    filePath = "EliteConnect.xcodeproj/project.pbxproj"
    
    fin = open(filePath, "rt")
    data = fin.read()
    
    # Replace the content with the .json file
    data = data.replace(notification_service_bundle_id, newValue)
    fin.close()
    
    ## Write content to the file
    fin = open(filePath, "wt")
    fin.write(data)
    fin.close()

def update_notification_contentID(newValue):
    print("Updating Notification Content ID ...")
    
    filePath = "EliteConnect.xcodeproj/project.pbxproj"
    
    fin = open(filePath, "rt")
    data = fin.read()
    
    # Replace the content with the .json file
    data = data.replace(notification_content_bundle_id, newValue)
    fin.close()
    
    ## Write content to the file
    fin = open(filePath, "wt")
    fin.write(data)
    fin.close()
    
# Notification Extension Build Number Changes
def update_notification_content_build_number(newValue):
    print("Updating Build Version ...")
    
#    filePath = "NotificationContent/Info.plist"
    filePath = "EliteConnect.xcodeproj/project.pbxproj"
    
    fin = open(filePath, "rt")
    data = fin.read()
    
    # Replace the content with the parameters.json
    data = data.replace(build_number, newValue)
    fin.close()
    
    ## Write content to the file
    fin = open(filePath, "wt")
    fin.write(data)
    fin.close()

def update_notification_service_build_number(newValue):
    print("Updating Build Version ...")
    
#    filePath = "NotificationService/Info.plist"
    filePath = "EliteConnect.xcodeproj/project.pbxproj"
    
    fin = open(filePath, "rt")
    data = fin.read()
    
    # Replace the content with the parameters.json
    data = data.replace(build_number, newValue)
    fin.close()
    
    ## Write content to the file
    fin = open(filePath, "wt")
    fin.write(data)
    fin.close()
    
#    Notification Extension Version Number Changes
#def update_notification_service_version_number(newValue):
#    print("Updating Notification Service Version Number ...")
#
##    filePath = "NotificationService/Info.plist"
#    filePath = "EliteConnect.xcodeproj/project.pbxproj"
#
#    fin = open(filePath, "rt")
#    data = fin.read()
#
#    # Replace the content with the parameters.json
#    data = data.replace(notification_service_version_number, newValue)
#    fin.close()
#
#    ## Write content to the file
#    fin = open(filePath, "wt")
#    fin.write(data)
#    fin.close()
#
#def update_notification_content_version_number(newValue):
#    print("Updating Notification Content Version Number ...")
#
##    filePath = "NotificationContent/Info.plist"
#    filePath = "EliteConnect.xcodeproj/project.pbxproj"
#
#    fin = open(filePath, "rt")
#    data = fin.read()
#
#    # Replace the content with the parameters.json
#    data = data.replace(notification_content_version_number, newValue)
#    fin.close()
#
#    ## Write content to the file
#    fin = open(filePath, "wt")
#    fin.write(data)
#    fin.close()
    

if __name__ == '__main__':
    
    parameterFile = sys.argv[1]
    try:
        fin = open(parameterFile, "r")
        dataValues = json.load(fin)
        for key, val in dataValues.items():
#            if key == "AppName":
#                update_app_name(val)
            if key == "applicationId":
                update_applicationID(val)
            if key == "AppleTeamID":
                update_apple_teamID(val)
                update_export_option_plist(val)
                update_export_option_adHoc_plist(val)
            if key == "Info":
                replace_info_file(val)
            if key == "Resources":
                replace_resource(val)
            if key == "AssetsFile":
                replace_assets(val)
            if key == "PrimaryColor":
                replace_assets_primary_color(val)
            if key == "Version":
                update_project_version_number(val)
            if key == "Build":
                update_project_build_number(val)
#                UpdateBuild(val)
#                update_notification_content_build_number(val)
#                update_notification_service_build_number(val)
            if key == "NotificationServiceID":
                update_notification_serviceID(val)
            if key == "NotificaitonContentID":
                update_notification_contentID(val)
#            if key == "ServiceIDBuildVersion":
#                update_notification_service_version_number(val)
#            if key == "ContentIDBuildVersion":
#                update_notification_content_version_number(val)
    
    
    finally:
        fin.close()
