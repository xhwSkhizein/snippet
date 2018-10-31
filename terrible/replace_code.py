import re
import os
from stat import S_ISDIR
from stat import ST_MODE
from stat import S_ISREG

TARGET_PATTERN = re.compile(r'.*(get\w+)\(\"get\w+\"\)\,')

TO_REPLACE_PATTERN = re.compile(r'(CKInterface\.get\w+\.getValue\(\))')

WORK_DIR = "C:\\Users\\xuhongwei5\\workspace\\brand\\brand-service\\src\\main\\java\\com\\jd\\bpp\\ppzh\\service"

"""
正则匹配字符串并转化成特定格式
"""
def get_target_key_set():
    template_file = 'aaa.txt'
    keySet = set()
    with open(template_file, 'r', encoding='UTF-8') as fd:
        for line in fd:
            result = TARGET_PATTERN.match(line)
            if result != None:
                target = result.group(1)
                keySet.add(target)
    return {("CKInterface.%s.getValue()" % key) for key in keySet}

get_target_key_set()


"""
遍历文件目录，将目标文件(match PATTERN && has "Impl")保存到list中并返回
"""
def travel_dir(dirPath):
    target_java_file = []
    dir_list = os.listdir(dirPath)
    for file in dir_list:
        pathname = os.path.join(dirPath, file)
        mode = os.stat(pathname)[ST_MODE]
        if S_ISDIR(mode):
            travel_dir(pathname)
        elif S_ISREG(mode) and ("Impl" in pathname):
            target_java_file.append(pathname)
#         else:
#             print("skipping %s" % pathname)
    return target_java_file

"""
替换文件中符合匹配的行
"""
def replace_file_content(file):
    need_rewrite = False
    with open(file, 'r', encoding='UTF-8') as f:
        text = ""
        for line in f:
            result = TO_REPLACE_PATTERN.search(line)
            if result is not None:
                need_rewrite = True
                line = line.replace(".getValue()", "")
            text = text+line
        if need_rewrite:
            print("update %s" % file)
            with open(file, 'w', encoding='UTF-8') as f:
                f.write(text)

# 找到所有待修改文件
target_java_file = travel_dir(WORK_DIR)
print(target_java_file)
# 替换
for f in target_java_file:
    replace_file_content(f)
    #     # for test
    #     ctn = input("continue? \n")
    #     if ctn is not "y":
    #         break;
