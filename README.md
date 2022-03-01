# Welcome to the PimpMyPhototheque!


![PimpMyJDownloader](https://raw.githubusercontent.com/coxifred/PimpMyPhototheque/main/images_resources4wiki/PimpMyPhototheque.png)

## **Quick description**
![Overview](https://github.com/coxifred/PimpMyJDownloader/blob/master/images_resources4wiki/monkey.png?raw=true)

Perhaps as me, you've got more than 100000 pictures managed on my share home folder. Space is getting tight and lot of my pictures are blurred.

<center>
<img src="https://raw.githubusercontent.com/coxifred/PimpMyPhototheque/main/images_resources4wiki/blurred.jpg" width="250"/></center><br>

Based on <a href=https://pyimagesearch.com/2015/09/07/blur-detection-with-opencv/>this greate article</a>, i tried to create a GUI to manage my picture folders analysis. The implementation is simple, start a python webserver, add folders to be analysed and take decisions.Close my PC, and see tomorrow morning the progression.

Decisions can be :

 - Delete all the blurred pictures.
 - See picture and delete one by one.

## **Installation**

  Python 3.8 required, just run install.bat or install.sh

## **Configuration**

  Only one configuration file (website.json) :
  ```sh
  {
    "instance"              : "PimpMyPhototheque instance #1",
    "debug"                 : true,
	"webserver"             : true,
    "webserverDebug"        : true,
    "webClass"              : "site",
    "httpBind"              : "0.0.0.0",
	"httpPort"              : 60000,
	"backgroundJobInterval" : 30,
	"resultPath"			: "/var/tmp"
}
```

## **Launch**

 After installation
  - On unix run ./venv/bin/python webserver.py website.json
  - On windows run venv\scripts\python website.py website.json
 
 After fews seconds html page is browseable on port 60000 (http)

<center>
<img src="https://raw.githubusercontent.com/coxifred/PimpMyPhototheque/main/images_resources4wiki/main.jpg" width="800"/></center><br>

## **Demo**

<center>
<img src="https://raw.githubusercontent.com/coxifred/PimpMyPhototheque/main/images_resources4wiki/demo.gif" width="800"/></center><br>

## **Considerations**

- Logs are written in the same place than the webserver.py file
- resultPath in config file, will contain analysis results.

