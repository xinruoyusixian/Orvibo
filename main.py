







import time

import bafa,taskFunc
from machine import WDT,RTC

_Stat="_Stat"
try:
    task=taskFunc.Task()  

    def p_data(topic,msg):
       print("recv:",topic,msg)
       pass
       msg=msg.decode()
       cmd=msg.split("#")
       if cmd[0]=="cmd":
         if cmd[1]=='reset':
             machine.reset()
             
         if cmd[1]=='on':
           power.sw(1)
           lib.file(_Stat,"1")

         if cmd[1]=='off':
           power.sw(0) 
           lib.file(_Stat,"0")

         led("red") if power.sw('') else led("blue")
         print("被动发送状态") 
         _bfmq.publish( "r-on" if power.sw('') else "r-off")
         _bfmq.publish("%s/%s/%s %s:%s:%s"%time.localtime()[:6]+ " Run:%.2f h,free:%s kb"%(time.ticks_ms()/3600000,gc.mem_free()/8/1024))
         _bfmq.publish(str(wifi.ifconfig()[0]))

       if cmd[0]=="time":
          list=[int(item) for item in cmd[1].split("|")]
          rtc = RTC()
          rtc.datetime((list[0], list[1], list[2] ,None,list[3], list[4], list[5] ,0))
          _bfmq.publish(b"时间已更新") 
          return
       if cmd[0]=="add" or cmd[0]=="del" or cmd[0]=="query":
         ret=task.TaskMsg(msg)
         _bfmq.publish(ret) 

 

       

    Prav_key=key
    _bfmq=bafa.bfMqtt(Prav_key,topic,p_data)
    _bfmq.connect()
    _bfmq.publish("IP:%s"%str(wifi.ifconfig()[0]))
    lib.update_time()

    wdt=WDT()
    while 1:
      #检查网络
      gc.collect()
      if  not wifi.isconnected():
          p4.sw(delay=150)
          continue
          
      wdt.feed()
      #print("start",time.ticks_ms()/1000)
      #time.sleep(0.1)
      r=task.doTask()
      sec=time.localtime()[5]
      if r!= None:
        power.sw(r)
        lib.file(_Stat,"1" if power.sw('') else "0")
        led("red") if power.sw('') else led("blue")


      p4.sw(delay=500)

      if _bfmq.online:
        dely_time= 40 

      else:
          dely_time= 2
          p12.sw(delay=150)
          
          
          
      if(sec%30==0):
        #睡0.8秒防止在一秒内循环
        time.sleep(1)
        #30秒主动上报状态
        _bfmq.publish( "r-on" if power.sw('') else "r-off")
        

        
      if(sec%2==0):
        #2秒检测一次led状态
        led("red") if power.sw('') else led("blue")
        

      _bfmq.check_msg()



except:

  machine.reset()







