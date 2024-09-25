class SequentialFlow:
    def __init__(self, agent, model):
        self.agent = agent
        self.model = model

    def generate_prompt(self, user_prompt):
        return f"{self.agent} {user_prompt}"

    def execute(self, user_prompt):
        full_prompt = self.generate_prompt(user_prompt)
        return self.model.generate_image(full_prompt)
