
import lib,time

class Task:
  def __init__(self,f=None):
      self.cfg= f if f !=None else "task_cfg.py"
      self.list=lib.file(self.cfg)
      self.list= eval(self.list) if self.list else []   
          
  def doTask(self):
        if len(self.list)!=0:
          currentDate=time.localtime()[:3]
          for i in self.list:
            currentSec=time.mktime((currentDate+(i[0],i[1])+(1,0,0)))
            if  currentSec == time.time():
              if not i[3]:
                self.list.remove(i)
                lib.file(self.cfg,str(self.list))
                time.sleep(1)
              return(i[2])
  
  def TaskMsg(self,msg): 
        if msg[:3]=='add':
          try:
            #"add#20:16#1#1" 时间:操作:运行
            msg=msg.split("#")[1:]
            msg=msg[0].split(":")+msg[1:]
            self.list.append(tuple(int(i) for i in msg))
            lib.file(self.cfg,str(self.list))
            return(str(self.list))
            
          except Exception as e:
            return str(e)
         
        if msg[:3]=='del':
          try:
            self.list.remove( self.list[int(msg.split("#")[1])])
            lib.file(self.cfg,str(self.list))
            return str(self.list)
       
          except Exception as e:
            return str(e)       
         
        if msg=="query":
          try:
            return str(self.list)
          except Exception as e:
            return str(e) 
         
    
