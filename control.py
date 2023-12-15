import argparse
import utils
import lvm_cmds
import sys


class LVMExtend(object):

    def __init__(self):
        self.config_file = utils.ConfFile()
        self.config_file.check_config()
        self.config_yaml = self.config_file.read_yaml()
        self.vg_config = self.config_yaml.get('vg', [])

    def extend_lvm(self):
        for vg in self.vg_config:
            devices = vg.get('device', [])
            if devices:
                print("String extend VG")
                for device in devices:
                    self.extend_vg(vg, device)

            thin_pool = vg.get('thin_pool')
            if thin_pool:
                for pool in thin_pool:
                    if pool.get('name') and pool.get('size'):
                        print("String extend Thinpool")
                        self.extend_thinpool(vg, pool)

    @staticmethod
    def extend_vg(vg, device):
        try:
            vg_name = vg['name']
        except KeyError:
            print("Invalid VG configuration")
            return

        result = lvm_cmds.check_device(device)
        if "No such file or directory" in result:
            print(f"Cannot open {device}: No such file or directory")
            sys.exit()
        else:
            print(f"Creating PV: {device}")
            result = lvm_cmds.create_pv(device)
            if "successfully" in result:
                print(f"The {device} is successfully created ")
            else:
                print(result)
            print(f"Expanding VG: {vg_name}")
            result = lvm_cmds.extend_vg(vg_name, device)
            if "successfully" in result:
                print(f"The {vg_name} is successfully rescaled ")

    @staticmethod
    def extend_thinpool(vg, pool):
        try:
            pool_name = pool["name"]
            size = pool["size"]
        except KeyError:
            print("Invalid thin pool configuration")
            return

        print(f"Expanding Thinpool: {pool_name}")
        result = lvm_cmds.extend_pool(pool_name, vg['name'], size)
        if "successfully" in result:
            print(f"The {pool_name} is successfully rescaled ")
        else:
            print(result)
