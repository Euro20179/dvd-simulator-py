import random
class DVDS:
    def __init__(self, VARS, SH, SW, SX=False, SY=False):
        if not SX:
            SX = random.randint(0, round(VARS["winWidth"] - SW))
            SY = random.randint(0, round(VARS["winHeight"] - SH))
        self.SX, self.SY = SX, SY
        self.SH, self.SW = SH, SW
        self.wallHits = 0
        self.SXGain = random.choice([(VARS["winWidth"] + VARS["winHeight"]) / 2 / 700, -((VARS["winWidth"] + VARS["winHeight"]) / 2 / 700)]); self.SYGain = random.choice([self.SXGain, -self.SXGain])
        self.currentLogo = random.choice(VARS["DVD_Logos"])
        self.dispInfo = False
        
    def __call__(self, VAR):
        self.SX += self.SXGain
        self.SY += self.SYGain

        if self.SX <= 0 or self.SX + self.SW >= VAR["winWidth"]:
            self.SXGain *= (-1 + random.uniform(-.1, .1))
            self.currentLogo = random.choice(VAR["DVD_Logos"])
            self.wallHits += 1
            self.SX += self.SXGain / 2

        if self.SY <= 0 or self.SY + self.SH >= VAR["winHeight"]:
            self.SYGain *= (-1 + random.uniform(-.1, .1))
            self.currentLogo = random.choice(VAR["DVD_Logos"])
            self.wallHits += 1
            self.SY += self.SYGain / 2
       
