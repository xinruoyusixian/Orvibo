import time
import bafa
        

try:
    ##定时
    try:
      import task
    except:
      lib.file("task.py",'list=[]')
      import task
    def doTask():
      if len(task.list)!=0:
        for i in task.list:
          if time.mktime(i[0]+(0,0)) < time.time():
            task.list.remove(i)
            power.sw(i[1])
            lib.file("task.py",'list='+str(task.list))
            _bfmq.publish(b"on") if power.sw('') else _bfmq.publish(b"off")
    def doTaskMsg(msg):        
      if msg[:3]=='add':
        try:
          task.list.append([tuple( int(i) for i in msg.split("#")[1].split("-")),int(msg.split("#")[2])])
          lib.file("task.py",'list='+str(task.list))
          _bfmq.publish(b'success')
          return 
        except OSError as e:
          _bfmq.publish(str(e).encode())
          return 
      if msg[:3]=='del':
        try:
          task.list.remove( task.list[int(msg.split("#")[1])])
          lib.file("task.py",'list='+str(task.list))
          _bfmq.publish(str(task.list))
          return 
        except OSError as e:
          _bfmq.publish(str(e).encode())       
          return
      if msg=="query":
        try:
          _bfmq.publish(str(task.list))
          return 
        except OSError as e:
          _bfmq.publish(str(e).encode())  
          return 
      
    DEBUG=1

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
       doTaskMsg(msg.decode()) 
       
    Prav_key=key
    _bfmq=bafa.bfMqtt(Prav_key,"power001",p_data)
    _bfmq.connect()

    _bfmq.publish(str(wifi.ifconfig()).encode())
    lib.update_time()
    while 1:
      doTask()
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
