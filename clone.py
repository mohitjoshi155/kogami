import os
import sys
if not os.path.isdir('accounts'):
  print("Account folder containing SA's JSON not fount")
  sys.exit()
print("Hi👋\nThis script is to make your gclone/fclone experience much smoother. No more long commands, no need to remember all commands, flags and all. Just provide folder IDs and script will do the rest 😎)")
print("\n\nBest part is this script can be used in any system which can run a py script.\n\nIf using in windows, make sure all below mentioned things are in one folder\n1. accounts folder containing all SA\n2. gclone.exe\n3. fclone.exe\n4. This script\n\nIf running in a system other than windows, make sure gclone and fclone is installed globally + accounts folder and this script both are in one folder.")
OPN = input("\nwhich operation you wanna run now?🤔\n1. Copy\n2. Move\n3. Sync\n4. Dedupe\nChoose either 1/2/3/4:")
text_file = open("clone.conf", "w")
text_file.write("[gs]\ntype = drive\nscope = drive\nservice_account_file = accounts/1.json\nservice_account_file_path = accounts/")
text_file.close()
if OPN == "1":
  OPNC = input("Which way you want to do it?\n\n1. Gclone (Super accurate but slow)\n2. Fclone (Blazing fast but skips files)\n3. Fclone + Gclone (1st run using fclone to save time, then 2nd run using gclone to take care of all the files skipped by fclone)\nChoose either 1/2/3:")
  if OPNC not in ["1","2","3"]:
    print("Wrong Input 🤬. Exiting..... !!!\n")
    sys.exit()
  SID = input("Provide Source ID:")
  DID = input("Provide Destination ID:")
  if OPNC == "1":
    print("Starting copy using gclone...")
    os.system("gclone --config=clone.conf copy gs:{"+SID+"} gs:{"+DID+"} -P -q --stats-one-line --stats=8s --ignore-existing --drive-server-side-across-configs --drive-acknowledge-abuse --drive-keep-revision-forever")
  elif OPNC == "2":
    print("Starting copy using fclone...")
    os.system("fclone --config=clone.conf copy gs:{"+SID+"} gs:{"+DID+"} -P -q --stats-one-line --stats=8s --ignore-existing --drive-server-side-across-configs --drive-acknowledge-abuse --drive-keep-revision-forever --checkers=256 --transfers=256 --drive-pacer-min-sleep=1ms --drive-pacer-burst=5000 --check-first")
  else:
    print("Starting 1st run using fclone..")
    os.system("fclone --config=clone.conf copy gs:{"+SID+"} gs:{"+DID+"} -P -q --stats-one-line --stats=8s --ignore-existing --drive-server-side-across-configs --drive-acknowledge-abuse --drive-keep-revision-forever --checkers=256 --transfers=256 --drive-pacer-min-sleep=1ms --drive-pacer-burst=5000 --check-first")
    print("\n\nStarting 2nd run using gclone..")
    os.system("gclone --config=clone.conf copy gs:{"+SID+"} gs:{"+DID+"} -P -q --stats-one-line --stats=8s --ignore-existing --drive-server-side-across-configs --drive-acknowledge-abuse --drive-keep-revision-forever")
elif OPN == "2":
  SID = input("Provide Source ID:")
  DID = input("Provide Destination ID:")
  print("Starting move using gclone..")
  os.system("gclone --config=clone.conf move gs:{"+SID+"} gs:{"+DID+"} -P -q --stats-one-line --stats=8s")
elif OPN == "3":
  SID = input("Provide Source ID:")
  DID = input("Provide Destination ID:")
  DRY = input("Wanna see what will happen if you will actually run this sync operation??\nFYI - we wont sync anything in this case. Its just to see what will happen if we started syncing, which will help us in decision making\nBECAUSE SYNCING WILL DELETE FILES FROM DESTINATION, So we gotta be careful\n\n1. Yes, I want to be sure\n2. Nah, I know what will happen.Just run it\n(Choose either Y/N): ")
  if DRY == "Y":
    print("Running a DRY RUN......\n")
    os.system("gclone --config=clone.conf sync gs:{"+SID+"} gs:{"+DID+"} -P --stats=10s --dry-run")
    DRYR = input("So......\nSatisfied with DRY RUN results??\n1. Yes, now I am sure.Please start the sync\n2. Noo, I don't wanna run this sync\n(Choose either Y/N):")
    if DRYR == "Y":
      os.system("gclone --config=clone.conf sync gs:{"+SID+"} gs:{"+DID+"} -P --stats=10s")
    elif DRYR == "N":
      print("Okay..Exiting...")
      sys.exit()
    else:
      print("Wrong Input 🤬. Exiting..... !!!\n")
      sys.exit()  
  elif DRY == "N":
    os.system("gclone --config=clone.conf sync gs:{"+SID+"} gs:{"+DID+"} -P --stats=10s")
  else:
    print("Wrong Input 🤬. Exiting..... !!!\n")
    sys.exit() 
elif OPN == "4":
  DDS = input("Which way you wanna delete duplicates??\n1. Interactive mode - each time rclone will ask you what you wanna do?\n2. Removes identical files then skips anything left\n3. removes identical files then keeps the first one\n4. removes identical files then keeps the newest one\n5. removes identical files then keeps the oldest one\n6. removes identical files then keeps the largest one\n7. removes identical files then renames the rest to be different\n(Choose either 1/2/3/4/5/6/7): ")
  SID = input("Provide Source ID:")
  S = "gs:{"+SID+"}"
  if DDS == "1":
    print("Starting to delete duplicates...")
    os.system("gclone --config=clone.conf dedupe \"{0}\" -P --dedupe-mode interactive".format(S))
  elif DDS == "2":
    print("Starting to delete duplicates...")
    os.system("gclone --config=clone.conf dedupe \"{0}\" -P --dedupe-mode skip".format(S))
  elif DDS == "3":
    print("Starting to delete duplicates...")
    os.system("gclone --config=clone.conf dedupe \"{0}\" -P --dedupe-mode first".format(S))
  elif DDS == "4":
    print("Starting to delete duplicates...")
    os.system("gclone --config=clone.conf dedupe \"{0}\" -P --dedupe-mode newest".format(S))
  elif DDS == "5":
    print("Starting to delete duplicates...")
    os.system("gclone --config=clone.conf dedupe \"{0}\" -P --dedupe-mode oldest".format(S))
  elif DDS == "6":
    print("Starting to delete duplicates...")
    os.system("gclone --config=clone.conf dedupe \"{0}\" -P --dedupe-mode largest".format(S))
  elif DDS == "7":
    print("Starting to delete duplicates...")
    os.system("gclone --config=clone.conf dedupe \"{0}\" -P --dedupe-mode rename".format(S))
  else:
    print("Wrong Input 🤬. Exiting..... !!!\n")
    sys.exit()  
else:
      print("Wrong Input 🤬. Exiting..... !!!\n")
      sys.exit()      
print("\n\nThx for using my script.\nWritten by https://warezforums.com/@Smoke ✌️\nFor all the cloning tools users out there ❤️")      
    