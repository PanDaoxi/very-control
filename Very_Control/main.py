# Copyright 2022 by PanDaoxi. All rights reserved.
from socket import socket, AF_INET, SOCK_DGRAM
from os import system, name
from time import strftime, sleep
from colorama import init, Fore, Back
from requests import get

version = "1.3.5.0"
updateFiles = {
    "./manage.py": "https://pandaoxi-project.github.io/very-control/Very_Control/manage.py",
    __file__: "https://pandaoxi-project.github.io/very-control/Very_Control/main.py",
    "./VeryControl/asgi.py": "https://pandaoxi-project.github.io/very-control/Very_Control/VeryControl/asgi.py",
    "./VeryControl/settings.py": "https://pandaoxi-project.github.io/very-control/Very_Control/VeryControl/settings.py",
    "./VeryControl/urls.py": "https://pandaoxi-project.github.io/very-control/Very_Control/VeryControl/urls.py",
    "./VeryControl/wsgi.py": "https://pandaoxi-project.github.io/very-control/Very_Control/VeryControl/wsgi.py",
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44",
}

def update():
    for i in updateFiles.keys():
        with open(i, "wb") as f:
            f.write(get(updateFiles[i], headers=headers).content)
        sleep(0.3)

def getIP():
    try:
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
    finally:
        sock.close()
    return ip

if __name__ == "__main__" and name == "nt":
    temp = get('https://pandaoxi-project.github.io/very-control/Very_Control/VeryControl/VERSION',headers=headers)
    temp.encoding = 'utf-8'
    latest = temp.text
    if latest != version:
        print('Please wait a moment, we are updating the software for you ...')
        update()
    system('cls')
    print(
        """                                                                         _..._       .-\'\'\'-.                                    .-\'\'\'-.          
                                                                      .-'_..._''.   '   _    \                                 '   _    \  .---. 
 .----.     .----.   __.....__                                      .' .'      '.\/   /` '.   \    _..._                     /   /` '.   \ |   | 
  \    \   /    /.-''         '.         .-.          .-           / .'          .   |     \  '  .'     '.                  .   |     \  ' |   | 
   '   '. /'   //     .-''"'-.  `. .-,.--.\ \        / /          . '            |   '      |  '.   .-.   .     .|  .-,.--. |   '      |  '|   | 
   |    |'    //     /________\   \|  .-. |\ \      / /           | |            \    \     / / |  '   '  |   .' |_ |  .-. |\    \     / / |   | 
   |    ||    ||                  || |  | | \ \    / /            | |             `.   ` ..' /  |  |   |  | .'     || |  | | `.   ` ..' /  |   | 
   '.   `'   .'\    .-------------'| |  | |  \ \  / /             . '                '-...-'`   |  |   |  |'--.  .-'| |  | |    '-...-'`   |   | 
    \        /  \    '-.____...---.| |  '-    \ `  /               \ '.          .              |  |   |  |   |  |  | |  '-                |   | 
     \      /    `.             .' | |         \  /                 '. `._____.-'/              |  |   |  |   |  |  | |                    |   | 
      '----'       `''-...... -'   | |         / /                    `-.______ /               |  |   |  |   |  '.'| |                    '---' 
                                   |_|     |`-' /                              `                |  |   |  |   |   / |_|                          
                                            '..'                                                '--'   '--'   `'-'                               \n\n"""
    )

    init(autoreset=True)
    print(
        "Welcome to Very_Control !\nControlled end:",
        Fore.RED + "http://%s:%s/\n" % (getIP(), strftime("%Y")),
    )
    system("python manage.py runserver %s:%s" % (getIP(), strftime("%Y")))
    input()
