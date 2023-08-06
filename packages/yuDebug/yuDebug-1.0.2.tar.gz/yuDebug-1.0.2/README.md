# Description
To help students to upload their codes along with errors, this module comes up. Based on the work of cgitb, it provides more functionalities to simply gather the code and the errors for teachers to have a clean view on where the bug might be.
# Usage
Simply <code>import yuDebug</code>. When an error pops up, there will be guide in the console.

# 介绍
为帮助学生更好地向老师提供自己的代码特写此模块。在教学过程中，经常有学生书写的代码出现了bug，但是绝大多数情况下，学生无法完整截取代码图片，这导致了老师在解答问题时无法更好地解答，经常需要反复要求学生截全，大大降低了答疑的效率。

# 使用
只需要：
```
import yuDebug
```
模块会接管报错流，并当出现错误时，自动将源代码和报错信息整合到一个文件中，再提示学生复制该文件内容。

# 示例

当出现错误时，模块会在console里输出
> 发生异常，代码及报错已保存到./yuLog.txt
> 请双击打开文件，并复制全部内容，粘贴到qq群内寻求帮助
yuLog.txt的内容如下
```
[Author: PuluterYu]

[=====Raw Code Part=====]
    1 #coding:utf-8
    2 import yud
    3 
    4 a = 1/0
    5 b = 1/3
    6 c = 1/4
    7 b = 1/3
    8 c = 1/4
    9 d = 1/0
[=======================]


[=====Basic Part=====]
ZeroDivisionError
Python 3.7.0: C:\Users\HASEE\AppData\Local\Programs\Python\Python37\python.exe
Sun Feb 16 13:37:24 2020
[====================]


[=====Data Part=====]
a undefined
[===================]


[=====Raw Error=====]
ZeroDivisionError: division by zero

    The above is a description of an error in a Python program.  Here is
    the original traceback:

    Traceback (most recent call last):
  File ".\er.py", line 4, in <module>
    a = 1/0
ZeroDivisionError: division by zero
[===================]
```

主要包括了：
1. 全部源代码
2. 运行环境
3. 局部变量值
4. 原生报错信息