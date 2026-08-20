#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MyText v3.2 Alpha 若您进入为英文，进入HELP菜单即可修改
本程序初期开发漏洞排查由ChatGPT 5辅助完成
非常不建议您精细查看代码，因为本程序注释十分模糊且代码编写极差
"""

import tkinter as tk
from tkinter import ttk, filedialog, font as tkfont, messagebox, simpledialog
import os, sys, random, string, hashlib, base64, re, json, html
from datetime import datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import urllib.parse

# 文字统一管理
LANG = {
    "zh": {
        "file": "文件", "edit": "编辑", "view": "视图", "tools": "工具",
        "convert": "转换", "encrypt_menu": "加密", "help": "帮助",
        "new_tab": "新建标签页", "close_tab": "关闭标签页",
        "new": "新建", "open": "打开...", "save": "保存", "save_as": "另存为...",
        "print": "打印...", "exit": "退出",
        "undo": "撤销", "redo": "重做", "cut": "剪切", "copy": "复制",
        "paste": "粘贴", "delete": "删除", "select_all": "全选",
        "find": "查找...", "replace": "替换...", "goto": "转到行...",
        "insert_time": "插入日期和时间",
        "word_wrap": "自动换行", "font_menu": "字体...",
        "zoom_in": "放大", "zoom_out": "缩小", "zoom_reset": "重置缩放",
        "theme_light": "浅色主题", "theme_dark": "深色主题",
        "status_bar": "状态栏", "fullscreen": "全屏",
        "case_conv": "大小写 / 命名",
        "line_conv": "行处理",
        "encode_conv": "编码 / 解码",
        "hash_conv": "哈希",
        "format_conv": "格式化",
        "code_conv": "代码转换",
        "batch_conv": "批量操作",
        "newline_conv": "换行符",
        "to_uppercase": "转大写", "to_lowercase": "转小写",
        "title_case": "Title Case", "sentence_case": "Sentence case",
        "camel_case": "camelCase", "pascal_case": "PascalCase",
        "snake_case": "snake_case", "kebab_case": "kebab-case",
        "screaming_snake": "SCREAMING_SNAKE",
        "trim_spaces": "去除多余空格", "remove_empty_lines": "删除空行",
        "trim_lines": "去除行首尾空格", "add_line_numbers": "添加行号",
        "remove_line_numbers": "移除行号",
        "tabs_to_spaces": "Tab → 空格", "spaces_to_tabs": "空格 → Tab",
        "sort_lines": "排序行", "reverse_lines": "反转行",
        "shuffle_lines": "随机打乱", "remove_duplicates": "去重",
        "base64_encode": "Base64 编码", "base64_decode": "Base64 解码",
        "url_encode": "URL 编码", "url_decode": "URL 解码",
        "html_encode": "HTML 编码", "html_decode": "HTML 解码",
        "unicode_escape": "Unicode 转义", "unicode_unescape": "Unicode 反转义",
        "md5_hash": "MD5", "sha1_hash": "SHA-1",
        "sha256_hash": "SHA-256", "sha512_hash": "SHA-512",
        "json_format": "JSON 格式化", "json_minify": "JSON 压缩",
        "xml_format": "XML 格式化", "sql_format": "SQL 格式化",
        "csv_align": "CSV 对齐",
        "to_csharp_string": "转 C# 字符串", "to_python_string": "转 Python 字符串",
        "add_prefix": "添加前缀...", "add_suffix": "添加后缀...",
        "remove_first_chars": "移除前 N 字符...", "remove_last_chars": "移除后 N 字符...",
        "newline_crlf": "换行符 → CRLF", "newline_lf": "换行符 → LF",
        "newline_cr": "换行符 → CR",
        "text_stats": "文本统计",
        "encrypt_password": "密码加密...", "decrypt_password": "密码解密...",
        "encrypt_mtep": "MTEP 密钥加密...", "decrypt_mtep": "MTEP 密钥解密...",
        "language": "语言", "chinese": "中文", "english": "English",
        "about": "关于 MyText", "help_contents": "帮助内容",
        "app_title": "MyText",
        "unsaved_title": "未保存的更改",
        "unsaved_msg": "文件尚未保存，是否保存？",
        "confirm": "确认", "error": "错误", "success": "成功", "info": "信息", "warning": "警告",
        "ready": "就绪", "chars": "字符", "words": "单词", "lines": "行", "bytes": "字节",
        "col": "列", "ln": "行", "zoom_label": "缩放",
        "find_title": "查找", "find_prompt": "请输入要查找的文本：",
        "replace_title": "替换", "replace_prompt": "请输入要查找的文本：",
        "replace_with_prompt": "请输入替换为的文本：",
        "goto_title": "转到行", "goto_prompt": "请输入行号：",
        "password_title": "密码加密", "password_prompt": "请输入加密密码：",
        "password_encrypt_success": "密码加密成功！",
        "password_decrypt_success": "密码解密成功！",
        "password_wrong": "密码错误或文件损坏！",
        "mtep_encrypt_title": "MTEP 加密",
        "mtep_encrypt_msg": "MTEP 加密完成！密钥文件已保存。",
        "mtep_decrypt_title": "MTEP 解密",
        "mtep_decrypt_msg": "请选择对应的 .mtepkey 密钥文件：",
        "mtep_key_missing": "未找到对应的密钥文件！",
        "stats_title": "文本统计", "about_title": "关于",
        "about_text": "MyText v3.2\n\n\n基于Python\n极简快速\n\nMyText 仅发布于GITHUB\n\n E-mail Nxhegmk@gmail.com",
        "theme_switching": "正在切换主题...",
        "file_saved": "文件已保存", "file_loaded": "文件已加载",
        "filter_txt": "文本文件", "filter_all": "所有文件",
        "filter_mtep": "MTEP 加密文件", "filter_mtepkey": "MTEP 密钥文件",
        "no_selection": "（无选区）", "select_range_prompt": "请先选中要操作的文本范围",
        "prefix_prompt": "请输入前缀：", "suffix_prompt": "请输入后缀：",
        "remove_chars_prompt": "请输入要移除的字符数：",
        "not_found": "未找到匹配项", "found_count": "找到 %d 处匹配",
        "pwd_too_short": "密码至少4个字符",
        "enter_replace": "替换为：",
        "line_num": "行号：",
        "encrypt_done": "加密完成", "decrypt_done": "解密完成",
        "select_mtep": "选择MTEP文件", "select_keyfile": "选择密钥文件",
        "save_encrypted": "保存加密文件", "save_as_mtep": "保存为MTEP加密文件",
        "invalid_mtep": "不是有效的 MTEP 加密文件",
        "key_mismatch": "密钥文件不匹配或文件已损坏！",
        "editor_label": "MyText 文本编辑器",
        "close": "关闭",
        "no_content": "没有可加密的内容",
        "tab_untitled": "未命名",
        "tab_close_confirm": "该标签页有未保存的更改，确定关闭？",
        "next_tab": "下一个标签页", "prev_tab": "上一个标签页",
        "tab_rightclick_close": "关闭标签页",
        "tab_rightclick_close_others": "关闭其他标签页",
        "tab_rightclick_new": "新建标签页",
    },
    "en": {
        "file": "File", "edit": "Edit", "view": "View", "tools": "Tools",
        "convert": "Convert", "encrypt_menu": "Encrypt", "help": "Help",
        "new_tab": "New Tab", "close_tab": "Close Tab",
        "new": "New", "open": "Open...", "save": "Save", "save_as": "Save As...",
        "print": "Print...", "exit": "Exit",
        "undo": "Undo", "redo": "Redo", "cut": "Cut", "copy": "Copy",
        "paste": "Paste", "delete": "Delete", "select_all": "Select All",
        "find": "Find...", "replace": "Replace...", "goto": "Go To Line...",
        "insert_time": "Insert Date/Time",
        "word_wrap": "Word Wrap", "font_menu": "Font...",
        "zoom_in": "Zoom In", "zoom_out": "Zoom Out", "zoom_reset": "Reset Zoom",
        "theme_light": "Light Theme", "theme_dark": "Dark Theme",
        "status_bar": "Status Bar", "fullscreen": "Fullscreen",
        "case_conv": "Case / Naming",
        "line_conv": "Line Ops",
        "encode_conv": "Encode / Decode",
        "hash_conv": "Hash",
        "format_conv": "Format",
        "code_conv": "Code Convert",
        "batch_conv": "Batch Ops",
        "newline_conv": "Newline",
        "to_uppercase": "To UPPERCASE", "to_lowercase": "To lowercase",
        "title_case": "Title Case", "sentence_case": "Sentence case",
        "camel_case": "camelCase", "pascal_case": "PascalCase",
        "snake_case": "snake_case", "kebab_case": "kebab-case",
        "screaming_snake": "SCREAMING_SNAKE",
        "trim_spaces": "Trim Extra Spaces", "remove_empty_lines": "Remove Empty Lines",
        "trim_lines": "Trim Line Edges", "add_line_numbers": "Add Line Numbers",
        "remove_line_numbers": "Remove Line Numbers",
        "tabs_to_spaces": "Tab → Spaces", "spaces_to_tabs": "Spaces → Tab",
        "sort_lines": "Sort Lines", "reverse_lines": "Reverse Lines",
        "shuffle_lines": "Shuffle Lines", "remove_duplicates": "Remove Duplicates",
        "base64_encode": "Base64 Encode", "base64_decode": "Base64 Decode",
        "url_encode": "URL Encode", "url_decode": "URL Decode",
        "html_encode": "HTML Encode", "html_decode": "HTML Decode",
        "unicode_escape": "Unicode Escape", "unicode_unescape": "Unicode Unescape",
        "md5_hash": "MD5", "sha1_hash": "SHA-1",
        "sha256_hash": "SHA-256", "sha512_hash": "SHA-512",
        "json_format": "JSON Format", "json_minify": "JSON Minify",
        "xml_format": "XML Format", "sql_format": "SQL Format",
        "csv_align": "CSV Align",
        "to_csharp_string": "To C# String", "to_python_string": "To Python String",
        "add_prefix": "Add Prefix...", "add_suffix": "Add Suffix...",
        "remove_first_chars": "Remove First N Chars...", "remove_last_chars": "Remove Last N Chars...",
        "newline_crlf": "Newline → CRLF", "newline_lf": "Newline → LF",
        "newline_cr": "Newline → CR",
        "text_stats": "Text Statistics",
        "encrypt_password": "Encrypt with Password...", "decrypt_password": "Decrypt with Password...",
        "encrypt_mtep": "Encrypt with MTEP Key...", "decrypt_mtep": "Decrypt with MTEP Key...",
        "language": "Language", "chinese": "中文", "english": "English",
        "about": "About MyText", "help_contents": "Help Contents",
        "app_title": "MyText",
        "unsaved_title": "Unsaved Changes",
        "unsaved_msg": "File has unsaved changes. Save now?",
        "confirm": "Confirm", "error": "Error", "success": "Success", "info": "Info", "warning": "Warning",
        "ready": "Ready", "chars": "Chars", "words": "Words", "lines": "Lines", "bytes": "Bytes",
        "col": "Col", "ln": "Ln", "zoom_label": "Zoom",
        "find_title": "Find", "find_prompt": "Enter text to find:",
        "replace_title": "Replace", "replace_prompt": "Enter text to find:",
        "replace_with_prompt": "Replace with:",
        "goto_title": "Go To Line", "goto_prompt": "Enter line number:",
        "password_title": "Password Encrypt", "password_prompt": "Enter encryption password:",
        "password_encrypt_success": "Password encryption successful!",
        "password_decrypt_success": "Password decryption successful!",
        "password_wrong": "Wrong password or corrupted file!",
        "mtep_encrypt_title": "MTEP Encrypt",
        "mtep_encrypt_msg": "MTEP encryption done! Key file saved.",
        "mtep_decrypt_title": "MTEP Decrypt",
        "mtep_decrypt_msg": "Select the .mtepkey file:",
        "mtep_key_missing": "Key file not found!",
        "stats_title": "Text Statistics", "about_title": "About",
        "about_text": "MyText v3.2\nMinimalist Powerful Text Editor\n\nPython / Tkinter\nMinimal deps (cryptography only)\n\n© 2026 MyText Project",
        "theme_switching": "Switching theme...",
        "file_saved": "File saved", "file_loaded": "File loaded",
        "filter_txt": "Text Files", "filter_all": "All Files",
        "filter_mtep": "MTEP Files", "filter_mtepkey": "MTEP Key Files",
        "no_selection": "(no selection)", "select_range_prompt": "Please select text first",
        "prefix_prompt": "Enter prefix:", "suffix_prompt": "Enter suffix:",
        "remove_chars_prompt": "Enter number of chars to remove:",
        "not_found": "Not found", "found_count": "Found %d matches",
        "pwd_too_short": "Password must be at least 4 characters",
        "enter_replace": "Replace with:",
        "line_num": "Line:",
        "encrypt_done": "Encryption done", "decrypt_done": "Decryption done",
        "select_mtep": "Select MTEP file", "select_keyfile": "Select key file",
        "save_encrypted": "Save encrypted file", "save_as_mtep": "Save as MTEP encrypted file",
        "invalid_mtep": "Not a valid MTEP file",
        "key_mismatch": "Key file mismatch or file corrupted!",
        "editor_label": "MyText Minimalist Powerful Text Editor",
        "close": "Close",
        "no_content": "No content to encrypt",
        "tab_untitled": "Untitled",
        "tab_close_confirm": "This tab has unsaved changes. Close anyway?",
        "next_tab": "Next Tab", "prev_tab": "Previous Tab",
        "tab_rightclick_close": "Close Tab",
        "tab_rightclick_close_others": "Close Other Tabs",
        "tab_rightclick_new": "New Tab",
    }
}

current_lang = "zh"

def T(key):
    return LANG[current_lang].get(key, key)

#标签状态
class TabState:
    """标签页状态"""
    def __init__(self):
        self.file_path = None
        self.modified = False

class AppState:
    def __init__(self):
        self.word_wrap = True
        self.dark_theme = False
        self.zoom_pct = 100
        self.fullscreen = False

state = AppState()

#主题
THEMES = {
    "light": {
        "bg": "#FFFFFF", "fg": "#000000",
        "status_bg": "#F0F0F0", "status_fg": "#3C3C3C",
        "sel_bg": "#0078D7", "sel_fg": "#FFFFFF",
        "menu_bg": "#FFFFFF", "menu_fg": "#000000",
        "toolbar_bg": "#F8F8F8", "toolbar_fg": "#333333",
        "notebook_bg": "#E8E8E8",
        "insert_bg": "#FFFFFF", "insert_fg": "#000000",
    },
    "dark": {
        "bg": "#1E1E1E", "fg": "#DCDCDC",
        "status_bg": "#2D2D2D", "status_fg": "#B4B4B4",
        "sel_bg": "#0096FF", "sel_fg": "#FFFFFF",
        "menu_bg": "#2D2D2D", "menu_fg": "#DCDCDC",
        "toolbar_bg": "#252525", "toolbar_fg": "#DCDCDC",
        "notebook_bg": "#333333",
        "insert_bg": "#1E1E1E", "insert_fg": "#DCDCDC",
    }
}

#加密引擎
def derive_key_pbkdf2(password, salt, iterations=100000):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32,
                      salt=salt, iterations=iterations, backend=default_backend())
    return kdf.derive(password.encode('utf-8'))

def aes256_encrypt(key, iv, data):
    padder = padding.PKCS7(128).padder()
    padded = padder.update(data) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(padded) + encryptor.finalize()

def aes256_decrypt(key, iv, data):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded = decryptor.update(data) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(padded) + unpadder.finalize()

def calc_hmac_sha256(key, data):
    return hashlib.sha256(key + data).digest()

#字体BUG修复(ChatGPT)
def get_safe_font():
    """防倒转"""
    try:
        available = list(tkfont.families())
        preferred = [
            "Microsoft YaHei",
            "Segoe UI",
            "SimHei",
            "Noto Sans CJK SC",
            "Consolas",
            "Courier New",
        ]
        for f in preferred:
            if f in available:
                return (f, 14)
        if available:
            return (available[0], 14)
    except:
        pass
    return ("TkDefaultFont", 14)

# ==================== 应用程序类 ====================
class MyTextApp:
    def __init__(self, root):
        self.root = root
        self.root.title(T("app_title"))
        self.root.geometry("950x680")
        self.root.minsize(550, 380)

        try:
            self.root.iconname("MyText")
        except:
            pass

        # 标签页管理：tab_id -> {text, frame, state}
        self.tabs = {}
        self.tab_order = []  # 保持顺序
        self.current_tab_id = None
        self._tab_counter = 0

        self._build_ui()
        self._bind_events()
        self._apply_theme()

        # 创建初始标签页
        self._new_tab()

        # 命令行参数打开文件
        if len(sys.argv) > 1:
            self._open_file_path(sys.argv[1])

    #GUI
    def _build_ui(self):
        # 工具栏
        self.toolbar = tk.Frame(self.root, relief=tk.FLAT, bd=0)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        btn_cfg = dict(relief=tk.FLAT, padx=8, pady=4, font=("Segoe UI", 9))
        self.b_new = tk.Button(self.toolbar, text="📄 " + T("new"), command=self._new_file, **btn_cfg)
        self.b_open = tk.Button(self.toolbar, text="📂 " + T("open"), command=self._open_file, **btn_cfg)
        self.b_save = tk.Button(self.toolbar, text="💾 " + T("save"), command=self._save_file, **btn_cfg)
        self.b_save_as = tk.Button(self.toolbar, text="💿 " + T("save_as"), command=self._save_as, **btn_cfg)
        self.b_find = tk.Button(self.toolbar, text="🔍 " + T("find"), command=self._show_find, **btn_cfg)
        self.b_replace = tk.Button(self.toolbar, text="🔄 " + T("replace"), command=self._show_replace, **btn_cfg)
        self.b_undo = tk.Button(self.toolbar, text="↩ " + T("undo"), command=self._undo, **btn_cfg)
        self.b_redo = tk.Button(self.toolbar, text="↪ " + T("redo"), command=self._redo, **btn_cfg)
        self.b_theme = tk.Button(self.toolbar, text="🌙", command=self._toggle_theme, **btn_cfg)
        self.b_stats = tk.Button(self.toolbar, text="📊 " + T("text_stats"), command=self._show_stats, **btn_cfg)

        for b in [self.b_new, self.b_open, self.b_save, self.b_save_as,
                  self.b_find, self.b_replace, self.b_undo, self.b_redo,
                  self.b_theme, self.b_stats]:
            b.pack(side=tk.LEFT, padx=1)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)
        self.notebook.bind("<Button-3>", self._on_tab_rightclick)
        self.notebook.bind("<Double-1>", self._on_tab_doubleclick)
        self.status_bar = tk.Frame(self.root, relief=tk.FLAT, height=26)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_left = tk.Label(self.status_bar, text=T("ready"), anchor=tk.W, font=("Segoe UI", 9))
        self.status_left.pack(side=tk.LEFT, padx=8)
        self.status_right = tk.Label(self.status_bar, text="", anchor=tk.E, font=("Segoe UI", 9))
        self.status_right.pack(side=tk.RIGHT, padx=8)
        self._build_menu()

        self.tab_menu = tk.Menu(self.root, tearoff=0)
        self.tab_menu.add_command(label=T("tab_rightclick_new"), command=self._new_tab)
        self.tab_menu.add_command(label=T("tab_rightclick_close"), command=self._close_current_tab)
        self.tab_menu.add_command(label=T("tab_rightclick_close_others"), command=self._close_other_tabs)

    def _build_menu(self):
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        self.m_file = tk.Menu(self.menubar, tearoff=0)
        self.m_file.add_command(label=T("new_tab"), accelerator="Ctrl+T", command=self._new_tab)
        self.m_file.add_command(label=T("new"), accelerator="Ctrl+N", command=self._new_file)
        self.m_file.add_command(label=T("open"), accelerator="Ctrl+O", command=self._open_file)
        self.m_file.add_command(label=T("save"), accelerator="Ctrl+S", command=self._save_file)
        self.m_file.add_command(label=T("save_as"), command=self._save_as)
        self.m_file.add_separator()
        self.m_file.add_command(label=T("close_tab"), accelerator="Ctrl+W", command=self._close_current_tab)
        self.m_file.add_separator()
        self.m_file.add_command(label=T("print"), command=self._print)
        self.m_file.add_separator()
        self.m_file.add_command(label=T("exit"), command=self._on_close)
        self.menubar.add_cascade(label=T("file"), menu=self.m_file)
        self.m_edit = tk.Menu(self.menubar, tearoff=0)
        self.m_edit.add_command(label=T("undo"), accelerator="Ctrl+Z", command=self._undo)
        self.m_edit.add_command(label=T("redo"), accelerator="Ctrl+Y", command=self._redo)
        self.m_edit.add_separator()
        self.m_edit.add_command(label=T("cut"), accelerator="Ctrl+X", command=self._cut)
        self.m_edit.add_command(label=T("copy"), accelerator="Ctrl+C", command=self._copy)
        self.m_edit.add_command(label=T("paste"), accelerator="Ctrl+V", command=self._paste)
        self.m_edit.add_command(label=T("delete"), command=self._delete)
        self.m_edit.add_separator()
        self.m_edit.add_command(label=T("select_all"), accelerator="Ctrl+A", command=self._select_all)
        self.m_edit.add_separator()
        self.m_edit.add_command(label=T("find"), accelerator="Ctrl+F", command=self._show_find)
        self.m_edit.add_command(label=T("replace"), accelerator="Ctrl+H", command=self._show_replace)
        self.m_edit.add_command(label=T("goto"), accelerator="Ctrl+G", command=self._show_goto)
        self.m_edit.add_command(label=T("insert_time"), command=self._insert_time)
        self.menubar.add_cascade(label=T("edit"), menu=self.m_edit)
        self.m_view = tk.Menu(self.menubar, tearoff=0)
        self.wrap_var = tk.BooleanVar(value=state.word_wrap)
        self.m_view.add_checkbutton(label=T("word_wrap"), variable=self.wrap_var, command=self._toggle_wrap)
        self.m_view.add_command(label=T("font_menu"), command=self._choose_font)
        self.m_view.add_separator()
        self.m_view.add_command(label=T("zoom_in"), accelerator="Ctrl++", command=self._zoom_in)
        self.m_view.add_command(label=T("zoom_out"), accelerator="Ctrl+-", command=self._zoom_out)
        self.m_view.add_command(label=T("zoom_reset"), command=self._zoom_reset)
        self.m_view.add_separator()
        self.theme_light_var = tk.BooleanVar(value=not state.dark_theme)
        self.theme_dark_var = tk.BooleanVar(value=state.dark_theme)
        self.m_view.add_checkbutton(label=T("theme_light"), variable=self.theme_light_var, command=lambda: self._set_theme(False))
        self.m_view.add_checkbutton(label=T("theme_dark"), variable=self.theme_dark_var, command=lambda: self._set_theme(True))
        self.m_view.add_separator()
        self.m_view.add_command(label=T("fullscreen"), command=self._toggle_fullscreen)
        self.menubar.add_cascade(label=T("view"), menu=self.m_view)

        self.m_tools = tk.Menu(self.menubar, tearoff=0)

        self.m_case = tk.Menu(self.m_tools, tearoff=0)
        self.m_case.add_command(label=T("to_uppercase"), command=lambda: self._apply_transform("upper"))
        self.m_case.add_command(label=T("to_lowercase"), command=lambda: self._apply_transform("lower"))
        self.m_case.add_separator()
        self.m_case.add_command(label=T("title_case"), command=lambda: self._apply_transform("title"))
        self.m_case.add_command(label=T("sentence_case"), command=lambda: self._apply_transform("sentence"))
        self.m_case.add_separator()
        self.m_case.add_command(label=T("camel_case"), command=lambda: self._apply_transform("camel"))
        self.m_case.add_command(label=T("pascal_case"), command=lambda: self._apply_transform("pascal"))
        self.m_case.add_command(label=T("snake_case"), command=lambda: self._apply_transform("snake"))
        self.m_case.add_command(label=T("kebab_case"), command=lambda: self._apply_transform("kebab"))
        self.m_case.add_command(label=T("screaming_snake"), command=lambda: self._apply_transform("screaming"))
        self.m_tools.add_cascade(label=T("case_conv"), menu=self.m_case)

        self.m_line = tk.Menu(self.m_tools, tearoff=0)
        self.m_line.add_command(label=T("trim_spaces"), command=lambda: self._apply_transform("trim_spaces"))
        self.m_line.add_command(label=T("trim_lines"), command=lambda: self._apply_transform("trim_lines"))
        self.m_line.add_command(label=T("remove_empty_lines"), command=lambda: self._apply_transform("remove_empty"))
        self.m_line.add_separator()
        self.m_line.add_command(label=T("add_line_numbers"), command=lambda: self._apply_transform("add_ln"))
        self.m_line.add_command(label=T("remove_line_numbers"), command=lambda: self._apply_transform("remove_ln"))
        self.m_line.add_separator()
        self.m_line.add_command(label=T("tabs_to_spaces"), command=lambda: self._apply_transform("tabs2sp"))
        self.m_line.add_command(label=T("spaces_to_tabs"), command=lambda: self._apply_transform("sp2tabs"))
        self.m_line.add_separator()
        self.m_line.add_command(label=T("sort_lines"), command=lambda: self._apply_transform("sort"))
        self.m_line.add_command(label=T("reverse_lines"), command=lambda: self._apply_transform("reverse"))
        self.m_line.add_command(label=T("shuffle_lines"), command=lambda: self._apply_transform("shuffle"))
        self.m_line.add_command(label=T("remove_duplicates"), command=lambda: self._apply_transform("dedup"))
        self.m_tools.add_cascade(label=T("line_conv"), menu=self.m_line)

        self.m_enc = tk.Menu(self.m_tools, tearoff=0)
        self.m_enc.add_command(label=T("base64_encode"), command=lambda: self._apply_transform("b64e"))
        self.m_enc.add_command(label=T("base64_decode"), command=lambda: self._apply_transform("b64d"))
        self.m_enc.add_separator()
        self.m_enc.add_command(label=T("url_encode"), command=lambda: self._apply_transform("urle"))
        self.m_enc.add_command(label=T("url_decode"), command=lambda: self._apply_transform("urld"))
        self.m_enc.add_separator()
        self.m_enc.add_command(label=T("html_encode"), command=lambda: self._apply_transform("htmle"))
        self.m_enc.add_command(label=T("html_decode"), command=lambda: self._apply_transform("htmld"))
        self.m_enc.add_separator()
        self.m_enc.add_command(label=T("unicode_escape"), command=lambda: self._apply_transform("uniesc"))
        self.m_enc.add_command(label=T("unicode_unescape"), command=lambda: self._apply_transform("uniunesc"))
        self.m_tools.add_cascade(label=T("encode_conv"), menu=self.m_enc)

        # 哈希
        self.m_hash = tk.Menu(self.m_tools, tearoff=0)
        self.m_hash.add_command(label=T("md5_hash"), command=lambda: self._apply_transform("md5"))
        self.m_hash.add_command(label=T("sha1_hash"), command=lambda: self._apply_transform("sha1"))
        self.m_hash.add_command(label=T("sha256_hash"), command=lambda: self._apply_transform("sha256"))
        self.m_hash.add_command(label=T("sha512_hash"), command=lambda: self._apply_transform("sha512"))
        self.m_tools.add_cascade(label=T("hash_conv"), menu=self.m_hash)

        # 格式化
        self.m_fmt = tk.Menu(self.m_tools, tearoff=0)
        self.m_fmt.add_command(label=T("json_format"), command=lambda: self._apply_transform("jsonf"))
        self.m_fmt.add_command(label=T("json_minify"), command=lambda: self._apply_transform("jsonm"))
        self.m_fmt.add_separator()
        self.m_fmt.add_command(label=T("xml_format"), command=lambda: self._apply_transform("xmlf"))
        self.m_fmt.add_separator()
        self.m_fmt.add_command(label=T("sql_format"), command=lambda: self._apply_transform("sqlf"))
        self.m_fmt.add_command(label=T("csv_align"), command=lambda: self._apply_transform("csva"))
        self.m_tools.add_cascade(label=T("format_conv"), menu=self.m_fmt)

        # 代码转换
        self.m_code = tk.Menu(self.m_tools, tearoff=0)
        self.m_code.add_command(label=T("to_csharp_string"), command=lambda: self._apply_transform("csharp"))
        self.m_code.add_command(label=T("to_python_string"), command=lambda: self._apply_transform("python"))
        self.m_tools.add_cascade(label=T("code_conv"), menu=self.m_code)

        #  批量操作
        self.m_batch = tk.Menu(self.m_tools, tearoff=0)
        self.m_batch.add_command(label=T("add_prefix"), command=self._add_prefix)
        self.m_batch.add_command(label=T("add_suffix"), command=self._add_suffix)
        self.m_batch.add_separator()
        self.m_batch.add_command(label=T("remove_first_chars"), command=self._remove_first)
        self.m_batch.add_command(label=T("remove_last_chars"), command=self._remove_last)
        self.m_tools.add_cascade(label=T("batch_conv"), menu=self.m_batch)

        #换行符
        self.m_nl = tk.Menu(self.m_tools, tearoff=0)
        self.m_nl.add_command(label=T("newline_crlf"), command=lambda: self._apply_transform("nl_crlf"))
        self.m_nl.add_command(label=T("newline_lf"), command=lambda: self._apply_transform("nl_lf"))
        self.m_nl.add_command(label=T("newline_cr"), command=lambda: self._apply_transform("nl_cr"))
        self.m_tools.add_cascade(label=T("newline_conv"), menu=self.m_nl)

        self.menubar.add_cascade(label=T("convert"), menu=self.m_tools)

        # 加密
        self.m_crypt = tk.Menu(self.menubar, tearoff=0)
        self.m_crypt.add_command(label=T("encrypt_password"), command=self._encrypt_password)
        self.m_crypt.add_command(label=T("decrypt_password"), command=self._decrypt_password)
        self.m_crypt.add_separator()
        self.m_crypt.add_command(label=T("encrypt_mtep"), command=self._encrypt_mtep)
        self.m_crypt.add_command(label=T("decrypt_mtep"), command=self._decrypt_mtep)
        self.menubar.add_cascade(label=T("encrypt_menu"), menu=self.m_crypt)

        # 文本统计
        self.menubar.add_command(label=T("text_stats"), command=self._show_stats)

        #帮助
        self.m_help = tk.Menu(self.menubar, tearoff=0)
        self.m_help.add_command(label=T("about"), command=self._show_about)

        self.m_lang = tk.Menu(self.m_help, tearoff=0)
        self.lang_var = tk.StringVar(value=current_lang)
        self.m_lang.add_radiobutton(label=T("chinese"), variable=self.lang_var, value="zh", command=self._set_lang_zh)
        self.m_lang.add_radiobutton(label=T("english"), variable=self.lang_var, value="en", command=self._set_lang_en)
        self.m_help.add_cascade(label=T("language"), menu=self.m_lang)

        self.menubar.add_cascade(label=T("help"), menu=self.m_help)

    def _rebuild_menu(self):
        try:
            self.root.config(menu="")
        except:
            pass
        self._build_menu()

    #标签页管理
    def _create_text_widget(self, parent):
        """创建一个新的文本编辑组件"""
        font_cfg = get_safe_font()

        text_frame = tk.Frame(parent)

        text = tk.Text(
            text_frame, wrap=tk.WORD if state.word_wrap else tk.NONE,
            font=font_cfg, insertwidth=2,
            relief=tk.FLAT, bd=0, padx=8, pady=8,
        )

        # 撤销机制
        try:
            text.configure(undo=True, maxundo=100)
        except:
            pass

        scrollbar = tk.Scrollbar(text_frame, command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        return text, text_frame

    def _new_tab(self, path=None):
        """创建新标签页"""
        self._tab_counter += 1
        tab_id = "tab_{}".format(self._tab_counter)

        tab_state = TabState()
        text, text_frame = self._create_text_widget(self.notebook)

        text.bind("<<Modified>>", lambda e, t=text: self._on_modified(e, t))
        text.bind("<KeyRelease>", lambda e, t=text: self._update_status_for_text(t))

        tab_info = {
            'id': tab_id,
            'text': text,
            'frame': text_frame,
            'state': tab_state,
        }

        self.tabs[tab_id] = tab_info
        self.tab_order.append(tab_id)

        display_name = T("tab_untitled") + " " + str(self._tab_counter)
        self.notebook.add(text_frame, text=display_name)

        # 切换到新标签
        self.notebook.select(text_frame)
        self.current_tab_id = tab_id

        if path:
            self._open_file_path_in_current(path)

        self._update_title()
        self._update_status()
        return tab_info

    def _new_file(self):
        """新建文件 → 总是创建新标签页"""
        self._new_tab()

    def _get_current_tab(self):
        """获取当前活动标签页信息"""
        if self.current_tab_id and self.current_tab_id in self.tabs:
            return self.tabs[self.current_tab_id]
        return None

    def _get_current_text(self):
        tab = self._get_current_tab()
        if tab:
            return tab['text']
        return None

    def _on_tab_changed(self, event):
        """Notebook 标签切换事件"""
        try:
            selected = self.notebook.select()
            if not selected:
                return
            for tid, tinfo in self.tabs.items():
                if str(tinfo['frame']) == selected:
                    self.current_tab_id = tid
                    break
        except:
            pass
        self._update_title()
        self._update_status()

    def _on_tab_rightclick(self, event):
        """右键点击标签 → 弹出菜单"""
        try:
            # 获取点击的标签索引
            idx = self.notebook.index("@%d,%d" % (event.x, event.y))
            self.notebook.select(idx)
            # 更新当前 tab
            selected = self.notebook.select()
            for tid, tinfo in self.tabs.items():
                if str(tinfo['frame']) == selected:
                    self.current_tab_id = tid
                    break
            # 刷新菜单文字
            self.tab_menu.entryconfigure(0, label=T("tab_rightclick_new"))
            self.tab_menu.entryconfigure(1, label=T("tab_rightclick_close"))
            self.tab_menu.entryconfigure(2, label=T("tab_rightclick_close_others"))
            self.tab_menu.tk_popup(event.x_root, event.y_root)
        except:
            pass

    def _on_tab_doubleclick(self, event):
        """双击标签 → 关闭该标签页"""
        try:
            idx = self.notebook.index("@%d,%d" % (event.x, event.y))
            self.notebook.select(idx)
            self._close_current_tab()
        except:
            pass

    def _close_current_tab(self):
        """关闭当前标签页"""
        tab = self._get_current_tab()
        if not tab:
            return
        self._close_tab_internal(tab)

        if not self.tabs:
            self._new_tab()

    def _close_other_tabs(self):
        """关闭除当前外的所有标签页"""
        current = self._get_current_tab()
        if not current:
            return
        to_close = [tid for tid in self.tab_order if tid != current['id']]
        for tid in to_close:
            if tid in self.tabs:
                self._close_tab_internal(self.tabs[tid], confirm_save=True)

    def _close_tab_internal(self, tab_info, confirm_save=False):
        """内部关闭标签页"""
        tab_id = tab_info['id']

        if tab_id not in self.tabs:
            return False

        if tab_info['state'].modified and confirm_save:
            self.notebook.select(tab_info['frame'])
            self.current_tab_id = tab_id
            r = messagebox.askyesnocancel(T("unsaved_title"), T("unsaved_msg"))
            if r is None:  # 取消
                return False
            if r:  # 是 - 保存
                self._save_file()
                if tab_id not in self.tabs:
                    self._refresh_tab_titles()
                    return True

        # 从 Notebook 移除
        try:
            self.notebook.forget(tab_info['frame'])
        except:
            pass

        # 销毁组件
        try:
            tab_info['text'].destroy()
            tab_info['frame'].destroy()
        except:
            pass

        # 从管理结构中移除
        if tab_id in self.tabs:
            del self.tabs[tab_id]
        if tab_id in self.tab_order:
            self.tab_order.remove(tab_id)

        # 更新当前标签
        if self.current_tab_id == tab_id:
            if self.tab_order:
                new_id = self.tab_order[-1]
                self.current_tab_id = new_id
                try:
                    self.notebook.select(self.tabs[new_id]['frame'])
                except:
                    pass
            else:
                self.current_tab_id = None

        self._update_title()
        self._update_status()
        return True

    def _refresh_tab_titles(self):
        """刷新所有标签的标题显示（修改状态、文件名变化）"""
        for tid in self.tab_order:
            if tid not in self.tabs:
                continue
            tab = self.tabs[tid]
            ts = tab['state']
            if ts.file_path:
                name = os.path.basename(ts.file_path)
            else:
                # 从 tab_order 位置推断编号
                idx_in_order = self.tab_order.index(tid) + 1
                name = T("tab_untitled") + " " + str(idx_in_order)

            mod_mark = " ●" if ts.modified else ""
            try:
                self.notebook.tab(tab['frame'], text=name + mod_mark)
            except:
                pass

    def _next_tab(self):
        if len(self.tab_order) > 1:
            idx = self.tab_order.index(self.current_tab_id)
            next_idx = (idx + 1) % len(self.tab_order)
            next_id = self.tab_order[next_idx]
            try:
                self.notebook.select(self.tabs[next_id]['frame'])
            except:
                pass

    def _prev_tab(self):
        if len(self.tab_order) > 1:
            idx = self.tab_order.index(self.current_tab_id)
            prev_idx = (idx - 1) % len(self.tab_order)
            prev_id = self.tab_order[prev_idx]
            try:
                self.notebook.select(self.tabs[prev_id]['frame'])
            except:
                pass

    # 事件绑定
    def _bind_events(self):
        self.root.bind("<Control-n>", lambda e: self._new_file())
        self.root.bind("<Control-t>", lambda e: self._new_tab())
        self.root.bind("<Control-o>", lambda e: self._open_file())
        self.root.bind("<Control-s>", lambda e: self._save_file())
        self.root.bind("<Control-w>", lambda e: self._close_current_tab())
        self.root.bind("<Control-z>", lambda e: self._undo())
        self.root.bind("<Control-y>", lambda e: self._redo())
        self.root.bind("<Control-f>", lambda e: self._show_find())
        self.root.bind("<Control-h>", lambda e: self._show_replace())
        self.root.bind("<Control-g>", lambda e: self._show_goto())
        self.root.bind("<Control-plus>", lambda e: self._zoom_in())
        self.root.bind("<Control-minus>", lambda e: self._zoom_out())
        self.root.bind("<Control-0>", lambda e: self._zoom_reset())
        self.root.bind("<Control-Tab>", lambda e: self._next_tab())
        self.root.bind("<Control-Shift-Tab>", lambda e: self._prev_tab())
        self.root.bind("<MouseWheel>", self._on_mousewheel)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    # 主题
    def _apply_theme(self):
        theme = THEMES["dark" if state.dark_theme else "light"]
        try:
            self.root.configure(bg=theme["bg"])
        except: pass
        try:
            self.toolbar.configure(bg=theme["toolbar_bg"])
        except: pass
        for child in self.toolbar.winfo_children():
            try:
                child.configure(bg=theme["toolbar_bg"], fg=theme["toolbar_fg"],
                                activebackground=theme["sel_bg"], activeforeground=theme["sel_fg"])
            except:
                pass

        # 应用到所有标签页的 text widget
        for tab in self.tabs.values():
            text = tab['text']
            try:
                text.configure(
                    bg=theme["bg"], fg=theme["fg"],
                    insertbackground=theme["fg"],
                    selectbackground=theme["sel_bg"], selectforeground=theme["sel_fg"],
                    relief=tk.FLAT, highlightthickness=0,
                )
            except: pass
            try:
                tab['frame'].configure(bg=theme["bg"])
            except: pass

        try:
            self.status_bar.configure(bg=theme["status_bg"])
            self.status_left.configure(bg=theme["status_bg"], fg=theme["status_fg"])
            self.status_right.configure(bg=theme["status_bg"], fg=theme["status_fg"])
        except: pass

        # Notebook 样式
        try:
            s = ttk.Style()
            s.configure("TNotebook", background=theme["notebook_bg"])
            s.configure("TNotebook.Tab",
                        background=theme["notebook_bg"],
                        foreground=theme["fg"],
                        padding=[12, 4])
            s.map("TNotebook.Tab",
                  background=[("selected", theme["bg"]), ("active", theme["notebook_bg"])],
                  foreground=[("selected", theme["fg"])])
        except: pass

        self._refresh_tab_titles()

    def _toggle_theme(self):
        self._set_theme(not state.dark_theme)

    def _set_theme(self, dark):
        state.dark_theme = dark
        self.theme_light_var.set(not dark)
        self.theme_dark_var.set(dark)
        self._apply_theme()
        self._update_status()
        try:
            self.b_theme.configure(text="☀️" if dark else "🌙")
        except: pass

    # 状态栏
    def _update_status(self):
        text = self._get_current_text()
        if text:
            self._update_status_for_text(text)
        else:
            try:
                self.status_left.configure(text=T("ready"))
                self.status_right.configure(text="")
            except:
                pass

    def _update_status_for_text(self, text):
        try:
            content = text.get("1.0", "end-1c")
        except:
            content = ""
        chars = len(content)
        lines = content.count('\n') + 1 if content else 1
        words = len([w for w in content.split() if w.strip()])

        try:
            cursor = text.index("insert")
            ln, col = cursor.split('.')
            ln = int(ln); col = int(col)
        except:
            ln, col = 1, 0

        mod = ""
        tab = self._get_current_tab()
        if tab and tab['state'].modified:
            mod = " ●"

        try:
            self.status_left.configure(text=f"{T('ready')}{mod}  |  {T('chars')}: {chars}  {T('words')}: {words}  {T('lines')}: {lines}")
            self.status_right.configure(text=f"{T('ln')} {ln}:{col}  |  {T('zoom_label')}: {state.zoom_pct}%")
        except:
            pass

    def _update_title(self):
        tab = self._get_current_tab()
        if not tab:
            self.root.title(T("app_title"))
            return
        ts = tab['state']
        mod = " ●" if ts.modified else ""
        if ts.file_path:
            self.root.title(f"{T('app_title')} - {os.path.basename(ts.file_path)}{mod}")
        else:
            idx = self.tab_order.index(tab['id']) + 1 if tab['id'] in self.tab_order else 1
            self.root.title(f"{T('app_title')} - {T('tab_untitled')} {idx}{mod}")

    # 文件操作
    def _open_file(self):
        path = filedialog.askopenfilename(
            title=T("open"),
            filetypes=[
                (T("filter_txt"), "*.txt"),
                (T("filter_mtep"), "*.mtep"),
                (T("filter_all"), "*.*"),
            ]
        )
        if path:
            cur = self._get_current_tab()
            if (cur and
                not cur['state'].file_path and
                not cur['state'].modified):
                self._open_file_path_in_current(path)
            else:
                self._new_tab(path)

    def _open_file_path(self, path):
        self._open_file_path_in_current(path)

    def _open_file_path_in_current(self, path):
        text = self._get_current_text()
        if not text:
            return

        ext = os.path.splitext(path)[1].lower()
        if ext == ".mtep":
            self._decrypt_mtep_with_file(path)
            return

        try:
            with open(path, 'rb') as f:
                raw = f.read()
            if raw[:3] == b'\xef\xbb\xbf':
                content = raw[3:].decode('utf-8')
            elif raw[:2] in (b'\xff\xfe', b'\xfe\xff'):
                content = raw.decode('utf-16')
            else:
                try:
                    content = raw.decode('utf-8')
                except:
                    content = raw.decode('gbk', errors='replace')

            text.delete("1.0", "end")
            text.insert("1.0", content)

            tab = self._get_current_tab()
            if tab:
                tab['state'].file_path = path
                tab['state'].modified = False

            try:
                text.edit_modified(False)
            except:
                pass

            self._update_title()
            try:
                self.status_left.configure(text=f"{T('ready')}  |  {T('file_loaded')}")
            except: pass
            self._update_status()
            self._refresh_tab_titles()
        except Exception as e:
            messagebox.showerror(T("error"), str(e))

    def _save_file(self):
        text = self._get_current_text()
        if not text:
            return

        tab = self._get_current_tab()
        if not tab:
            return

        ts = tab['state']

        if not ts.file_path:
            self._save_as()
            return

        try:
            content = text.get("1.0", "end-1c")
            with open(ts.file_path, 'wb') as f:
                f.write(b'\xef\xbb\xbf' + content.encode('utf-8'))
            ts.modified = False
            try:
                text.edit_modified(False)
            except:
                pass
            try:
                self.status_left.configure(text=f"{T('ready')}  |  {T('file_saved')}")
            except: pass
            self._update_title()
            self._update_status()
            self._refresh_tab_titles()
        except Exception as e:
            messagebox.showerror(T("error"), str(e))

    def _save_as(self):
        text = self._get_current_text()
        if not text:
            return

        path = filedialog.asksaveasfilename(
            title=T("save_as"),
            defaultextension=".txt",
            filetypes=[(T("filter_txt"), "*.txt"), (T("filter_all"), "*.*")]
        )
        if path:
            tab = self._get_current_tab()
            if tab:
                tab['state'].file_path = path
                self._save_file()
                self._refresh_tab_titles()

    def _print(self):
        messagebox.showinfo(T("info"), "打印功能需要系统支持。\n请您尝试Ctrl+P。")

    # 编辑操作
    def _undo(self):
        text = self._get_current_text()
        if text:
            try: text.edit_undo()
            except: pass
            self._update_status()

    def _redo(self):
        text = self._get_current_text()
        if text:
            try: text.edit_redo()
            except: pass
            self._update_status()

    def _cut(self):
        text = self._get_current_text()
        if text:
            try: text.event_generate("<<Cut>>")
            except: pass

    def _copy(self):
        text = self._get_current_text()
        if text:
            try: text.event_generate("<<Copy>>")
            except: pass

    def _paste(self):
        text = self._get_current_text()
        if text:
            try: text.event_generate("<<Paste>>")
            except: pass

    def _delete(self):
        text = self._get_current_text()
        if text:
            try: text.delete("sel.first", "sel.last")
            except: pass

    def _select_all(self):
        text = self._get_current_text()
        if text:
            try: text.tag_add("sel", "1.0", "end")
            except: pass

    def _insert_time(self):
        text = self._get_current_text()
        if text:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try: text.insert("insert", now)
            except: pass

    def _on_modified(self, event, text_widget):
        if not self.current_tab_id:
            return
        try:
            if text_widget.edit_modified():
                tab = self._get_current_tab()
                if tab:
                    tab['state'].modified = True
                    text_widget.edit_modified(False)
                    self._update_title()
                    self._update_status()
                    self._refresh_tab_titles()
        except:
            pass

    # 查找替换
    def _show_find(self):
        self._find_replace_dialog(False)

    def _show_replace(self):
        self._find_replace_dialog(True)

    def _find_replace_dialog(self, with_replace):
        dlg = tk.Toplevel(self.root)
        dlg.title(T("find_title") if not with_replace else T("replace_title"))
        dlg.geometry("420x180" if not with_replace else "420x240")
        dlg.transient(self.root)
        dlg.resizable(False, False)

        tk.Label(dlg, text=T("find_prompt")).pack(anchor=tk.W, padx=16, pady=(16,4))
        find_entry = tk.Entry(dlg, font=("Segoe UI", 11), width=40)
        find_entry.pack(padx=16, fill=tk.X)
        find_entry.focus_set()

        replace_entry = None
        if with_replace:
            tk.Label(dlg, text=T("replace_with_prompt")).pack(anchor=tk.W, padx=16, pady=(12,4))
            replace_entry = tk.Entry(dlg, font=("Segoe UI", 11), width=40)
            replace_entry.pack(padx=16, fill=tk.X)

        btn_frame = tk.Frame(dlg)
        btn_frame.pack(pady=16)

        def do_find():
            text = self._get_current_text()
            if not text: return
            target = find_entry.get()
            if not target: return
            try:
                start = text.index("insert")
                result = text.search(target, start, tk.END)
                if not result:
                    result = text.search(target, "1.0", tk.END)
                if result:
                    end = f"{result}+{len(target)}c"
                    text.tag_remove("sel", "1.0", "end")
                    text.tag_add("sel", result, end)
                    text.mark_set("insert", end)
                    text.see(result)
                else:
                    messagebox.showinfo(T("info"), T("not_found"))
            except Exception as e:
                messagebox.showerror(T("error"), str(e))

        def do_replace():
            text = self._get_current_text()
            if not text or not replace_entry: return
            target = find_entry.get()
            repl = replace_entry.get()
            try:
                content = text.get("1.0", "end-1c")
                if target in content:
                    new_content = content.replace(target, repl)
                    text.delete("1.0", "end")
                    text.insert("1.0", new_content)
                    messagebox.showinfo(T("success"), T("found_count") % content.count(target))
            except Exception as e:
                messagebox.showerror(T("error"), str(e))

        tk.Button(btn_frame, text=T("find_title"), command=do_find, width=10).pack(side=tk.LEFT, padx=4)
        if with_replace:
            tk.Button(btn_frame, text=T("replace_title"), command=do_replace, width=10).pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text=T("close"), command=dlg.destroy, width=10).pack(side=tk.LEFT, padx=4)

    def _show_goto(self):
        text = self._get_current_text()
        if not text: return
        val = simpledialog.askinteger(T("goto_title"), T("goto_prompt"), parent=self.root)
        if val:
            try:
                text.mark_set("insert", f"{max(1,val)}.0")
                text.see("insert")
            except: pass

    # 视图 
    def _toggle_wrap(self):
        state.word_wrap = self.wrap_var.get()
        for tab in self.tabs.values():
            try:
                tab['text'].configure(wrap=tk.WORD if state.word_wrap else tk.NONE)
            except: pass

    def _choose_font(self):
        try:
            fonts = list(tkfont.families())
        except:
            fonts = ["Microsoft YaHei", "Segoe UI", "Consolas", "SimHei", "Arial"]
        cjk_keywords = ['yahei', 'ya hei', '宋体', '黑体', '楷体', '仿宋', '思源', 'noto', 'cjk', 'ming', 'simsun', 'simhei', 'wenquan']
        cjk_fonts = [f for f in fonts if any(k in f.lower() for k in cjk_keywords)]
        other_fonts = [f for f in fonts if f not in cjk_fonts]
        fonts_sorted = sorted(cjk_fonts) + sorted(other_fonts)

        dlg = tk.Toplevel(self.root)
        dlg.title(T("font_menu"))
        dlg.geometry("350x400")
        dlg.transient(self.root)

        tk.Label(dlg, text="字体:").pack(anchor=tk.W, padx=12, pady=(12,4))
        lb = tk.Listbox(dlg, height=12)
        for f in fonts_sorted: lb.insert(tk.END, f)
        lb.pack(padx=12, fill=tk.BOTH, expand=True)

        size_var = tk.IntVar(value=14)
        tk.Label(dlg, text="大小:").pack(anchor=tk.W, padx=12, pady=(8,4))
        tk.Spinbox(dlg, from_=8, to=36, textvariable=size_var, width=10).pack(anchor=tk.W, padx=12)

        def apply():
            sel = lb.curselection()
            if sel:
                f = lb.get(sel[0])
                for tab in self.tabs.values():
                    try:
                        tab['text'].configure(font=(f, size_var.get()))
                    except: pass
            dlg.destroy()

        tk.Button(dlg, text=T("confirm"), command=apply).pack(pady=8)

    def _zoom_in(self):
        state.zoom_pct = min(500, state.zoom_pct + 10)
        self._refresh_font_size()
        self._update_status()

    def _zoom_out(self):
        state.zoom_pct = max(30, state.zoom_pct - 10)
        self._refresh_font_size()
        self._update_status()

    def _zoom_reset(self):
        state.zoom_pct = 100
        self._refresh_font_size()
        self._update_status()

    def _refresh_font_size(self):
        try:
            cur = self._get_current_text()
            if cur:
                cur_font = cur.cget("font")
                if isinstance(cur_font, str):
                    parts = cur_font.split()
                    name = parts[0] if parts else "Microsoft YaHei"
                elif isinstance(cur_font, tuple):
                    name = cur_font[0]
                else:
                    name = "Microsoft YaHei"
                cjk_names = ["Microsoft YaHei", "SimHei", "SimSun", "Noto Sans CJK SC", "WenQuanYi Micro Hei"]
                if name not in cjk_names:
                    name = "Microsoft YaHei"
                base = 14
                for tab in self.tabs.values():
                    try:
                        tab['text'].configure(font=(name, int(base * state.zoom_pct / 100)))
                    except: pass
        except:
            pass

    def _toggle_fullscreen(self):
        state.fullscreen = not state.fullscreen
        try:
            self.root.attributes("-fullscreen", state.fullscreen)
        except: pass

    def _on_mousewheel(self, event):
        if event.state & 0x4:  # Ctrl
            if event.delta > 0: self._zoom_in()
            else: self._zoom_out()
            return "break"

    # 文本转换引擎
    def _get_selection_or_all(self):
        text = self._get_current_text()
        if not text:
            return "", False
        try:
            sel = text.get("sel.first", "sel.last")
            return sel, True
        except:
            try:
                return text.get("1.0", "end-1c"), False
            except:
                return "", False

    def _replace_text(self, new_text, had_selection):
        text = self._get_current_text()
        if not text: return
        if had_selection:
            try:
                text.delete("sel.first", "sel.last")
                text.insert("sel.first", new_text)
            except:
                try:
                    text.delete("1.0", "end")
                    text.insert("1.0", new_text)
                except: pass
        else:
            try:
                text.delete("1.0", "end")
                text.insert("1.0", new_text)
            except: pass
        self._update_status()

    def _apply_transform(self, transform):
        text, has_sel = self._get_selection_or_all()
        if not text:
            return
        result = text

        if transform == "upper": result = text.upper()
        elif transform == "lower": result = text.lower()
        elif transform == "title": result = text.title()
        elif transform == "sentence":
            result = '. '.join(s.strip().capitalize() for s in text.split('. '))
        elif transform == "camel":
            words = re.findall(r'[a-zA-Z0-9]+', text)
            if words:
                result = words[0].lower() + ''.join(w.capitalize() for w in words[1:])
            else: result = text.lower().replace(' ', '')
        elif transform == "pascal":
            words = re.findall(r'[a-zA-Z0-9]+', text)
            result = ''.join(w.capitalize() for w in words) if words else text.title().replace(' ', '')
        elif transform == "snake": result = re.sub(r'[^a-zA-Z0-9]+', '_', text).strip('_').lower()
        elif transform == "kebab": result = re.sub(r'[^a-zA-Z0-9]+', '-', text).strip('-').lower()
        elif transform == "screaming": result = re.sub(r'[^a-zA-Z0-9]+', '_', text).strip('_').upper()
        elif transform == "trim_spaces":
            result = '\n'.join(re.sub(r' +', ' ', line) for line in text.split('\n'))
        elif transform == "remove_empty":
            result = '\n'.join(line for line in text.split('\n') if line.strip())
        elif transform == "trim_lines":
            result = '\n'.join(line.strip() for line in text.split('\n'))
        elif transform == "add_ln":
            result = '\n'.join(f"{i+1}. {l}" for i, l in enumerate(text.split('\n')))
        elif transform == "remove_ln":
            lines = text.split('\n')
            cleaned = []
            for l in lines:
                m = re.match(r'^\d+[\.\)]\s*', l)
                cleaned.append(l[m.end():] if m else l)
            result = '\n'.join(cleaned)
        elif transform == "tabs2sp": result = text.replace('\t', '    ')
        elif transform == "sp2tabs": result = re.sub(r' {4}', '\t', text)
        elif transform == "sort": result = '\n'.join(sorted(text.split('\n')))
        elif transform == "reverse": result = '\n'.join(reversed(text.split('\n')))
        elif transform == "shuffle":
            lines = text.split('\n'); random.shuffle(lines); result = '\n'.join(lines)
        elif transform == "dedup":
            seen = set(); lines = []
            for l in text.split('\n'):
                if l not in seen: seen.add(l); lines.append(l)
            result = '\n'.join(lines)
        elif transform == "b64e": result = base64.b64encode(text.encode('utf-8')).decode('ascii')
        elif transform == "b64d":
            try: result = base64.b64decode(text.encode('ascii')).decode('utf-8')
            except: result = text
        elif transform == "urle": result = urllib.parse.quote(text, safe='')
        elif transform == "urld": result = urllib.parse.unquote(text)
        elif transform == "htmle":
            esc = {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}
            result = ''.join(esc.get(c, c if ord(c)<128 else f'&#{ord(c)};') for c in text)
        elif transform == "htmld": result = html.unescape(text)
        elif transform == "uniesc":
            result = ''.join(f'\\u{ord(c):04x}' if ord(c)>127 else c for c in text)
        elif transform == "uniunesc":
            try: result = text.encode('utf-8').decode('unicode_escape')
            except: result = text
        elif transform == "md5": result = hashlib.md5(text.encode('utf-8')).hexdigest()
        elif transform == "sha1": result = hashlib.sha1(text.encode('utf-8')).hexdigest()
        elif transform == "sha256": result = hashlib.sha256(text.encode('utf-8')).hexdigest()
        elif transform == "sha512": result = hashlib.sha512(text.encode('utf-8')).hexdigest()
        elif transform == "jsonf":
            try:
                obj = json.loads(text)
                result = json.dumps(obj, indent=2, ensure_ascii=False)
            except: result = text
        elif transform == "jsonm":
            try:
                obj = json.loads(text)
                result = json.dumps(obj, separators=(',', ':'), ensure_ascii=False)
            except: result = re.sub(r'\s+', '', text)
        elif transform == "xmlf":
            text = re.sub(r'>\s+<', '><', text)
            result = ""
            indent = 0
            for token in re.split(r'(<[^>]+>)', text):
                if not token: continue
                if token.startswith('</'):
                    indent -= 1
                    result += '  ' * indent + token + '\n'
                elif token.startswith('<') and not token.startswith('<!--'):
                    result += '  ' * indent + token + '\n'
                    if not token.endswith('/>') and not token.startswith('<?'):
                        indent += 1
                else:
                    result += '  ' * indent + token.strip() + '\n'
        elif transform == "sqlf":
            keywords = ['SELECT','FROM','WHERE','AND','OR','INSERT','UPDATE','DELETE','CREATE','TABLE','JOIN','LEFT','RIGHT','INNER','OUTER','GROUP BY','ORDER BY','HAVING','LIMIT']
            result = text
            for kw in keywords:
                result = re.sub(rf'\b{kw}\b', kw, result, flags=re.IGNORECASE)
            result = re.sub(r'\s+', ' ', result).strip()
            for kw in keywords:
                result = result.replace(f' {kw} ', f'\n{kw} ')
        elif transform == "csva":
            lines = text.split('\n')
            rows = [l.split(',') for l in lines if l.strip()]
            if rows:
                max_cols = max(len(r) for r in rows)
                col_widths = [max(len(r[i]) if i<len(r) else 0 for r in rows) for i in range(max_cols)]
                result = '\n'.join(' | '.join((r[i] if i<len(r) else '').ljust(col_widths[i]) for i in range(max_cols)) for r in rows)
            else: result = text
        elif transform == "csharp":
            lines = text.split('\n')
            result = '\n'.join('"' + l.replace('\\','\\\\').replace('"','\\"') + '" +' for l in lines)
            if result.endswith('+'):
                result = result[:-1].rstrip()
        elif transform == "python":
            lines = text.split('\n')
            result = '\n'.join('"' + l.replace('\\','\\\\').replace('"','\\"') + '"' for l in lines)
        elif transform == "nl_crlf": result = text.replace('\r\n','\n').replace('\r','\n').replace('\n','\r\n')
        elif transform == "nl_lf": result = text.replace('\r\n','\n').replace('\r','\n')
        elif transform == "nl_cr": result = text.replace('\r\n','\n').replace('\n','\r')

        self._replace_text(result, has_sel)

    def _add_prefix(self):
        val = simpledialog.askstring(T("add_prefix"), T("prefix_prompt"))
        if val is None: return
        text, has_sel = self._get_selection_or_all()
        result = '\n'.join(val + l for l in text.split('\n'))
        self._replace_text(result, has_sel)

    def _add_suffix(self):
        val = simpledialog.askstring(T("add_suffix"), T("suffix_prompt"))
        if val is None: return
        text, has_sel = self._get_selection_or_all()
        result = '\n'.join(l + val for l in text.split('\n'))
        self._replace_text(result, has_sel)

    def _remove_first(self):
        val = simpledialog.askinteger(T("remove_first_chars"), T("remove_chars_prompt"), minvalue=1)
        if val is None: return
        text, has_sel = self._get_selection_or_all()
        result = text[val:] if len(text) > val else ""
        self._replace_text(result, has_sel)

    def _remove_last(self):
        val = simpledialog.askinteger(T("remove_last_chars"), T("remove_chars_prompt"), minvalue=1)
        if val is None: return
        text, has_sel = self._get_selection_or_all()
        result = text[:-val] if len(text) > val else ""
        self._replace_text(result, has_sel)

    # 加密
    def _encrypt_password(self):
        text = ""
        cur = self._get_current_text()
        if cur:
            try: text = cur.get("1.0", "end-1c")
            except: pass
        if not text:
            messagebox.showerror(T("error"), T("no_content"))
            return

        pwd = simpledialog.askstring(T("password_title"), T("password_prompt"), show='*')
        if not pwd or len(pwd) < 4:
            if pwd is not None: messagebox.showwarning(T("warning"), T("pwd_too_short"))
            return

        salt = os.urandom(16)
        iv = os.urandom(16)
        key = derive_key_pbkdf2(pwd, salt, 100000)
        data = text.encode('utf-8')
        encrypted = aes256_encrypt(key, iv, data)

        out = b'MTEP' + bytes([1]) + salt + iv + (100000).to_bytes(4, 'big') + encrypted

        path = filedialog.asksaveasfilename(
            title=T("save_encrypted"),
            defaultextension=".mtep",
            filetypes=[(T("filter_mtep"), "*.mtep")]
        )
        if path:
            with open(path, 'wb') as f: f.write(out)
            messagebox.showinfo(T("success"), T("password_encrypt_success"))

    def _decrypt_password(self):
        path = filedialog.askopenfilename(
            title=T("select_mtep"),
            filetypes=[(T("filter_mtep"), "*.mtep")]
        )
        if not path: return

        with open(path, 'rb') as f: data = f.read()
        if data[:4] != b'MTEP':
            messagebox.showerror(T("error"), T("invalid_mtep"))
            return

        ver = data[4]
        salt = data[5:21]
        iv = data[21:37]
        iterations = int.from_bytes(data[37:41], 'big')
        ct = data[41:]

        pwd = simpledialog.askstring(T("password_title"), T("password_prompt"), show='*')
        if not pwd: return

        key = derive_key_pbkdf2(pwd, salt, iterations)
        try:
            decrypted = aes256_decrypt(key, iv, ct)
            text_content = decrypted.decode('utf-8')
            new_tab = self._new_tab()
            new_tab['text'].delete("1.0", "end")
            new_tab['text'].insert("1.0", text_content)
            new_tab['state'].modified = True
            self._update_title()
            self._refresh_tab_titles()
            try:
                self.status_left.configure(text=f"{T('ready')}  |  {T('decrypt_done')}")
            except: pass
            self._update_status()
        except Exception:
            messagebox.showerror(T("error"), T("password_wrong"))

    def _encrypt_mtep(self):
        text = ""
        cur = self._get_current_text()
        if cur:
            try: text = cur.get("1.0", "end-1c")
            except: pass
        if not text:
            messagebox.showerror(T("error"), T("no_content"))
            return

        master_key = os.urandom(32)
        salt = os.urandom(16)
        iv = os.urandom(16)
        iterations = 100000

        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32,
                         salt=salt, iterations=iterations, backend=default_backend())
        aes_key = kdf.derive(master_key)

        data = text.encode('utf-8')
        encrypted = aes256_encrypt(aes_key, iv, data)

        hmac_key = os.urandom(32)
        hmac_val = calc_hmac_sha256(hmac_key, encrypted)

        out = b'MTEP' + bytes([2]) + salt + iterations.to_bytes(4,'big') + iv + hmac_key + hmac_val + encrypted

        path = filedialog.asksaveasfilename(
            title=T("save_as_mtep"),
            defaultextension=".mtep",
            filetypes=[(T("filter_mtep"), "*.mtep")]
        )
        if not path: return

        with open(path, 'wb') as f: f.write(out)

        key_data = master_key + salt + iterations.to_bytes(4,'big') + iv + hmac_key + hmac_val
        key_path = path + ".mtepkey"
        with open(key_path, 'wb') as f: f.write(key_data)

        messagebox.showinfo(T("success"), T("mtep_encrypt_msg"))

    def _decrypt_mtep(self):
        path = filedialog.askopenfilename(
            title=T("select_mtep"),
            filetypes=[(T("filter_mtep"), "*.mtep")]
        )
        if not path: return
        self._decrypt_mtep_with_file(path)

    def _decrypt_mtep_with_file(self, path):
        key_path = path + ".mtepkey"
        if not os.path.exists(key_path):
            key_path = filedialog.askopenfilename(
                title=T("mtep_decrypt_msg"),
                filetypes=[(T("filter_mtepkey"), "*.mtepkey")]
            )
            if not key_path:
                messagebox.showerror(T("error"), T("mtep_key_missing"))
                return

        with open(path, 'rb') as f: data = f.read()
        with open(key_path, 'rb') as f: key_data = f.read()

        if data[:4] != b'MTEP':
            messagebox.showerror(T("error"), T("invalid_mtep"))
            return

        p = 5
        salt = data[p:p+16]; p+=16
        iterations = int.from_bytes(data[p:p+4], 'big'); p+=4
        iv = data[p:p+16]; p+=16
        hmac_key = data[p:p+32]; p+=32
        stored_hmac = data[p:p+32]; p+=32
        ct = data[p:]

        calc_hmac = calc_hmac_sha256(hmac_key, ct)
        if calc_hmac != stored_hmac:
            messagebox.showerror(T("error"), T("key_mismatch"))
            return

        master_key = key_data[:32]

        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32,
                         salt=salt, iterations=iterations, backend=default_backend())
        derived = kdf.derive(master_key)

        try:
            decrypted = aes256_decrypt(derived, iv, ct)
            text_content = decrypted.decode('utf-8')
            new_tab = self._new_tab()
            new_tab['text'].delete("1.0", "end")
            new_tab['text'].insert("1.0", text_content)
            new_tab['state'].modified = True
            self._update_title()
            self._refresh_tab_titles()
            try:
                self.status_left.configure(text=f"{T('ready')}  |  {T('decrypt_done')}")
            except: pass
            self._update_status()
        except Exception:
            messagebox.showerror(T("error"), T("password_wrong"))

    # 统计
    def _show_stats(self):
        text = self._get_current_text()
        if not text: return
        try:
            content = text.get("1.0", "end-1c")
        except:
            content = ""
        chars = len(content)
        lines = content.count('\n') + 1 if content else 1
        words = len([w for w in content.split() if w.strip()])
        try:
            bytes_utf8 = len(content.encode('utf-8'))
        except:
            bytes_utf8 = 0

        msg = f"{T('chars')}: {chars}\n{T('words')}: {words}\n{T('lines')}: {lines}\n{T('bytes')}: {bytes_utf8}\n{T('zoom_label')}: {state.zoom_pct}%"
        messagebox.showinfo(T("stats_title"), msg)

    # 语言切换
    def _set_lang_zh(self):
        global current_lang
        current_lang = "zh"
        self._refresh_ui_text()

    def _set_lang_en(self):
        global current_lang
        current_lang = "en"
        self._refresh_ui_text()

    def _refresh_ui_text(self):
        try:
            self.b_new.configure(text="📄 " + T("new"))
            self.b_open.configure(text="📂 " + T("open"))
            self.b_save.configure(text="💾 " + T("save"))
            self.b_save_as.configure(text="💿 " + T("save_as"))
            self.b_find.configure(text="🔍 " + T("find"))
            self.b_replace.configure(text="🔄 " + T("replace"))
            self.b_undo.configure(text="↩ " + T("undo"))
            self.b_redo.configure(text="↪ " + T("redo"))
            self.b_stats.configure(text="📊 " + T("text_stats"))
            self.b_theme.configure(text="☀️" if state.dark_theme else "🌙")
        except: pass

        self._rebuild_menu()
        self._update_title()
        self._update_status()
        self._refresh_tab_titles()
        self._apply_theme()

    #关于
    def _show_about(self):
        messagebox.showinfo(T("about_title"), T("about_text"))

    # 关闭
    def _on_close(self):
        # 检查所有标签页
        for tid in list(self.tab_order):
            if tid not in self.tabs:
                continue
            tab = self.tabs[tid]
            if tab['state'].modified:
                self.notebook.select(tab['frame'])
                self.current_tab_id = tid
                r = messagebox.askyesnocancel(T("unsaved_title"), T("unsaved_msg"))
                if r is None: return  # 取消退出
                if r:  # 保存
                    self._save_file()

        try: self.root.destroy()
        except: pass

#启动
if __name__ == "__main__":
    root = tk.Tk()
    app = MyTextApp(root)
    root.mainloop()
