# funct_call_test.py



def fa():
    return "FA_result"

def fb(a, b):
    return f"FB_result_{a}_{b}"

def fc(a, b, sep=None):
    return f"FB_result_{a}_{b}_{sep}"

def test():
    d = {
        "FA": (fa, ()),
        "FB": (fb, (1,2)),
        "FC": (fc, (1,2), {"sep":"<BR>"} ),
    }

    print("--- CALL FA ___")
    item = d.get("FA")
    print(f"  {item=}")
    f = item[0]
    args = item[1]
    r = f(*args)
    print(f"  result={r}")

    print("--- CALL FB ___")
    item = d.get("FB")
    print(f"  {item=}")
    f = item[0]
    args = item[1]
    r = f(*args)
    print(f"  result={r}")

    print("--- CALL FB ___")
    item = d.get("FB")
    print(f"  {item=}")
    f = item[0]
    args = item[1]
    r = f(*args)
    print(f"  result={r}")

    print("--- CALL FC ___")
    item = d.get("FC")
    print(f"  {item=}")
    f = item[0]
    args = item[1]
    kw = item[2]
    r = f(*args, **kw)
    print(f"  result={r}")


test()

###
