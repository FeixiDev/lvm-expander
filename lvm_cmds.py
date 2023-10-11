import utils


def create_pv(device):
    cmd = f"pvcreate {device}"
    result = utils.exec_cmd(cmd)

    return result


def extend_vg(vg_name, pv_name):
    cmd = f"vgextend {vg_name} {pv_name}"
    result = utils.exec_cmd(cmd)

    return result


def extend_pool(pool_name, vg_name, size):
    cmd = f"lvextend -L +{size} {vg_name}/{pool_name}"
    result = utils.exec_cmd(cmd)

    return result


def check_device(device):
    cmd = f"fdisk -l {device}"
    result = utils.exec_cmd(cmd)

    return result


# def check_vg(vg_name):
#     cmd = f"vgdisplay {vg_name}"
#     result = utils.exec_cmd(cmd)
#
#     return result
