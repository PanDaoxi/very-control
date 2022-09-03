from django.urls import path as site
from django.shortcuts import HttpResponse
from os import system, remove, environ
from base64 import a85decode, b64encode
from sys import path
from requests import get
from pyautogui import screenshot
from tkinter import Tk
from time import strftime, sleep
from cv2 import VideoCapture, imwrite
from pyttsx3 import init as ttsInit

# 定义 TTS 朗读者
tts_name = []
engine = ttsInit()
voices = engine.getProperty('voices') 
for voice in voices:
    tts_name.append(voice.name) 
engine.stop()
del engine
tts_name.append('Windows <kbd>SAPI.spVoice</kbd>')

# 求最大公因数
def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


# 适配图片比例
def change(a, b):
    x = gcd(a, b)
    a /= x
    b /= x
    while a < 500 or b < 500:
        a *= 2
        b *= 2
    return (a, b)


# 拍照
def get_photo():
    cap = VideoCapture(0)
    f, frame = cap.read()
    imwrite("./photo.png", frame)
    with open("./photo.png", "rb") as f:
        temp = b64encode(f.read()).decode()
    remove("./photo.png")
    cap.release()
    return "data:image/png;base64,%s" % temp


# 主页
def main(request):
    return HttpResponse(
        """<title>Very Control</title>
<style>
body{
background-image: url(https://pic1.zhimg.com/80/v2-fbbb97b977b5cebc66dc3cefab0ac981_1440w.jpg?source=1940ef5c);
}
input,textarea{
filter:alpha(Opacity=30);
-moz-opacity:0.4;
opacity:0.6;
}
</style>
    <form id="run" action="/run" method="post" enctype="multipart/form-data">    
    <h1>Very Control 多对一远程控制平台</h1>    
    <p>输入命令： <input type="text" name="command" placeholder="输入 Windows 命令 "/></p>
    <p>带有回显的命令：<input type="text" name="echo" placeholder="输入命令，并返回输出内容 "/>
    <p>上传应用程序：<input type="file" name="runf"/></p>
    <p>提交批处理文件的源代码：</p>
    <p><textarea name="code" rows="10" cols="75" placeholder="输入你的 Windows Batch 代码"></textarea></p>
    <input type="submit" value="运行"/>
    </form>
    <br><br>
<hr>
<center><p>其他功能：<a href="ss">截取屏幕</a>\t\t<a href="inf">查看被控制者信息</a>\t\t<a href="cam">捕获摄像头</a>\t\t<a href="sendm">发送消息</a>\t\t<a href="rn">阅读官方通知</a></p></center>
"""
    )


# 阅读通知
def readNotice(request):
    return HttpResponse(
        """<title>阅读官方通知</title>
<h1>官方通知</h1>
<hr><br>
<iframe src="https://pandaoxi.github.io/very-control/" width="800" height="450"></iframe>
<p>页面加载较慢是正常现象，请耐心等候。</p>
<br><hr>
<p>软件信息：</p>
<p>开发者：<b><font face="Consolas"><a href="https://pandaoxi.github.io/" target="_blank">PanDaoxi</a></font></b></p>
<p>开发者邮箱（欢迎意见反馈和技术支持）：<a target="_blank" href="http://mail.qq.com/cgi-bin/qm_share?t=qm_mailme&email=5paHiIKHiZ6P1NbU1KaXl8iFiYs" style="text-decoration:none;"><img src="http://rescdn.qqmail.com/zh_CN/htmledition/images/function/qm_open/ico_mailme_02.png"/></a></p>
<p><a href="https://github.com/pandaoxi/very-control/tree/main/Very_Control"><kbd>Very_Control</kbd>软件已经开源，欢迎前来查看😀</a></p>
<center><a href="jump">回到主页</a></center>
"""
    )


