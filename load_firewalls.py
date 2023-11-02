import os
import re

def success(output):
  return len(re.findall(r"command not found", output))>0

def main():
  while 1:
    ufw_installed = os.popen("ufw -v").read()
    if success(ufw_installed):
      break
    install_ufw = os.popen("sudo apt-get ufw").read()
    if not success(install_ufw):
      install_ufw = os.popen("sudo yum ufw").read()
    print(install_ufw)
    input("")

if __name__ == "__main__":
  main()