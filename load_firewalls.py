import os
import re

def success(output):
  return not len(re.findall(r"command not found", output))>0

def install():
  # Install ufw
  print("Initializing ufw")
  for i in "12345":
    ufw_installed = os.popen("sudo ufw status").read()
    if success(ufw_installed):
      return True
    display_header()
    input("ufw not found, retrying")
    install_ufw = os.popen("sudo apt-get ufw").read()
    if not success(install_ufw):
      install_ufw = os.popen("sudo yum ufw").read()
    if not success(install_ufw):
      install_ufw = os.popen("sudo apt update; sudo apt install ufw").read()
    print(install_ufw)
    input(f"Failed, installing attempt {i}/5")
  return False

def enable_defaults():
  # Enable ufw
  return success(os.popen("sudo ufw enable").read()) and \
  success(os.popen("sudo ufw default deny incoming").read()) and \
  success(os.popen("sudo ufw default allow outgoing").read())

def title(text):
  print("="*(32+len(text)))
  print("="*15,"\033[32m"+text+"\033[0m","="*15)
  print("="*(32+len(text)))

def display_header():
  os.system("clear")
  title("Linux Firewall Setup")

def display_menu():
  display_header()
  print("""
  0. Exit
  1. Initialize ufw
""")

def main():
  while 1:
    display_menu()
    try:
      choice = int(input("Select an option: "))
    except ValueError:
      continue
    if choice == 0:
      break
    elif choice == 1:
      code = True
      if code:
        code = install()
        if code:
          code = enable_defaults()
  print("Successfully Exited")
  
  

if __name__ == "__main__":
  main()