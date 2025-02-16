class BaseCharacter():
    def __init__(self, name):
        self.name = name
        self.max_health = 100
        self.health = 100
        self.damage = 20
        self.mana = 70
        self.max_mana = 70
        self.isparry = False
        self.successful = False
    def change_damage(self, reduce_damage):
        self.damage += reduce_damage
        print(f"{self.name}: Your current damage: {self.damage}")
    
    def change_health(self, reduce_health):
        self.health += reduce_health
        if self.health > self.max_health:
            self.health = self.max_health
        elif self.health <= 0:
            self.health = 0
        print(f"{self.name}: Your current health: {self.health}")

    def change_mana(self, reduce_health):
        self.mana += reduce_health
        if self.mana > self.max_mana:
            self.mana = self.max_mana
        print(f"{self.name}: Your current mana: {self.mana}")

    def attack(self, target):
        if not target:
            return 
        if self.mana < 10:
            print(f"{self.name}: You don't have enough mana to attack.")
            return
        self.change_mana(-10)
        if target.isparry:
            damage = 0
            target.successful = True
            return
        damage = 0 - self.damage
        target.change_health(damage)

    def change_parry(self, parry):
        self.isparry = parry

    def parry(self):
        if self.mana < 30:
            print(f"{self.name}: You don't have enough mana to parry.")
            self.successful = False
            self.isparry = False
            return
        if self.parry:
            if self.successful:
                self.change_mana(20)
            else:
                self.change_mana(-30)
        self.successful = False
        self.isparry = False
    