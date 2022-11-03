import argparse

def str2bool(v):
    if isinstance(v, bool):
        return v
    v = v.lower()
    if v in ('true', 't', '1'):
        return True
    elif v in ('false', 'f', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError()
