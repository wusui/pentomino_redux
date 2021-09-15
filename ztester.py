"""
Tester
"""
from solver.find_pents import build_pent_tree


def expand(counter):
    prev = 0
    for cnt, cstart in enumerate([2, 6, 12, 20]):
        if counter >= prev and counter < cstart:
            yoff = counter - prev - cnt
            xoff = cnt + 1 -  abs(yoff)
            return [xoff, yoff]
        prev = cstart
    return 0

def deconstruct(fignumb):
    counter = 0
    numbers = []
    while fignumb > 0:
        if fignumb % 2 == 1:
            numbers.append(expand(counter))
        counter += 1
        fignumb //= 2
    return numbers


if __name__ == "__main__":
    Z = build_pent_tree()
    print(Z)
    flist = []
    for entry in Z:
        if entry != {}:
            if 'fig_value' in entry:
                flist.append(entry['fig_value'])
    flist.sort()
    print(flist)
    print(len(flist))
    for figure in flist:
        print(deconstruct(figure))
    fig_chk = {}
    for node in Z:
        if 'pent_type' in node:
            if node['pent_type'] not in fig_chk:
                fig_chk[node['pent_type']] = 1
            else:
                fig_chk[node['pent_type']] += 1
    print(fig_chk)
    
