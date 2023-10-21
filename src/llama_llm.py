from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from constants import LOCAL_HOST, PORT_NO, MODELS


class LLM:
    def __init__(self, model_name):
        self.llm = Ollama(
            base_url=f"{LOCAL_HOST}:{PORT_NO}",
            model=model_name,
            callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
        )

    def generateResponse(self, prompt):
        return self.llm(prompt)


if __name__ == "__main__":
    llm = LLM(MODELS["resume"]["name"])
    llm.generateResponse("Generate resume for Senior Full Stack Developer.")
