# MTG deckbuilder
import numpy as np
import matplotlib.pyplot as plt

clrnames = ['W', 'U', 'B', 'R', 'G', 'C']
typenames = ['cre', 'src', 'ins', 'enc', 'art', 'lnd']

class manacost:
    def __init__(self, W, U, B, R, G, C):
        self.clrs = [W, U, B, R, G, C]
        self.W = W
        self.U = U
        self.B = B
        self.R = R
        self.G = G
        self.C = C
        self.tot = W + U + B + R + G + C
        
class types:
    def __init__(self, cre, src, ins, enc, art, lnd):
        self.types = [cre, src, ins, enc, art, lnd]
        self.cre = cre
        self.src = src
        self.ins = ins
        self.enc = enc
        self.art = art
        self.lnd = lnd
            

class card:
    def __init__(self, name, types, types2, rules, power, tough, mana, num):
        self.name = str(name)
        self.types = types
        if types2:
            self.types2 = str(types2)
        else:
            self.types2 = None
        self.rules = str(rules)
        self.power = power
        self.tough = tough
        self.mana = mana
        self.num = num
        
    def print_card(self):
        print "%dx %s -" %(self.num, self.name),
        for i, t in enumerate(self.types.types):
            if t:
                print typenames[i],
        if self.types2 != None:
            print self.types2,
        print "-",
        for j, c in enumerate(self.mana.clrs):
            if c:
                print "%d%s" %(j, clrnames[j]),
        print "%dtot" %self.mana.tot
        if self.types.cre:
            print "%s/%s" %(self.power, self.tough)
        print "%s\n" %self.rules

        

class deck:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def print_info(self):
        numcards = 0
        numcre = 0
        numlnd = 0
        for c in self.cards:
            numcards += c.num
            numcre += c.num * c.types.cre
            numlnd += c.num * c.types.lnd
        print "%s deck: %d cards, %d creatures, %d other, %d lands" \
        %(self.name, numcards, numcre, numcards - numcre - numlnd, numlnd)

    def load_cards(self, filename):
        data = np.loadtxt(filename, dtype = str, delimiter = "\t", \
        skiprows = 1)
        
        for i, c in enumerate(data):
            if not c[0]:
                continue
            
            name = c[0]
            num = int(c[1])
            t = types(int(c[2]), int(c[3]), int(c[4]), \
            int(c[5]), int(c[6]), int(c[7]))
            if c[8] == "0":
                t2 = None
            else:
                t2 = c[8]
            rules = c[9]
            power = int(c[10])
            tough = int(c[11])
            mana = manacost(int(c[12]), int(c[13]), int(c[14]), int(c[15]),\
            int(c[16]), int(c[17]))
            
            self.cards.append(card(name, t, t2, rules, power, tough, mana, num))

    def print_deck(self):
            for c in self.cards:
                if c.num > 0:
                    c.print_card()

    def search_cards(self):
        key = raw_input("enter search keyword: ")        
        for c in self.cards:
            text = c.name + str(c.types2) + c.rules
            if text.find(key) != -1:
                c.print_card()
    
    def mana_curve(self):
        clrs = np.array([[0 for i in range(11)] for j in range(6)])
        tot = [0 for i in range(11)]
        
        for c in self.cards:
            if c.types.lnd:
                continue
            
            clrs[0][c.mana.tot] += c.mana.W * c.num
            clrs[1][c.mana.tot] += c.mana.U * c.num
            clrs[2][c.mana.tot] += c.mana.B * c.num
            clrs[3][c.mana.tot] += c.mana.R * c.num
            clrs[4][c.mana.tot] += c.mana.G * c.num
            #clrs[5][c.mana.tot] += c.mana.C * c.num
            tot[c.mana.tot] += 1 * c.num
        
        max_mana = 0
        for m, val in enumerate(tot):
            if val != 0:
                    max_mana = m
        
        costs = np.array([i for i in range(11)])
        plt.bar(costs - 0.5, tot, width = 1, color = 'grey')
        plt.xlim(0, max_mana + 1)
        plt.xlabel("converted mana cost")
        plt.ylabel("number of cards")
        plt.show()
        
        colors = ['yellow', 'blue', 'black', 'red', 'green']
        plt.bar(costs - 0.5, tot, width = 1, color = 'grey')
        for k in range(5):
            plt.bar(costs - 0.5 + (1./5) * k, clrs[k], width = (1./5), color = colors[k])
            plt.xlim(0, max_mana + 1)
        plt.xlabel("colour mana cost")
        plt.ylabel("sum of contributions per card")
        plt.show()
            
    def colourpie(self):
        numlnd = 0.0
        numcards = 0.0
        mana_wedges = np.array([0 for i in range(6)])
        wedges = np.array([0 for i in range(5)])
        for c in self.cards:
            if c.types.lnd:
                numlnd += c.num * sum(np.array(c.mana.clrs))
                mana_wedges = mana_wedges + np.array(c.mana.clrs) * c.num
                continue
            numcards += c.num * sum(np.array(c.mana.clrs[:-1]))
            wedges = wedges + np.array(c.mana.clrs[:-1]) * c.num
            
        sources = mana_wedges        
        mana_wedges = mana_wedges/numlnd
        wedges = wedges/numcards
        mwedge_fl = map(float, mana_wedges)
        wedge_fl = map(float, wedges)
        wedge_str = ['%.2f'%wedge_fl[i] for i in range(5)]
        
        plt.pie(wedges, colors = ('y', 'b', 'k', 'r', 'g'), \
        labels = wedge_str)
        plt.pie(mana_wedges, colors = ('y', 'b', 'k', 'r', 'g', 'grey'), \
        radius = 0.8)        
        plt.text(-1, -1.3, "land mana: %.2fW %.2fU %.2fB %.2fR %.2fG" \
        %(mwedge_fl[0], mwedge_fl[1], mwedge_fl[2], mwedge_fl[3], mwedge_fl[4]))
        plt.text(-1, -1.5, "mana sources: %dW %dU %dB %dR %dG"\
        %(sources[0], sources[1], sources[2], sources[3], sources[4]))
        plt.title(self.name)
        plt.savefig("BW_Allies_pie.png")        
        plt.show()
        
            
        
Allies = deck("Mardu Allies")
Allies.load_cards("Mardu_Allies.txt")

        
        


    