import random
import hashlib
import datetime

import numpy as np


def deal_dmg(m1, m2, attack_nr):
    # compute and deal damage from m1 attacking m2
    if random.uniform(0, 1) <= float(m1.attacks[f'att_{attack_nr}']['acc']):
        dmg_dealt = round(int(m1.attacks[f'att_{attack_nr}']['dmg']) * m1.att / m2.dfn)
        print(f"{m1.name} attacks with {m1.attacks[f'att_{attack_nr}']['name']} and deals {dmg_dealt} damage points.")
        m2.hp_act = int(m2.hp_act - dmg_dealt)
    else:
        print(f"{m1.name} attacks with {m1.attacks[f'att_{attack_nr}']['name']} but misses...")
    if m2.hp_act <= 0:
        m2.fight_lost()


class Mnstr:
    def __init__(self, ms_id, ms_lvl):
        self.id = ms_id
        self.p_id = None
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
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        with open('mnstr_data.txt', 'r', encoding='utf-8') as file:
            for line in file:
                data = line.strip().split('|')
                if data[0] == self.id:
                    self.name = data[1]
                    self.type = data[3]
                    self.exp_base = int(data[10])
                    self.exp_target = int(self.lvl * self.exp_base)
                    # Compute individual base values from the value ranges in mnstr_data
                    self.hp_base = random.uniform(float(data[4]), float(data[5]))
                    self.att_base = random.uniform(float(data[6]), float(data[7]))
                    self.dfn_base = random.uniform(float(data[8]), float(data[9]))
                    self.hp = round(self.lvl * self.hp_base)
                    self.hp_act = self.hp
                    self.att = round(self.lvl * self.att_base)
                    self.dfn = round(self.lvl * self.dfn_base)
                    # Prepare Attack Stats
                    for i in np.arange(1, 8, step=2):
                        self.attacks["att_" + str((i + 1) // 2)] = {"id": data[i + 10], "lvl_req": data[i + 11],
                                                                    "name": None, "a_type": None,
                                                                    "dmg": None, "acc": None,
                                                                    "stat": None, "stat_acc": None,
                                                                    "ap": None,
                                                                    "is_active": self.lvl >= int(data[i + 11])}
                    # Generate personal ID
                    unique_string = f"{self.hp_base}|{self.att_base}|{self.dfn_base}|{timestamp}"
                    self.p_id = hashlib.md5(unique_string.encode()).hexdigest()
                    break

    def load_attack_data(self):
        # Fill Attack Stats based on Attack id
        with open('attack_data.txt', 'r', encoding='utf-8') as file:
            for line in file:
                data = line.strip().split('|')
                for k, v in self.attacks.items():
                    if v['id'] == data[0]:
                        v['name'] = data[1]
                        v['a_type'] = data[2]
                        v['dmg'] = data[3]
                        v['acc'] = data[4]
                        v['ap'] = data[5]
                        # stat and stat_acc are placeholders for status-influencing effects.
                        # These effects are not yet implemented.
                        # stat defines the type of status effect and stat_acc the accuracy, e.g. the probability of the
                        # effect to get activated each turn.
                        v['stat'] = data[6]
                        v['stat_acc'] = data[7]

    def lvl_up(self):
        # Sets new Level, Base Stats and Exp. Target.
        # Unlocks new Attacks if available.
        self.lvl += 1
        rest_exp = self.exp - self.exp_target
        self.exp = rest_exp
        self.exp_target = self.exp_base * self.lvl
        # Store previous max HP
        hp_init = self.hp
        # Compute new Max HP
        self.hp = round(self.lvl * self.hp_base)
        self.att = round(self.lvl * self.att_base)
        self.dfn = round(self.lvl * self.dfn_base)
        # If Monstr is alive, add HP raise to actual HP
        if self.is_active:
            self.hp_act += (self.hp - hp_init)
        # Check for new Attacks
        for k, v in self.attacks.items():
            if int(v['lvl_req']) == self.lvl:
                v['is_active'] = True

    def fight_lost(self):
        self.is_active = False
        self.hp_act = 0

    def get_stat(self, stat_name):
        pass

    def get_exp(self, exp_delta):
        # Adds Exp. gained and checks for Level Up
        self.exp += exp_delta
        # Use while Loop in order to allow more than one Level Up
        while self.exp >= self.exp_target:
            self.lvl_up()

    def print_stats(self):
        # Debug Function. Prints all relevant stats.
        return (f"ID: {self.id} / {self.p_id}\n"
                f"Alive: {self.is_active}\n"
                f"Level: {self.lvl} / XP: {self.exp} / XP for next Level: {self.exp_target}\n"
                f"Name: {self.name}\n"
                f"Type: {self.type}\n"
                f"Base Attributes (HP MAX, ATT, DEF): {self.hp_base, self.att_base, self.dfn_base}\n"
                f"Actual Attributes(HP MAX, HP, ATT, DEF): {self.hp, self.hp_act, self.att, self.dfn}\n"
                f"Attack 1: {self.attacks['att_1']}\n"
                f"Attack 2: {self.attacks['att_2']}\n"
                f"Attack 3: {self.attacks['att_3']}\n"
                f"Attack 4: {self.attacks['att_4']}\n")
