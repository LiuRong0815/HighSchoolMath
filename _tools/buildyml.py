#! /usr/bin/python

# 输出 yml 文件

print('This tool is located in ~/tools, and could build yml data file from well-named tex files.\n')

import os,re

# tex 文件名列表
texFileNames = []

# 当前目录文件列表
fileList = os.listdir()

# 保存 tex 文件名
for files in fileList:
    
    matchFile = re.match( r'(.*)\.(.*)', files)
    # 过滤文件夹或没有后缀的文件
    if(matchFile == None):
        continue
    
    fileName = matchFile.group(1) # 文件名
    fileExt  = matchFile.group(2) # 后缀
    
    if(fileExt == 'tex'):
        texFileNames.append(fileName) # tex 文件名列表

# 排序并求长
texFileNames.sort()
texFileNum = len(texFileNames)

# 若无 tex 文件，则退出
if(texFileNum == 0):
    print("Sorry, no tex files!")
    quit()

# 开始准备必要的数据

# 去掉日期里开头的零，列表的列表：[[year,month,day]]
fileDateTrim = []

for num in range(0,texFileNum):
    fileDate = re.match( r'(\d{4})-(\d{2})(\d{2})', texFileNames[num])
    if(fileDate == None):
        continue
    year  = fileDate.group(1)
    month = fileDate.group(2)
    day   = fileDate.group(3)
    monthNum = int(month) # 去掉开头的零
    dayNum   = int(day)
    fileDateTrim.append([year,str(monthNum),str(dayNum)])  # 年、月、日

# 若无合适的 tex 文件，则退出
if(len(fileDateTrim) == 0):
    print('No well-named tex files! Should be named like Year-MonthDay.tex, for example 2020-0922.tex.')
    quit()
    
fp = open('output.yml','w')

# 输出数据表开始六行，即第一个文件信息
fp.write('- year: ' + fileDateTrim[0][0] + '\n' # 年
    +    '  months:\n'
    +    '  - month: '+ fileDateTrim[0][1] + '\n' # 月
    +    '    days:\n'
    +    '      - name: ' + fileDateTrim[0][1] + ' 月 ' \
    +                       fileDateTrim[0][2] + ' 日\n'
    +    '        link: ' + texFileNames[0] + '.html\n')

# 输出每个文件对应日期和名称
for num in range(1,texFileNum):
    # 如果当前文件与上一个文件月份不同，则添加新的月份
    if(fileDateTrim[num][1] != fileDateTrim[num-1][1]):
        fp.write('  - month: '+ fileDateTrim[num][1] + '\n' # 月
            +    '    days:\n')
    # 然后继续输出对应日期和名称
    fp.write('      - name: ' + fileDateTrim[num][1] + ' 月 ' \
        + fileDateTrim[num][2] + ' 日\n' \
        +    '        link: ' + texFileNames[num] + '.html\n')

fp.close()

print('finished building output.yml!')
