<!-- A client has a Linux server that has just paged you because of a high load average issue. Upon connecting and running uptime you see: 12:20:50 up 1 day, 10:52, 6 users, load average: 44.28, 33.34, 30.44 How would you troubleshoot this issue to find out what is the source of the load and what tools would you use? Please also list what you would look for in the output of the commands you would run. -->

### COMMANDS TO INVESTIGATE
#### Check the Uptime and Average Load Average
```sh
uptime
```
![alt text](image.png)
#### Check Proccess Tables and Running Process
![alt text](image-1.png)
```sh
top
```
#### Check if the swap memory is high
```sh
free -gh
```
![alt text](image-5.png)
#### Check the PID's of the Top Process for Troubleshooting
```sh
ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%cpu | head

```
![alt text](image-2.png)

#### Check for memory blockage and Usage
```sh
vmstat
```
![alt text](image-3.png)

#### Check for System Logs
```sh
journalctl -xe
```
![alt text](image-4.png)