import sys
from update_history import insert_history
from update_risk_area import update_risk_area
from update_details import update_details
from update_hotsearch import update_hotsearch

if __name__ == "__main__":
    if len(sys.argv) == 1:
        s = """参数说明：
        0 update_history 
        1 update_details
        3 update_risk
        others update_hotsearch
        """
        print(s)
    else:
        _choice = sys.argv[1]
        if _choice == "0":
            insert_history()
        elif _choice == "1":
            update_details()
        elif _choice == "2":
            update_risk_area()
        else:
            update_hotsearch()
