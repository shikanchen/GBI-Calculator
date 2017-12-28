from GBIManager import *

if __name__ == "__main__":
    fbase = 'base'
    gbiManager = GBIManager(fbase)
    gbi = gbiManager.calculate_gbi()
    # error range 1.5%
    print('GBI:', gbi)
