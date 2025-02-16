from character.basecharacter import BaseCharacter

class Assasin(BaseCharacter):
    def __init__(self,name):
        super().__init__(name)
        self.max_health = 70
        self.health = 70
        self.damage = 60
        self.mana = 60
        self.max_mana = 60
