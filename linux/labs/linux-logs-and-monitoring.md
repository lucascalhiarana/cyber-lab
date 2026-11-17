\# Linux Lab: Logs and System Monitoring



\## 1. Overview



This lab explores Linux system logs, authentication events, SSH service monitoring, and real-time log analysis using `journalctl`.



The objective is to understand how Linux records system activity, identify relevant events, investigate authentication failures, and monitor services.



\*\*Environment:\*\* Kali Linux Rolling  

\*\*Filesystem:\*\* ext4  

\*\*Log management:\*\* systemd journal  

\*\*Focus:\*\* Linux administration, log analysis, and Blue Team fundamentals



\## 2. Identifying the Linux Environment



The operating system information was checked using:



```bash

cat /etc/os-release

```



The command initially failed. Further investigation showed that `/etc/os-release` was a symbolic link pointing to `/usr/lib/os-release`.



```bash

ls -l /etc/os-release

cat /usr/lib/os-release

cat /etc/issue

cat /etc/debian\_version

```



The environment was identified as Kali GNU/Linux Rolling, based on Debian.



\## 3. Exploring the Log Directory



The `/var/log` directory was inspected:



```bash

ls -lah /var/log

```



Several log files and directories were identified.



| File or Directory | Purpose |

|---|---|

| `boot.log` | Boot-related events |

| `dpkg.log` | Package installation and removal records |

| `alternatives.log` | System alternatives configuration changes |

| `journal/` | Persistent systemd journal data |

| `apache2/` | Apache web server logs |

| `nginx/` | Nginx web server logs |

| `mysql/` | MySQL-related logs |



The traditional `/var/log/auth.log` file was not present in this environment.



Authentication and system events were therefore investigated using the systemd journal.



\## 4. Querying System Logs with journalctl



The most recent journal entries were displayed using:



```bash

journalctl --no-pager -n 15

```



The output included VirtualBox shared clipboard messages related to X11.



These messages were associated with the virtualized graphical environment and were not, by themselves, evidence of malicious activity.



\### Filtering by priority



Error messages:



```bash

journalctl -p err --no-pager -n 20

```



Warning messages and higher-priority events:



```bash

journalctl -p warning --no-pager -n 20

```



Several events were identified during the investigation:



| Event | Observation |

|---|---|

| `vmwgfx` errors | Graphics driver compatibility messages in the virtualized environment |

| PAM warnings | Authentication-related configuration messages |

| `evolution-source-registry.service not found` | GNOME service lookup failure |

| `systemd-ssh-generator terminated by signal ABRT` | SSH generator process terminated abnormally |

| Journal corruption or unclean shutdown warning | Journal reported an unclean shutdown or corrupted journal file |

| UPower errors | Power management information could not be retrieved |



These events demonstrate why log analysis requires context. An operational error does not automatically indicate a security incident.



\## 5. Inspecting the SSH Service



The SSH service status was checked:



```bash

systemctl status ssh --no-pager

```



The service was active and running.



The output showed:



```text

Active: active (running)

```



The SSH server was listening on:



```text

0.0.0.0 port 22

:: port 22

```



This indicates that SSH was listening on the available IPv4 and IPv6 interfaces.



The SSH configuration directory was also inspected:



```bash

ls -lah /etc/ssh/

```



Relevant files included:



\- `ssh\_config`: SSH client configuration.

\- `sshd\_config`: SSH server configuration.

\- `ssh\_config.d/`: Additional client configuration.

\- `sshd\_config.d/`: Additional server configuration.

\- `ssh\_host\_\*`: SSH server host keys.



Private host keys must be protected and should never be published in a public repository.



\## 6. Investigating SSH Authentication Events



The traditional authentication log file was checked:



```bash

ls -lah /var/log/auth.log\*

```



It was not available in this environment.



The systemd journal was used instead:



```bash

journalctl \_COMM=sshd --no-pager -n 30

```



The output showed SSH service startup and shutdown events.



To investigate authentication activity, the following filters were used:



\### Failed authentication attempts



```bash

sudo journalctl --no-pager | grep -iE 'failed password|authentication failure|invalid user'

```



\### Successful authentication events



```bash

sudo journalctl --no-pager | grep -iE 'accepted password|accepted publickey'

```



\### SSH service events



```bash

sudo journalctl -u ssh --since today --no-pager

```



\### Observed authentication events



The historical records included:



\*\*Successful authentication:\*\*



```text

Oct 22 13:52:50

Accepted password for kali from 192.168.56.1

```



\*\*Failed authentication attempts:\*\*



```text

Oct 22 13:58:06

Failed password for kali from 10.0.2.15



Oct 22 13:58:14

Failed password for kali from 10.0.2.15



Oct 22 13:58:25

Failed password for kali from 10.0.2.15

```



