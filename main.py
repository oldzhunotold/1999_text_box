#日志
#新增：1999角色
#变动：1999背景
#重大变动：从快捷键变为窗口
#把角色文件夹全放进character文件夹里
#添加监视@功能
#特殊功能

print("""
快捷键说明:
Enter: 生成图片
Esc: 退出程序
Ctrl+Shift+S: 显示/隐藏角色选择窗口

窗口界面操作说明:
双击列表中的角色名称可以切换角色
点击"切换角色"按钮确认选择
点击"刷新列表"可以重新加载角色列表
当前选中的角色会高亮显示
窗口可以一直保持打开，随时切换角色

程序说明：
这个版本的程序占用体积较小，但是需要预加载，初次更换角色后需要等待数秒才能正常使用，望周知（
按ctrl+Tab可清除生成图片，降低占用空间，但清除图片后需重启才能正常使用
默认是菲林士多（我是导演厨咋地）
感谢各位的支持

改动说明：
默认启用窗口白名单，只在微信和QQ等聊天窗口前台时才响应热键，避免误触发
更改了背景图，和新加几个角色
添加了图形界面选择角色功能，窗口可一直保持打开
"""
      )

# 角色配置
current_character_index = 1  # 初始角色为菲林士多（索引从1开始）

mahoshojo_postion = [728, 355]  # 文本范围起始位置
mahoshojo_over = [2339, 800]  # 文本范围右下角位置
# 用户选择的特定皮肤，格式为 {角色名: 皮肤编号}
user_selected_skins = {}


# 特殊功能开关
special_feature_enabled = False
SPECIAL_CHARACTER = "john_titor"  # 触发十六进制功能的角色
DOG_BARK_CHARACTER = "pickles"    # 触发狗叫功能的角色
# 检查@字符功能开关
check_at_enabled = False  # 默认关闭，避免影响现有功能
def convert_to_hex_with_original(text):
    """将文本转换为十六进制编码，并在下面显示原始文本"""
    try:
        if not text or text.strip() == "":
            return text

        # 将文本转换为十六进制，每个字符用空格分隔
        hex_text = ''.join([hex(ord(c))[2:].upper().zfill(2) for c in text])
        # 添加黄色标记的原始文本
        # 使用特殊格式标记黄色文本：<yellow>原始文本</yellow>
        result = f"{hex_text}\n（{text}）"
        return result
    except Exception as e:
        print(f"转换为十六进制时出错: {e}")
        return text


def convert_to_dog_bark(text):
    """将文本转换为有规律的狗叫"""
    try:
        if not text or text.strip() == "":
            return text

        # 定义狗叫模式：交替使用"汪"和"吠"
        result_lines = []
        bark_patterns = ["汪", "吠", "汪汪", "吠吠", "汪～", "吠～"]

        # 根据文本长度生成狗叫
        words = text.split()
        for i, word in enumerate(words):
            # 根据单词长度选择狗叫模式
            bark_count = min(len(word), 20)
            if bark_count == 0:
                continue

            # 选择模式
            pattern_index = i % len(bark_patterns)
            base_bark = bark_patterns[pattern_index]

            # 生成狗叫
            bark_line = base_bark * bark_count
            if i < len(words) - 1:
                bark_line += "，"
            result_lines.append(bark_line)

        # 合并狗叫
        bark_text = "".join(result_lines)

        # 添加原文在括号中
        result = f"{bark_text}\n（{text}）"
        return result
    except Exception as e:
        print(f"转换为狗叫时出错: {e}")
        return text
import sys
import random
import time
import keyboard
import pyperclip
import io
from PIL import Image, ImageTk
import win32clipboard
import os
import re
import shutil
import threading
import win32gui
import win32process
import psutil
import tkinter as tk
from tkinter import ttk, messagebox
from text_fit_draw import draw_text_auto
from image_fit_paste import paste_image_auto


# ===== PyInstaller 资源路径处理函数 =====
def get_resource_path(relative_path):
    """获取资源文件的绝对路径，兼容开发环境和打包后的环境"""
    try:
        # PyInstaller 创建临时文件夹，路径存储在 _MEIPASS 中
        base_path = sys._MEIPASS
    except AttributeError:
        # 开发环境中使用当前文件所在目录
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)


i = -1
value_1 = -1
expression = None

# 前台窗口白名单
windowwhitelist = ["TIM.exe", "WeChat.exe", "Weixin.exe", "WeChatApp.exe", "QQ.exe", "WhatsApp.exe", "discord.exe"]
enablewhitelist = True
# 角色配置字典
character = {

    "noire": {"emotion_count": 4, "font": "font3.ttf"},
    "recoleta": {"emotion_count": 4, "font": "font3.ttf"},
    "vertin": {"emotion_count": 4, "font": "font3.ttf"},
    "sentinel": {"emotion_count": 4, "font": "font3.ttf"},
    "brume": {"emotion_count": 2, "font": "font3.ttf"},
    "isolde": {"emotion_count": 5, "font": "font3.ttf"},
    "kakania": {"emotion_count": 5, "font": "font3.ttf"},
    "melania": {"emotion_count": 5, "font": "font3.ttf"},
    "nautika": {"emotion_count": 3, "font": "font3.ttf"},
    "liang": {"emotion_count": 4, "font": "font3.ttf"},
    "flutterpage": {"emotion_count": 3, "font": "font3.ttf"},
    "regulus": {"emotion_count": 6, "font": "font3.ttf"},
    "moldir": {"emotion_count": 4, "font": "font3.ttf"},
    "thirty-seven": {"emotion_count": 5, "font": "font3.ttf"},
    "six": {"emotion_count": 7, "font": "font3.ttf"},
    "a_knight": {"emotion_count": 4, "font": "font3.ttf"},
    "sotheby": {"emotion_count": 7, "font": "font3.ttf"},
    "charon": {"emotion_count": 3, "font": "font3.ttf"},
    "APPLe": {"emotion_count": 5, "font": "font3.ttf"},
    "marcus": {"emotion_count": 4, "font": "font3.ttf"},
    "aleph": {"emotion_count": 4, "font": "font3.ttf"},
    "sonetto": {"emotion_count": 8, "font": "font3.ttf"},
    "hofmann": {"emotion_count": 1, "font": "font3.ttf"},
    "rubuska": {"emotion_count": 5, "font": "font3.ttf"},
    "corvus": {"emotion_count": 3, "font": "font3.ttf"},
    "mesmer_jr.": {"emotion_count": 3, "font": "font3.ttf"},
    "jiu_niangzi": {"emotion_count": 4, "font": "font3.ttf"},
    "sophia": {"emotion_count": 2, "font": "font3.ttf"},
    "210": {"emotion_count": 2, "font": "font3.ttf"},
    "door": {"emotion_count": 1, "font": "font3.ttf"},
    "bunny_bunny": {"emotion_count": 3, "font": "font3.ttf"},
    "matilda": {"emotion_count": 6, "font": "font3.ttf"},
    "eagle": {"emotion_count": 4, "font": "font3.ttf"},
    "argus": {"emotion_count": 3, "font": "font3.ttf"},
    "mr.duncan": {"emotion_count": 3, "font": "font3.ttf"},
    "dikke": {"emotion_count": 3, "font": "font3.ttf"},
    "tooth_fairy": {"emotion_count": 5, "font": "font3.ttf"},
    "windsong": {"emotion_count": 5, "font": "font3.ttf"},
    "cristallo": {"emotion_count": 3, "font": "font3.ttf"},
    "barcarola": {"emotion_count": 4, "font": "font3.ttf"},
    "fatutu": {"emotion_count": 3, "font": "font3.ttf"},
    "kiperina": {"emotion_count": 3, "font": "font3.ttf"},
    "voyager": {"emotion_count": 4, "font": "font3.ttf"},
    "williow": {"emotion_count": 6, "font": "font3.ttf"},
    "druvis_III": {"emotion_count": 6, "font": "font3.ttf"},
    "spathodea": {"emotion_count": 6, "font": "font3.ttf"},
    "lopera": {"emotion_count": 3, "font": "font3.ttf"},
    "beryl": {"emotion_count": 2, "font": "font3.ttf"},
    "eternity": {"emotion_count": 4, "font": "font3.ttf"},
    "pickles": {"emotion_count": 3, "font": "font3.ttf"},
    "ezio": {"emotion_count": 2, "font": "font3.ttf"},
    "changeling": {"emotion_count": 6, "font": "font3.ttf"},
    "bkornblume": {"emotion_count": 3, "font": "font3.ttf"},
    "anjo_nala": {"emotion_count": 5, "font": "font3.ttf"},
    "oliver_fog": {"emotion_count": 3, "font": "font3.ttf"},
    "anan_lee": {"emotion_count": 4, "font": "font3.ttf"},
    "hissabeth": {"emotion_count": 3, "font": "font3.ttf"},
    "getian": {"emotion_count": 3, "font": "font3.ttf"},
    "schneider": {"emotion_count": 1, "font": "font3.ttf"},
    "arcana": {"emotion_count": 2, "font": "font3.ttf"},
    "joe": {"emotion_count": 4, "font": "font3.ttf"},
    "the_fool": {"emotion_count": 2, "font": "font3.ttf"},
    "enigma": {"emotion_count": 1, "font": "font3.ttf"},
    "ulrich": {"emotion_count": 4, "font": "font3.ttf"},
    "villa": {"emotion_count": 4, "font": "font3.ttf"},
    "shamane": {"emotion_count": 5, "font": "font3.ttf"},
    "kassandra": {"emotion_count": 2, "font": "font3.ttf"},
    "mercuria": {"emotion_count": 4, "font": "font3.ttf"},
    "felician": {"emotion_count": 1, "font": "font3.ttf"},
    "ms.radio": {"emotion_count": 2, "font": "font3.ttf"},
    "twins_sleep": {"emotion_count": 2, "font": "font3.ttf"},
    "medicine_pocket": {"emotion_count": 4, "font": "font3.ttf"},
    "x": {"emotion_count": 3, "font": "font3.ttf"},
    "yenisei_jr.": {"emotion_count": 3, "font": "font3.ttf"},
    "baby_blue": {"emotion_count": 3, "font": "font3.ttf"},
    "tuesday": {"emotion_count": 5, "font": "font3.ttf"},
    "centurion": {"emotion_count": 3, "font": "font3.ttf"},
    "ezra_theodore": {"emotion_count": 4, "font": "font3.ttf"},
    "black_dwarf": {"emotion_count": 6, "font": "font3.ttf"},
    "igor": {"emotion_count": 2, "font": "font3.ttf"},
    "aima": {"emotion_count": 2, "font": "font3.ttf"},
    "balloon_party": {"emotion_count": 3, "font": "font3.ttf"},
    "la_source": {"emotion_count": 2, "font": "font3.ttf"},
    "horropedia": {"emotion_count": 3, "font": "font3.ttf"},
    "marsha": {"emotion_count": 3, "font": "font3.ttf"},
    "charlie": {"emotion_count": 3, "font": "font3.ttf"},
    "forget_me_not": {"emotion_count": 1, "font": "font3.ttf"},
    "creius": {"emotion_count": 1, "font": "font3.ttf"},
    "black_ibis": {"emotion_count": 1, "font": "font3.ttf"},
    "semmelweis": {"emotion_count": 6, "font": "font3.ttf"},
    "qixing": {"emotion_count": 2, "font": "font3.ttf"},
    "poitier": {"emotion_count": 1, "font": "font3.ttf"},
    "name_day": {"emotion_count": 3, "font": "font3.ttf"},
    "valentina": {"emotion_count": 1, "font": "font3.ttf"},
    "pyrrhos": {"emotion_count": 1, "font": "font3.ttf"},
    "john_titor": {"emotion_count": 2, "font": "font3.ttf"},
    "coppelia": {"emotion_count": 1, "font": "font3.ttf"},
    "xu_niangzi": {"emotion_count": 1, "font": "font3.ttf"},
    "urd": {"emotion_count": 4, "font": "font3.ttf"},
    "lucy": {"emotion_count": 4, "font": "font3.ttf"},
    "caroline": {"emotion_count": 2, "font": "font3.ttf"},
    "hunting": {"emotion_count": 1, "font": "font3.ttf"},
    "katz": {"emotion_count": 1, "font": "font3.ttf"},
    "z": {"emotion_count": 1, "font": "font3.ttf"},
    "marian": {"emotion_count": 1, "font": "font3.ttf"},
    "merel": {"emotion_count": 2, "font": "font3.ttf"},
    "octavia": {"emotion_count": 1, "font": "font3.ttf"},
    "77": {"emotion_count": 1, "font": "font3.ttf"},
    "jailer": {"emotion_count": 1, "font": "font3.ttf"},
    "garcía": {"emotion_count": 1, "font": "font3.ttf"},
    "roberta": {"emotion_count": 1, "font": "font3.ttf"},
    "888": {"emotion_count": 1, "font": "font3.ttf"},
    "ring": {"emotion_count": 1, "font": "font3.ttf"},
    "lilya": {"emotion_count": 6, "font": "font3.ttf"},
    "ms.newBabel": {"emotion_count": 3, "font": "font3.ttf"},
    "charlton": {"emotion_count": 1, "font": "font3.ttf"},
    "frey": {"emotion_count": 1, "font": "font3.ttf"},
    "prismagreen": {"emotion_count": 1, "font": "font3.ttf"},
    "pointer": {"emotion_count": 1, "font": "font3.ttf"},
    "alexios": {"emotion_count": 2, "font": "font3.ttf"},
    "verity": {"emotion_count": 1, "font": "font3.ttf"},
    "lorelei": {"emotion_count": 2, "font": "font3.ttf"},
    "buddy_fairchild": {"emotion_count": 2, "font": "font3.ttf"},
    "ONiON": {"emotion_count": 1, "font": "font3.ttf"},
    "loggerhead": {"emotion_count": 2, "font": "font3.ttf"},
    "brimley": {"emotion_count": 3, "font": "font3.ttf"},
    "barbara": {"emotion_count": 2, "font": "font3.ttf"},
    "afsivi": {"emotion_count": 2, "font": "font3.ttf"},
    "ulu": {"emotion_count": 2, "font": "font3.ttf"},
    "desert_flannel": {"emotion_count": 3, "font": "font3.ttf"},
    "kanjira": {"emotion_count": 3, "font": "font3.ttf"},
    "diggers": {"emotion_count": 3, "font": "font3.ttf"},
    "blonney": {"emotion_count": 4, "font": "font3.ttf"},
    "paper_heron": {"emotion_count": 2, "font": "font3.ttf"},
    "cheng_heguang": {"emotion_count": 2, "font": "font3.ttf"},
    "huigu": {"emotion_count": 1, "font": "font3.ttf"},
}

