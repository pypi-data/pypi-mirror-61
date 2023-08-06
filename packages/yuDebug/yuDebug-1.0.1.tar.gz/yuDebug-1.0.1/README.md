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