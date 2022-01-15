import os
import sys
print("Hi👋\nwhenever we wanna unzip cloud stored stuff using vps, we will perform these steps\n\n1. Rclone copy from cloud to vps storage\n2. Wait till it gets completed\n3. Start unzipping files\n4. Wait till unzipping gets completed\n5. Delete original zipped files from vps storage\n6. Upload the unzipped files to cloud storage using rclone\n7. Wait till it upload gets completed\n8. Delete unzipped file from vps storage\n\nSo many individual steps/works and shit tons of waiting time. No?")
print("\nThis script will do all these steps automatically one by one. No more time wasting. Just provide asked input and sit back/relax/forget about it. Script will do the whole job\n\nFeatures of the script\n1. No need to know linux commands\n2. No more syntax/format/command errors\n3. Ability to extract password protected compressed files\n4. Options to select from zip/7z/rar/tar")

# asking questions

print("\n\nIs it a Direct download link? like public index or FTP or workers.dev index link??\nor\nIs it stored in some cloud storage which rclone supports?\n")
ASK_FIRST = input("1. Yes, It's a DDL link\n2. Noo, Its not a DDL link. It's in a cloud storage which is supported by rclone\nChoose either 1/2:")
if ASK_FIRST not in ["1", "2"]:
  print("Wrong input 🤬. Exiting!!!")
  sys.exit()

if os.path.isfile("/bot/.config/rclone/rclone.conf"):
  print("Found rclone.conf at default location i.e., /bot/.config/rclone/rclone.conf")
  RCLONE_PATH = "/bot/.config/rclone/rclone.conf"
else:
  print("rclone.conf not found at default location 😬i.e., /bot/.config/rclone/rclone.conf\nExiting!!!")
  RCLONE_PATH = input("Provide full path to rclone.conf")
    
if not os.path.isfile(RCLONE_PATH):
  print("rclone.conf can not be found at the provided path 😬😔.\nPlease try again. Exiting !!!")
  sys.exit()

ASK_SECOND = input("\n\nIs it a password protected compressed file? 🤔\nChoose Y/N:")
if ASK_SECOND not in ["Y", "N"]:
  print("Wrong input 🤬. Exiting!!!")
  sys.exit()
if ASK_SECOND == "Y":
  PASSWORD = input("Provide password for the file:")

ASK_THIRD = input("What type of compressed file it is? 🤔\n1. a .zip file\n2. a .7z file\n3. a .rar file\n4. a .tar file\nChoose either 1/2/3/4:")
if ASK_FIRST not in ["1", "2", "3", "4"]:
  print("Wrong input 🤬. Exiting!!!")
  sys.exit()
  
#Taking inputs from users

if ASK_FIRST == "1":
  LINK = input("Provide your DDL:\n\n(with http(S) password if any) (google it to know the format of sending a http(S) password protected link)")
else:
  SOURCE_REMOTE = input("Provide Source remote:")
  SOURCE_ID = input("Provide source path:\n\n(Provide path to a single compressed file, not path to a folder)")
  S = SOURCE_REMOTE+":"+SOURCE_ID
  
  
DESTINATION_REMOTE = input("Provide Destination remote:")
DESTINATION_ID = input("Provide Destination path:")
D = DESTINATION_REMOTE+":"+DESTINATION_ID

#Actual processing
print("Creating required directories....")
os.system("mkdir /bot/compressed && mkdir /bot/unzip")
print("\n\nDownloading to local storage...")
if ASK_FIRST == "1":
  os.system("wget \"{0}\" --quiet --show-progress -P /bot/compressed".format(LINK))
else:
  os.system("rclone --config="+RCLONE_PATH+" copy \"{0}\" /bot/compressed -P -q --stats=10s".format(S))
FILE_NAME = os.listdir("/bot/compressed")[0]
print("\n\nExtracting....")
if ASK_SECOND =="Y":
  if ASK_THIRD in ["1", "2"]:
    os.system("7z x -P\"{0}\" /bot/compressed/\"{1}\" -o/bot/unzip".format(PASSWORD,FILE_NAME))
  elif ASK_THIRD == "3":
    os.system("unrar x -P\"{0}\" /bot/compressed/\"{1}\" /bot/unzip -idq".format(PASSWORD,FILE_NAME))
  else:
    print("This script does not support extracting password protected tar files. Sorry")
else:  
  if ASK_THIRD in ["1", "2"]:
    os.system("7z x /bot/compressed/\"{0}\" -o/bot/unzip".format(FILE_NAME))
  elif ASK_THIRD == "3":
    os.system("unrar x /bot/compressed/\"{0}\" /bot/unzip -idq".format(FILE_NAME))
  else:
    os.system("tar -C /bot/unzip -xf /bot/compressed/\"{0}\"".format(FILE_NAME))
print("\n\nStarted uploading.......")
os.system("rclone --config="+RCLONE_PATH+" move /bot/unzip \"{0}\" -P -q --stats=10s".format(D))
print("\n\nCleaning local storage....\n")
os.system("rm -r /bot/compressed && rm -r /bot/unzip")

print("Thx for using my script.\nWritten by https://warezforums.com/@Smoke✌️\nFor everyone ❤️")
  