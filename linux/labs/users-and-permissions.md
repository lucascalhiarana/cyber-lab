\# Linux Lab: Users, Groups and Permissions



\## 1. Overview



This lab explores Linux user and group management, directory permissions, file ownership, and the SGID (Set Group ID) permission.



The goal is to understand how Linux controls access to shared directories and how group inheritance works when files are created.



\*\*Environment:\*\* Kali Linux  

\*\*Filesystem:\*\* ext4  

\*\*Focus:\*\* Linux administration and cybersecurity fundamentals



\## 2. Creating a User and Group



First, a dedicated group and user were created for the lab.



```bash

sudo groupadd security-lab

sudo useradd -m analyst

sudo passwd analyst

sudo usermod -aG security-lab analyst

```



To verify the configuration:



```bash

id analyst

getent group security-lab

```



The output confirmed that the `analyst` user belonged to both the `analyst` and `security-lab` groups.



\## 3. Creating a Shared Directory



A directory was created to simulate a shared workspace.



```bash

mkdir -p \~/linux-labs/users-permissions

cd \~/linux-labs/users-permissions



mkdir team-share

sudo chgrp security-lab team-share

chmod 2770 team-share

```



The permissions were checked with:



```bash

ls -ld team-share

```



Example output:



```text

drwxrws--- 2 kali security-lab ... team-share

```



\### Understanding the permissions



\- `d`: identifies a directory.

\- `rwx`: the owner can read, write, and access the directory.

\- `rws`: the group has read, write, and access permissions, with SGID enabled.

\- `---`: other users have no permissions.



The `2770` permission value means:



\- `2`: enables SGID.

\- `7`: gives the owner read, write, and execute permissions.

\- `7`: gives the group read, write, and execute permissions.

\- `0`: gives other users no permissions.



\## 4. Understanding SGID



SGID (Set Group ID) on a directory makes newly created files and subdirectories inherit the directory's group.



This is useful when multiple users need to collaborate inside a shared directory.



The following command explicitly enables SGID:



```bash

sudo chmod g+s team-share

```



To inspect the directory permissions:



```bash

stat -c '%A %a %U:%G %n' team-share

```



\## 5. Testing Group Inheritance



The `analyst` user was used to create a file inside the shared directory.



```bash

sudo -u analyst sh -c 'id; touch team-share/teste-final.txt'

```



Then, file ownership and group membership were checked:



```bash

ls -l team-share

```



The relevant result was:



```text

\-rw-r--r-- 1 analyst analyst       ... notes.txt

\-rw-r--r-- 1 analyst security-lab  ... teste-final.txt

\-rw-r--r-- 1 analyst analyst       ... testes-sgid.txt

```



The file `teste-final.txt` inherited the `security-lab` group, confirming that SGID was working.



The older files retained their original group ownership. Enabling SGID does not automatically change the group of files that already exist.



\## 6. Troubleshooting and Verification



During the exercise, the first newly created test file did not show the expected group inheritance.



The following commands were used to investigate:



```bash

getfacl team-share

findmnt -T team-share -o TARGET,FSTYPE,OPTIONS

```



The results showed:



\- No additional ACL entries on the directory.

\- The filesystem was `ext4`.

\- SGID was visible in the directory permissions.



SGID was explicitly enabled again:



```bash

sudo chmod g+s team-share

```



A new file was created afterward, and its group was correctly inherited.



This investigation reinforced the importance of verifying permissions and file ownership instead of assuming that a configuration is working as intended.



\## 7. Commands Learned



| Command | Purpose |

|---|---|

| `groupadd` | Creates a group |

| `useradd` | Creates a user |

| `passwd` | Sets or changes a user's password |

| `usermod -aG` | Adds a user to supplementary groups |

| `id` | Displays user and group information |

| `getent group` | Retrieves group information |

| `chgrp` | Changes a file or directory group |

| `chmod` | Changes permissions |

| `stat` | Displays detailed file information |

| `ls -l` | Displays file permissions and ownership |

| `getfacl` | Displays access control lists |

| `findmnt` | Displays filesystem mount information |

| `sudo -u` | Executes a command as another user |



\## 8. Key Takeaways



Through this lab, I practiced:



\- Creating and managing Linux users and groups.

\- Understanding Linux file ownership.

\- Reading and interpreting permission strings.

\- Configuring shared directories.

\- Enabling and verifying SGID.

\- Understanding group inheritance for newly created files.

\- Investigating unexpected permission behavior using Linux tools.



\## 9. Relevance to Cybersecurity



Linux user and permission management is an important foundation for system administration and Blue Team operations.



Understanding ownership, group membership, and access permissions helps security analysts investigate access issues, identify misconfigurations, and understand how users interact with system resources.



\*\*Lab status:\*\* Completed  

\*\*Next step:\*\* Explore file permissions in more depth, including SUID, SGID, and the sticky bit.

