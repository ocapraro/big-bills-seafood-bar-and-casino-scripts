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
      print("ufw Installed")
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
  print("Enabling default firewall settings")
  code =  success(os.popen("sudo ufw enable").read()) and \
  success(os.popen("sudo ufw default deny incoming").read()) and \
  success(os.popen("sudo ufw default allow outgoing").read())
  print("Enabled")
  return code


  
def allow_service(service):
  display_header()
  print(f"Allowing {service}")
  code = success(os.popen(f"sudo ufw allow {service}").read())
  print(f"{service} allowed")
  return code

def allow_ip(ip):
  return allow_service(f"from {ip}")

def check_status():
  status = os.popen("sudo ufw status").read()
  display_header()
  print("Checking status...")
  print(status)
  return success(status)

def deny_service(service):
  display_header()
  print(f"Denying {service}")
  code = success(os.popen(f"sudo ufw delete allow {service}").read())
  print(f"{service} denied")
  return code

def deny_ip(ip):
  return deny_service(f"from {ip}")

def enable_logs():
  display_header()
  print("Enabling logs")
  code = success(os.popen("sudo ufw logging on").read())
  display_header()
  print("Enabled! The logs can be found in /var/log/ufw.log")
  return code

def disable_logs():
  display_header()
  print("Disable logs")
  code = success(os.popen("sudo ufw logging off").read())
  display_header()
  print("Disabled")
  return code

def reload():
  display_header()
  print("Reloading...")
  code = success(os.popen("sudo ufw reload").read())
  display_header("Success!")
  return code

def title(text):
  print("="*(32+len(text)))
  print("="*15,"\033[32m"+text+"\033[0m","="*15)
  print("="*(32+len(text)))

def display_header():
  os.system("clear")
  title("Linux Firewall Setup")
  print("")

def display_menu():
  display_header()
  print("""  0. Exit
  1. Initialize ufw
  2. Allow IP
  3. Allow ssh
  4. Allow http
  5. Check status
  6. Deny IP
  7. Deny Service
  8. Enable logs
  9. Disable logs
 10. Reload
""")

def main():
  code = True
  while code:
    display_menu()
    try:
      choice = int(input("Select an option: "))
    except ValueError:
      continue
    if choice == 0:
      break
    elif choice == 1:
      display_header()
      code = install()
      if code:
        code = enable_defaults()
    elif choice == 2:
      code = allow_ip(input("Enter the IP: "))
    elif choice == 3:
      code = allow_service("ssh")
    elif choice == 4:
      code = allow_service("http")
    elif choice == 5:
      code = check_status()
    elif choice == 6:
      code = deny_ip(input("Enter the IP: "))
    elif choice == 7:
      code = deny_service(input("Enter the Service: "))
    elif choice == 8:
      code = enable_logs()
    elif choice == 9:
      code = disable_logs()
    elif choice == 10:
      code = reload()
    input("")
  print("Successfully Exited")
  
  

if __name__ == "__main__":
  main()