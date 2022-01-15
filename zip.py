import os
import sys
print("Hi,\nwhenever we wanna zip cloud stored stuff using vps, we will perform these steps\n\n1. Rclone copy from cloud to vps storage\n2. Wait till it gets completed\n3. Start zipping files\n4. Wait till zipping gets completed\n5. Delete original unzipped files from vps storage\n6. Upload the zip to cloud storage using rclone\n7. Wait till it upload gets completed\n8. Delete zip file from vps storage\n\nSo many individual steps/works and shit tons of waiting time. No?")
print("\nThis script will do all these steps automatically one by one. No more time wasting. Just provide asked input and sit back/relax/forget about it. Script will do the whole job\n\nFeatures of the script\n1. No need to know linux commands\n2. No more syntax/format/command errors\n3. Ability to add password to output compressed file\n4. Options to select from zip/7z/rar\n5. Both gclone and rclone is supported")

# asking questions

ASK_FIRST = input("\nBoth of your source and destination is GD/TD??\n1. Yes, both are GD/TD\n2. Noo. Its some other cloud storage\nChoose either 1/2:")
if ASK_FIRST not in ["1", "2"]:
  print("Wrong input 🤬. Exiting!!!")
  sys.exit()
if ASK_FIRST == "1":
  CLONE_METHOD = "gclone"
  SAS = input("Do you have service accounts and want to use in gclone? 🤔\n1. Yes\n2. No\nChoose either Y/N:")
  if SAS not in ["Y", "N"]:
    print("wrong input 🤬. Exiting!!!")
    sys.exit()
  if SAS == "Y":
    text_file = open("clone.conf", "w")
    text_file.write("[gs]\ntype = drive\nscope = drive\nservice_account_file = accounts/1.json\nservice_account_file_path = accounts/")
    text_file.close()
    RCLONE_PATH = ("/bot/clone.conf")
  else:
    RCLONE_PATH = "/bot/.config/rclone/rclone.conf"
else:
  CLONE_METHOD = "rclone"
  RCLONE_PATH = "/bot/.config/rclone/rclone.conf"
if RCLONE_PATH == "/bot/.config/rclone/rclone.conf":
  if not os.path.isfile("/bot/.config/rclone/rclone.conf"):
    print("rclone.conf not found at /bot/.config/rclone/rclone.conf.\nYou can't use rclone/gclone without rclone.conf\nExiting!!!")
    sys.exit()

ASK_SECOND = input("Wanna protect your output compressed file with password? 👀\n1. Yes\n2. No\nChoose either Y/N:")
if ASK_SECOND not in ["Y", "N"]:
  print("Wrong input 🤬. Exiting!!!")
  sys.exit()
if ASK_SECOND == "Y":
  PASSWORD = input("Provide your password\n\nIt should be a single word, No space allowed")
else:
  print("Noice, Let's go to next step\n\n")

ASK_THIRD = input ("What kind of output compressed file you want? 🤔\n1. zip\n2. 7z\n3. rar\nChoose either 1/2/3:")
if ASK_THIRD not in ["1", "2", "3"]:
  print("Wrong input 🤬. Exiting!!!")
  sys.exit()

  
#Taking inputs from users
DESIRED_FOLDER_NAME = input("Provide Folder name:\n\nWhat's this?\nIt is the folder name, which user will get after extraction.So...please select an appropriate name")
DESIRED_FILE_NAME = input("Provide desired name for the resultant compressed file (with file extension name):\n\nProvide appropriate file extention name according to options selected above, otherwise you will face errors")
N = "/bot/files/"+DESIRED_FOLDER_NAME

if CLONE_METHOD == "gclone":
  if SAS == "Y":
    SOURCE_ID = input("Provide source ID:")
    DESTINATION_ID = input("Provide Destination ID:")
    S = "gs:{"+SOURCE_ID+"}"
    D = "gs:{"+DESTINATION_ID+"}"
  elif SAS == "N":
    SOURCE_REMOTE = input("Provide Source remote:")
    SOURCE_ID = input("Provide source ID:")
    DESTINATION_REMOTE = input("Provide Destination remote:")
    DESTINATION_ID = input("Provide Destination ID:")
    S = SOURCE_REMOTE+":{"+SOURCE_ID+"}"
    D = DESTINATION_REMOTE+":{"+DESTINATION_ID+"}"
  else:
   SOURCE_REMOTE = input("Provide Source remote:")
   SOURCE_PATH = input("Provide source path:")
   DESTINATION_REMOTE = input("Provide Destination remote:")
   DESTINATION_PATH = input("Provide Destination path:")
   S = SOURCE_REMOTE+":"+SOURCE_PATH
   D = DESTINATION_REMOTE+":"+DESTINATION_PATH
  
#Actual Process
print("Creating required directories....")
os.system("mkdir /bot/files && mkdir /bot/zip && mkdir /bot/files/+\"{0}\"".format(DESIRED_FOLDER_NAME))
print("\n\nDownloading to local storage.......")
os.system(CLONE_METHOD+" --config="+RCLONE_PATH+" copy \"{0}\" \"{1}\" -P -q --stats=10s".format(S,N))
print("\n\nStarted the compression.....")
if ASK_SECOND == "Y":
  if ASK_THIRD in ["1","2"]:
   os.system("cd /bot/files && 7z a -mx=1 -p\"{0}\" /bot/zip/\"{1}\" ./\"{2}\" ".format(PASSWORD,DESIRED_FILE_NAME,DESIRED_FOLDER_NAME))
  else:
    os.system("cd /bot/files && rar a -m0 -p\"{0}\" /bot/zip/\"{1}\" ./\"{2}\" ".format(PASSWORD,DESIRED_FILE_NAME,DESIRED_FOLDER_NAME))
else:
  if ASK_THIRD in ["1","2"]:
    os.system("cd /bot/files && 7z a -mx=1 /bot/zip/\"{0}\" ./\"{1}\" ".format(DESIRED_FILE_NAME,DESIRED_FOLDER_NAME))
  else:
    os.system("cd /bot/files && rar a -m0 /bot/zip/\"{0}\" ./\"{1}\" ".format(DESIRED_FILE_NAME,DESIRED_FOLDER_NAME))
print("\n\nStarted uploading......")
os.system(CLONE_METHOD+" --config="+RCLONE_PATH+" move /bot/zip \"{0}\" -P -q --stats=10s".format(D))
print("\n\nCleaning local storage....")
os.system("rm -r /bot/files && rm -r /bot/zip")

print("Thx for using my script.\nWritten by https://warezforums.com/@Smoke ✌️\nFor everyone ❤️")