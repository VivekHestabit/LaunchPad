Linux commands inside Docker container : 

container Details : 

container Name : day1-container
Base-image : node:18-alpine



1.list files :ls
ls : list all files  
->index.js           package-lock.json  package.json

2.ps : running process inside the container : 
->     1 root      0:00 npm start
   18 root      0:00 node index.js
   42 root      0:00 /bin/sh
   49 root      0:00 ps
3.top : CPU and Memory Usage
    1     0 root     S     299m   1%   2   0% npm start
   18     1 root     S     261m   1%   0   0% node index.js
   58     0 root     S     1708   0%   8   0% /bin/sh
   64    58 root     R     1636   0%   8   0% top
4.Docker logs : 

> docker-day1@1.0.0 start
> node index.js

Server started on port 3000
Request received


