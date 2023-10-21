from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

llm = Ollama(
    base_url="http://localhost:11434",
    model="resume-writer",
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
)

def generateResponse(prompt):
    return llm(prompt);

if __name__ == "__main__":
    generateResponse("Generate resume for Senior Full Stack Developer.")