# Linux Command Cheatsheet

A practical reference of Linux commands, syntax, and examples.

This document is part of my Linux studies and cybersecurity learning journey.

---

## 1. Navigation and Directories

### `pwd`
Displays the current working directory.

```bash
pwd
```

### `ls`
Lists files and directories.

```bash
ls
ls -l       # Detailed listing
ls -a       # Includes hidden files
ls -la      # Detailed listing including hidden files
```

### `cd`
Changes the current directory.

```bash
cd /home/user
cd ..       # Move one directory up
cd ~        # Go to the home directory
cd -        # Return to the previous directory
```

---

## 2. File Management

### `cat`
Displays file contents.

```bash
cat file.txt
cat file1.txt file2.txt
```

### `touch`
Creates an empty file or updates its timestamp.

```bash
touch file.txt
```

### `mkdir`
Creates directories.

```bash
mkdir projects
mkdir -p projects/linux/labs
```

### `cp`
Copies files and directories.

```bash
cp file.txt backup.txt
cp -r folder/ backup/
```

### `mv`
Moves or renames files and directories.

```bash
mv file.txt /home/user/
mv old-name.txt new-name.txt
```

### `rm`
Removes files and directories.

```bash
rm file.txt
rm -r folder/
```

**Warning:** Be careful when using `rm`, especially with recursive or forced deletion.

---

## 3. Reading and Searching Files

### `less`
Views file contents page by page.

```bash
less file.txt
```

### `head`
Displays the first lines of a file.

```bash
head file.txt
head -n 20 file.txt
```

### `tail`
Displays the last lines of a file.

```bash
tail file.txt
tail -n 20 file.txt
tail -f /var/log/syslog
```

### `grep`
Searches for patterns inside files.

```bash
grep "error" file.txt
grep -i "error" file.txt
grep -r "password" /var/log/
```

### `find`
Searches for files and directories.

```bash
find . -name "file.txt"
find /home -type f
find . -type d
find . -type f -size 1033c
```

### `file`
Identifies the type of a file.

```bash
file document.txt
file *
```

---

## 4. Text Processing

### `sort`
Sorts lines alphabetically or numerically.

```bash
sort file.txt
sort -n numbers.txt
```

### `uniq`
Filters adjacent repeated lines.

```bash
uniq file.txt
uniq -u file.txt
```

For identifying unique lines across an entire file, sort it first:

```bash
sort file.txt | uniq -u
```

### `wc`
Counts lines, words, and bytes.

```bash
wc file.txt
wc -l file.txt
wc -w file.txt
```

### `strings`
Extracts readable text sequences from binary files.

```bash
strings file.bin
```

---

## 5. Permissions and Ownership

### `chmod`
Changes file permissions.

```bash
chmod 755 script.sh
chmod +x script.sh
```

### `chown`
Changes file ownership.

```bash
sudo chown user:user file.txt
```

### `ls -l`
Displays file permissions and ownership.

```bash
ls -l
```

---

## 6. Users and System Information

### `whoami`
Displays the current username.

```bash
whoami
```

### `id`
Displays user and group identification information.

```bash
id
```

### `hostname`
Displays the system hostname.

```bash
hostname
```

### `uname`
Displays system information.

```bash
uname -a
```

### `sudo`
Executes commands with elevated privileges.

```bash
sudo command
```

---

## 7. Networking and Remote Access

### `ssh`
Connects to a remote machine.

```bash
ssh username@server
ssh username@server -p 2222
```

### `ip`
Displays and manages network interfaces and addresses.

```bash
ip addr
ip route
ip link
```

### `ping`
Tests network connectivity.

```bash
ping 8.8.8.8
```

### `ss`
Displays network sockets and connections.

```bash
ss -tuln
ss -tunap
```

### `curl`
Transfers data using URLs and supports HTTP requests.

```bash
curl https://example.com
curl -I https://example.com
```

---

## 8. Processes and Services

### `ps`
Displays running processes.

```bash
ps aux
```

### `top`
Provides real-time process and resource monitoring.

```bash
top
```

### `kill`
Sends a signal to a process.

```bash
kill PID
kill -9 PID
```

### `systemctl`
Manages system services.

```bash
systemctl status ssh
sudo systemctl start ssh
sudo systemctl stop ssh
sudo systemctl restart ssh
```

---

## 9. Logs and Monitoring

### `journalctl`
Queries system logs collected by systemd.

```bash
journalctl
journalctl -n 50
journalctl -u ssh
journalctl -f
```

### `dmesg`
Displays kernel-related messages.

```bash
dmesg
dmesg | tail
```

### `tail -f`
Monitors new lines added to a log file.

```bash
tail -f /var/log/auth.log
```

---

## 10. Compression and Encoding

### `tar`
Creates and extracts archive files.

```bash
tar -czvf archive.tar.gz folder/
tar -xzvf archive.tar.gz
```

### `base64`
Encodes or decodes Base64 data.

```bash
base64 file.txt
base64 -d encoded.txt
```

---

## 11. Pipes and Redirection

### Pipe `|`
Sends the output of one command to another command.

```bash
cat file.txt | grep "error"
```

### Output redirection `>`
Writes command output to a file, replacing existing content.

```bash
echo "Hello Linux" > output.txt
```

### Append redirection `>>`
Appends output to a file.

```bash
echo "New line" >> output.txt
```

### Error redirection `2>`
Redirects standard error.

```bash
find / -name "file.txt" 2>/dev/null
```

### Combined redirection

```bash
command > output.txt 2>&1
```

---

## 12. Useful Command Combinations

### Find readable files

```bash
find . -type f -exec file {} +
```

### Search for a specific string

```bash
grep -r "keyword" .
```

### Monitor authentication logs

```bash
sudo tail -f /var/log/auth.log
```

### Find listening network ports

```bash
ss -tuln
```

---

## Notes

- Commands may behave differently depending on the Linux distribution.
- Some operations require elevated privileges using `sudo`.
- Always understand a command before executing it, especially commands involving deletion, permissions, and system administration.
- This cheatsheet will be updated as I progress through my Linux and cybersecurity studies.

## References

- [Linux Manual Pages](https://man7.org/linux/man-pages/)
- [GNU Coreutils Documentation](https://www.gnu.org/software/coreutils/manual/)
- [Ubuntu Documentation](https://documentation.ubuntu.com/)