from src.character.character import Character
from src.goals.goal import Goal


class AccountAndGoal():
    def __init__(self, character: Character, goal: Goal):
        self.character = character
        self.goal = goal

    def getName(self):
        return self.character.name

    def run_function(self):
        is_empty_queue = self.character.queue_len() < 1
        if is_empty_queue:
            self.next_goal_step()
        else:
            self.character.run_function()

    def next_goal_step(self):
        character_name = self.getName()
        next_step = self.goal.get_next_step(character_name=character_name)
        next_step.run(character=self.character)


