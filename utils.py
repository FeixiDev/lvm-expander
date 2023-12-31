import subprocess
import logging
import datetime
import socket
import sys
import yaml
import re
import time


def get_host_ip():
    """
    查询本机ip地址
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def check_ip(ip):
    """检查IP格式"""
    re_ip = re.compile(
        r'^((2([0-4]\d|5[0-5]))|[1-9]?\d|1\d{2})(\.((2([0-4]\d|5[0-5]))|[1-9]?\d|1\d{2})){3}$')
    result = re_ip.match(ip)
    if result:
        return True
    else:
        print(f"ERROR in IP format of {ip}, please check.")
        return False


def exec_cmd(cmd):
    result = subprocess.getoutput(cmd)
    result = result.decode() if isinstance(result, bytes) else result
    log_data = f'{get_host_ip()} - {cmd} - {result}'
    Log().logger.info(log_data)
    if result:
        result = result.rstrip('\n')
    return result


class ConfFile(object):
    def __init__(self):
        self.yaml_file = "lvm_config.yaml"
        self.config = self.read_yaml()

    def read_yaml(self):
        """读YAML文件"""
        try:
            with open(self.yaml_file, 'r', encoding='utf-8') as f:
                yaml_dict = yaml.safe_load(f)
            return yaml_dict
        except FileNotFoundError:
            print(
                f"File {self.yaml_file} not found,but creating a default yaml,"
                f"please check the contents of the lvm_config.yaml")
            self.create_default_yaml()
            sys.exit()
        except TypeError:
            print("Error in the type of file name.")

    def create_default_yaml(self):
        """创建默认的YAML文件"""
        default_config = {
            "vg": [
                {
                    "name": "<vg name>",
                    "device": ["<device>"],  # 修改为列表
                    "thin_pool": [
                        {
                            "name": "<thin_pool name>",
                            "size": "<size>"
                        }
                    ]
                }
            ]
        }
        with open(self.yaml_file, 'w', encoding='utf-8') as f:
            yaml.dump(default_config, f, default_flow_style=False)

    def update_yaml(self):
        """更新文件内容"""
        with open(self.yaml_file, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, default_flow_style=False)

    def check_config(self):
        if self.config["vg"] is None:
            print("Configuration 'vg' is None in lvm_config.yaml")
            sys.exit()
        try:
            for vg in self.config["vg"]:
                if not vg["name"]:
                    print(f'Please check whether the name in lvm_config.yaml is entered')
                    sys.exit()
                else:
                    result = exec_cmd(f"vgdisplay {vg['name']}")
                    if "Cannot" in result:
                        print(f"Please check lvm_config.yaml, VG({vg['name']}) does not exist,")
                        sys.exit()
        except KeyError as e:
            print(f"Missing configuration item {e}.")
            sys.exit()


class Log(object):
    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            Log._instance = super().__new__(cls)
            Log._instance.logger = logging.getLogger()
            Log._instance.logger.setLevel(logging.INFO)
            Log.set_handler(Log._instance.logger)
        return Log._instance

    @staticmethod
    def set_handler(logger):
        now_time = datetime.datetime.now().strftime('%Y-%m-%d')
        file_name = "vsdslvmexpander_" + str(now_time) + '.log'
        fh = logging.FileHandler(file_name, mode='a')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        fh.setFormatter(formatter)
        logger.addHandler(fh)
