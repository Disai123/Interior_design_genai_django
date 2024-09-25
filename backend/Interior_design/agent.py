class Task:
    def __init__(self, description):
        self.description = description

    def __str__(self):
        return self.description

class InputType:
    def __init__(self, input_description):
        self.input_description = input_description

    def __str__(self):
        return self.input_description

class OutputType:
    def __init__(self, output_description):
        self.output_description = output_description

    def __str__(self):
        return self.output_description

class Agent:
    def __init__(self, expertise, task, input_type, output_type):
        self.expertise = expertise
        self.task = task
        self.input_type = input_type
        self.output_type = output_type

    def __str__(self):
        return f"You are {self.expertise}, your task is to {self.task}. I will give you {self.input_type}, give me a {self.output_type}."
