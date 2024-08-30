import random
import numpy as np

class Mnstr:
    def __init__(self, ms_id, ms_lvl):
        self.id = ms_id
        self.name = None
        self.lvl = ms_lvl
        self.exp_base = None
        self.exp = 0
        self.exp_target = None
        self.type = None
        self.hp_base = None
        self.att_base = None
        self.dfn_base = None
        self.hp = None
        self.att = None
        self.dfn = None
        self.hp_act = None
        self.is_active = True
        self.attacks = {}

        self.load_initial_data()
        self.load_attack_data()

    def load_initial_data(self):
        with open('mnstr_data.txt', 'r') as file:
            for line in file:
                data = line.strip().split('|')
                if data[0] == self.id:
                    self.name = data[1]
                    self.type = data[3]
                    self.exp_base = data[10]
                    self.exp_target = self.lvl * self.exp_base
                    self.hp_base = random.uniform(float(data[4]), float(data[5]))
                    self.att_base = random.uniform(float(data[6]), float(data[7]))
                    self.dfn_base = random.uniform(float(data[8]), float(data[9]))
                    self.hp = self.lvl * self.hp_base
                    self.hp_act = self.hp
                    self.att = self.lvl * self.att_base
                    self.dfn = self.lvl * self.dfn_base
                    for i in np.arange(1, 8, step = 2):
                        self.attacks["att_" + str((i + 1) // 2)] = {"id": data[i + 10], "level_req": data[i + 11],
                                                                    "name": None, "a_type": None,
                                                                    "dmg": None, "acc": None,
                                                                    "stat": None, "stat_acc": None,
                                                                    "ap": None, "is_active": self.lvl >= int(data[i + 11])}
                    break

    def load_attack_data(self):
        with open('attack_data.txt', 'r') as file:
            for line in file:
                data = line.strip().split('|')
                for k, v in self.attacks.items():
                    if v['id'] == data[0]:
                        v['name'] = data[1]
                        v['a_type'] = data[2]
                        v['dmg'] = data[3]
                        v['acc'] = data[4]
                        v['ap'] = data[5]
                        v['stat'] = data[6]
                        v['stat_acc'] = data[7]

    def deal_dmg(self):
        pass

    def get_dmg(self):
        pass

    def deal_stat(self):
        pass

    def get_stat(self):
        pass

    def get_exp(self):
        pass

    def lvl_up(self):
        pass

    def print_stats(self):
        return (f"ID: {self.id}\n"
                f"Name: {self.name}\n"
                f"Type: {self.type}\n"
                f"Base Attributes: {self.hp_base, self.att_base, self.dfn_base}\n"
                f"Actual Attributes: {self.hp, self.hp_act, self.att, self.dfn}\n"
                f"Attack 1: {self.attacks['att_1']}\n"
                f"Attack 2: {self.attacks['att_2']}\n"
                f"Attack 3: {self.attacks['att_3']}\n"
                f"Attack 4: {self.attacks['att_4']}\n")