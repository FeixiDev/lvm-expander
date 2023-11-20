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
            if vg.get('thin_pool') is not None:
                print("String extend Thinpool")
                self.extend_thinpool(vg)

    def extend_vg(self, vg):
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
                else:
                    print(result)

    def extend_thinpool(self, vg):
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='None')
    parser.add_argument('-v', '--version', action='store_true',
                        help='Show version information')
    args = parser.parse_args()
    if args.version:
        print("version: v1.0.0")
    else:
        LVMExtend().extend_lvm()
