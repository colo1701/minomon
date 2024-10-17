import mnstr_class as mnstr

if __name__ == '__main__':
    minomon_1 = mnstr.Mnstr("MS-005", 28)
    minomon_2 = mnstr.Mnstr("MS-006", 28)
    print(minomon_1.print_stats())
    print(minomon_2.print_stats())

    att_cnt = 0
    active_m, passive_m = minomon_2, minomon_1

    while passive_m.is_active:
        att_cnt += 1
        active_m, passive_m = passive_m, active_m
        print(f"Hit number {att_cnt} dealt by {active_m.name}. Attack: {active_m.attacks[f'att_2']['name']}")
        mnstr.deal_dmg(active_m, passive_m, 2)
        print(f"HP Attacker: {active_m.hp_act}, HP Defender: {passive_m.hp_act}")


    print("Fight done!\n")
    print(minomon_1.print_stats())
    print(minomon_2.print_stats())
