import mnstr_class as mnstr

if __name__ == '__main__':
    minomon_1 = mnstr.Mnstr("MS-003", 11)
    print(minomon_1.print_stats())
    minomon_1.get_exp(28000)
    print(minomon_1.print_stats())