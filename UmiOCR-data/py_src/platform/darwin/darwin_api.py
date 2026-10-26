# ==============================================
# =============== macOS系统API =================
# ==============================================

import os
import sys
import shlex
import subprocess
from PySide2.QtCore import QStandardPaths as Qsp

from umi_log import logger
from umi_about import UmiAbout


# ==================== 快捷方式 ====================
class _Shortcut:
    @staticmethod
    def _getPath(position):
        if position == "desktop":
            return os.path.expanduser("~/Desktop")
        elif position == "startMenu":
            apps = os.path.expanduser("~/Applications")
            if not os.path.exists(apps):
                os.makedirs(apps, exist_ok=True)
            return apps
        elif position == "startup":
            launch_agents = os.path.expanduser("~/Library/LaunchAgents")
            if not os.path.exists(launch_agents):
                os.makedirs(launch_agents, exist_ok=True)
            return launch_agents
        return os.path.expanduser("~")

    @staticmethod
    def createShortcut(position):
        try:
            lnkName = UmiAbout["name"]
            appPath = UmiAbout["app"]["path"]
            if not appPath:
                return "[Error] 未找到程序入口文件。\n[Error] App path does not exist."

            destDir = _Shortcut._getPath(position)
            if position in ("desktop", "startMenu"):
                lnkPath = os.path.join(destDir, lnkName)
                if os.path.exists(lnkPath) or os.path.islink(lnkPath):
                    os.remove(lnkPath)
                os.symlink(appPath, lnkPath)
                logger.info(f"创建快捷方式： {lnkPath}")
                return "[Success]"
            elif position == "startup":
                plist_path = os.path.join(destDir, "com.umiocr.desktop.plist")
                plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.umiocr.desktop</string>
    <key>ProgramArguments</key>
    <array>
        <string>{appPath}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
"""
                with open(plist_path, "w", encoding="utf-8") as f:
                    f.write(plist_content)
                logger.info(f"创建开机启动配置： {plist_path}")
                return "[Success]"
        except Exception as e:
            return f"[Error] 创建快捷方式失败。\n[Error] Failed to create shortcut: {e}"

    @staticmethod
    def deleteShortcut(position):
        try:
            lnkName = UmiAbout["name"]
            destDir = _Shortcut._getPath(position)
            num = 0
            if position in ("desktop", "startMenu"):
                lnkPath = os.path.join(destDir, lnkName)
                if os.path.islink(lnkPath) or os.path.exists(lnkPath):
                    os.remove(lnkPath)
                    num += 1
            elif position == "startup":
                plist_path = os.path.join(destDir, "com.umiocr.desktop.plist")
                if os.path.exists(plist_path):
                    os.remove(plist_path)
                    num += 1
            return num
        except Exception as e:
            logger.error(f"删除快捷方式失败: {e}", exc_info=True)
            return 0


# ==================== 硬件控制 ====================
class _HardwareCtrl:
    @staticmethod
    def shutdown():
        try:
            subprocess.run(["osascript", "-e", 'tell app "System Events" to shut down'], check=False)
        except Exception as e:
            logger.error(f"关机指令执行异常: {e}")

    @staticmethod
    def hibernate():
        try:
            subprocess.run(["osascript", "-e", 'tell app "System Events" to sleep'], check=False)
        except Exception as e:
            logger.error(f"休眠指令执行异常: {e}")


# ==================== 对外接口 ====================
class Api:
    Shortcut = _Shortcut()
    HardwareCtrl = _HardwareCtrl()

    @staticmethod
    def getOpenGLUse():
        return "AA_UseDesktopOpenGL"

    @staticmethod
    def getKeyName(key):
        if not isinstance(key, str):
            if hasattr(key, "name") and key.name:
                key = key.name
            elif hasattr(key, "char") and key.char:
                key = key.char
            else:
                key = str(key)
        if not key:
            return "unknown"
        if key.startswith("'") and key.endswith("'"):
            key = key[1:-1]
        if key.startswith("Key."):
            key = key[4:]
        if "_" in key:
            key = key.split("_", 1)[0]
        return key.lower() if key else "unknown"

    @staticmethod
    def runNewProcess(path, args=""):
        cmd = shlex.split(args) if args else []
        if path.endswith(".py"):
            cmd = [sys.executable, path] + cmd
        else:
            cmd = [path] + cmd
        subprocess.Popen(cmd)

    @staticmethod
    def startfile(path):
        subprocess.Popen(["open", path])
