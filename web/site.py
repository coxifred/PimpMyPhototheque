import os
import json
import jsons
from utils.functions import Functions
from utils.singleton import Singleton
from flask import Flask
from flask_caching import Cache
from flask import request, send_from_directory
import datetime
import time

from flask import render_template
from thread.detectBlur import detectBlur 



class site():
    def __init__(self):
        self.singleton=Singleton()
        Functions.log("DBG","Site instance created starting site...","site")
		
        self.create_app()

    def create_app(self):
        # create and configure the app
        template_dir = os.path.abspath('./web/templates')
        static_dir = os.path.abspath('./web/static')
        app = Flask("PimpMySuperWatt", instance_relative_config=True,template_folder=template_dir,static_folder=static_dir)
        # For disabling cache, usefull for online html/css/js script modifications
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        app.config['EXPLAIN_TEMPLATE_LOADING'] = True
        cache = Cache(config={'CACHE_TYPE': 'null'})
        cache.init_app(app)

        # ensure the instance folder exists
        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass

        @app.route('/')
        @cache.cached(timeout=1)
        def index():
            cache.clear()
            return render_template('index.html')

        @app.route('/shutdown')
        def shutdown():
            Functions.log("INF","Site instance shutdowning...","site")
            singleton=Singleton()
            for analysis in singleton.analysis:
                analysis.step="Aborting..."
                analysis.stop=True
                w=10
                Functions.log("DBG","Waiting 10s to stop properly " + analysis.id,"site")
                while w > 0:
                    w-=1
                    time.sleep(1.0)
                    if analysis.aborted:
                        Functions.log("DBG","Analysis with id " + analysis.id + " aborted","site")
                        break
                Functions.log("DBG","Deleting Analysis with id " + analysis.id,"site")
                os.remove(analysis.resultBlurredFile)
                os.remove(analysis.resultNotBlurredFile)
                singleton.analysis.remove(analysis)
            os._exit(0)

        @app.route('/addAnalysis')
        def addAnalysis(): 
            imagePath = request.args.get('imagePath') 
            threshold= request.args.get('threshold')
            if imagePath != "" and threshold != "":			
                Functions.log("DBG","New Analysis on " + imagePath + " with threshold = " + threshold + "% starts in 5secs","site")
                aDetectBlurAnalysis=detectBlur()
                aDetectBlurAnalysis.prepare(imagePath,int(threshold))
                singleton=Singleton()
                singleton.schedulerThread.add_job(aDetectBlurAnalysis.run, 'date', run_date=datetime.datetime.now()+datetime.timedelta(seconds=5), id=aDetectBlurAnalysis.id, max_instances=10)
                return "OK"
            else:
                Functions.log("DBG","ImagePath " + imagePath + " or threshold = " + threshold + " are incorrects","site")
                return "KO"

        @app.route('/deleteFile')
        def deleteFile(): 
            id = request.args.get('id')
            blurredFile = request.args.get('blurredFile')
            if blurredFile != "" and id != "" and ( id.lower().endswith("png") or id.lower().endswith("jpg") or id.lower().endswith("jpeg") or id.lower().endswith("gif") or id.lower().endswith("tif") or id.lower().endswith("bmp")):
                Functions.removeLineFromFile(blurredFile,id)
                os.remove(id)
            return "OK"

        @app.route('/deleteAllPicturesAnalysis')
        def deleteAllPicturesAnalysis():
            id = request.args.get('id')
            singleton=Singleton()
            for analysis in singleton.analysis:
                if analysis.id == id:
                    Functions.log("DBG","Deleting Analysis with id " + id,"site")
                    
                for analysis in singleton.analysis:
                    if analysis.id == id:
                        Functions.log("DBG","Deleting files from Analysis with id " + id,"site")
                        with open(analysis.resultBlurredFile, "r") as f:
                            for line in f.readlines():
                                file=Functions.getFieldFromString(line,";",1)
                                Functions.log("DBG","Deleting file " + file,"site")
                                os.remove(file)
                            f.close()
            return "OK"

        @app.route('/deleteAnalysis')
        def deleteAnalysis(): 
            id = request.args.get('id')
            if id != "":
                singleton=Singleton()
                for analysis in singleton.analysis:
                    if analysis.id == id:
                        analysis.step="Aborting..."
                        analysis.stop=True
                        w=10
                        Functions.log("DBG","Waiting 10s to stop properly " + id,"site")
                        while w > 0:
                            w-=1
                            time.sleep(1.0)
                            if analysis.aborted:
                                Functions.log("DBG","Analysis with id " + id + " aborted","site")
                                break
                        Functions.log("DBG","Deleting Analysis with id " + id,"site")
                        os.remove(analysis.resultBlurredFile)
                        os.remove(analysis.resultNotBlurredFile)
                        singleton.analysis.remove(analysis)
            return "OK"

        @app.route('/getFileDetail')
        def getFileDetail(): 
            id = request.args.get('id')
            rangeFrom = request.args.get('from')
            rangeTo = request.args.get('to')
            details=[]
            if id != "" and rangeFrom != "" and rangeTo != "":
                singleton=Singleton()
                for analysis in singleton.analysis:
                    if analysis.id == id:
                        try:
                            lines=Functions.loadFileInArrayWithRange(analysis.resultBlurredFile,int(rangeFrom),int(rangeTo))
                            for line in lines:
                                aResult={}
                                aResult["filePath"]=Functions.getFieldFromString(line,";",1)
                                aResult["percent"]=Functions.getFieldFromString(line,";",2)
                                aResult["threshold"]=Functions.getFieldFromString(line,";",3)
                                aResult["size"]=Functions.getFieldFromString(line,";",4)
                                details.append(aResult)
                        except Exception as err:
                            pass
            return jsons.dumps(details)

        @app.route('/status')
        def status():
            singleton=Singleton()
            return jsons.dumps(singleton.analysis)

        @app.route('/loadPicture')
        def loadPicture():
            picture = request.args.get('picture')
            if picture != "":
                dir_path=os.path.dirname(os.path.realpath(picture))
                basename=os.path.basename(picture)
                return send_from_directory(dir_path, basename)

        
        self.singleton.scheduler.init_app(app)
        self.singleton.scheduler.start()
        app.run(self.singleton.parameters["httpBind"],self.singleton.parameters["httpPort"])
		
		
        
		
        Functions.log("DBG","Site instance started","site")

    def runWebApp(self,app):
        try:
            Functions.log("DBG","Trying to start","site")
            app.run(self.singleton.parameters["httpBind"],self.singleton.parameters["httpPort"],self.singleton.parameters["webserverDebug"])

        except E:
            Functions.log("ERR","Error for starting web","site")
