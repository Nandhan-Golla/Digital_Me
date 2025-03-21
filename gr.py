import gradio as gr
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

llm = ChatGroq(model_name="llama-3.3-70b-versatile", api_key="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")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a translation expert. Translate the following text from {source_lang} to {target_lang}:"),
        ("user", "{text}")
    ]
)

chain = prompt | llm

supported_languages = ["English", "Spanish", "French", "German", "Italian", "Telugu", "Hindi", "Tamil"]

def translate_text(text, source_lang, target_lang):
    if not text:
        return "Please enter text to translate."
    result = chain.invoke({"text": text, "source_lang": source_lang, "target_lang": target_lang})
    return result.content
with gr.Blocks(title="Translator Model") as demo:
    gr.Markdown("#Translator\nTranslate text with peak accuracy")
    
    with gr.Row():
        with gr.Column():
            #text_input = gr.Textbox(label="Text to Translate", placeholder="Enter your text here...")
            source_lang = gr.Dropdown(label="Source Language", choices=supported_languages, value="English")
            target_lang = gr.Dropdown(label="Target Language", choices=supported_languages, value="Hindi")
            text_input = gr.Textbox(label="Text to Translate", placeholder="Enter your text here...")
            translate_btn = gr.Button("Translate")
        with gr.Column():
            output = gr.Textbox(label="Translated Text", interactive=False)
    

    translate_btn.click(
        fn=translate_text,
        inputs=[text_input, source_lang, target_lang],
        outputs=output
    )


demo.launch()