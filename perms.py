class Perm(dict): 
    """The class defining a perm."""
     
    def __init__(self, data=None): 
        """Loads up a Perm instance.""" 
        if data: 
            for key, value in enumerate(data): 
                self[key] = value
                 
    def __missing__(self, key): 
         """Enters the key into the dict and returns the key.""" 
         self[key] = key 
         return key
        
    def __call__(self, *args): 
        """Returns the product of the perm and the cycle.""" 
        changed = {} 
        n = len(args) 
        for i in range(n): 
            changed[args[i]] = self[args[(i + 1) % n]] 
        self.update(changed) 
        return self
    
    def is_identity(self): 
        """Test if the perm is the identity perm.""" 
        return all(self[key] == key for key in self)

    def __invert__(self):   
        """Finds the inverse of the perm."""
        perm = Perm() 
        for key in self: 
            perm[self[key]] = key 
        return perm

    def __mul__(self, other): 
        """Returns the product of the perms.""" 
        perm = Perm()
        # Let us collect all keys.
        # First keys from other, because self can grow up. 
        for key in other: 
            perm[key] = self[other[key]] 
        for key in self: 
            perm[key] = self[other[key]] 
        return perm

    def __eq__(self, other): 
        """Test if the perms are equal.""" 
        return (self * ~other).is_identity()

    def __ne__(self, other): 
        """Test if the perms are not equal.""" 
        return not self == other

    def __getitem__(self, key): 
        """Finds the item on the given position."""
        return dict.__getitem__(self, key)

    def __pow__(self, n): 
        """Finds powers of the perm.""" 
        if n < 0: 
            return pow(~self, -n) 
        elif n == 0: 
            return Perm() 
        elif n == 1: 
            return self 
        elif n == 2: 
            return self * self 
        else: # binary exponentiation 
            perm = self 
            res = Perm() # identity 
        while True: 
            if n % 2 == 1: 
                res = res * perm 
                n = n - 1 
                if n == 0:
                    break 
            if n % 2 == 0: 
                perm = perm * perm 
                n = n / 2 
        return res

    def support(self):
        """Returns the elements moved by the perm.""" 
        return [key for key in self if self[key] != key]
    
    def max(self): 
        """Return the highest element moved by the perm."""
        if self.is_identity():
            return 0
        else:
            return max(key for key in self if self[key] != key)
        
    def min(self): 
        """Return the lowest element moved by the perm.""" 
        if self.is_identity(): 
            return 0 
        else: 
            return min(key for key in self if self[key] != key)
        
    def list(self, size=None): 
        """Returns the perm in array form.""" 
        if size is None:
            size = self.max() + 1
        elif size < self.max() + 1: 
            raise ValueError("size is too small") 
        return [self[key] for key in range(size)]
    
    def label(self, size=None): 
        """Returns the string label for the perm.""" 
        if size is None: 
            size = self.max() + 1 
        if size > 62: 
            raise ValueError("size is too large for labels") 
        letters = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ" 
        letters = letters + "abcdefghijklmnopqrstuvwxyz_" 
        chars = [] 
        for key in range(size): 
            chars.append(letters[self[key]]) 
        return "".join(chars)

a = Perm(),
ab = Perm()(1, 2),
ac = Perm()(1, 3),
ad = Perm()(1, 4),
bc = Perm()(2, 3),
bd = Perm()(2, 4),
cd = Perm()(3, 4),
abc = Perm()(1, 2, 3),
abd = Perm()(1, 2, 4),
acb = Perm()(1, 3, 2),
adb = Perm()(1, 4, 2),
bcd = Perm()(2, 3, 4),
bdc = Perm()(2, 4, 3),
acd = Perm()(1, 3, 4),
adc = Perm()(1, 4, 3),
abcd = Perm()(1, 2, 3, 4),
abdc = Perm()(1, 2, 4, 3),
acbd = Perm()(1, 3, 2, 4),
acdb = Perm()(1, 3, 4, 2),
adbc = Perm()(1, 4, 2, 3),
adcb = Perm()(1, 4, 3, 2),
ab_cd = Perm()(1, 2) * Perm()(3, 4),
ac_bd = Perm()(1, 3) * Perm()(2, 4),
ad_bc = Perm()(1, 4) * Perm()(2, 3)

S4 = [a, ab, ac, ad, bc, bd, cd, abc, acb, abd, adb, acd, adc, bcd, bdc, \
      abcd, abdc, acbd, acdb, adbc, adcb, ab_cd, ac_bd, ad_bc]

##class alg():
##    def __init__(self, coefs): # x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, \
##        #x11, x12, x13, x14, x15, x16, x17, x18, x19, x20, 21, x22, x23, x24):
##        self.coef = {}
##        for i in range(24):
##            self.coef[i] = coefs[i]
##
##    def product(self, other):
##        product_coefs = []
##        for i in range(24):
##            product_coefs.append(self.coef[i] * other.coef[i])
##        return alg()(product_coefs)
