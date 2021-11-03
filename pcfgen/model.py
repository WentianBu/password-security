from typing import Iterable
import math
import heapq
import time
import re
import functools
import itertools
from tqdm import tqdm


class Model:
    def __init__(self) -> None:
        self.patts = dict()
        # {'L3': {'abc':1, 'bcd':2}, 'D4':{'1234':5, '0000':2}}
        self.terms = dict()

    def fit(self, passwd: Iterable):
        def _analyze(p):
            """
            analyze a single password

            return a pattern string ('L3D8') and a terminal list (['Abc', '12345678'])
            """
            """ Some test cases (use with print and doctest)
            >>> _analyze('Ady7774))')
            L3D4S2
            ['Ady', '7774', '))']
            >>> _analyze('58863847')
            D8
            ['58863847']
            >>> _analyze('m8S3ZeN4')
            L1D1L1D1L3D1
            ['m', '8', 'S', '3', 'ZeN', '4']
            >>> _analyze('associated1017')
            L10D4
            ['associated', '1017']
            >>> _analyze('^&$Qmf&*#)2009')
            S3L3S4D4
            ['^&$', 'Qmf', '&*#)', '2009']
            """
            status = 0
            count = 0
            patt = ''
            terms = []

            def _submit(p, i):
                nonlocal status, count, patt, terms
                if status == 0:
                    return
                s = {1: 'L', 2: 'D', 3: 'S'}.get(status)
                patt += s + str(count)
                terms.append(p[i-count:i])
                count = 0

            i = 0
            while i < len(p):
                if p[i].isalpha() and status != 1:
                    _submit(p, i)
                    status = 1
                elif p[i].isdigit() and status != 2:
                    _submit(p, i)
                    status = 2
                elif p[i] in R'~!@#$%^&*()_+-=`;:"\',.?/|\[]\{\}<>' and status != 3:
                    _submit(p, i)
                    status = 3
                elif not p[i].isalnum() and not p[i] in R'~!@#$%^&*()_+-=`;:"\',.?/|\[]\{\}<>':
                    return None, None

                count += 1
                i += 1
            _submit(p, i)

            return patt, terms

        # analyze and process each password
        training_set_size = 0
        for p in tqdm(passwd):
            if not p:
                continue
            patt, termlist = _analyze(p)
            if patt is None:
                continue
            # update the pattern frequency or add a new pattern
            pc = self.patts.get(patt)
            self.patts[patt] = pc + 1 if pc else 1

            # process the terminal list
            for t in termlist:  # terminal
                if t[0].isalpha():
                    pt = 'L'
                elif t[0].isdigit():
                    pt = 'D'
                else:
                    pt = 'S'
                pt += str(len(t))  # terminal pattern, like 'L3', 'D8', ...
                td = self.terms.get(pt)  # terminal-frequency dict of a pattern
                if td:  # pattern exists
                    tf = td.get(t)  # existed terminal frequecy
                    # update frequency or add a new terminal
                    td[t] = td[t] + 1 if tf else 1

                else:  # pattern not exists
                    self.terms[pt] = dict()  # create a dict for this pattern
                    self.terms[pt][t] = 1
            training_set_size += 1

        # now the patterns, the terminals and their frequencies are in the dicts
        # calculate the probablity of the patterns
        self.patt_probs = dict()
        for k, v in self.patts.items():
            self.patt_probs[k] = math.log(v/training_set_size)
        # calculate the probablity of the terminals for each pattern
        self.term_probs = dict()
        for p, d in self.terms.items():
            self.term_probs[p] = dict()
            # the total frequency of the terminals of a pattern
            tc = sum(d.values())
            for t, f in d.items():
                self.term_probs[p][t] = math.log(f/tc)

    def export(self, filename) -> None:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('[PATTERNS]\n')
            f.writelines(
                map(lambda x: x[0]+'\t'+str(x[1])+'\n', self.patt_probs.items()))
            f.write('\n\n\n')
            f.write('[TERMINALS]\n')
            for p, d in self.term_probs.items():
                f.write('[=>'+p+'\n')
                f.writelines(
                    map(lambda x: x[0]+'\t'+str(x[1])+'\n', d.items()))
                f.write('<=]\n')

    def load_model(self, filename):
        print('Loading model ...')
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.readlines()
        self.patt_probs = dict()
        self.term_probs = dict()
        state = 0
        cur_patt = ''
        for c in filter(lambda x: x, map(lambda x: x.rstrip(), content)):
            if c == '[PATTERNS]':
                state = 1
            elif c == '[TERMINALS]':
                state = 2
            elif c.startswith('[=>'):
                state = 3
                cur_patt = c.lstrip('[=>')
                self.term_probs[cur_patt] = dict()
            elif c.startswith('<=]'):
                state = 2
                cur_patt = ''
            else:
                l = c.split('\t')
                if state == 1:
                    self.patt_probs[l[0]] = float(l[1])
                elif state == 3:
                    self.term_probs[cur_patt][l[0]] = float(l[1])

        print('Done.')
        return self

    def generate(self, filename, num: int, withprob=True):
        gs_time = time.time()
        # get the maximum possible probability of a single pattern
        mp = dict()
        for sp, termd in self.term_probs.items():
            mp[sp] = max(termd.items(), key=lambda x: x[1])

        h = []
        heapq.heapify(h)  # h is a heap, h[0] has the smallest probablity

        # sort the patterns by probablity
        for patt, pattprob in sorted(self.patt_probs.items(), reverse=True, key=lambda x: x[1]):
            print('Current pattern: ', patt)

            # calculate the maximum probability of a password in the pattern
            max_possi_prob = functools.reduce(
                lambda x, y: x+y, map(lambda x: mp[x][1], re.findall(r'([LDS]\d+)', patt)), pattprob)
            # if max probability is less than the heap top, skip the pattern
            if len(h) == num and h[0][0] > max_possi_prob:
                print('skip.')
                continue

            # for every single pattern (L3) in the pattern (L3D8S3), sort and choose the top probability words (i.e. top 5000)
            buf = list(map(lambda x: list(
                self.term_probs[x].items()), re.findall(r'([LDS]\d+)', patt)))
            newbuf = []
            for termlist in buf:
                termlist.sort(key=lambda x: x[1], reverse=True)
                if len(termlist) > num:
                    # if the number of terminals in a pattern > L (the length of pwd dict, i.e. 5000)
                    # we can sort the terminals by probability and use the top L
                    # so the number of products is restrict to L^k (k is the number of single patterns)
                    # which is much less than l1*l2*..., (li is the number of the terminals in i-th single pattern)
                    newbuf.append(termlist[:num])
                else:
                    newbuf.append(termlist)

            for t in tqdm(itertools.product(*map(lambda x: range(len(x)), newbuf)), mininterval=1):
                passwd = []  # use list and join them only when need, it is faster than string '+'
                passprob = pattprob
                for idx, idy in enumerate(t):
                    passprob += newbuf[idx][idy][1]
                    passwd.append(newbuf[idx][idy][0])
                if len(h) < num:
                    heapq.heappush(h, (passprob, ''.join(passwd)))
                elif h[0][0] < passprob:
                    heapq.heapreplace(h, (passprob, ''.join(passwd)))

            '''
            # This is a iterator which can generate all the password of a pattern
            for pwd, prb in tqdm(map(lambda x: functools.reduce(lambda p, q: (p[0]+q[0], p[1]+q[1]), x, ('', pattprob)),
                                     itertools.product(*map(lambda x: range(len(x)), buf)))):
                if len(h) < num:
                    # add the (prob, password) tuple to the heap
                    heapq.heappush(h, (prb, pwd))

                elif h[0][0] < prb:
                    # push the password to heap
                    heapq.heapreplace(h, (prb, pwd))
            '''

        h.sort(key=lambda x: x[0], reverse=True)
        with open(filename, 'w', encoding='utf-8') as f:
            for prob, passwd in h:
                if withprob:
                    f.write(passwd + '\t' + str(prob) + '\n')
                else:
                    f.write(passwd+'\n')
        print('====================================================')
        print('Generate complete.')
        print(f'Time elapsed: {time.time()-gs_time} seconds.')

    def stat(self, topn):
        print(f'Top {topn} patterns:')
        s = sorted(self.patt_probs.items(), reverse=True, key=lambda x: x[1])
        for i in range(topn):
            print(s[i])