# 运行
def run(request):
    system("chcp 65001 >nul")
    text = request.POST.get("command")
    code = request.POST.get("code")
    runf = request.FILES.get("runf")
    echo = request.POST.get("echo")
    if code:  # 优先级最高的 执行批处理脚本
        with open("temp.bat", "w", encoding="utf-8") as f:
            f.write(code + "\nexit")
        system("start %s\\temp.bat" % path[0])
    if runf:  # 次之的应用程序
        with open("temp.exe", "wb") as f:
            f.write(b"")
        with open("temp.exe", "wb") as f:
            for i in runf.chunks():
                f.write(i)
        system("start %s\\temp.exe" % path[0])
    if text:  # 最后是直接执行命令
        system(text)
    if echo:  # 带回显的执行命令
        try:
            remove("temp.txt")
        except:
            pass
        system("%s >> temp.txt" % echo)
        with open("temp.txt", "r", encoding="utf-8") as f:
            ret = f.read().splitlines()
        s = ""
        for i in ret:
            s += "<p>%s</p>\n" % i
        return HttpResponse(
            """<title>程序运行结果</title>
%s

<br><hr><br>
<center><a href="jump">回到主页</a></center>"""
            % s
        )
    return HttpResponse('<center><h1>运行成功！🎉🎉</h1></center><meta http-equiv="refresh" content="2;url=jump"/>')


# 截图
def ss(request):
    window = Tk()
    window.withdraw()
    width = window.winfo_screenwidth()
    height = window.winfo_screenheight()
    image = screenshot(region=(0, 0, width, height))
    image.save("./screenshot.png")
    with open("./screenshot.png", "rb") as f:
        content = b64encode(f.read()).decode()
    remove("./screenshot.png")
    w, h = change(width, height)
    return HttpResponse(
        """<title>Screen Shot</title>
<center>
    <img src="data:image/png;base64,%s" alt="截图" height="%d" width="%d">
    <br><br><hr>
    <a href="jump">回到主页</a>\t\t<a href="ss">重新截图</a>
</center>
    """
        % (content, h, w)
    )
    window.mainloop()


# 环境信息
def inf(request):
    system("chcp 65001 >nul")
    s1 = ""
    for i in environ.keys():
        s1 += "<p>%s\t%s</p>\n" % (i, environ[i])
    try:
        remove("temp.txt")
    except:
        pass
    system("tasklist>>temp.txt")
    with open("temp.txt", "r", encoding="utf-8") as f:
        s2 = f.read().splitlines()
    remove("temp.txt")
    s3 = ""
    for i in s2:
        s3 += "<p>%s</p>\n" % i
    return HttpResponse(
        """<title>Os_Environ</title>
<h1>系统环境变量 </h1>
%s

<br><br><hr>
<h1>运行的进程（如需对齐可以看此网页的源代码） </h1>
%s
<br><br><hr>
<center><a href="jump">返回主页</a></center>
"""
        % (s1, s3)
    )


# 拍照
def camera(request):
    return HttpResponse(
        """<title>摄像头捕获</title>
<center>
    <img src="%s" alt="摄像头捕获" height="450" width="800">
    <br><br>
    <p>该功能可能会比较卡顿；如果不能正常显示出摄像头图像，可能是因为被控制设备的摄像头无法访问。</p>
    <br><hr>
    <a href="jump">回到主页</a>\t\t<a href="cam">重新拍照</a>
</center>
    """
        % get_photo()
    )


# 发送消息文本
def sendMessage(request):
    return HttpResponse(
        """<title>发送消息文本</title>
<style>
body{
background-image: url(https://pic1.zhimg.com/80/f56513788384645db768d0ec542dec33_1440w.jpg);
}
input,textarea{
filter:alpha(Opacity=30);
-moz-opacity:0.4;
opacity:0.6;
}
</style>
    <form id="show" action="/showm" method="post" enctype="multipart/form-data">    
    <h1>Very Control - 消息发送器</h1>    
    <p>发送语音消息（内容将会在被控制端朗读，您可以<b><a href="/settts">自定义朗读者</a></b>，或使用默认值）：<input type="text" name="reader" placeholder="输入要发送的内容"/></p>
    <p>输入发送给被控制端的消息，消息将会以<b>警示框</b>的形式表现：</p>
    <p><textarea name="msg" rows="25" cols="100" placeholder="输入你的 消息文本"></textarea></p>
    <input type="submit" value="发送"/>  
    <br><br>

<br><br><hr>
<center><a href="jump">回到主页</a></center>  
"""
    )


