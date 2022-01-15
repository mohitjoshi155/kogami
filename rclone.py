import os
import sys
print("Hi!\nThis script is made to make your rclone experience much smoother.\nNo need to remember commands, flags, formats and all.\nJust provide remotes and paths by selecing appropriate options and script will do the rest\n\nAnd best part is, you can use this script in any system which can run a py script.\nJust make sure, your system can detect rclone")
print("\n\nLooking for conf....")
if os.path.isfile('/bot/.config/rclone/rclone.conf'):
  print("\n\nrclone.conf found at /bot/.config/rclone/rclone.conf 🥳")
  PATH = ("/bot/.config/rclone/rclone.conf")
else:
  print("rclone.conf not found at /bot/.config/rclone/rclone.conf")
  PATH = input("Provide your full custom path to rclone.conf")
if not os.path.isfile(PATH):
  print("Unable to locate conf at provided path. Exiting...")
  sys.exit()
OPN = input("\n\nWhich operation you want to run? 🤔\n1. List all remotes\n2. Calculate Size\n3. Copy files and folders\n4. Move files and folders\n5. Sync\n6. List Directory(s) of the remote and path\n7. Delete Duplicates\n8. Generate public link of files and folders\n9. Empty the Trash in one go\n10.Check rclone version\n(Choose either 1/2/3/4/5/6/7/8/9/10):")
if OPN in ["3", "4", "5"]:
  SCR = input("Provide Source remote")
  SCP = input("Provide Source path")
  DSR = input("Provide Destination remote")
  DSP = input("Provide Destination path")
  S = SCR+":"+SCP
  D = DSR+":"+DSP
  if OPN == "3":
    print("Strating the copy process.....\n")
    os.system("rclone --config="+PATH+" copy \"{0}\" \"{1}\" -P -q --stats=10s --ignore-existing --drive-server-side-across-configs --drive-acknowledge-abuse --drive-keep-revision-forever".format(S,D))
  elif OPN == "4":
    print("Strating the copy process.....\n")
    os.system("rclonee --config="+PATH+" move \"{0}\" \"{1}\" -P -q --stats=10s --ignore-existing --drive-server-side-across-configs --drive-acknowledge-abuse --drive-keep-revision-forever".format(S,D))
  else:
    DRY = input("Wanna see what will happen if you will actually run this sync operation??\nFYI - we wont sync anything in this case. Its just to see what will happen if we started syncing, which will help us in decision making\nBECAUSE SYNCING WILL DELETE FILES FROM DESTIANTION, So we gotta be careful\n\n1. Yes, I want to be sure\n2. Nah, I know what will happen.Just run it\n(Choose either Y/N): ")
    if DRY == "Y":
      print("Running a DRY RUN......\n")
      os.system("rclone --config="+PATH+" sync \"{0}\" \"{1}\" -P --stats=10s --dry-run".format(S,D))
      DRYR = input("So......\nSatisfied with DRY RUN results??\n1. Yes, now I am sure.Please start the sync\n2. Noo, I don't wanna run this sync\n(Choose either Y/N):")
      if DRYR == "Y":
        os.system("rclone --config="+PATH+" sync \"{0}\" \"{1}\" -P --stats=10s".format(S,D))
      elif DRYR == "N":
        print("Okay..Exiting...")
      else:
        print("Wrong Input 🤬. Exiting..... !!!\n")
        sys.exit()
if OPN in ["2", "6", "7", "8"]:
  SCR = input("Provide Source remote")
  SCP = input("Provide Source path")
  S = SCR+":"+SCP
  if OPN == "2":
    print("Calculating size. Please wait...\n\nFYI - Intentionally not using --disable ListR\n")
    os.system("rclone --config="+PATH+" size \"{0}\" ".format(S))
  elif OPN == "6":
    os.system("rclone --config="+PATH+" lsd \"{0}\" ".format(S))
  elif OPN == "7":
    DDS = input("Which way you wanna delete duplicates??\n1. Interactive mode - each time rclone will ask you what you wanna do?\n2. Removes identical files then skips anything left\n3. removes identical files then keeps the first one\n4. removes identical files then keeps the newest one\n5. removes identical files then keeps the oldest one\6. removes identical files then keeps the largest one\n7. removes identical files then renames the rest to be different\n(Choose either 1/2/3/4/5/6/7): ")
    if DDS == "1":
      print("Starting to delete duplicates...")
      os.system("rclone --config="+PATH+" dedupe \"{0}\" -P --dedupe-mode interactive".format(S))
    elif DDS == "2":
      print("Starting to delete duplicates...")
      os.system("rclone --config="+PATH+" dedupe \"{0}\" -P --dedupe-mode skip".format(S))
    elif DDS == "3":
      print("Starting to delete duplicates...")
      os.system("rclone --config="+PATH+" dedupe \"{0}\" -P --dedupe-mode first".format(S))
    elif DDS == "4":
      print("Starting to delete duplicates...")
      os.system("rclone --config="+PATH+" dedupe \"{0}\" -P --dedupe-mode newest".format(S))
    elif DDS == "5":
      print("Starting to delete duplicates...")
      os.system("rclone --config="+PATH+" dedupe \"{0}\" -P --dedupe-mode oldest".format(S))
    elif DDS == "6":
      print("Starting to delete duplicates...")
      os.system("rclone --config="+PATH+" dedupe \"{0}\" -P --dedupe-mode largest".format(S))
    elif DDS == "7":
      print("Starting to delete duplicates...")
      os.system("rclone --config="+PATH+" dedupe \"{0}\" -P --dedupe-mode rename".format(S))
    else:
      print("Wrong Input 🤬. Exiting..... !!!\n")
      sys.exit()
  else:
    print("Generating public link....\nFYI -\nPublic link for TD Folder not possible, only TD File's link generation possible")
    os.system("rclone --config="+PATH+" link \"{0}\" ".format(S))
if OPN == "9":
  SCR = input("Provide Source remote")
  S = SCR+":"
  print("Cleaning... Please wait 😅")
  os.system("rclone --config="+PATH+" cleanup \"{0}\"".format(S))
if OPN in ["1", "10"]:
  if OPN == "1":
    os.system("rclone --config="+PATH+" listremotes")
  else:
    os.system("rclone version")
print("\nThx for using my script.\nWritten by https://warezforums.com/@Smoke ✌️\nFor all the rclone users out there ❤️")