Three failed SSH authentication attempts were observed for the `kali` user from `10.0.2.15`.



A successful authentication was also recorded from `192.168.56.1`.



These are different IP addresses.



The virtual machine was configured with two network adapters, which provides relevant context for the different addresses. However, the relationship between the observed events should not be assumed without further verification.



\### Investigation notes



Three failed attempts alone are not sufficient to classify an event as a brute-force attack.



Relevant investigation steps include:



\- Identifying the source IP address.

\- Checking the targeted username.

\- Comparing timestamps and event frequency.

\- Reviewing historical login patterns.

\- Checking for successful authentication after failed attempts.

\- Understanding the network environment and expected access sources.

\- Monitoring subsequent activity.



The events were treated as suspicious activity worth investigating, not as confirmed malicious activity.



\## 7. Reviewing Login History



The login history was inspected using:



```bash

last -n 10

```



To include remote host information when available:



```bash

last -ai | head -20

```



The output included sessions associated with the `kali` user and the `lightdm` graphical login manager.



This information can help establish a baseline of normal login activity and identify unusual access patterns.



\## 8. Real-Time Log Monitoring



The system journal was monitored in real time:



```bash

sudo journalctl -f

```



The `-f` option follows new journal entries as they are generated.



To monitor only SSH events:



```bash

sudo journalctl -f -u ssh

```



A controlled SSH service restart was performed in another terminal:



```bash

sudo systemctl restart ssh

```



The monitoring terminal displayed events such as:



```text

Stopping ssh.service

Deactivated successfully

Stopped ssh.service

Starting ssh.service

Server listening on 0.0.0.0 port 22

Server listening on :: port 22

Started ssh.service

```



This exercise demonstrated how service activity can be observed as it happens.



Press `Ctrl + C` to stop real-time monitoring.



\## 9. Filtering Events by User



The journal was filtered using the UID of the current `kali` user:



```bash

sudo journalctl \_UID=1000 --since today --no-pager -n 30

```



The results included:



\- Sudo session activity.

\- Commands executed with elevated privileges.

\- XFCE desktop services.

\- Screensaver authentication-related events.



An example of a useful administrative record was:



```text

kali : TTY=pts/1 ; PWD=/home/kali ;

USER=root ; COMMAND=/usr/bin/systemctl restart ssh

```



This record identifies the user who executed the command, the terminal, the working directory, the target user, and the command itself.



Such information can help reconstruct administrative activity during an investigation.



\## 10. Counting Authentication Events



The following commands can be used to count matching events in the available journal:



```bash

sudo journalctl --since today --no-pager | grep -ic "Failed password"

```



```bash

sudo journalctl --since today --no-pager | grep -ic "Accepted password"

```



```bash

sudo journalctl --since today --no-pager | grep -ic "authentication failure"

```



These commands provide a quick overview of matching events.



The counts should be interpreted in context. A high number of failed logins may require further investigation, but the count alone does not establish malicious activity.



\## 11. Commands Learned



| Command | Purpose |

|---|---|

| `journalctl` | Queries the systemd journal |

| `journalctl -f` | Follows new journal events |

| `journalctl -u` | Filters events by systemd unit |

| `journalctl -p` | Filters events by priority |

| `journalctl \_COMM=` | Filters by process name |

| `journalctl \_UID=` | Filters by user ID |

| `systemctl status` | Checks service status |

| `systemctl restart` | Restarts a service |

| `ls -lah` | Lists files with detailed information |

| `grep -iE` | Searches using case-insensitive extended patterns |

| `grep -c` | Counts matching lines |

| `last` | Displays login history |

| `uname -a` | Displays kernel information |



\## 12. Key Takeaways



Through this lab, I practiced:



\- Exploring Linux log directories.

\- Identifying systemd journal as a source of system events.

\- Filtering logs by priority, service, process, and user.

\- Inspecting SSH service status and configuration files.

\- Identifying successful and failed authentication events.

\- Reviewing login history.

\- Investigating potentially suspicious authentication activity.

\- Monitoring system events in real time.

\- Correlating events while considering network context.

\- Distinguishing operational errors from potential security indicators.



\## 13. Relevance to Blue Team and SOC Operations



Log analysis is a fundamental activity in defensive security.



Security analysts use system and authentication logs to investigate access attempts, monitor service activity, identify unusual behavior, and reconstruct events.



This lab provided practical experience with Linux logging tools and basic investigation techniques that are relevant to future SOC operations.



\*\*Lab status:\*\* Completed



\*\*Next steps:\*\* Continue practicing Linux log analysis, authentication monitoring, and security event investigation.