# 显示信息
def showMessage(request):
    msg = request.POST.get("msg")
    reader = request.POST.get("reader")
    if msg:
        with open("temp.py", "w+", encoding="utf-8") as f:
            f.write("from easygui import msgbox\nmsgbox('''%s''',\"Very Control\")" % msg)
        system("start /min cmd /c temp.py")
    if reader:
        tts_config = []
        try:
            with open("TTS_config", "r", encoding="utf-8") as f:
                tts_config = f.read().splitlines()
            c1, c2, c3 = int(tts_config[0]), int(tts_config[1]), float(tts_config[2])
        except:
            c1, c2, c3 = 0, 100, 1.0
        if tts_config[0] == "2":
            with open("say.vbs", "w", encoding="ANSI") as f:
                f.write("set sapi = createObject(\"SAPI.SpVoice\")\nsapi.Speak \"%s\"" % reader)
            system("start /min cmd /c call \"say.vbs\"")
        else:
            engine = ttsInit()
            engine.setProperty("rate", c2)
            engine.setProperty("volume", c3)
            voices = engine.getProperty("voices") 
            engine.setProperty("voice", voices[c1].id)
            engine.say(reader)
            engine.runAndWait()
            engine.stop()
    return HttpResponse("""<center><h1>发送成功！✨</h1></center><meta http-equiv="refresh" content="2;url=sendm"/>""")


def setupTTS(request):
    temps = ""
    for i in range(len(tts_name)-1, -1, -1):
        temps += "  <input type=\"radio\" name=\"tts_id\" value=\"%d\" checked>%s<br>\n" % (i, tts_name[i])
    return HttpResponse(
        """<title>自定义 TTS</title>
<style>
body{
background-image: url(https://pic1.zhimg.com/80/f56513788384645db768d0ec542dec33_1440w.jpg);
}
input,textarea{
filter:alpha(Opacity=30);
-moz-opacity:0.4;
opacity:0.6;
}
</style>
    <form id="setup" action="/upd_tts" method="post" enctype="multipart/form-data">    
    <h1>Very Control - 自定义 TTS 朗读者</h1>    
    <p>设置朗读者音色：<br><br>
    %s
    </p>
    <p>以下设置，仅对非 <kbd>SAPI</kbd> 有效；错误的设置将使用默认值。</p>
    <p>语速：<input type="text" name="tts_speed" placeholder="输入正整数，默认为 100"/><p>
    <p>音量：<input type="text" name="tts_volume" placeholder="输入小数，默认为 1.0"/><p>
    <p><a href="/upd_tts">恢复默认设置</a></p>
    <input type="submit" value="保存"/>  
    <br><br>

<br><br><hr>
<center><a href="javascript:history.back(-1)"">回到上一页</a></center>  
"""
        % temps
    )


def updateTTS(request):
    tts_id = request.POST.get("tts_id")
    tts_speed = request.POST.get("tts_speed")
    tts_volume = request.POST.get("tts_volume")
    if tts_id == None and tts_speed == None and tts_volume == None:
        tts_id = "0"
        tts_speed = "100"
        tts_volume = "1.0"
    with open("TTS_config", "w", encoding="utf-8") as f:
        f.write("%s\n%s\n%s" % (tts_id, tts_speed, tts_volume))
    return HttpResponse("""<center><h1>保存完成！🎈</h1></center><meta http-equiv="refresh" content="2;url=sendm"/>""")

urlpatterns = [
    site("", main),
    site("jump", main),
    site("run", run),
    site("ss", ss),
    site("inf", inf),
    site("cam", camera),
    site("sendm", sendMessage),
    site("showm", showMessage),
    site("rn", readNotice),
    site("settts", setupTTS),
    site("upd_tts", updateTTS),
]
