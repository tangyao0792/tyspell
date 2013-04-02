import cPickle
import os

def getDistance(word1, word2):
    len1 = len(word1)
    len2 = len(word2)
    size = max(len1, len2) + 1
    dp = []
    for i in xrange(size):
        temp = []
        for j in xrange(size):
            temp.append(0)
        dp.append(temp)
    for i in xrange(size):
        dp[i][0] = i
        dp[0][i] = i
    for i in xrange(1, len1+1):
        for j in xrange(1, len2+1):
            cost = 0
            if word1[i-1] != word2[j-1]:
                cost = 1
            exchangeCost = dp[i-1][j-1] + cost
            insertCost = dp[i][j-1] + 1
            deleteCost = dp[i-1][j] + 1
            dp[i][j] = min(exchangeCost, insertCost, deleteCost)
    return dp[len1][len2]

def myCmp(term0, term1):
    if term0[1] != term1[1]:
        return cmp(term0[1], term1[1])
    else:
        return cmp(term1[0][0], term0[0][0])

class BDTree():
    def __init__(self):
        self.bdtree = dict()
        self.bdtree[0] = ('', 0)
        # load bdtree
        if os.path.exists('tempfile'):
            print 'loading from cache...'
            with open('tempfile', 'rb') as fin:
                self.bdtree = cPickle.load(fin)
        else:
            # load from file
            print 'loading from file'
            with open('freq.txt') as fin:
                for l in fin.readlines():
                    word, tmp, freq = l.split()
                    self.__insert(word, int(freq))
            with open('tempfile', 'wb+') as fout:
                cPickle.dump(self.bdtree, fout)

    def __insert(self, word, freq):
        pos = self.bdtree
        dis = getDistance(word, pos[0][0])
        while dis in pos:
            pos = pos[dis]
            dis = getDistance(word, pos[0][0])
            if dis == 0:
                return
        pos[dis] = dict()
        pos[dis][0] = (word, freq)

    def __find(self, word, k, pos):
        dis = getDistance(word, pos[0][0])
        ans = []
        for i in xrange(max(1, dis-k), dis+k+1):
            if i in pos:
                ans += self.__find(word, k, pos[i])
        if dis <= k:
            ans.append((pos[0],dis))
        return ans
    
    def find(self, word, k):
        ans = self.__find(word, k, self.bdtree)
#        ans = sorted(ans, lambda x,y: cmp(x[1], y[1]))
        ans = sorted(ans, cmp = myCmp)
        return ans
        
bdt = BDTree()
print 'build over'

def correct(spell):
    return bdt.find(spell, 1)

if __name__ == '__main__':
    while True:
        spell = raw_input()
        for l in correct(spell):
            print l
        print '**'
