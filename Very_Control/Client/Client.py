# Author:PanDaoxi
from requests import post,get
from base64 import a85encode
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from easygui import *
from time import sleep

title = 'Very Control'
hide = Tk()
hide.withdraw()

def update():
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44',
            }
    with open(__file__,'wb') as f:
        f.write(get('https://pandaoxi.coding.net/p/pandaoxi/d/Projects/git/raw/master/Very_Control/Client/Client.py',headers=headers).content)
    
    sleep(0.2)
    temp = get('https://pandaoxi.coding.net/p/pandaoxi/d/Projects/git/raw/master/Very_Control/Client/VERSION',headers=headers)
    temp.encoding = 'utf-8'
    return temp.text
    
try:
    title = title + ' (V %s)' % update()
    server = enterbox('输入你的服务器IP：',title)
    getfile = askopenfilename(title=title,filetypes=(('可执行的应用程序','*.exe'),))
    with open(getfile,'rb') as f:
        tmp = a85encode(f.read()).decode()
    data = {'runf':tmp}
    post(server + 'run',data=data)
    msgbox('完成！',title)
    
except Exception as e:
    msgbox('错误：\n%s' % e,title)
hide.mainloop()