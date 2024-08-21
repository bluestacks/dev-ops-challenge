# Devops Challenge

# Assignment 1

This assignment is to create an Amazon CloudFront(CDN) for your static content website which you have to host on S3 bucket (https://xxxxxxxxx.cloudfront.net/)

Case A. If the user opens (https://xxxxxxxxx.cloudfront.net/) it should be seen "Hello, CDN origin is working fine"

      A.1 This behavior object content stays in an Edge Cache at for at least 48 hours 

Case B. If the user opens (https://xxxxxxxxx.cloudfront.net/devops-folder/) it should fetch from other S3 bucket and user should see "Hello, CDN 2 origin is working fine"

# NOTE: Please create only one CloudFront Distribution without the Alternate Domain Names (CNAMEs) and share the CDN domain name to validate the assignment.

# NOTE: Both the URLs should not include index.html or any .html extension.`

# Assignment 2

We want to gather some basic statistics for our security team. They want to know the top 8 IP addresses that hit our web servers.

Your task will be the following:
Implement a script (use any language you want) to get the top 8 IP addresses out of an existing log file
Save your script with no file extension
It has to be an executable file
there is no need to use arguments
The output format will be the following:(8 lines - top saw IP addresses by the number of hits):

<ip_address><space><number_of_hits>

A real example output would look like this:

$ count

92.6.41.236 22

186.248.72.9 19

81.243.137.36 18

217.118.78.16 15

213.118.39.51 15

93.146.139.64 14

80.116.15.0 14

186.213.159.176 11

Logfile: [Click here](https://github.com/bluestacks/dev-ops-challenge/blob/master/logfile)


# Assignment 3
A client has a Linux server that has just paged you because of a high load average issue. Upon connecting and running uptime you see: 12:20:50 up 1 day, 10:52, 6 users, load average: 44.28, 33.34, 30.44 How would you troubleshoot this issue to find out what is the source of the load and what tools would you use? Please also list what you would look for in the output of the commands you would run.


# NOTE: Use AWS free tier for hosting.

