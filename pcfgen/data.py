import prettytable
import time
from typing import Iterable
from tqdm import tqdm


class CSDN:
    def __init__(self, filename) -> None:
        with open(filename, 'r', encoding='ISO-8859-1') as f:
            lines = f.readlines()
        self.len = len(lines)
        self.passwds = map(lambda x: x.rstrip().split(' # ', 2)[1], lines)

    def __iter__(self):
        return self.passwds

    def __len__(self):
        return self.len


class Yahoo:
    def __init__(self, filename) -> None:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        self.len = len(lines)
        self.passwds = map(lambda x: x.rstrip().split(':', 2)[2], lines)

    def __iter__(self):
        return self.passwds

    def __len__(self):
        return self.len


class Pwdlist:
    def __init__(self, filename) -> None:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        self.len = len(lines)
        self.pwdlist = list(map(lambda x: x.rstrip().split('\t')[0], lines))

    def check(self, pwd):
        return pwd in self.pwdlist

    def test(self, pwds: Iterable):
        print('Testing...')
        stime = time.time()
        # record the num of trials for every target in testset
        tc_record = []
        hit_record = dict()  # record the num of hits for every passwd in the password dict
        for target in tqdm(pwds, mininterval=1):
            idx = 0
            while idx < len(self.pwdlist):
                cur = self.pwdlist[idx]
                if target == cur:
                    tc_record.append(idx+1)
                    hit_record[cur] = hit_record[cur] + \
                        1 if hit_record.get(cur) else 1
                    break
                idx += 1
            else:
                tc_record.append(0)

        hit_rate = (len(tc_record) - tc_record.count(0))/len(tc_record)
        average_trials = sum(filter(None, tc_record)) / \
            (len(tc_record) - tc_record.count(0))
        print(f'====================== RESULT ======================')
        print(f'Time elapsed: {time.time() - stime} seconds')
        print(f'Hit rate: {hit_rate}')
        print(f'Average num of trials: {average_trials}')
        print(f'Hit rate top 20 passwords: ')
        table = prettytable.PrettyTable(
            ['Password', 'Num of hits', 'Hit rate'])
        for idx, (p, f) in enumerate(sorted(hit_record.items(), reverse=True, key=lambda x: x[1])):
            table.add_row([p, f, f/len(pwds)])
            if idx > 19:
                break
        print(table)

    def __len__(self):
        return self.len
