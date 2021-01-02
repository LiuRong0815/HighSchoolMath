#! /usr/bin/python

# 将 tex 文件转化为 html 文件，输出文件信息（年、月、日、前后链接、例题标签），
# 并添加适当的标签

# TODO: 修改 includegraphics
# TODO: 修改 myindex
# TODO: 修改 \qquad ??

print('This tool is located in ~/tools, and could convert well-named tex files to html files.\n')

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

#开始转换，并准备必要的数据

# 去掉日期里开头的零，列表的列表：[[year,month,day]]
fileDateTrim = []
# xxxx 年 x 月 x 日列表
fileDateName = [] 

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
    fileDateName.append(year + ' 年 ' + str(monthNum) + ' 月 ' \
        + str(dayNum) + ' 日')

# 若无合适的 tex 文件，则退出
if(len(fileDateTrim) == 0):
    print('No well-named tex files! Should be named like Year-MonthDay.tex, for example 2020-0922.tex.')
    quit()
else:
    print('Found ' + str(texFileNum) + ' tex files, converting...')

for num in range(0,texFileNum):

    fp = open(texFileNames[num]+'.html','w') # 新建 html
    lines = open(texFileNames[num]+'.tex','r').readlines()  #读入每一行

    exano = 0 # 例题个数
    # 处理 example 环境
    for oneline in lines: 
        beginexample = oneline.find('begin{example}')
        # 找到 example 环境
        if(beginexample != -1):
            exano += 1

    chapterName = fileDateTrim[num][0] + ' 年 ' \
        + fileDateTrim[num][1] + ' 月' # xxxx 年 x 月
    
    # 文件抬头信息
    fp.write('---\n' \
        + 'year: '  + fileDateTrim[num][0] + '\n' # 年
        + 'month: ' + fileDateTrim[num][1] + '\n' # 月
        + 'day: '   + fileDateTrim[num][2] + '\n' # 日
        + 'chapter: ' + chapterName + '\n' \
        + 'title: ' + fileDateName[num] + '答疑记录\n')
    
    # 上下文链接
    if(num == 0): # 第一个的上一页链接为主目录
        fp.write('prev-url: /ZHR-records\n' \
            + 'prev-name: ZHR 的答疑记录\n')
    else:
        fp.write('prev-url: ' + texFileNames[num-1] +'\n' \
            + 'prev-name: ' + fileDateName[num-1]+'\n')
    
    # 除最后一个外，均有下一页链接
    if(num < texFileNum-1): 
        fp.write('next-url: ' + texFileNames[num+1] +'\n' \
            + 'next-name: ' + fileDateName[num+1]+'\n')

    # 例题标签列表
    fp.write('sidetag:\n')
    if(exano > 0):
        for i in range(1, exano+1):
            fp.write('  - tag: exa-' + texFileNames[num] \
                + '-' + str(i) + '\n')
            fp.write('    name: 例 ' + str(i) + '\n')
    # 抬头信息结束
    fp.write('---\n')

    emptyHeadLines = 1

    # 替换其他部分
    for oneline in lines:
        
        # 匹配首行的 \section{...}，并删除该行
        if(re.search( r'\\section\{.*\}', oneline)):
            continue
    
        # 去掉接下来的空行
        if(emptyHeadLines):
            oneline = oneline.strip()  # 先去掉一行前后的空字符
            if(len(oneline) ==0):      # 如果还是空行
                continue
            else:                      # 如果非空
                emptyHeadLines = 0     # 文件开头已没有的空行
                oneline = '\n<p>' + oneline  # 补一个换行
        
        # 匹配并替换 \subsection{...} 为 h2 标题
        subsection = re.search( r'\\subsection\{(.*)\}', oneline)
        if(subsection):
            oneline = '<h2>' + subsection.group(1) + '</h2>\n'
            fp.write(oneline)
            continue
    
        # example
        oneline = oneline.replace('\\begin{example}', \
            '<a class="anchor" aria-hidden="true" id="exa-' \
            + texFileNames[num] + '-' + \
            str(exano) + '"></a>\n<myexample>\n<p>')
        oneline = oneline.replace('\\end{example}', '</p>\n</myexample>')
        
        # ~
        online = oneline.replace('~', ' ')
        
        # <
        online = oneline.replace('<', '< ')
        
        # solution
        oneline = oneline.replace('\\begin{solution}', \
            '<mysolution>\n  <p>')
        oneline = oneline.replace('\\end{solution}', '</p>\n</mysolution>')
        
        # remark
        oneline = oneline.replace('\\begin{remark}',\
            '<myremark>\n  <p>')
        oneline = oneline.replace('\\end{remark}', '</p>\n</myremark>')
        
        # align*
        oneline = oneline.replace('\\begin{align*}',\
            '\\[\\begin{aligned}')
        oneline = oneline.replace('\\end{align*}', '\\end{aligned}\]')
        
        # center
        oneline = oneline.replace('\\begin{center}', '<center>')
        oneline = oneline.replace('\\end{center}', '</center>')
        
        # figs
        figName = re.search( r'includegraphics.*\{(.*)\}', oneline)
        if(figName):
            oneline = '  <embed src="figs/' + figName.group(1) + '.svg">\n'
            fp.write(oneline)
            continue
        
        # subproblem
        oneline = oneline.replace('\\begin{subproblem}', '<mysubproblem>')
        oneline = oneline.replace('\\end{subproblem}', '</mysubproblem>')
        
        # item
        myItem = re.search( r'\\item', oneline)
        if(myItem):
            # 先替换开头的 \item，再去掉结尾的换行符
            oneline = oneline.replace('\\item', '<p>').rstrip()
            oneline += '</p>\n'  # 补上换行符
            fp.write(oneline)
            continue
        
        # index
        myIndex = re.search( r'(.*)\\myindex\{(.*)\}\{.*\}(.*)', oneline)
        if(myIndex):
            oneline = myIndex.group(1) + '<myindex>' \
                + myIndex.group(2) + '</myindex>' + myIndex.group(3) 
        
        # figs
        figName = re.search( r'includegraphics.*\{(.*)\}', oneline)
        if(figName):
            oneline = '  <embed src="figs/' + figName.group(1) + '.svg">\n'
            fp.write(oneline)
            continue
        
        # 各段加段落标签
        realLine = oneline.strip() # 删掉开头结尾的空字符
        if( 0 == len(realLine) ):
            oneline = '</p>\n\n<p>\n'
        
        # 逐行写入
        fp.write(oneline)
    fp.close()

print('finished converting ' + str(texFileNum) + ' tex files!')
