from form_filling_agent.agent import FormFillingAgent
from form_filling_agent.memory import FormMemory
from form_filling_agent.utils import setup_openai_api

def main():
    setup_openai_api()
    memory = FormMemory()
    agent = FormFillingAgent(memory=memory)
    try:
        agent.fill_form()
    finally:
        agent.quit()

if __name__ == "__main__":
    main()
