import argparse
import utils
import lvm_cmds
import sys


class LVMExtend(object):

    def __init__(self):
        self.config_yaml = utils.ConfFile().read_yaml()
        self.vg_config = self.config_yaml.get('vg', [])

    def extend_lvm(self):
        for vg in self.vg_config:
            if vg.get('device') is not None:
                print("String extend VG")
                self.extend_vg(vg)
                
            thin_pool = vg.get('thin_pool')
            if thin_pool and thin_pool.get('name') and thin_pool.get('size'):

    @staticmethod
    def extend_vg(vg):
        try:
            vg_name = vg['name']
            devices = vg['device']
        except KeyError:
            print("Invalid VG configuration")
            return
        for device in devices:
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
    def extend_thinpool(vg):
        try:
            thin_pool = vg['thin_pool']
            pool_name = thin_pool["name"]
            size = thin_pool["size"]
        except KeyError:
            print("Invalid thin pool configuration")
            return

        print(f"Expanding Thinpool: {pool_name}")
        result = lvm_cmds.extend_pool(pool_name, vg['name'], size)
        if "successfully" in result:
            print(f"The {pool_name} is successfully rescaled ")
        else:
            print(result)