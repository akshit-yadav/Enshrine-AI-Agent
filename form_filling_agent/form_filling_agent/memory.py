from form_filling_agent.config import RESUME_PATH

class FormMemory:
    def __init__(self):
        self.data = {"resume_path": RESUME_PATH}
    
    def update(self, field, value):
        self.data[field] = value
