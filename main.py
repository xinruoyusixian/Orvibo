import time
import bafa,taskFunc


try:
    task=taskFunc.Task()  
    def p_data(topic,msg):
       print(topic,msg)
       if msg==b'reset':
           machine.reset()
       if msg==b'on':
         power.sw(1)
         led("red")
       if msg==b'off':
         power.sw(0)  
         led("blue")
       if msg==b'get':  
          _bfmq.publish(b"on") if power.sw('') else _bfmq.publish(b"off")
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
    while 1:
      r=task.doTask()
      if r!= None:
        power.sw(r)
      if  not wifi.isconnected():
          p4.sw(delay=150)
          continue
      p4.sw(delay=500)
      if _bfmq.online:
        dely_time= 40 
      else:
          dely_time= 2
          p12.sw(delay=150)
      if time.time()%dely_time==0:
        led("red") if power.sw('') else led("blue")
        _bfmq.publish( "on" if power.sw('') else "off")
        
        time.sleep(1)
      _bfmq.check_msg()

except:
  machine.reset()