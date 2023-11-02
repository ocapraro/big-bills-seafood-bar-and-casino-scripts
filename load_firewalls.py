import os
import re

def success(output):
  return len(re.findall(r"command not found", output))>0

def install():
  # Install ufw
  for i in "12345":
    ufw_installed = os.popen("sudo ufw status").read()
    if success(ufw_installed):
      return True
    os.system("clear")
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


def main():
  code = True
  if code:
    code = install()
    if code:
      code = enable_defaults()
  
  

if __name__ == "__main__":
  main()