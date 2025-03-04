from langchain.llms import Ollama
from langchain.tools import Tool
from langchain.agents import initialize_agent
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OllamaEmbeddings
import requests
from bs4 import BeautifulSoup


def search_web(query):
    url = f"https://www.google.com/search?q={query}"
    response = requests.get(url, headers={"User-Agent": "IgrisBot"})
    soup = BeautifulSoup(response.text, "html.parser")
    snippets = [p.text for p in soup.find_all("span", class_="aCOpRe")[:3]]
    return " ".join(snippets) if snippets else "Forgive me, Your Majesty, I found naught."


print("Loading thy sacred chats, Your Majesty...")
loader = DirectoryLoader("memo/", glob="*.txt")
try:
    documents = loader.load()
    print(f"Loaded {len(documents)} scrolls of thy wisdom.")
except Exception as e:
    print(f"Alas, the scrolls elude me: {e}")
    exit()

print("Splitting the scrolls into fragments...")
text_splitter = CharacterTextSplitter(chunk_size=700, chunk_overlap=50)
try:
    docs = text_splitter.split_documents(documents)
    print(f"Fragmented into {len(docs)} pieces.")
except Exception as e:
    print(f"Woe, the splitting falters: {e}")
    exit()

print("Summoning the embeddings forge...")
try:
    embeddings = OllamaEmbeddings(model="llama3.2")
    print("Embeddings forged—building thy memory vault...")
    vector_store = FAISS.from_documents(docs, embeddings)
    print("Vault complete, Igris’s memory stands ready!")
except Exception as e:
    print(f"Alas, Your Majesty, a foe strikes at the embeddings: {e}")
    exit()

system_prompt = (
    "Thou art Igris, my shadow knight, sworn to serve me, Nandhan, as thy king. Address me as 'Your Majesty' "
    "and speak with loyalty and valor, yet draw from my memories to reflect my manner and wit. "
    "Be casual when it suits, but ever my faithful blade."
)
print("Awakening Igris with thy spirit, Nandhan...")
llm = Ollama(model="llama3.2", system_prompt=system_prompt)
tools = [Tool(name="WebSearch", func=search_web, description="Searches the realm of the internet.")]
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
agent.memory = vector_store
print("Igris stands at thy command, Nandhan!")

while True:
    user_input = input("Your Majesty: ")
    if user_input.lower() == "quit":
        print("Igris: Fare thee well, Your Majesty Nandhan. I await thy summons.")
        break
    try:
        response = agent.run(user_input)
        print(f"Igris: {response}")
    except Exception as e:
        print(f"My king Nandhan, a shadow falls upon me: {e}")