class Skill():
    def __init__(self, name, description, mana_cost, skill_function):
        self.name = name
        self.description = description
        self.mana_cost = mana_cost
        self.skill_function = skill_function
    def use(self, object):
        self.skill_function(object)
