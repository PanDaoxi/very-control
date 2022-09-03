@echo off
title Install Packages

echo Installing Django...
pip install django -i http://mirrors.aliyun.com/pypi/simple >nul

echo Installing Easygui...
pip install easygui -i http://mirrors.aliyun.com/pypi/simple >nul

echo Installing Requests... 
pip install requests -i http://mirrors.aliyun.com/pypi/simple >nul

echo Installing Colorama...
pip install colorama -i http://mirrors.aliyun.com/pypi/simple >nul

echo Installing PyautoGUI...
pip install pyautogui -i http://mirrors.aliyun.com/pypi/simple >nul

echo Installing OpenCV-Python...
pip install pyautogui -i http://mirrors.aliyun.com/pypi/simple >nul

echo Installing PyTTSx3...
pip install pyttsx3 -i http://mirrors.aliyun.com/pypi/simple >nul

echo All Right.
pause