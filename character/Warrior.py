from character.basecharacter import BaseCharacter

class Warrior(BaseCharacter):
    def __init__(self,name):
        super().__init__(name)
        self.max_health = 150
        self.health = 150
        self.damage = 10
        self.mana = 100
        self.max_mana = 100