# 角色文字配置字典 - 每个角色对应4个文字配置
text_configs_dict = {
    "noire": [  # 菲林士多
        {"text": "菲", "position": (759, 73), "font_color": (182, 62, 31), "font_size": 186},
        {"text": "林", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "士", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "多", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Noire", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "recoleta": [  # 虚构集
        {"text": "虚", "position": (759, 73), "font_color": (54, 97, 81), "font_size": 186},
        {"text": "构", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "集", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (0, 0), "font_color": (255, 255, 255), "font_size": 1},
        {"text": "/Recoleta", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "vertin": [  # 维尔汀
        {"text": "维", "position": (759, 73), "font_color": (134, 157, 167), "font_size": 186},
        {"text": "尔", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "汀", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (0, 0), "font_color": (255, 255, 255), "font_size": 1},
        {"text": "/Vertin", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "sentinel": [  # 玛丽安娜
        {"text": "玛", "position": (759, 73), "font_color": (211, 202, 203), "font_size": 186},
        {"text": "丽", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "安", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "娜", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Sentinel", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "brume": [  # 灰调蓝
        {"text": "灰", "position": (759, 73), "font_color": (66, 137, 186), "font_size": 186},
        {"text": "调", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "蓝", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (0, 0), "font_color": (255, 255, 255), "font_size": 1},
        {"text": "/Brume", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "isolde": [  # 伊索尔德
        {"text": "伊", "position": (759, 73), "font_color": (69, 52, 112), "font_size": 186},
        {"text": "索", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "尔", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "德", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Isolde", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "kakania": [  # 卡卡尼亚
        {"text": "卡", "position": (759, 73), "font_color": (95, 147, 136), "font_size": 186},
        {"text": "卡", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "尼", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "亚", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Kakania", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "melania": [  # 梅兰妮
        {"text": "梅", "position": (759, 73), "font_color": (100, 8, 13), "font_size": 186},
        {"text": "兰", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "妮", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (0, 0), "font_color": (255, 255, 255), "font_size": 1},
        {"text": "/Melania", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "nautika": [  # 诺谛卡
        {"text": "诺", "position": (759, 73), "font_color": (240, 195, 176), "font_size": 186},
        {"text": "谛", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "卡", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (0, 0), "font_color": (255, 255, 255), "font_size": 1},
        {"text": "/Mautika", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "liang": [  # 梁月
        {"text": "梁", "position": (759, 73), "font_color": (96, 105, 95), "font_size": 186},
        {"text": "月", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "", "position": (0, 0), "font_color": (255, 255, 255), "font_size": 1},
        {"text": "", "position": (0, 0), "font_color": (255, 255, 255), "font_size": 1},
        {"text": "/Liang", "position": (1030, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "flutterpage": [  # 纸信圈儿
        {"text": "纸", "position": (759, 73), "font_color": (31, 88, 115), "font_size": 186},
        {"text": "信", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "圈", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "儿", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Flutterpage", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "regulus": [  # 星锑
        {"text": "星", "position": (759, 73), "font_color": (142, 39, 21), "font_size": 186},
        {"text": "锑", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "", "position": (0, 0), "font_color": (255, 255, 255), "font_size": 1},
        {"text": "", "position": (0, 0), "font_color": (255, 255, 255), "font_size": 1},
        {"text": "/Regulus", "position": (1030, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "moldir": [  # 莫莉德尔
        {"text": "莫", "position": (759, 73), "font_color": (64, 45, 35), "font_size": 186},
        {"text": "莉", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "德", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "尔", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Moldir", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "thirty-seven": [  # 37
        {"text": "37", "position": (759, 73), "font_color": (124, 158, 168), "font_size": 186},
        {"text": "", "position": (0, 0), "font_color": (255, 255, 255), "font_size": 1},
        {"text": "", "position": (0, 0), "font_color": (255, 255, 255), "font_size": 1},
        {"text": "", "position": (0, 0), "font_color": (255, 255, 255), "font_size": 1},
        {"text": "/Thirty-seven", "position": (990, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "six": [  # 6
        {"text": "6", "position": (759, 73), "font_color": (192, 184, 149), "font_size": 186},
        {"text": "", "position": (0, 0), "font_color": (255, 255, 255), "font_size": 1},
        {"text": "", "position": (0, 0), "font_color": (255, 255, 255), "font_size": 1},
        {"text": "", "position": (0, 0), "font_color": (255, 255, 255), "font_size": 1},
        {"text": "/Six", "position": (890, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "a_knight": [  # 未锈铠
        {"text": "未", "position": (759, 73), "font_color": (82, 74, 66), "font_size": 186},
        {"text": "锈", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "铠", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (0, 0), "font_color": (255, 255, 255), "font_size": 1},
        {"text": "/A knight", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "sotheby": [  # 苏芙比
        {"text": "苏", "position": (759, 73), "font_color": (236, 228, 191), "font_size": 186},
        {"text": "芙", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "比", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (0, 0), "font_color": (255, 255, 255), "font_size": 1},
        {"text": "/Sotheby", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "charon": [  # 卡戎
        {"text": "卡", "position": (759, 73), "font_color": (164, 169, 163), "font_size": 186},
        {"text": "戎", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "", "position": (0, 0), "font_color": (255, 255, 255), "font_size": 1},
        {"text": "", "position": (0, 0), "font_color": (255, 255, 255), "font_size": 1},
        {"text": "/Charon", "position": (1030, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "APPLe": [  # APPLe
        {"text": "APPLe", "position": (759, 73), "font_color": (192, 41, 40), "font_size": 186},
        {"text": "", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "", "position": (0, 0), "font_color": (255, 255, 255), "font_size": 1},
        {"text": "", "position": (0, 0), "font_color": (255, 255, 255), "font_size": 1},
        {"text": "/APPLe", "position": (1300, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "marcus": [  # 马库斯
        {"text": "马", "position": (759, 73), "font_color": (236, 228, 191), "font_size": 186},
        {"text": "库", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "斯", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (0, 0), "font_color": (255, 255, 255), "font_size": 1},
        {"text": "/Marcus", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "aleph": [  # 阿莱夫
        {"text": "阿", "position": (759, 73), "font_color": (192, 41, 40), "font_size": 186},
        {"text": "莱", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "夫", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (0, 0), "font_color": (255, 255, 255), "font_size": 1},
        {"text": "/Aleph", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "sonetto": [  # 十四行诗
        {"text": "十", "position": (759, 73), "font_color": (198, 96, 53), "font_size": 186},
        {"text": "四", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "行", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "诗", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Sonetto", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "hofmann": [  # 霍夫曼
        {"text": "霍", "position": (759, 73), "font_color": (162, 152, 141), "font_size": 186},
        {"text": "夫", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "曼", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "Hofmann", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "rubuska": [  # 野树莓
        {"text": "野", "position": (759, 73), "font_color": (136, 2, 2), "font_size": 186},
        {"text": "树", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "莓", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Rubuska", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "corvus": [  # 告死鸟
        {"text": "告", "position": (759, 73), "font_color": (151, 152, 118), "font_size": 186},
        {"text": "死", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "鸟", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Corvus", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "mesmer_jr.": [  # 小梅斯梅尔
        {"text": "小", "position": (759, 73), "font_color": (112, 67, 66), "font_size": 186},
        {"text": "梅", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "斯", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "梅尔", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Mesmer Jr.", "position": (1350, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "jiu_niangzi": [  # 曲娘
        {"text": "曲", "position": (759, 73), "font_color": (91, 123, 100), "font_size": 186},
        {"text": "娘", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Jiu Niangzi", "position": (1030, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "sophia": [  # 苏菲亚
        {"text": "苏", "position": (759, 73), "font_color": (208, 50, 46), "font_size": 186},
        {"text": "菲", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "亚", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Sophia", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "210": [  # 210
        {"text": "210", "position": (759, 73), "font_color": (93, 63, 210), "font_size": 186},
        {"text": "", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
    ],
    "door": [  # 门
        {"text": "门", "position": (759, 73), "font_color": (255, 255, 255), "font_size": 186},
        {"text": "", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Door", "position": (990, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "bunny_bunny": [  # 芭妮芭妮
        {"text": "芭", "position": (759, 73), "font_color": (252, 225, 173), "font_size": 186},
        {"text": "妮", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "芭", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "妮", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Bunny Bunny", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "matilda": [  # 玛蒂尔达
        {"text": "玛", "position": (759, 73), "font_color": (252, 225, 173), "font_size": 186},
        {"text": "蒂", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "尔", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "达", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Matilda", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "eagle": [  # 小春雀儿
        {"text": "小", "position": (759, 73), "font_color": (71, 84, 86), "font_size": 186},
        {"text": "春", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "雀", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "儿", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Eagle", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "argus": [  # 阿尔古斯
        {"text": "阿", "position": (759, 73), "font_color": (53, 153, 120), "font_size": 186},
        {"text": "尔", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "古", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "斯", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Argus", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "mr.duncan": [  # 邓肯先生
        {"text": "邓", "position": (759, 73), "font_color": (171, 152, 67), "font_size": 186},
        {"text": "肯", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "先", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "生", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Mr.Duncan", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "dikke": [  # 帕米埃
        {"text": "帕", "position": (759, 73), "font_color": (191, 76, 59), "font_size": 186},
        {"text": "米", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "埃", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Dikke", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "tooth_fairy": [  # 牙仙
        {"text": "牙", "position": (759, 73), "font_color": (203, 156, 77), "font_size": 186},
        {"text": "仙", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Tooth Fairy", "position": (1030, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "windsong": [  # 北方哨歌
        {"text": "北", "position": (759, 73), "font_color": (54, 95, 120), "font_size": 186},
        {"text": "方", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "哨", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "歌", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Windsong", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "cristallo": [  # 铅玻璃
        {"text": "铅", "position": (759, 73), "font_color": (64, 97, 88), "font_size": 186},
        {"text": "玻", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "璃", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Cristallo", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "barcarola": [  # 芭卡洛儿
        {"text": "芭", "position": (759, 73), "font_color": (85, 183, 219), "font_size": 186},
        {"text": "卡", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "洛", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "儿", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Barcarola", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "fatutu": [  # 图图石子
        {"text": "图", "position": (759, 73), "font_color": (130, 172, 28), "font_size": 186},
        {"text": "图", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "石", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "子", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Fatutu", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "kiperina": [  # 库珀花环
        {"text": "库", "position": (759, 73), "font_color": (201, 51, 102), "font_size": 186},
        {"text": "珀", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "花", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "环", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Kiperina", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "voyager": [  # 远旅
        {"text": "远", "position": (759, 73), "font_color": (102, 101, 164), "font_size": 186},
        {"text": "旅", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Voyager", "position": (1030, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "williow": [  # 笃笃骨
        {"text": "笃", "position": (759, 73), "font_color": (102, 101, 164), "font_size": 186},
        {"text": "笃", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "骨", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Williow", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "druvis_III": [  # 槲寄生
        {"text": "槲", "position": (759, 73), "font_color": (60, 185, 150), "font_size": 186},
        {"text": "寄", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "生", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Druvis III", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "spathodea": [  # 可燃点
        {"text": "可", "position": (759, 73), "font_color": (223, 96, 105), "font_size": 186},
        {"text": "燃", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "点", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Spathodea", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "lopera": [  # 洛佩拉
        {"text": "洛", "position": (759, 73), "font_color": (255, 64, 0), "font_size": 186},
        {"text": "佩", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "拉", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Lopera", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "beryl": [  # 贝丽尔
        {"text": "贝", "position": (759, 73), "font_color": (96, 177, 252), "font_size": 186},
        {"text": "丽", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "尔", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Beryl", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "eternity": [  # 温妮弗雷德
        {"text": "温", "position": (759, 73), "font_color": (96, 177, 252), "font_size": 186},
        {"text": "妮", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "弗", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "雷德", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Eternity", "position": (1390, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "pickles": [  # 皮克勒斯
        {"text": "皮", "position": (759, 73), "font_color": (78, 103, 237), "font_size": 186},
        {"text": "克", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "勒", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "斯", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Pickles", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "ezio": [  # 艾吉奥
        {"text": "艾", "position": (759, 73), "font_color": (158, 116, 105), "font_size": 186},
        {"text": "吉", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "奥", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Ezio Auditore", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "changeling": [  # 洁西卡
        {"text": "洁", "position": (759, 73), "font_color": (52, 77, 140), "font_size": 186},
        {"text": "西", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "卡", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Changeling", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "bkornblume": [  # 柏林以东
        {"text": "柏", "position": (759, 73), "font_color": (62, 72, 140), "font_size": 186},
        {"text": "林", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "以", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "东", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Bkornblume", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "anjo_nala": [  # 天使娜娜
        {"text": "天", "position": (759, 73), "font_color": (195, 84, 158), "font_size": 186},
        {"text": "使", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "娜", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "娜", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Anjo Nala", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "oliver_fog": [  # 雾行者
        {"text": "雾", "position": (759, 73), "font_color": (34, 0, 97), "font_size": 186},
        {"text": "行", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "者", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Oliver Fog", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "anan_lee": [  # 泥鯭的士
        {"text": "泥", "position": (759, 73), "font_color": (190, 219, 105), "font_size": 186},
        {"text": "鯭", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "的", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "士", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/An-an Lee", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "hissabeth": [  # 冷周六
        {"text": "冷", "position": (759, 73), "font_color": (113, 197, 247), "font_size": 186},
        {"text": "周", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "六", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Hissabeth", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "getian": [  # 葛天
        {"text": "葛", "position": (759, 73), "font_color": (207, 159, 107), "font_size": 186},
        {"text": "天", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Getian", "position": (1030, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "schneider": [  # 斯奈德
        {"text": "斯", "position": (759, 73), "font_color": (215, 86, 77), "font_size": 186},
        {"text": "奈", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "德", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Schneider", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "arcana": [  # 阿尔卡纳
        {"text": "阿", "position": (759, 73), "font_color": (36, 32, 166), "font_size": 186},
        {"text": "尔", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "卡", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "纳", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Arcana", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "joe": [  # j
        {"text": "J", "position": (759, 73), "font_color": (200, 84, 84), "font_size": 186},
        {"text": "", "position": (0, 0), "font_color": (255, 255, 255), "font_size": 1},
        {"text": "", "position": (0, 0), "font_color": (255, 255, 255), "font_size": 1},
        {"text": "", "position": (0, 0), "font_color": (255, 255, 255), "font_size": 1},
        {"text": "/Joe", "position": (990, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "the_fool": [  # 弄臣
        {"text": "弄", "position": (759, 73), "font_color": (68, 36, 104), "font_size": 186},
        {"text": "臣", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/The Fool", "position": (1030, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "enigma": [  # 哑谜
        {"text": "哑", "position": (759, 73), "font_color": (96, 84, 76), "font_size": 186},
        {"text": "谜", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Enigma(Adler Hofmann)", "position": (1030, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "ulrich": [  # 乌尔里希
        {"text": "乌", "position": (759, 73), "font_color": (161, 137, 71), "font_size": 186},
        {"text": "尔", "position": (945, 175), "font_color": (255, 255, 255), "": 92},
        {"text": "里", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "希", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Ulrich", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69}
    ],
    "villa": [  # 维拉
        {"text": "维", "position": (759, 73), "font_color": (117, 208, 241), "font_size": 186},
        {"text": "拉", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Вила", "position": (1030, 225), "font_color": (104, 97, 92), "font_size": 69},

    ],
    "shamane": [  # 鬃毛沙砾
        {"text": "鬃", "position": (759, 73), "font_color": (223, 192, 149), "font_size": 186},
        {"text": "毛", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "沙", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "砾", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Shamane", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "kassandra": [  # 卡珊德拉
        {"text": "卡", "position": (759, 73), "font_color": (122, 71, 3), "font_size": 186},
        {"text": "珊", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "德", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "拉", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Kassandra", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "mercuria": [  # 环状水星
        {"text": "环", "position": (759, 73), "font_color": (211, 251, 255), "font_size": 186},
        {"text": "状", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "水", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "星", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Mercuria", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "felician": [  # 费利西安
        {"text": "费", "position": (759, 73), "font_color": (156, 98, 156), "font_size": 186},
        {"text": "利", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "西", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "安", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Felician", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "ms.radio": [  # 无线电小姐
        {"text": "无", "position": (759, 73), "font_color": (93, 197, 142), "font_size": 186},
        {"text": "线", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "电", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "小姐", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Ms.Radio", "position": (1390, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "twins_sleep": [  # 丽莎&路易斯
        {"text": "丽", "position": (759, 73), "font_color": (244, 180, 102), "font_size": 186},
        {"text": "莎&", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "路", "position": (1105, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "易斯", "position": (1246, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Twins Sleep", "position": (1420, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "medicine_pocket": [  # 兔毛手袋
        {"text": "兔", "position": (759, 73), "font_color": (113, 165, 105), "font_size": 186},
        {"text": "毛", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "手", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "袋", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Medicine Pocket", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "x": [  # X
        {"text": "X", "position": (759, 73), "font_color": (99, 133, 150), "font_size": 186},
        {"text": "", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/X", "position": (930, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "yenisei_jr.": [  # 小叶尼塞
        {"text": "小", "position": (759, 73), "font_color": (105, 169, 186), "font_size": 186},
        {"text": "叶", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "尼", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "塞", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Енисей", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "baby_blue": [  # 婴儿蓝
        {"text": "婴", "position": (759, 73), "font_color": (130, 217, 255), "font_size": 186},
        {"text": "儿", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "蓝", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Baby Blue", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "tuesday": [  # 蓝手帕
        {"text": "蓝", "position": (759, 73), "font_color": (198, 16, 93), "font_size": 186},
        {"text": "手", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "帕", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Tuesday", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "centurion": [  # 百夫长
        {"text": "百", "position": (759, 73), "font_color": (237, 203, 136), "font_size": 186},
        {"text": "夫", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "长", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Centurion", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "ezra_theodore": [  # 爱兹拉
        {"text": "爱", "position": (759, 73), "font_color": (237, 203, 136), "font_size": 186},
        {"text": "兹", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "拉", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Ezra Theodore", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "black_dwarf": [  # 伽菈波那
        {"text": "伽", "position": (759, 73), "font_color": (237, 203, 136), "font_size": 186},
        {"text": "菈", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "波", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "那", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Black Dwarf", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "igor": [  # 伊戈尔
        {"text": "伊", "position": (759, 73), "font_color": (141, 141, 141), "font_size": 186},
        {"text": "戈", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "尔", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Igor", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "aima": [  # 艾玛
        {"text": "艾", "position": (759, 73), "font_color": (46, 82, 84), "font_size": 186},
        {"text": "玛", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Aima", "position": (1030, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "balloon_party": [  # 气球派对
        {"text": "气", "position": (759, 73), "font_color": (203, 95, 137), "font_size": 186},
        {"text": "球", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "派", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "对", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Balloon Party", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "balloon_party": [  # 气球派对
        {"text": "气", "position": (759, 73), "font_color": (203, 95, 137), "font_size": 186},
        {"text": "球", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "派", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "对", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Balloon Party", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "la_source": [  # 拉拉泉
        {"text": "拉", "position": (759, 73), "font_color": (207, 173, 142), "font_size": 186},
        {"text": "拉", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "泉", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/La source", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "horropedia": [  # 恐怖通
        {"text": "恐", "position": (759, 73), "font_color": (207, 173, 142), "font_size": 186},
        {"text": "怖", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "通", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Horropedia", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "marsha": [  # 玛尔莎
        {"text": "玛", "position": (759, 73), "font_color": (191, 72, 76), "font_size": 186},
        {"text": "尔", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "莎", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Marsha", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "charlie": [  # 夏利
        {"text": "夏", "position": (759, 73), "font_color": (73, 40, 136), "font_size": 186},
        {"text": "利", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Charlie", "position": (1030, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "forget_me_not": [  # 勿忘我
        {"text": "勿", "position": (759, 73), "font_color": (76, 86, 85), "font_size": 186},
        {"text": "忘", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "我", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Forget Me Not", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "creius": [  # 刻雷乌斯
        {"text": "刻", "position": (759, 73), "font_color": (176, 74, 47), "font_size": 186},
        {"text": "雷", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "乌", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "斯", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Creius", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "black_ibis": [  # 黑鹮
        {"text": "黑", "position": (759, 73), "font_color": (40, 40, 37), "font_size": 186},
        {"text": "鹮", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Black Ibis", "position": (1030, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "semmelweis": [  # 塞梅尔维斯
        {"text": "塞", "position": (759, 73), "font_color": (87,50,136), "font_size": 186},
        {"text": "梅", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "尔", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "维斯", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Semmelweis", "position": (1390, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "qixing": [  # 奇星
        {"text": "奇", "position": (759, 73), "font_color": (222, 180, 166), "font_size": 186},
        {"text": "星", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Qi Xing", "position": (1030, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "poitier": [  # 波蒂埃
        {"text": "波", "position": (759, 73), "font_color": (56, 76, 117), "font_size": 186},
        {"text": "蒂", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "埃", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Poitier", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "name_day": [  # 命名日
        {"text": "命", "position": (759, 73), "font_color": (125, 161, 130), "font_size": 186},
        {"text": "名", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "日", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Name Day", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "valentina": [  # 瓦伦缇娜
        {"text": "瓦", "position": (759, 73), "font_color": (153, 122, 122), "font_size": 186},
        {"text": "伦", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "缇", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "娜", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Valentina", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "pyrrhos": [  # 鲍里斯
        {"text": "鲍", "position": (759, 73), "font_color": (193, 170, 158), "font_size": 186},
        {"text": "里", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "斯", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Pyrrhos", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "john_titor": [  # 约翰·提托
        {"text": "约", "position": (759, 73), "font_color": (119, 187, 119), "font_size": 186},
        {"text": "翰·", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "提", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "托", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/John Titor", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "coppelia": [  # 珐琅眼
        {"text": "珐", "position": (759, 73), "font_color": (30, 67, 190), "font_size": 186},
        {"text": "琅", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "眼", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Coppelia", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "xu_niangzi": [  # 许娘子
        {"text": "许", "position": (759, 73), "font_color": (215, 159, 56), "font_size": 186},
        {"text": "娘", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "子", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Xu Niangzi", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "urd": [  # 兀尔德
        {"text": "兀", "position": (759, 73), "font_color": (134, 157, 167), "font_size": 186},
        {"text": "尔", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "德", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Urd", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "lucy": [  # 露西女士
        {"text": "露", "position": (759, 73), "font_color": (233, 251, 57), "font_size": 186},
        {"text": "西", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "女", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "士", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Lucy", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "caroline": [  # 卡洛琳
        {"text": "卡", "position": (759, 73), "font_color": (224, 219, 199) ,"font_size": 186},
        {"text": "洛", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "琳", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Caroline Bartley", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "hunting": [  # 编辑亨廷
        {"text": "编", "position": (759, 73), "font_color": (114, 71, 61) ,"font_size": 186},
        {"text": "辑", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "亨", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "廷", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Editor Hunting", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "katz": [  # 卡兹
        {"text": "卡", "position": (759, 73), "font_color": (204, 188, 144) ,"font_size": 186},
        {"text": "兹", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Katz", "position": (1030, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "z": [  # z
        {"text": "Z", "position": (759, 73), "font_color": (27, 22, 23), "font_size": 186},
        {"text": "", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Madam Z", "position": (930, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "marian": [  # 玛丽安
        {"text": "玛", "position": (759, 73), "font_color": (134, 107, 106), "font_size": 186},
        {"text": "丽", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "安", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Marian", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "merel": [  # 梅蕾尔
        {"text": "梅", "position": (759, 73), "font_color": (203, 186, 146), "font_size": 186},
        {"text": "蕾", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "尔", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Merel", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "octavia": [  # 奥克塔维奥
        {"text": "奥", "position": (759, 73), "font_color": (193, 176, 209), "font_size": 186},
        {"text": "克", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "塔", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "维奥", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Octavia", "position": (1390, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "77": [  # 77
        {"text": "77", "position": (759, 73), "font_color": (124, 158, 168), "font_size": 186},
        {"text": "", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Seventy-seven", "position": (990, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "jailer": [  # 狱卒
        {"text": "狱", "position": (759, 73), "font_color": (170, 128, 89), "font_size": 186},
        {"text": "卒", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Jailer", "position": (990, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "garcía": [  # 加西亚
        {"text": "加", "position": (759, 73), "font_color": (67, 70, 68), "font_size": 186},
        {"text": "西", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "亚", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/García", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "roberta": [  # 罗贝托
        {"text": "罗", "position": (759, 73), "font_color": (134, 96, 83), "font_size": 186},
        {"text": "贝", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "托", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Roberta", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "888": [  # 888
        {"text": "888", "position": (759, 73), "font_color": (226, 224, 236), "font_size": 186},
        {"text": "", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/888", "position": (1186, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "ring": [  # 圈环
        {"text": "圈", "position": (759, 73), "font_color": (114, 95, 87), "font_size": 186},
        {"text": "环", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/The Ring", "position": (1030, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "lilya": [  # 红弩箭
        {"text": "红", "position": (759, 73), "font_color": (239, 132, 52), "font_size": 186},
        {"text": "弩", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "箭", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Lilya", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "ms.newBabel": [  # 新巴别塔
        {"text": "新", "position": (759, 73), "font_color": (249, 215, 130), "font_size": 186},
        {"text": "巴", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "别", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "塔", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Ms. NewBabel", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "charlton": [  # 查尔顿
        {"text": "查", "position": (759, 73), "font_color": (148, 110, 91), "font_size": 186},
        {"text": "尔", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "顿", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Charlton", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "frey": [  #弗里莱
        {"text": "弗", "position": (759, 73), "font_color": (191, 181, 124), "font_size": 186},
        {"text": "里", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "莱", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Frey", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "prismagreen": [  #绿棱镜
        {"text": "绿", "position": (759, 73), "font_color": (204, 165, 162), "font_size": 186},
        {"text": "棱", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "镜", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Prismagreen", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "pointer": [  # 指针
        {"text": "指", "position": (759, 73), "font_color": (226, 217, 176), "font_size": 186},
        {"text": "针", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Pointer", "position": (1030, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "alexios": [  # 阿利克西欧斯
        {"text": "阿", "position": (759, 73), "font_color": (158, 68, 43), "font_size": 186},
        {"text": "利", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "克", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "西欧斯", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Alexios", "position": (1460, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "verity": [  # 空心木
        {"text": "空", "position": (759, 73), "font_color": (158, 68, 43), "font_size": 186},
        {"text": "心", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "木", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Verity", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "lorelei": [  # 罗蕾莱
        {"text": "罗", "position": (759, 73), "font_color": (40, 189, 156), "font_size": 186},
        {"text": "蕾", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "莱", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Lorelei", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "buddy_fairchild": [  # 嚼嚼松果
        {"text": "嚼", "position": (759, 73), "font_color": (255, 183, 109), "font_size": 186},
        {"text": "嚼", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "松", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "果", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Buddy Fairchild", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "ONiON": [  # 洋葱头
        {"text": "洋", "position": (759, 73), "font_color": (239, 185, 117), "font_size": 186},
        {"text": "葱", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "头", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/ONiON", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "loggerhead": [  # 空脑袋
        {"text": "空", "position": (759, 73), "font_color": (192, 202, 119), "font_size": 186},
        {"text": "脑", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "袋", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Loggerhead", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "brimley": [  # 宽檐帽
        {"text": "宽", "position": (759, 73), "font_color": (235, 169, 105), "font_size": 186},
        {"text": "檐", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "帽", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Brimley", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "barbara": [  # 数羊羔
        {"text": "数", "position": (759, 73), "font_color": (199, 219, 77), "font_size": 186},
        {"text": "羊", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "羔", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Barbara", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "afsivi": [  # 阿夫西维
        {"text": "阿", "position": (759, 73), "font_color": (182, 255, 239), "font_size": 186},
        {"text": "夫", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "西", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "维", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Авксивий", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "ulu": [  # 和平乌鲁
        {"text": "和", "position": (759, 73), "font_color": (239, 159, 81), "font_size": 186},
        {"text": "平", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "乌", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "鲁", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Ulu", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "desert_flannel": [  # 沙丝绒
        {"text": "沙", "position": (759, 73), "font_color": (183, 241, 150), "font_size": 186},
        {"text": "丝", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "绒", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Desert Flannel", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "kanjira": [  # 坎吉拉
        {"text": "坎", "position": (759, 73), "font_color": (174, 131, 195), "font_size": 186},
        {"text": "吉", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "拉", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Kanjira", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "diggers": [  # 挖掘艺术
        {"text": "挖", "position": (759, 73), "font_color": (227, 148, 101), "font_size": 186},
        {"text": "掘", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "艺", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "术", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Diggers", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "blonney": [  # 金蜜儿
        {"text": "金", "position": (759, 73), "font_color": (239, 156, 178), "font_size": 186},
        {"text": "蜜", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "儿", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Blonney", "position": (1290, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "paper_heron": [  # 鹭鸶剪
        {"text": "鹭", "position": (759, 73), "font_color": (164, 47, 25), "font_size": 186},
        {"text": "鸶", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "剪", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Paper Heron", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "cheng_heguang": [  # 程和光
        {"text": "程", "position": (759, 73), "font_color": (21, 42, 62), "font_size": 186},
        {"text": "和", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "光", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Cheng Heguang", "position": (1190, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
    "huigu": [  # 惠姑
        {"text": "惠", "position": (759, 73), "font_color": (150, 167, 81), "font_size": 186},
        {"text": "姑", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "/Mayfly", "position": (990, 225), "font_color": (104, 97, 92), "font_size": 69},
    ],
}
import getpass

# 获取当前用户名
username = getpass.getuser()

# 构建用户文档路径
if os.name == 'nt':  # Windows系统
    user_documents = os.path.join('C:\\', 'Users', username, 'Documents')
else:  # 其他系统
    user_documents = os.path.expanduser('~/Documents')

# 构建"1999"文件夹路径
magic_cut_folder = os.path.join(user_documents, '1999')

# 创建"1999"文件夹（如果不存在）
os.makedirs(magic_cut_folder, exist_ok=True)

# 角色列表（按顺序对应角色）
character_list = list(character.keys())

# 背景图列表
backgrounds = [
    {"file": "c1.png", "name": "维尔汀箱子内（白天）"},
    {"file": "c2.png", "name": "拉普拉斯康复中心"},
    {"file": "c3.png", "name": "基金会外面森林"},
    {"file": "c4.png", "name": "基金会外面"},
    {"file": "c5.png", "name": "基金会大厅"},
    {"file": "c6.png", "name": "拉普拉斯科算中心"},
    {"file": "c7.png", "name": "维尔汀箱子内（夜晚）"},
    {"file": "c8.png", "name": "第一防线学校教室"},
    {"file": "c9.png", "name": "康斯坦丁办公室"},
    {"file": "c10.png", "name": "第一防线学校走廊"},
    {"file": "c11.png", "name": "沛城城门"},
    {"file": "c12.png", "name": "海岛海滩"},
    {"file": "c13.png", "name": "维也纳街道路口（白天）"},
    {"file": "c14.png", "name": "沛城城内"},
    {"file": "c15.png", "name": "西线山丘"},
    {"file": "c16.png", "name": "维也纳街道路口（暴雨）"},
    {"file": "c17.png", "name": "基金会图书馆"},
    {"file": "c18.png", "name": "伦敦小巷"},
    {"file": "c19.png", "name": "卡卡尼亚心理咨询室"},
    {"file": "c20.png", "name": "沛城外的草原"},
    {"file": "c21.png", "name": "里正办公室"},
    {"file": "c22.png", "name": "办公室（夜晚）"},
    {"file": "c23.png", "name": "伦敦海岸"},
    {"file": "c24.png", "name": "办公室（白天）"},
    {"file": "c25.png", "name": "战地医院"},
    {"file": "c26.png", "name": "心理咨询室晚上"},
    {"file": "c27.png", "name": "众议院外面"},
    {"file": "c28.png", "name": "维尔汀海岛房间"},
    {"file": "c29.png", "name": "维也纳街头"},
    {"file": "c30.png", "name": "海岛众议院"},
    {"file": "c31.png", "name": "画展"},
    {"file": "c32.png", "name": "哑谜办公室"},
]
# 默认背景索引
current_background_index = 1  # 初始使用c1.png
user_selected_background = {}  # 格式为 {角色名: 背景编号}

# 获取当前背景图路径的函数
def get_current_background_path():
    """获取当前使用的背景图路径"""
    bg_info = backgrounds[current_background_index - 1]
    return get_resource_path(os.path.join("background", bg_info["file"]))

def get_current_background_name():
    """获取当前背景图名称"""
    return backgrounds[current_background_index - 1]["name"]

# 创建中文字典映射（用于在界面中显示中文名）
character_chinese_names = {
    "noire": "菲林士多",
    "recoleta": "虚构集",
    "vertin": "维尔汀",
    "sentinel": "玛丽安娜",
    "brume": "灰调蓝",
    "isolde": "伊索尔德",
    "kakania": "卡卡尼亚",
    "melania": "梅兰妮",
    "nautika": "诺谛卡",
    "liang": "梁月",
    "flutterpage": "纸信圈儿",
    "regulus": "星锑",
    "moldir": "莫莉德尔",
    "thirty-seven": "37",
    "six": "6",
    "a_knight": "未锈铠",
    "sotheby": "苏芙比",
    "charon": "卡戎",
    "APPLe": "APPLe",
    "marcus": "马库斯",
    "aleph": "阿莱夫",
    "sonetto": "十四行诗",
    "hofmann": "霍夫曼",
    "rubuska": "野树莓",
    "corvus": "告死鸟",
    "mesmer_jr.": "小梅斯梅尔",
    "jiu_niangzi": "曲娘",
    "sophia": "苏菲亚",
    "210": "210",
    "door": "门",
    "bunny_bunny": "芭妮芭妮",
    "matilda": "玛蒂尔达",
    "eagle": "小春雀儿",
    "argus": "阿尔古斯",
    "mr.duncan": "邓肯先生",
    "dikke": "帕米埃",
    "tooth_fairy": "牙仙",
    "windsong": "北方哨歌",
    "cristallo": "铅玻璃",
    "barcarola": "芭卡洛儿",
    "fatutu": "图图石子",
    "kiperina": "库珀花环",
    "voyager": "远旅",
    "williow": "笃笃骨",
    "druvis_III": "槲寄生",
    "spathodea": "可燃点",
    "lopera": "洛佩拉",
    "beryl": "贝丽尔",
    "eternity": "温妮弗雷德",
    "pickles": "皮克勒斯",
    "ezio": "艾吉奥",
    "changeling": "洁西卡",
    "bkornblume": "柏林以东",
    "anjo_nala": "天使娜娜",
    "oliver_fog": "雾行者",
    "anan_lee": "泥鯭的士",
    "hissabeth": "冷周六",
    "getian": "葛天",
    "schneider": "斯奈德",
    "arcana": "阿尔卡纳",
    "joe": "J",
    "the_fool": "弄臣",
    "enigma": "哑谜",
    "ulrich": "乌尔里希",
    "villa": "维拉",
    "shamane": "鬃毛沙砾",
    "kassandra": "卡珊德拉",
    "mercuria": "环状水星",
    "felician": "费利西安",
    "ms.radio": "无线电小姐",
    "twins_sleep": "丽莎&路易斯",
    "medicine_pocket": "兔毛手袋",
    "x": "X",
    "yenisei_jr.": "小叶尼塞",
    "baby_blue": "婴儿蓝",
    "tuesday": "蓝手帕",
    "centurion": "百夫长",
    "ezra_theodore": "爱兹拉",
    "black_dwarf": "伽菈波那",
    "igor": "伊戈尔",
    "aima": "艾玛",
    "balloon_party": "气球派对",
    "la_source": "拉拉泉",
    "horropedia": "恐怖通",
    "marsha": "玛尔莎",
    "charlie": "夏利",
    "forget_me_not": "勿忘我",
    "creius": "刻雷乌斯",
    "black_ibis": "黑鹮",
    "semmelweis": "塞梅尔维斯",
    "qixing": "奇星",
    "poitier": "波蒂埃",
    "name_day": "命名日",
    "valentina": "瓦伦缇娜",
    "pyrrhos": "鲍里斯",
    "john_titor": "约翰·提托",
    "coppelia": "珐琅眼",
    "xu_niangzi": "许娘子",
    "urd": "兀尔德",
    "lucy": "露西女士",
    "caroline": "卡洛琳",
    "hunting": "编辑亨廷",
    "katz": "卡兹",
    "z": "Z",
    "marian": "玛丽安",
    "merel": "梅蕾尔",
    "octavia": "奥克塔维奥",
    "77": "77",
    "jailer": "狱卒",
    "garcía": "加西亚",
    "roberta": "罗贝托",
    "888": "888",
    "ring": "圈环",
    "lilya": "红弩箭",
    "ms.newBabel": "新巴别塔",
    "charlton": "查尔顿",
    "frey": "弗里莱",
    "prismagreen": "绿棱镜",
    "pointer": "指针",
    "alexios": "阿利克西欧斯",
    "verity": "空心木",
    "lorelei": "罗蕾莱",
    "buddy_fairchild": "嚼嚼松果",
    "ONiON": "洋葱头",
    "loggerhead": "空脑袋",
    "brimley": "宽檐帽",
    "barbara": "数羊羔",
    "afsivi": "阿夫西维",
    "ulu": "和平乌鲁",
    "desert_flannel": "沙丝绒",
    "kanjira": "坎吉拉",
    "diggers": "挖掘艺术",
    "blonney": "金蜜儿",
    "paper_heron": "鹭鸶剪",
    "cheng_heguang": "程和光",
    "huigu": "惠姑",
}

# 全局窗口变量
character_window = None
character_window_visible = True


# 获取当前角色信息
def get_current_character():
    return character_list[current_character_index - 1]


def get_current_font():
    # 使用 get_resource_path 获取字体文件路径
    return get_resource_path(character[get_current_character()]["font"])


def get_current_emotion_count():
    return character[get_current_character()]["emotion_count"]


def delate(folder_path, quality=85):
    """删除图片文件夹中的所有jpg文件"""
    try:
        if os.path.exists(folder_path):
            deleted_count = 0
            for filename in os.listdir(folder_path):
                if filename.lower().endswith('.jpg'):
                    file_path = os.path.join(folder_path, filename)
                    try:
                        os.remove(file_path)
                        deleted_count += 1
                    except Exception as e:
                        print(f"删除文件 {filename} 时出错: {e}")

            print(f"已清除 {deleted_count} 个图片文件")

            # 提示用户需要重新加载
            if deleted_count > 0:
                print("提示：清除图片后需要重新加载角色才能再次使用")

            return deleted_count
        else:
            print("图片文件夹不存在")
            return 0
    except Exception as e:
        print(f"清除图片时发生错误: {str(e)}")
        return 0


def generate_and_save_images(character_name, bg_index=None):
    # 获取当前角色的皮肤数量
    emotion_count = character[character_name]["emotion_count"]
    if bg_index is None:
        # 检查用户是否为此角色设置了特定背景
        if character_name in user_selected_background:
            bg_index = user_selected_background[character_name]
        else:
            bg_index = current_background_index  # 使用全局当前背景索引

    # 确保背景索引在有效范围内
    if bg_index < 1:
        bg_index = 1
    elif bg_index > len(backgrounds):
        bg_index = len(backgrounds)
    bg_info = backgrounds[bg_index - 1]
    print(f"正在为 {character_name} 加载背景 {bg_info['name']}...")

    # 只加载指定的背景图
    background_image_count = 1  # 现在我们只使用一个背景
    for i in range(background_image_count):
        for j in range(emotion_count):
            # 使用用户选择的背景或当前背景
            actual_bg_index = (bg_index - 1) + i
            if actual_bg_index >= len(backgrounds):
                actual_bg_index = len(backgrounds) - 1

            actual_bg_info = backgrounds[actual_bg_index]
            background_path = get_resource_path(os.path.join("background", actual_bg_info["file"]))
            overlay_path = get_resource_path(
                os.path.join("character", character_name, f"{character_name} ({j + 1}).png"))

            background = Image.open(background_path).convert("RGBA")
            overlay = Image.open(overlay_path).convert("RGBA")

            img_num = j * background_image_count + i + 1
            result = background.copy()
            result.paste(overlay, (0, 134), overlay)

            # 使用绝对路径保存生成的图片
            save_path = os.path.join(magic_cut_folder, f"{character_name}_bg{bg_info['name']}_({img_num}).jpg")
            result.convert("RGB").save(save_path, quality=95)

    print(f"加载完成，使用背景: {bg_info['name']}")

def switch_character(new_index):
    global current_character_index
    # 修复：允许索引范围从1到len(character_list)
    if 1 <= new_index <= len(character_list):
        current_character_index = new_index
        character_name = get_current_character()
        chinese_name = character_chinese_names.get(character_name, character_name)
        print(f"已切换到角色: {chinese_name}")

        # 生成并保存图片
        generate_and_save_images(character_name)

        return True
    return False


# 显示当前角色信息
def show_current_character():
    character_name = get_current_character()
    chinese_name = character_chinese_names.get(character_name, character_name)
    print(f"当前角色: {chinese_name} ({character_name})")


# 显示当前角色信息
show_current_character()

# 测试：生成当前角色的图片
generate_and_save_images(get_current_character())


def get_expression(i):
    global expression
    character_name = get_current_character()
    if i <= character[character_name]["emotion_count"]:
        print(f"已切换至第{i}个皮肤")
        expression = i

# 随机获取表情图片名称
# 优化版本：使用循环替代递归，避免栈溢出风险
# 维护上一次选择的表情类型，确保不连续选择相同表情
# 第280行，修改函数中的变量引用
def get_random_value():
    background_image = int(1)  # 现在我们每次只使用一个背景
    global value_1, expression

    character_name = get_current_character()
    emotion_count = get_current_emotion_count()
    total_images = background_image * emotion_count

    # 获取当前背景索引
    if character_name in user_selected_background:
        bg_index = user_selected_background[character_name]
    else:
        bg_index = current_background_index

    # 在函数开始处获取背景信息
    if character_name in user_selected_background:
        bg_index = user_selected_background[character_name]
    else:
        bg_index = current_background_index

    # 添加这两行来获取背景名称
    bg_info = backgrounds[bg_index - 1]  # 获取背景信息
    bg_name = bg_info["name"]  # 获取背景名称

    # 获取背景名称
    bg_info = backgrounds[bg_index - 1]  # 修复：添加这行来获取背景信息
    bg_name = bg_info["name"]  # 修复：添加这行来获取背景名称

    # 1. 首先检查用户是否通过窗口选择了特定皮肤
    if character_name in user_selected_skins and user_selected_skins[character_name] > 0:
        selected_skin = user_selected_skins[character_name]
        # 确保选择的皮肤编号在有效范围内
        if 1 <= selected_skin <= emotion_count:
            i = random.randint((selected_skin - 1) * background_image + 1,
                               selected_skin * background_image)
            value_1 = i
            print(f"使用用户选择的第{selected_skin}个皮肤，背景{bg_name}")
            return f"{character_name}_bg{bg_name}_({i})"

    # 2. 然后检查快捷键设置的皮肤
    if expression:
        i = random.randint((expression - 1) * background_image + 1, expression * background_image)
        value_1 = i
        expression = None  # 使用后清除，避免重复使用
        print(f"使用快捷键设置的皮肤，背景{bg_name}")
        return f"{character_name}_bg{bg_name}_({i})"

    # 3. 当没有选择特定皮肤时，不再随机选择，而是使用第一个皮肤
    # 修改：取消随机，总是使用第一个皮肤
    i = 1  # 总是使用第一个皮肤
    value_1 = i
    print(f"使用默认的第{i}个皮肤，背景{bg_name}")
    return f"{character_name}_bg{bg_name}_({i})"

HOTKEY = "enter"

# 全选快捷键, 此按键并不会监听,  而是会作为模拟输入
# 此值为字符串, 代表热键的键名, 格式同 HOTKEY
SELECT_ALL_HOTKEY = "ctrl+a"

# 剪切快捷键, 此按键并不会监听,  而是会作为模拟输入
# 此值为字符串, 代表热键的键名, 格式同 HOTKEY
CUT_HOTKEY = "ctrl+x"

# 黏贴快捷键, 此按键并不会监听,  而是会作为模拟输入
# 此值为字符串, 代表热键的键名, 格式同 HOTKEY
PASTE_HOTKEY = "ctrl+v"

# 发送消息快捷键, 此按键并不会监听,  而是会作为模拟输入
# 此值为字符串, 代表热键的键名, 格式同 HOTKEY
SEND_HOTKEY = "enter"

# 是否阻塞按键, 如果热键设置为阻塞模式, 则按下热键时不会将该按键传递给前台应用
# 如果生成热键和发送热键相同, 则强制阻塞, 防止误触发发送消息
# 此值为布尔值, True 或 False
BLOCK_HOTKEY = False

# 操作的间隔, 如果失效可以适当增大此数值
# 此值为数字, 单位为秒
DELAY = 0.1

# 是否自动黏贴生成的图片(如果为否则保留图片在剪贴板, 可以手动黏贴)
# 此值为布尔值, True 或 False
AUTO_PASTE_IMAGE = True

# 生成图片后是否自动发送(模拟回车键输入), 只有开启自动黏贴才生效
# 此值为布尔值, True 或 False
AUTO_SEND_IMAGE = True


def copy_png_bytes_to_clipboard(png_bytes: bytes):
    # 打开 PNG 字节为 Image
    image = Image.open(io.BytesIO(png_bytes))
    # 转换成 BMP 字节流（去掉 BMP 文件头的前 14 个字节）
    with io.BytesIO() as output:
        image.convert("RGB").save(output, "BMP")
        bmp_data = output.getvalue()[14:]
    # 打开剪贴板并写入 DIB 格式
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, bmp_data)
    win32clipboard.CloseClipboard()


# 判断窗口名
def get_window_exe_name():
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid)
        exe_path = process.exe()
        return os.path.basename(exe_path)
    except Exception as e:
        print(f"获取文件名时发生错误：{e}")
        return None


def cut_all_and_get_text() -> str:
    """
    #模拟 Ctrl+A / Ctrl+X 剪切全部文本，并返回剪切得到的内容。
    #delay: 每步之间的延时（秒），默认0.1秒。
    """
    # 备份原剪贴板
    old_clip = pyperclip.paste()

    # 清空剪贴板，防止读到旧数据
    pyperclip.copy("")

    # 发送 Ctrl+A 和 Ctrl+X
    keyboard.send(SELECT_ALL_HOTKEY)
    keyboard.send(CUT_HOTKEY)
    time.sleep(DELAY)

    # 获取剪切后的内容
    new_clip = pyperclip.paste()

    return new_clip


def try_get_image() -> Image.Image | None:
    """
    尝试从剪贴板获取图像，如果没有图像则返回 None。
    仅支持 Windows。
    """
    try:
        win32clipboard.OpenClipboard()
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_DIB):
            data = win32clipboard.GetClipboardData(win32clipboard.CF_DIB)
            if data:
                # 将 DIB 数据转换为字节流，供 Pillow 打开
                bmp_data = data
                # DIB 格式缺少 BMP 文件头，需要手动加上
                # BMP 文件头是 14 字节，包含 "BM" 标识和文件大小信息
                header = b'BM' + (len(bmp_data) + 14).to_bytes(4, 'little') + b'\x00\x00\x00\x00\x36\x00\x00\x00'
                image = Image.open(io.BytesIO(header + bmp_data))
                return image
    except Exception as e:
        print("无法从剪贴板获取图像：", e)
    finally:
        try:
            win32clipboard.CloseClipboard()
        except:
            pass
    return None


def perform_keyboard_actions(png_bytes):
    """在主线程中执行所有键盘操作"""
    if png_bytes is None:
        print("Generate image failed!")
        return

    copy_png_bytes_to_clipboard(png_bytes)

    if AUTO_PASTE_IMAGE:
        # 使用 call_later 确保 send 在 keyboard 自己的线程中运行
        keyboard.call_later(lambda: keyboard.send(PASTE_HOTKEY), delay=0.1)

        if AUTO_SEND_IMAGE:
            keyboard.call_later(lambda: keyboard.send(SEND_HOTKEY), delay=0.4)  # 增加延迟以确保粘贴完成


def Start():
    print("Start generate...")

    character_name = get_current_character()

    # 确定背景索引
    if character_name in user_selected_background:
        bg_index = user_selected_background[character_name]
    else:
        bg_index = current_background_index

    # 构建图片文件名
    address = os.path.join(magic_cut_folder, get_random_value() + ".jpg")
    BASEIMAGE_FILE = address

    # 检查文件是否存在，如果不存在则生成
    if not os.path.exists(BASEIMAGE_FILE):
        print(f"图片文件不存在，重新生成: {BASEIMAGE_FILE}")
        generate_and_save_images(character_name, bg_index)

    print(character_name, f"背景: {get_current_background_name()}")

    # 文本框左上角坐标 (x, y), 同时适用于图片框
    # 此值为一个二元组, 例如 (100, 150), 单位像素, 图片的左上角记为 (0, 0)
    TEXT_BOX_TOPLEFT = (mahoshojo_postion[0], mahoshojo_postion[1])
    # 文本框右下角坐标 (x, y), 同时适用于图片框
    # 此值为一个二元组, 例如 (100, 150), 单位像素, 图片的左上角记为 (0, 0)
    IMAGE_BOX_BOTTOMRIGHT = (mahoshojo_over[0], mahoshojo_over[1])

    text = pyperclip.paste()  # 暂时从剪贴板获取，而不是模拟按键
    image = try_get_image()


    if text == "" and image is None:
        print("no text or image")
        # 即使没有文本/图像，也调用回调以确保线程安全
        keyboard.call_later(perform_keyboard_actions, args=[None])
        return

    png_bytes = None

    # ===== 特殊功能处理 =====
    global special_feature_enabled
    original_text = text
    transformed_text = text

    # 检查是否为约翰·提托（十六进制转换）
    if special_feature_enabled and character_name == SPECIAL_CHARACTER and text != "":
        print("特殊功能激活：将文本转换为十六进制编码")
        transformed_text = convert_to_hex_with_original(text)
        print(f"原始文本: {text}")
        print(f"转换后文本: {transformed_text}")

    # 检查是否为皮克勒斯（狗叫转换）
    if special_feature_enabled and character_name == DOG_BARK_CHARACTER and text != "":
        print("狗叫功能激活：将文本转换为狗叫")
        transformed_text = convert_to_dog_bark(text)
        print(f"原始文本: {text}")
        print(f"转换后文本: {transformed_text}")

    if image is not None:
        try:
            print("Get image")
            png_bytes = paste_image_auto(
                image_source=BASEIMAGE_FILE,
                image_overlay=None,
                top_left=TEXT_BOX_TOPLEFT,
                bottom_right=IMAGE_BOX_BOTTOMRIGHT,
                content_image=image,
                align="center",
                valign="middle",
                padding=12,
                allow_upscale=True,
                keep_alpha=True,  # 使用内容图 alpha 作为蒙版
                role_name=character_name,  # 传递角色名称
                text_configs_dict=text_configs_dict,  # 传递文字配置字典
            )
        except Exception as e:
            print("Generate image failed:", e)
            keyboard.call_later(perform_keyboard_actions, args=[None])
            return

    elif transformed_text != "":
        print("Get text: " + original_text)
        try:
            png_bytes = draw_text_auto(
                image_source=BASEIMAGE_FILE,
                image_overlay=None,
                top_left=TEXT_BOX_TOPLEFT,
                bottom_right=IMAGE_BOX_BOTTOMRIGHT,
                text=transformed_text,  # 使用转换后的文本
                align="left",
                valign='top',
                color=(255, 255, 255),
                max_font_height=145,  # 例如限制最大字号高度为 145 像素
                font_path=get_current_font(),
                role_name=character_name,  # 传递角色名称
                text_configs_dict=text_configs_dict,  # 传递文字配置字典
            )

        except Exception as e:
            print("Generate image failed:", e)
            keyboard.call_later(perform_keyboard_actions, args=[None])
            return

    # 将 png_bytes 传递给主线程的 perform_keyboard_actions
    keyboard.call_later(perform_keyboard_actions, args=[png_bytes])

def run_start_in_thread():
    if enablewhitelist and get_window_exe_name() not in windowwhitelist:
        print("当前窗口不在白名单内")
        keyboard.send(HOTKEY)
        return

    # 1. 剪切文本
    text = cut_all_and_get_text()

    # 2. 检查@字符功能
    if check_at_enabled and text and "@" in text:
        print("检测到@字符，撤销剪切操作并直接发送文本")

        # 模拟Ctrl+Z撤销剪切操作
        keyboard.send('ctrl+z')

        # 增加延迟确保撤销完成
        time.sleep(0.15)

        # 直接发送文本（不需要粘贴，因为文本已恢复）
        keyboard.send(SEND_HOTKEY)

        return  # 不进行后续图像生成

    # 3. 如果没有@字符，正常处理图像
    threading.Thread(target=Start).start()

# 全局窗口变量
character_window = None
character_window_visible = True
# 创建角色选择窗口的函数

# 特殊按钮变量
special_button = None
is_special_character = False

# 修改后的 toggle_character_window 函数，放在 create_character_selection_window 函数之前
def toggle_character_window():
    global character_window, character_window_visible
    """切换@检查功能"""
    global check_at_enabled
    check_at_enabled = not check_at_enabled


    if character_window and character_window.winfo_exists():
        if character_window_visible:
            character_window.withdraw()
            character_window_visible = False
            print("角色选择窗口已隐藏")
        else:
            character_window.deiconify()
            character_window.lift()
            character_window.focus_force()
            character_window_visible = True
            print("角色选择窗口已显示")
    else:
        # 创建新窗口
        print("创建角色选择窗口")
        # 在新线程中运行窗口，避免阻塞主线程
        window_thread = threading.Thread(target=create_character_selection_window, daemon=True)
        window_thread.start()
    if check_at_enabled:
        at_check_button.config(text="@检查: 开", bg="#27AE60", activebackground="#27AE60")
        widgets.status_label.config(text="@检查功能已开启 - 文本中包含@时将撤销剪切并直接发送文本")
        print("@检查功能已开启")
    else:
        at_check_button.config(text="@检查: 关", bg="#3498DB", activebackground="#2980B9")
        widgets.status_label.config(text="@检查功能已关闭")
        print("@检查功能已关闭")

def create_character_selection_window():
    global character_window, character_window_visible

    # 当前角色的皮肤选择状态
    current_skin_selection = user_selected_skins.get(get_current_character(), 0)

    def on_quit():
        """退出程序"""
        import os
        print("正在退出程序...")

        # 先清除图片
        try:
            if os.path.exists(magic_cut_folder):
                deleted_count = 0
                for filename in os.listdir(magic_cut_folder):
                    file_path = os.path.join(magic_cut_folder, filename)
                    try:
                        if os.path.isfile(file_path) and filename.lower().endswith('.jpg'):
                            os.remove(file_path)
                            deleted_count += 1
                    except Exception as e:
                        print(f"删除文件 {filename} 时出错: {e}")

                print(f"已清除 {deleted_count} 个图片文件")
        except Exception as e:
            print(f"清除图片时发生错误: {str(e)}")

        # 再关闭窗口
        if character_window and character_window.winfo_exists():
            character_window.destroy()

        # 打印退出信息
        print("程序已退出")

        # 强制终止进程
        os._exit(0)

    def on_closing():
        """窗口关闭时的处理 - 改为退出程序"""
        print("窗口关闭，退出程序...")
        on_quit()

    def on_clear_images():
        """清除已生成的图片"""
        try:
            if os.path.exists(magic_cut_folder):
                deleted_count = 0
                for filename in os.listdir(magic_cut_folder):
                    file_path = os.path.join(magic_cut_folder, filename)
                    try:
                        if os.path.isfile(file_path) and filename.lower().endswith('.jpg'):
                            os.remove(file_path)
                            deleted_count += 1
                    except Exception as e:
                        print(f"删除文件 {filename} 时出错: {e}")

                if deleted_count > 0:
                    widgets.status_label.config(text=f"已清除 {deleted_count} 个图片文件")
                    messagebox.showinfo("清除完成",
                                        f"已清除 {deleted_count} 个图片文件\n清除后需要重新加载角色才能再次使用")
                else:
                    widgets.status_label.config(text="没有找到需要清除的图片文件")
                    messagebox.showinfo("清除完成", "没有找到需要清除的图片文件")
            else:
                widgets.status_label.config(text="图片文件夹不存在")
                messagebox.showinfo("提示", "图片文件夹不存在")

            # 刷新预览
            update_preview()

        except Exception as e:
            error_msg = f"清除图片时发生错误: {str(e)}"
            widgets.status_label.config(text=error_msg)
            messagebox.showerror("错误", error_msg)

    # 添加函数来更新背景选择
    def update_bg_combo(character_name):
        if character_name in user_selected_background:
            selected_bg = user_selected_background[character_name]
            if 1 <= selected_bg <= len(backgrounds):
                widgets.bg_combo.set(backgrounds[selected_bg - 1]["name"])
        else:
            widgets.bg_combo.set(backgrounds[current_background_index - 1]["name"])

    def on_bg_selected(event=None):
        global current_background_index

        current_char = get_current_character()
        current_chinese_name = character_chinese_names.get(current_char, current_char)
        selected_bg_name = bg_var.get()  # 获取选择的背景名称

        try:
            # 根据选择的背景名称找到对应的索引
            selected_bg_index = None
            for i, bg_info in enumerate(backgrounds, 1):
                if bg_info["name"] == selected_bg_name:  # 使用selected_bg_name而不是selected_name
                    selected_bg_index = i
                    break

            if selected_bg_index is not None and 1 <= selected_bg_index <= len(backgrounds):
                # 为此角色设置背景
                user_selected_background[current_char] = selected_bg_index

                # 更新全局当前背景（可选）
                current_background_index = selected_bg_index

                widgets.status_label.config(text=f"{current_chinese_name} 已设置为使用背景{selected_bg_name}")
                print(f"{current_chinese_name} 已设置为使用背景{selected_bg_name}")

                # 重新生成此角色的图片
                widgets.status_label.config(text=f"正在为{current_chinese_name}生成背景{selected_bg_name}的图片...")
                root.update()

                generate_and_save_images(current_char, selected_bg_index)

                # 更新预览
                skin_num = get_current_skin_num()
                update_preview(current_char, skin_num, selected_bg_index)

                widgets.status_label.config(text=f"{current_chinese_name} 背景{selected_bg_name}已生成")
            else:
                messagebox.showwarning("错误", f"未找到背景: {selected_bg_name}")
                update_bg_combo(current_char)
        except Exception as e:
            messagebox.showwarning("错误", f"无法解析背景编号: {str(e)}")
            update_bg_combo(current_char)

    # 修改 update_preview 函数以支持背景预览
    def get_current_skin_num():
        """获取当前选中的皮肤编号"""
        selected_text = skin_var.get()
        if selected_text == "随机":
            return None
        try:
            return int(selected_text.replace("皮肤", ""))
        except:
            return None



    def update_preview(character_name=None, skin_num=None, bg_num=None):
        """更新预览 - 显示角色皮肤与背景的组合"""
        nonlocal preview_image, preview_photo

        if character_name is None:
            character_name = get_current_character()

        if skin_num is None:
            skin_num = get_current_skin_num()

        if bg_num is None:
            if character_name in user_selected_background:
                bg_num = user_selected_background[character_name]
                bg_info = backgrounds[bg_index - 1]
                bg_name = bg_info["name"]
            else:
                bg_num = current_background_index

        # 如果没有选择皮肤，显示默认预览
        if skin_num is None:
            widgets.preview_canvas.delete("all")
            widgets.preview_canvas.create_text(75, 50,
                                               text="选择皮肤\n预览",
                                               font=("微软雅黑", 8),
                                               fill="#7F8C8D",
                                               justify=tk.CENTER)
            return

        # 尝试加载生成的图片
        try:
            # 构建图片路径
            bg_info = backgrounds[bg_num - 1]
            image_filename = f"{character_name}_bg{bg_info['name']}_({skin_num}).jpg"
            image_path = os.path.join(magic_cut_folder, image_filename)

            # 如果图片不存在，尝试生成
            if not os.path.exists(image_path):
                widgets.status_label.config(text="正在生成预览图片...")
                root.update()
                generate_and_save_images(character_name, bg_num)

            if os.path.exists(image_path):
                # 加载图片
                preview_image = Image.open(image_path)

                # 计算缩放比例以保持宽高比并填满预览区域
                original_width, original_height = preview_image.size
                target_width = 140
                target_height = 90

                width_ratio = target_width / original_width
                height_ratio = target_height / original_height
                scale_ratio = min(width_ratio, height_ratio)

                new_width = int(original_width * scale_ratio)
                new_height = int(original_height * scale_ratio)

                # 调整图片大小
                preview_image = preview_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

                # 创建新的背景图片（白色背景）
                final_image = Image.new('RGB', (target_width, target_height), (255, 255, 255))

                # 计算居中位置
                paste_x = (target_width - new_width) // 2
                paste_y = (target_height - new_height) // 2

                # 将调整后的图片粘贴到背景上
                final_image.paste(preview_image, (paste_x, paste_y))

                # 转换为PhotoImage
                preview_photo = ImageTk.PhotoImage(final_image)

                # 更新预览画布
                widgets.preview_canvas.delete("all")
                widgets.preview_canvas.create_image(75, 50, image=preview_photo)
                widgets.preview_canvas.image = preview_photo  # 保持引用
            else:
                # 如果图片生成失败，显示提示
                widgets.preview_canvas.delete("all")
                widgets.preview_canvas.create_text(75, 50,
                                                   text="预览\n生成中",
                                                   font=("微软雅黑", 8),
                                                   fill="#E74C3C",
                                                   justify=tk.CENTER)

        except Exception as e:
            print(f"加载预览图片时出错: {e}")
            widgets.preview_canvas.delete("all")
            widgets.preview_canvas.create_text(75, 50,
                                               text="加载\n失败",
                                               font=("微软雅黑", 8),
                                               fill="#E74C3C",
                                               justify=tk.CENTER)

    # 创建根窗口
    root = tk.Tk()
    character_window = root

    # 当前角色信息
    current_character = get_current_character()
    current_chinese_name = character_chinese_names.get(current_character, current_character)

    # 设置窗口标题
    root.title(f"角色选择 - 当前角色: {current_chinese_name}")

    # 设置窗口大小和位置 - 保持600x700
    root.geometry("600x700")
    root.resizable(True, True)

    # 设置窗口关闭时的行为
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # 创建一个容器来存储所有控件
    class Widgets:
        pass

    widgets = Widgets()
    current_display_indices = []

    # 当前选中的角色
    current_selected_character = current_character
    current_selected_chinese_name = current_chinese_name

    # 预览图片相关变量
    preview_image = None
    preview_photo = None

    # ========== 第一步：创建主容器 ==========
    try:
        bg_path = get_resource_path("background/window_bg.png")
        bg_image = Image.open(bg_path)
        tk_bg_image = ImageTk.PhotoImage(bg_image)

        canvas = tk.Canvas(root, width=600, height=700, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=tk_bg_image, anchor="nw")
        canvas.bg_image = tk_bg_image

        main_container = tk.Frame(canvas, bg="#FFFFFF", relief=tk.FLAT)
        main_container.place(relx=0.5, rely=0.5, anchor="center", width=560, height=660)
        main_container.config(highlightbackground="#CCCCCC", highlightthickness=1)

    except Exception as e:
        print(f"无法加载背景图片: {e}")
        root.configure(bg="#f5f7fa")
        main_container = tk.Frame(root, bg="#f5f7fa")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # ========== 第二步：创建所有控件 ==========

    # 标题区域
    title_frame = tk.Frame(main_container, bg="white")
    title_frame.pack(fill=tk.X, pady=(15, 10))

    title_label = tk.Label(title_frame, text="📁 角色选择器",
                           font=("微软雅黑", 16, "bold"),
                           fg="#2C3E50", bg="white")
    title_label.pack()

    subtitle_label = tk.Label(title_frame, text="选择您要使用的角色和皮肤",
                              font=("微软雅黑", 9),
                              fg="#7F8C8D", bg="white")
    subtitle_label.pack(pady=(3, 0))

    # 当前角色显示
    current_frame = tk.Frame(main_container, bg="#ECF0F1", relief=tk.RIDGE, borderwidth=1)
    current_frame.pack(fill=tk.X, pady=(0, 10))

    widgets.current_label = tk.Label(current_frame,
                                     text=f"当前使用: {current_chinese_name}",
                                     font=("微软雅黑", 10, "bold"),
                                     fg="#2C3E50", bg="#ffffff",
                                     padx=8, pady=5)
    widgets.current_label.pack()

    # ===== 皮肤选择、预览和特殊功能区域 =====
    skin_preview_frame = tk.Frame(main_container, bg="white")
    skin_preview_frame.pack(fill=tk.X, pady=(0, 10))

    # 第一列：皮肤选择（缩小）
    skin_column = tk.Frame(skin_preview_frame, bg="white")
    skin_column.pack(side=tk.LEFT, fill=tk.Y)

    skin_label = tk.Label(skin_column, text="皮肤:",
                          font=("微软雅黑", 9),
                          fg="#2C3E50", bg="white")
    skin_label.pack(anchor=tk.W, pady=(0, 3))

    skin_var = tk.StringVar()
    skin_var.set("皮肤1")

    current_character = get_current_character()
    skin_count = character[current_character]["emotion_count"]
    skin_options = [f"皮肤{i}" for i in range(1, skin_count + 1)]
    widgets.skin_combo = ttk.Combobox(skin_column, textvariable=skin_var,
                                      values=skin_options,
                                      state="readonly",
                                      font=("微软雅黑", 9),
                                      width=5)
    widgets.skin_combo.pack(anchor=tk.W)

    # 第二列：背景选择
    bg_column = tk.Frame(skin_preview_frame, bg="white")
    bg_column.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0))

    bg_label = tk.Label(bg_column, text="背景:",
                        font=("微软雅黑", 9),
                        fg="#2C3E50", bg="white")
    bg_label.pack(anchor=tk.W, pady=(0, 3))

    bg_var = tk.StringVar()
    bg_var.set(backgrounds[current_background_index - 1]["name"])

    # 创建背景选项
    bg_options = [bg_info["name"] for bg_info in backgrounds]
    widgets.bg_combo = ttk.Combobox(bg_column, textvariable=bg_var,
                                    values=bg_options,
                                    state="readonly",
                                    font=("微软雅黑", 9),
                                    width=20)
    widgets.bg_combo.pack(anchor=tk.W)

    # 第三列：预览区域（增大）
    preview_column = tk.Frame(skin_preview_frame, bg="white")
    preview_column.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 5))

    preview_label = tk.Label(preview_column, text="预览:",
                             font=("微软雅黑", 9),
                             fg="#2C3E50", bg="white")
    preview_label.pack(anchor=tk.W, pady=(0, 3))

    # 预览画布
    widgets.preview_canvas = tk.Canvas(preview_column, bg="white",
                                       width=150, height=100,
                                       highlightthickness=1,
                                       highlightbackground="#CCCCCC")
    widgets.preview_canvas.pack(anchor=tk.W)

    widgets.preview_text = widgets.preview_canvas.create_text(75, 50,
                                                              text="选择皮肤/背景\n预览",
                                                              font=("微软雅黑", 8),
                                                              fill="#7F8C8D",
                                                              justify=tk.CENTER)

    # 特殊功能
    special_column = tk.Frame(skin_preview_frame, bg="white")
    special_column.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))

    # 特殊功能按钮
    def update_special_button():
        global special_feature_enabled
        current_char = get_current_character()

        # 检查是否为特殊功能角色
        is_special = (current_char == SPECIAL_CHARACTER or current_char == DOG_BARK_CHARACTER)

        if is_special:
            widgets.special_button.config(state=tk.NORMAL)
            if special_feature_enabled:
                # 根据角色显示不同的文本
                if current_char == SPECIAL_CHARACTER:
                    special_text = "🔓 特殊功能: 十六进制"
                elif current_char == DOG_BARK_CHARACTER:
                    special_text = "🔓 特殊功能: 狗叫"
                else:
                    special_text = "🔓 特殊功能: 开"
                widgets.special_button.config(text=special_text, bg="#d1652f", activebackground="#d1652f")
            else:
                widgets.special_button.config(text="🔒 特殊功能: 关", bg="#131313", activebackground="#131313")
        else:
            widgets.special_button.config(state=tk.DISABLED)
            widgets.special_button.config(text="特殊功能", bg="#E0E0E0", activeforeground="#E0E0E0")

    def toggle_special_feature():
        global special_feature_enabled
        current_char = get_current_character()
        current_chinese_name = character_chinese_names.get(current_char, current_char)

        # 检查是否为特殊功能角色
        is_special = (current_char == SPECIAL_CHARACTER or current_char == DOG_BARK_CHARACTER)

        if is_special:
            if special_feature_enabled:
                special_feature_enabled = False
                widgets.special_button.config(text="🔒 特殊功能: 关", bg="#131313", activebackground="#131313")

                # 根据角色显示不同的关闭信息
                if current_char == SPECIAL_CHARACTER:
                    widgets.status_label.config(text="约翰·提托特殊功能已关闭")
                elif current_char == DOG_BARK_CHARACTER:
                    widgets.status_label.config(text="皮克勒斯狗叫功能已关闭")
            else:
                special_feature_enabled = True

                # 根据角色显示不同的开启信息
                if current_char == SPECIAL_CHARACTER:
                    widgets.special_button.config(text="🔓 特殊功能: 十六进制", bg="#d1652f", activebackground="#d1652f")
                    widgets.status_label.config(text="约翰·提托特殊功能已开启 - 文本将转换为十六进制编码，原文在括号内")
                elif current_char == DOG_BARK_CHARACTER:
                    widgets.special_button.config(text="🔓 特殊功能: 狗叫", bg="#d1652f", activebackground="#d1652f")
                    widgets.status_label.config(text="皮克勒斯狗叫功能已开启 - 文本将转换为有规律的狗叫，原文在括号内")
        else:
            messagebox.showinfo("提示", f"{current_chinese_name} 没有特殊功能")


    # 创建特殊功能按钮
    widgets.special_button = tk.Button(special_column, text="特殊功能",
                                       command=toggle_special_feature,
                                       bg="#E0E0E0", fg="white", font=("微软雅黑", 9),
                                       activebackground="#E0E0E0", activeforeground="white",
                                       relief=tk.FLAT, padx=12, pady=3, width=8)
    widgets.special_button.pack(anchor=tk.W, pady=(0, 5))


    # 特殊功能信息标签
    special_info_label = tk.Label(special_column,
                                  text=" 特殊功能\n（约翰·提托：十六进制\n  皮克勒斯：狗叫）",
                                  font=("微软雅黑", 8),
                                  fg="#666666",
                                  bg="white",
                                  wraplength=180,
                                  justify=tk.LEFT)
    special_info_label.pack(anchor=tk.W)

    # ===== 搜索区域（缩小）=====
    search_frame = tk.Frame(main_container, bg="white")
    search_frame.pack(fill=tk.X, pady=(0, 8))

    search_label = tk.Label(search_frame, text="🔍 搜索:",
                            font=("微软雅黑", 9),
                            fg="#2C3E50", bg="white")
    search_label.pack(side=tk.LEFT, padx=(0, 5))

    search_var = tk.StringVar()
    widgets.search_entry = tk.Entry(search_frame,
                                    textvariable=search_var,
                                    font=("微软雅黑", 9),
                                    width=18,  # 减小宽度
                                    relief=tk.SOLID,
                                    borderwidth=1,
                                    highlightthickness=1,
                                    highlightcolor="#3498DB")
    widgets.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

    widgets.search_entry.insert(0, "搜索角色...")  # 简化提示文字
    widgets.search_entry.config(fg="grey")

    # ===== 角色列表区域 =====
    list_frame = tk.Frame(main_container, bg="white")
    list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

    widgets.listbox = tk.Listbox(list_frame,
                                 font=("微软雅黑", 9),
                                 selectmode=tk.SINGLE,
                                 bg="white",
                                 fg="#2C3E50",
                                 selectbackground="#3498DB",
                                 selectforeground="white",
                                 relief=tk.FLAT,
                                 highlightthickness=1,
                                 highlightcolor="#BDC3C7",
                                 highlightbackground="#BDC3C7")
    widgets.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=widgets.listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    widgets.listbox.config(yscrollcommand=scrollbar.set)

    # ===== 按钮区域 =====
    button_frame = tk.Frame(main_container, bg="white")
    button_frame.pack(fill=tk.X, pady=(0, 10))

    def toggle_at_check():
        """切换@检查功能"""
        global check_at_enabled
        check_at_enabled = not check_at_enabled

        if check_at_enabled:
            at_check_button.config(text="@检查: 开", bg="#c56030", activebackground="#c56030")
            widgets.status_label.config(text="@检查功能已开启 - 文本中包含@时将直接发送文本")
            print("@检查功能已开启")
        else:
            at_check_button.config(text="@检查: 关", bg="#000000", activebackground="#000000")
            widgets.status_label.config(text="@检查功能已关闭")
            print("@检查功能已关闭")

    switch_button = tk.Button(button_frame, text="切换角色",
                              command=lambda: on_switch(),
                              bg="#c56030", fg="white", font=("微软雅黑", 9),
                              activebackground="#c56030", activeforeground="white",
                              relief=tk.FLAT, padx=12, pady=3, width=8)
    switch_button.pack(side=tk.LEFT, padx=3)

    refresh_button = tk.Button(button_frame, text="刷新列表",
                               command=lambda: refresh_list(),
                               bg="#c56030", fg="white", font=("微软雅黑", 9),
                               activebackground="#c56030", activeforeground="white",
                               relief=tk.FLAT, padx=12, pady=3, width=8)
    refresh_button.pack(side=tk.LEFT, padx=3)

    clear_button = tk.Button(button_frame, text="清除图片", command=on_clear_images,
                             bg="#c56030", fg="white", font=("微软雅黑", 9),
                             activebackground="#c56030", activeforeground="white",
                             relief=tk.FLAT, padx=12, pady=3, width=8)
    clear_button.pack(side=tk.LEFT, padx=3)

    # 添加@检查开关按钮
    at_check_button = tk.Button(button_frame, text="@检查: 关",
                                command=toggle_at_check,
                                bg="#000000", fg="white", font=("微软雅黑", 9),
                                activebackground="#c56030", activeforeground="white",
                                relief=tk.FLAT, padx=12, pady=3, width=8)
    at_check_button.pack(side=tk.LEFT, padx=3)
    # 退出按钮
    quit_button = tk.Button(button_frame, text="退出程序", command=on_quit,
                            bg="#c56030", fg="white", font=("微软雅黑", 9),
                            activebackground="#c56030", activeforeground="white",
                            relief=tk.FLAT, padx=12, pady=3, width=8)
    quit_button.pack(side=tk.LEFT, padx=3)

    # 状态栏
    at_info_label = tk.Label(main_container,
                             text="开启后，文本中包含@时将撤销剪切并直接发送文本",
                             font=("微软雅黑", 8),
                             fg="#666666",
                             bg="white",
                             wraplength=400,
                             justify=tk.LEFT)
    at_info_label.pack(fill=tk.X, pady=(0, 5))

    status_frame = tk.Frame(main_container, bg="#ECF0F1", height=20)
    status_frame.pack(fill=tk.X)
    status_frame.pack_propagate(False)
    widgets.status_label = tk.Label(status_frame,
                                    text="双击角色名称切换角色 | 默认使用皮肤1，可选择其他皮肤 | Ctrl+Shift+S显示/隐藏窗口",
                                    font=("微软雅黑", 8),
                                    fg="#666666",
                                    bg="#ECF0F1",
                                    anchor=tk.W,
                                    padx=8)
    widgets.status_label.pack(fill=tk.BOTH, expand=True)

    # ========== 第三步：定义所有函数 ==========
    def update_skin_combo(character_name):
        """更新皮肤选择下拉菜单"""
        skin_count = character[character_name]["emotion_count"]
        skin_options = [f"皮肤{i}" for i in range(1, skin_count + 1)]  # 移除"随机"选项
        widgets.skin_combo['values'] = skin_options

        if character_name in user_selected_skins:
            selected_skin = user_selected_skins[character_name]
            if 1 <= selected_skin <= skin_count:
                widgets.skin_combo.set(f"皮肤{selected_skin}")
                # 更新预览
                bg_num = None
                if character_name in user_selected_background:
                    bg_num = user_selected_background[character_name]
                update_preview(character_name, selected_skin, bg_num)
            else:
                widgets.skin_combo.set("皮肤1")  # 设置回第一个皮肤
                update_preview()
        else:
            widgets.skin_combo.set("皮肤1")  # 默认选择第一个皮肤
            update_preview()
    def on_skin_selected(event=None):
        """当用户选择皮肤时，立即将该皮肤设置为当前角色的输出并更新预览"""
        global user_selected_skins, special_feature_enabled, expression

        current_character = get_current_character()
        current_chinese_name = character_chinese_names.get(current_character, current_character)
        selected_text = skin_var.get()

        # 解析皮肤编号
        try:
            skin_num = int(selected_text.replace("皮肤", ""))
            skin_count = character[current_character]["emotion_count"]

            if 1 <= skin_num <= skin_count:
                user_selected_skins[current_character] = skin_num

                if current_character == SPECIAL_CHARACTER:
                    special_feature_enabled = True
                    widgets.special_button.config(text="🔓 特殊功能: 十六进制", bg="#d1652f", activebackground="#d1652f")
                    widgets.status_label.config(
                        text=f"{current_chinese_name} 已固定使用皮肤{skin_num}，特殊功能已开启")
                elif current_character == DOG_BARK_CHARACTER:
                    special_feature_enabled = True
                    widgets.special_button.config(text="🔓 特殊功能: 狗叫", bg="#d1652f", activebackground="#d1652f")
                    widgets.status_label.config(
                        text=f"{current_chinese_name} 已固定使用皮肤{skin_num}，狗叫功能已开启")
                else:
                    special_feature_enabled = False
                    widgets.status_label.config(text=f"{current_chinese_name} 已固定使用皮肤{skin_num}")

                expression = skin_num
                widgets.current_label.config(text=f"当前使用: {current_chinese_name} (皮肤{skin_num})")
                print(f"{current_chinese_name} 已设置为使用皮肤{skin_num}")

                # 更新预览
                bg_num = None
                if current_character in user_selected_background:
                    bg_num = user_selected_background[current_character]
                update_preview(current_character, skin_num, bg_num)

                if hasattr(widgets, 'listbox') and widgets.listbox.winfo_exists():
                    for i, char in enumerate(character_list):
                        if char == current_character:
                            widgets.listbox.selection_clear(0, tk.END)
                            if i < widgets.listbox.size():
                                widgets.listbox.selection_set(i)
                                widgets.listbox.see(i)
                            break
            else:
                messagebox.showwarning("错误", f"皮肤编号无效，该角色只有 {skin_count} 个皮肤")
                skin_var.set("皮肤1")  # 设置回第一个皮肤
                update_preview()

        except Exception as e:
            print(f"解析皮肤选择时出错: {e}")
            # 设置回第一个皮肤并重新调用
            skin_var.set("皮肤1")
            on_skin_selected(None)

    def search_characters():
        search_text = widgets.search_entry.get().strip()

        if search_text == "搜索角色...":
            widgets.listbox.delete(0, tk.END)
            current_display_indices.clear()

            for i, character_name in enumerate(character_list, 1):
                chinese_name = character_chinese_names.get(character_name, character_name)
                widgets.listbox.insert(tk.END, f"{i:3d}. {chinese_name}")
                current_display_indices.append(i - 1)

            widgets.status_label.config(text=f"共 {len(character_list)} 个角色，双击角色名称切换")
            return

        widgets.listbox.delete(0, tk.END)
        current_display_indices.clear()

        if search_text == "":
            for i, character_name in enumerate(character_list, 1):
                chinese_name = character_chinese_names.get(character_name, character_name)
                widgets.listbox.insert(tk.END, f"{i:3d}. {chinese_name}")
                current_display_indices.append(i - 1)
            widgets.status_label.config(text=f"共 {len(character_list)} 个角色，双击角色名称切换")
            return

        matched_count = 0
        search_text_lower = search_text.lower()

        for i, character_name in enumerate(character_list, 1):
            chinese_name = character_chinese_names.get(character_name, character_name)

            if (search_text_lower in chinese_name.lower() or
                    search_text_lower in character_name.lower()):
                widgets.listbox.insert(tk.END, f"{i:3d}. {chinese_name}")
                current_display_indices.append(i - 1)
                matched_count += 1

        if matched_count > 0:
            widgets.status_label.config(text=f"找到 {matched_count} 个匹配的角色")
        else:
            widgets.status_label.config(text="未找到匹配的角色，请尝试其他关键词")

    def refresh_list():
        """刷新列表，显示所有角色"""
        widgets.listbox.delete(0, tk.END)
        current_display_indices.clear()

        for i, character_name in enumerate(character_list, 1):
            chinese_name = character_chinese_names.get(character_name, character_name)
            widgets.listbox.insert(tk.END, f"{i:3d}. {chinese_name}")
            current_display_indices.append(i - 1)

        if current_character_index > 0:
            widgets.listbox.selection_set(current_character_index - 1)
            widgets.listbox.see(current_character_index - 1)

        widgets.status_label.config(text=f"共 {len(character_list)} 个角色，双击角色名称切换")
        update_skin_combo(get_current_character())
        update_bg_combo(get_current_character())

    def on_select(event):
        selection = widgets.listbox.curselection()
        if selection:
            index_in_display = selection[0]

            if index_in_display < len(current_display_indices):
                original_index = current_display_indices[index_in_display]
                selected_character = character_list[original_index]
                selected_chinese_name = character_chinese_names.get(selected_character, selected_character)
                widgets.current_label.config(text=f"当前选中: {selected_chinese_name}")

                nonlocal current_selected_character, current_selected_chinese_name
                current_selected_character = selected_character
                current_selected_chinese_name = selected_chinese_name

                update_skin_combo(selected_character)
                update_bg_combo(selected_character)  # 更新背景选择
                update_special_button()

                # 更新预览
                skin_num = None
                if selected_character in user_selected_skins:
                    skin_num = user_selected_skins[selected_character]
                bg_num = None
                if selected_character in user_selected_background:
                    bg_num = user_selected_background[selected_character]
                update_preview(selected_character, skin_num, bg_num)
            else:
                widgets.current_label.config(text="当前选中: 无效选择")

    def on_double_click(event):
        selection = widgets.listbox.curselection()
        if selection:
            index_in_display = selection[0]

            if index_in_display < len(current_display_indices):
                original_index = current_display_indices[index_in_display]
                selected_character = character_list[original_index]
                selected_chinese_name = character_chinese_names.get(selected_character, selected_character)

                if switch_character(original_index + 1):
                    widgets.status_label.config(text=f"正在加载{selected_chinese_name}...")
                    root.update()

                    if selected_character in user_selected_skins:
                        skin_num = user_selected_skins[selected_character]
                        if 1 <= skin_num <= character[selected_character]["emotion_count"]:
                            skin_var.set(f"皮肤{skin_num}")
                            on_skin_selected(None)

                            if selected_character == SPECIAL_CHARACTER:
                                global special_feature_enabled
                                special_feature_enabled = True
                                widgets.special_button.config(text="🔓 特殊: 开", bg="#d1652f",
                                                              activebackground="#d1652f")
                                widgets.status_label.config(
                                    text=f"已切换到{selected_chinese_name}，使用皮肤{skin_num}，特殊功能已开启")
                            else:
                                widgets.status_label.config(text=f"已切换到{selected_chinese_name}，使用皮肤{skin_num}")
                    else:
                        skin_var.set("皮肤1")  # 改为"皮肤1"
                        on_skin_selected(None)
                        widgets.status_label.config(text=f"已切换到{selected_chinese_name}，使用皮肤1")

                    root.title(f"角色选择 - 当前角色: {selected_chinese_name}")
                    refresh_list()
                    update_skin_combo(selected_character)
                    update_bg_combo(selected_character)  # 更新背景选择

                    if selected_character in user_selected_skins:
                        skin_num = user_selected_skins[selected_character]
                        widgets.current_label.config(text=f"当前使用: {selected_chinese_name} (皮肤{skin_num})")
                    else:
                        widgets.current_label.config(text=f"当前使用: {selected_chinese_name} (皮肤1)")  # 修改这里

                    # 更新预览
                    skin_num = None
                    if selected_character in user_selected_skins:
                        skin_num = user_selected_skins[selected_character]
                    bg_num = None
                    if selected_character in user_selected_background:
                        bg_num = user_selected_background[selected_character]
                    update_preview(selected_character, skin_num, bg_num)
            else:
                widgets.status_label.config(text="选择无效，请重新选择")
        else:
            widgets.status_label.config(text="请先选择一个角色")

    def on_switch():
        selection = widgets.listbox.curselection()
        if selection:
            index_in_display = selection[0]

            if index_in_display < len(current_display_indices):
                original_index = current_display_indices[index_in_display]
                selected_character = character_list[original_index]
                selected_chinese_name = character_chinese_names.get(selected_character, selected_character)

                if switch_character(original_index + 1):
                    widgets.status_label.config(text=f"正在加载{selected_chinese_name}...")
                    root.update()

                    if selected_character in user_selected_skins:
                        skin_num = user_selected_skins[selected_character]
                        if 1 <= skin_num <= character[selected_character]["emotion_count"]:
                            skin_var.set(f"皮肤{skin_num}")
                            on_skin_selected(None)

                            if selected_character == SPECIAL_CHARACTER:
                                global special_feature_enabled
                                special_feature_enabled = True
                                widgets.special_button.config(text="🔓 特殊: 开", bg="#d1652f",
                                                              activebackground="#d1652f")
                                widgets.status_label.config(
                                    text=f"已切换到{selected_chinese_name}，使用皮肤{skin_num}，特殊功能已开启")
                            else:
                                widgets.status_label.config(text=f"已切换到{selected_chinese_name}，使用皮肤{skin_num}")
                    else:
                        skin_var.set("皮肤1")  # 改为"皮肤1"
                        on_skin_selected(None)
                        widgets.status_label.config(text=f"已切换到{selected_chinese_name}，使用皮肤1")

                    root.title(f"角色选择 - 当前角色: {selected_chinese_name}")
                    refresh_list()
                    update_skin_combo(selected_character)
                    update_bg_combo(selected_character)  # 更新背景选择

                    if selected_character in user_selected_skins:
                        skin_num = user_selected_skins[selected_character]
                        widgets.current_label.config(text=f"当前使用: {selected_chinese_name} (皮肤{skin_num})")
                    else:
                        widgets.current_label.config(text=f"当前使用: {selected_chinese_name} (皮肤1)")  # 修改这里

                    # 更新预览
                    skin_num = None
                    if selected_character in user_selected_skins:
                        skin_num = user_selected_skins[selected_character]
                    bg_num = None
                    if selected_character in user_selected_background:
                        bg_num = user_selected_background[selected_character]
                    update_preview(selected_character, skin_num, bg_num)
            else:
                widgets.status_label.config(text="选择无效，请重新选择")
        else:
            widgets.status_label.config(text="请先选择一个角色")
    #绑定事件

    # 绑定背景选择事件
    widgets.bg_combo.bind("<<ComboboxSelected>>", on_bg_selected)

    # 绑定皮肤选择事件
    widgets.skin_combo.bind("<<ComboboxSelected>>", on_skin_selected)

    # 绑定搜索事件
    search_var.trace('w', lambda name, index, mode, sv=search_var: search_characters())

    # 绑定搜索框焦点事件
    is_searching = False

    def on_search_entry_focus_in(event):
        nonlocal is_searching
        is_searching = True
        if widgets.search_entry.get() == "搜索角色...":
            widgets.search_entry.delete(0, tk.END)
            widgets.search_entry.config(fg="black")

    def on_search_entry_focus_out(event):
        nonlocal is_searching
        is_searching = False
        current_text = widgets.search_entry.get().strip()
        if current_text == "":
            widgets.search_entry.insert(0, "搜索角色...")
            widgets.search_entry.config(fg="grey")

    widgets.search_entry.bind("<FocusIn>", on_search_entry_focus_in)
    widgets.search_entry.bind("<FocusOut>", on_search_entry_focus_out)

    # 绑定列表框事件
    widgets.listbox.bind('<<ListboxSelect>>', on_select)
    widgets.listbox.bind('<Double-Button-1>', on_double_click)

    # ========== 第五步：初始化 ==========

    # 初始化列表
    refresh_list()

    # 更新特殊功能按钮
    update_special_button()

    # 使窗口居中显示
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    # 启动窗口
    root.mainloop()
# 主程序入口
def main():
    print("程序启动中...")

    # 初始化角色窗口
    window_thread = threading.Thread(target=create_character_selection_window, daemon=True)
    window_thread.start()

    # 等待窗口创建
    time.sleep(0.5)

    # 显示当前角色信息
    show_current_character()

    # 绑定快捷键
    keyboard.add_hotkey('ctrl+shift+s', toggle_character_window)
    # 绑定 Ctrl+Alt+H 作为全局热键
    ok = keyboard.add_hotkey(HOTKEY, run_start_in_thread, suppress=BLOCK_HOTKEY or HOTKEY == SEND_HOTKEY)

    # 绑定Ctrl+0显示当前角色
    keyboard.add_hotkey('ctrl+0', show_current_character)

    print("程序已启动，按Enter生成图片，按Esc退出程序")
    print("按Ctrl+Tab清除生成的图片")
    print("按Ctrl+Shift+S显示/隐藏角色选择窗口")
    print("角色选择窗口已打开，可随时切换角色")
    print(f"总共有 {len(character_list)} 个角色")
    print(f"最后一个角色是: {character_chinese_names.get(character_list[-1], character_list[-1])}")

    # 保持程序运行
    keyboard.wait("Esc")

    # 退出程序
    print("程序正在退出...")
    if character_window and character_window.winfo_exists():
        character_window.quit()
    print("程序已退出")


if __name__ == "__main__":
    main()