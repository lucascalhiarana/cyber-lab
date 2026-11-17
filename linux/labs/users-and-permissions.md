# Linux Lab: Users, Groups, and Permissions

## Overview

This lab explores Linux user and group management, directory permissions, file ownership, and the SGID (Set Group ID) permission.

The goal is to understand how Linux controls access to shared directories and how group inheritance works when files are created.

- **Environment:** Kali Linux
- **Filesystem:** ext4
- **Focus:** Linux administration and cybersecurity fundamentals

## 1. Create a user and group

A dedicated group and user were created for the lab.

    sudo groupadd security-lab
    sudo useradd -m analyst
    sudo passwd analyst
    sudo usermod -aG security-lab analyst

The configuration was checked with:

    id analyst
    getent group security-lab

The output confirmed that the analyst user belonged to both the analyst and security-lab groups.

## 2. Create a shared directory

A directory was created to simulate a shared workspace.

    mkdir -p ~/linux-labs/users-permissions
    cd ~/linux-labs/users-permissions
    mkdir team-share
    sudo chgrp security-lab team-share
    chmod 2770 team-share

The permissions were checked with:

    ls -ld team-share

Example output:

    drwxrws--- 2 kali security-lab ... team-share

The permission value 2770 means:

- **2:** SGID is enabled.
- **7:** the owner has read, write, and execute permissions.
- **7:** the group has read, write, and execute permissions.
- **0:** other users have no permissions.

On a directory, SGID makes new files and subdirectories inherit the directory's group.

## 3. Verify SGID and group inheritance

SGID was explicitly enabled:

    sudo chmod g+s team-share

The directory permissions were inspected with:

    stat -c '%A %a %U:%G %n' team-share

The analyst user then created a file in the shared directory:

    sudo -u analyst sh -c 'id; touch team-share/teste-final.txt'
    ls -l team-share

The new file inherited the security-lab group. Older files kept their original group ownership; enabling SGID does not change files that already exist.

## 4. Troubleshooting

During the exercise, the first test file did not show the expected group inheritance. The following commands were used to investigate:

    getfacl team-share
    findmnt -T team-share -o TARGET,FSTYPE,OPTIONS

The results showed no additional ACL entries, an ext4 filesystem, and SGID enabled on the directory. SGID was enabled again with chmod, then a new file was created and checked.

This reinforced the importance of verifying permissions and ownership instead of assuming a configuration is working as intended.

## Commands practiced

| Command | Purpose |
| --- | --- |
| groupadd | Creates a group |
| useradd | Creates a user |
| passwd | Sets or changes a password |
| usermod -aG | Adds a user to supplementary groups |
| id | Displays user and group information |
| getent group | Retrieves group information |
| chgrp | Changes a file or directory group |
| chmod | Changes permissions |
| stat | Displays detailed file information |
| ls -l | Displays file permissions and ownership |
| getfacl | Displays access control lists |
| findmnt | Displays filesystem mount information |
| sudo -u | Runs a command as another user |

## Key takeaways

Through this lab, I practiced creating Linux users and groups, interpreting permission strings, configuring a shared directory, enabling SGID, and investigating unexpected ownership behavior.

These fundamentals are relevant to system administration and defensive security because they help explain how users access system resources and how permission issues can be investigated.

**Lab status:** Completed  
**Next study topic:** SUID, SGID, and the sticky bit
