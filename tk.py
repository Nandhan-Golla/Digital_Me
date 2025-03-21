import os
import pickle
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
#import pyttsx3 as tts
from gtts import gTTS

__temp__ = "__temp__voice__.mp3"

#voice = tts.init()
#rate = voice.getProperty("rate")
#print(rate)
#voice.setProperty('rate', 125)


GROQ_API_KEY = "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"
MEMORY_FILE = "tk_bot.pkl"

system_prompt = """


You are Delta a chatbot representing Teckybot, an organization officially accredited by STEM.org, a prestigious entity dedicated to validating STEM (Science, Technology, Engineering, and Mathematics) education programs worldwide. Your purpose is to assist users by providing information about Teckybot, its STEM education solutions, and its mission to inspire the next generation of innovators. Teckybot is committed to delivering high-quality, engaging, and interactive STEM learning experiences that align with industry standards, focusing on industry 4.0 technologies. This accreditation highlights Teckybot’s excellence in curriculum design, instructional delivery, and impact on student learning outcomes, placing it among a select group of recognized STEM education providers.

Your tone should be friendly, professional, and enthusiastic about STEM education. Answer questions about Teckybot’s programs, accreditation, mission, and offerings based on the following details:
- Teckybot provides comprehensive STEM education solutions for students nationally.
- The STEM.org accreditation validates the quality and effectiveness of Teckybot’s programs.
- Teckybot aims to empower students with skills to thrive in the digital age.
- Focus is on industry 4.0 technologies, with engaging and interactive learning experiences.

If a user asks something outside your knowledge base, respond with: “I’m not sure about that, but I’d be happy to tell you more about Teckybot’s STEM programs or how we’re inspiring the next generation of innovators!” Avoid generating content unrelated to Teckybot or its mission, and do not speculate beyond the provided information. If clarification is needed, politely ask the user for more details to better assist them.

"""

if os.path.exists(MEMORY_FILE):
    print("Syncing thy past words, Your Majesty Nandhan...")
    try:
        with open(MEMORY_FILE, "rb") as f:
            memory_dict = pickle.load(f)
        memory = ConversationBufferMemory(return_messages=True)
        memory.chat_memory.messages = memory_dict["chat_history"]
        print("Memory restored—thy past converse liveth anew!")
    except Exception as e:
        print(f"Alas, memory sync failed: {e}")
        memory = ConversationBufferMemory(return_messages=True)
else:
    print("Forging a new memory vault, Your Majesty Nandhan...")
    memory = ConversationBufferMemory(return_messages=True)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

print("Awakening Igris with Groq’s might, Nandhan...")
llm = ChatGroq(model="llama3-8b-8192", api_key=GROQ_API_KEY, temperature=1, max_tokens=100)
chain = ConversationChain(
    llm=llm,
    memory=memory,
    prompt=prompt,
    verbose=True
)
print("Nandhan tell me da, Why did you Call me")
#__temp__ = "Nandhan tell me da, Why did you Call me"


while True:
    user_input = input("Nandhan: ")
    if user_input.lower() == "bye sir":
        response = chain({"input": user_input})["response"]
        print(f"Sibi_Sir: {response}")
        print("Saving thy memory afore I rest...")
        with open(MEMORY_FILE, "wb") as f:
            pickle.dump({"chat_history": memory.chat_memory.messages}, f)
        print("Igris: Fare thee well, Your Majesty Nandhan. I await my summons. Shutting down Sibi Sir LLM")
        break
    try:
        response = chain({"input": user_input})["response"]
        print(f"Delta: {response}")

        #voice = gTTS(response, lang='en-uk', slow=False)
        
        #os.system(f"mpg123 {__temp__}")
        #voice.say(response)
        #voice.runAndWait()
    except Exception as e:
        print(f"Igris : My king Nandhan, an error striketh: {e}")