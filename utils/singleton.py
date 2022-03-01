from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_SCHEDULER_STARTED, EVENT_SCHEDULER_PAUSED, EVENT_SCHEDULER_RESUMED, EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, EVENT_JOB_MISSED, EVENT_JOB_MAX_INSTANCES, JobExecutionEvent, SchedulerEvent
import time


class Singleton(object):
        class __Singleton:
                def __str__(self):
                        return self
 

                
                def my_listener(self,event):
                    if isinstance(event, SchedulerEvent):
                         if event.code == EVENT_SCHEDULER_STARTED:
                             print("INF Scheduler has started ")
                             schedulerUptime = time.time()
                         if event.code == EVENT_SCHEDULER_PAUSED:
                             schedulerUptime = 0.0
                             print("INF Scheduler has paused ")
                         if event.code == EVENT_SCHEDULER_RESUMED:
                             schedulerUptime = time.time()
                             print("INF Scheduler has resumed ")
                    if isinstance(event, JobExecutionEvent):
                         if event.code == EVENT_JOB_EXECUTED:
                             print("INF The job " + event.job_id + " has runned successfully ")
                         if event.code == EVENT_JOB_ERROR:
                             print("INF The job " + event.job_id + " has crashed ")
                        
                def __init__(self):
                        self.hostName=''
                        self.debug=False
                        self.version=''
                        self.parameters={}
                        self.logs=[]
                        self.connector=''
                        self.webapp=''
                        self.scheduler=APScheduler()
                        self.internalScheduler=BackgroundScheduler()
                        self.internalScheduler.start()
                        self.ip=''
                        self.port=''
                        self.schedulerThread=BackgroundScheduler({'apscheduler.executors.default': {'class': 'apscheduler.executors.pool:ThreadPoolExecutor','max_workers': 10},'apscheduler.executors.processpool': {'type': 'processpool','max_workers': 10}})
                        self.schedulerThread.add_listener(self.my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR | EVENT_JOB_MISSED | EVENT_SCHEDULER_STARTED | EVENT_SCHEDULER_PAUSED | EVENT_SCHEDULER_RESUMED)
                        self.schedulerThread.start()
                        self.analysis=[]
 
        instance = None
		
		
 
        def __new__(c):
                if not Singleton.instance:
                        Singleton.instance = Singleton.__Singleton()
                return Singleton.instance
 
        def __getattr__(self, attr):
                return getattr(self.instance, attr)
        def __setattr__(self, attr):
                return setattr(self.instance, attr)
