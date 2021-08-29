
import uos, machine,time,lib
from httpServer import http
import gc
import webrepl
webrepl.start()
gc.collect()




#响应按键开关
device="Power"
power=lib.flashLed(5)#开关控制引脚
p4=lib.flashLed(4)
p12=lib.flashLed(12)
btn=lib.btn(14)#按键
config="cfg.py"
def led(c):
  if c=="red":
    p4.sw(0);p12.sw(1)
  if c=="blue":
    p4.sw(1);p12.sw(0)
  if c=="off":
    p4.sw(0);p12.sw(0)
led("blue")
def sw():

    power.sw()
    led("red") if power.sw('') else led("blue")

btn.click(sw)

#响应按键开关

def setFile(s=1):
      print("[Restart]:counter is running",type(s)      )
      fi="isRset.py"
      try:
        f=open(fi,"r")
        num=int(f.read())
      except:
        f=open(fi,"w")
        f.write("1")
        f.flush()
        f.close()        
        return 1
      del f
      if s=="read":
        return num
      f=open(fi,"w")
      int_1= str(0) if type(s).__name__=="Timer" or s==0 else (str(1+int(num)))
      f.write(int_1)
      f.flush()
      f.close()
      print("[Restart] counter set: ",int_1)
      return int(int_1)



def _reset(s=1):
    setFile()
    setFile()
    setFile()
    machine.reset()
    
btn.press(_reset,5000)
def wifi_setup(url):
        if url =="/":
          serv.sendall('<form action="wifi">SSD:<br><input type="text" name="ssd" value=""><br>PASSWORD<br><input type="text" name="pwd" value=""><hr>KEY<br><input type="text" name="key" value=""><input type="submit" value="Submit"></form> ')
          serv.sendall('<hr/>')
          ap_list=lib.wifi()[0].scan()
          for i in ap_list:
            serv.sendall("%s ,%d<br/>"%(i[0].decode(),i[3]))
        if url.find("/wifi")!=-1:
            d=(serv.get_Args(url))
            print(d)
            if d.get("ssd") !=None and d.get("pwd")!=None:
              conf="ssd='%s'\r\npwd='%s' \r\nkey='%s'"%(d.get("ssd"),d.get("pwd"),d.get("key"))
              wc=open(config,"wb")
              wc.write(conf)
              wc.flush()
              wc.close()
              serv.send("\r\n") 
              serv.send("设置成功，即将重启。")
              time.sleep(3)
              machine.reset()
        else:
         serv.send("666 \r\n")

try:
  #print("重启次数：",setFile("read"))
  #tim=machine.Timer(-1)     
  #tim.init(period=5000, mode=machine.Timer.ONE_SHOT, callback=setFile)
  if setFile("read") >=3:
      p4.flash(100)
      p12.flash(50)
      lib.ap(device)
      setFile(0)
      serv=http("0.0.0.0",80)
      while 1:
        serv.http(wifi_setup)    
  
except:
  #print("无法写入")
  pass
try:
  import cfg
  ssd=cfg.ssd
  pwd=cfg.pwd
  key=cfg.key
except:
  setFile()
  setFile()
  setFile()
wifi=lib.wifi(ssd,pwd,device)[0]