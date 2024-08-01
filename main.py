




import time

import bafa,taskFunc
from machine import WDT

_Stat="_Stat"
try:
    task=taskFunc.Task()  
    def p_data(topic,msg):
       print("recv:",topic,msg)

       if msg==b'reset':

           machine.reset()

       if msg==b'on':

         power.sw(1)

         lib.file(_Stat,"1")

       if msg==b'off':

         power.sw(0) 

         lib.file(_Stat,"0")

       led("red") if power.sw('') else led("blue") 

       if msg==b'get' or msg==b'off' or msg==b'on':  

          _bfmq.publish( "r-on" if power.sw('') else "r-off")
          print("被动发送状态")
          lib.update_time()

          _bfmq.publish("%s/%s/%s %s:%s:%s"%time.localtime()[:6]+ " Run:%.2f h"%(time.ticks_ms()/3600000))

          _bfmq.publish(str(wifi.ifconfig()[0]))

       ret=task.TaskMsg(msg.decode())

       if ret != None:
          _bfmq.publish( ret) 

       

    Prav_key=key

    _bfmq=bafa.bfMqtt(Prav_key,"power001",p_data)

    _bfmq.connect()



    _bfmq.publish(str(wifi.ifconfig()).encode())

    lib.update_time()

    wdt=WDT()
    while 1:
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
        
        #检查网络
        if  not wifi.isconnected():
          p4.sw(delay=150)
          continue
        
      if(sec%2==0):
        #2秒检测一次led状态
        led("red") if power.sw('') else led("blue")
        

      _bfmq.check_msg()



except:

  machine.reset()




