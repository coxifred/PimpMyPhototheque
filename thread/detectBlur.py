# import the necessary packages
from imutils import paths
from utils.functions import Functions
from utils.singleton import Singleton
from datetime import datetime
import time
import cv2
import os


class detectBlur:


    def variance_of_laplacian(self,image):
        # compute the Laplacian of the image and then return the focus
        # measure, which is simply the variance of the Laplacian
        return cv2.Laplacian(image, cv2.CV_64F).var()

    def prepare(self,imagePath,threshold):
        self.imagePath=imagePath
        self.threshold=threshold
        self.id=Functions.getDateFormat("default") + "_" + self.imagePath.replace("/","_").replace("\\","_").replace(":","_")
        self.progression=0
        self.step="Init"
        self.resultBlurredFile=""
        self.resultNotBlurredFile=""
        self.blurredCount=0
        self.notBlurredCount=0
        self.blurredSize=0
        self.startTime=datetime.now()
        self.total=0
        self.elapsedTime=0
        self.stop=False
        self.aborted=False
        singleton=Singleton()
        singleton.analysis.append(self)

    def run(self):
        singleton=Singleton()
        resultPath=singleton.parameters["resultPath"].replace("\\","/")
        Functions.log("DBG","Results will be stored into " + resultPath,"site")
        self.resultBlurredFile=resultPath + "/" + self.id + ".blurred"
        self.resultNotBlurredFile=resultPath + "/" + self.id + ".notblurred"
        blurredFile = open( self.resultBlurredFile, "w")
        notBlurredFile = open(self.resultNotBlurredFile, "w")
        # loop over the input images
        self.total=0
        self.step="Counting pictures"

        for imagePathing in paths.list_images(self.imagePath):
            self.total+=1
        i=0
        self.step="Working.."
        Functions.log("DBG","Starting Analysis on " + self.imagePath + " with threshold = " + str(self.threshold) + "%","site")
        for imagePathing in paths.list_images(self.imagePath):
            if self.stop:
                self.step="Aborting.."
                Functions.log("DBG"," -->  Aborting analysis " + imagePathing,"detectBlur")
                blurredFile.close()
                notBlurredFile.close()
                time.sleep(5.0)
                self.step="Aborted"
                time.sleep(5.0)
                self.aborted=True
                return
            Functions.log("DBG"," -->  Analysing " + imagePathing,"detectBlur")
            # load the image, convert it to grayscale, and compute the
            # focus measure of the image using the Variance of Laplacian
            # method
            image = cv2.imread(imagePathing)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            fm = self.variance_of_laplacian(gray)
            # if the focus measure is less than the supplied threshold,
            # then the image should be considered "blurry"
            if fm < self.threshold:
                Functions.log("DBG",imagePathing + " is blurry at " + str(fm) + "% threshold was " + str(self.threshold),"detectBlur")
                size=os.path.getsize(imagePathing)
                blurredFile.write("1;" + imagePathing + ";" + str(fm) + ";" + str(self.threshold) + ";" +  str(size) + "\n");
                self.blurredSize+=size
                self.blurredCount+=1
            else:
                Functions.log("DBG",imagePathing + " not blurry " + str(fm) + "% threshold was " + str(self.threshold),"detectBlur")
                notBlurredFile.write("0;" + imagePathing + ";" + str(fm) + ";" + str(self.threshold) +"\n");
                self.notBlurredCount+=1
            if i%10 == 0:
                blurredFile.flush()
                notBlurredFile.flush()
            i+=1
            self.progression=i * 100 / self.total;
            self.elapsedTime=datetime.now() - self.startTime
        Functions.log("DBG","Writing Blurred results inside " + str(blurredFile),"detectBlur")
        Functions.log("DBG","Writing Not Blurred results inside " + str(notBlurredFile),"detectBlur")
        blurredFile.close()
        notBlurredFile.close()
        self.step="Finished"
        Functions.log("DBG","Ending Analysis on " + self.imagePath + " with threshold = " + str(self.threshold) + "%","site")
