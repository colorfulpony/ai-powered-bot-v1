import os
from langchain.chat_models import ChatOpenAI
from llama_index import SimpleDirectoryReader, LLMPredictor, PromptHelper, GPTVectorStoreIndex
os.environ["OPENAI_API_KEY"] = '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'

# Load you data into 'Documents' a custom type by LlamaIndex
documents = SimpleDirectoryReader("Scrap Website Recursively/work/docs").load_data()
print(documents)
num_outputs = 4096

# define LLM
llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", max_tokens=num_outputs))
print(llm_predictor)

# define prompt helper
# set maximum input size
max_input_size = 4096
# set number of output tokens
num_output = 256
# set maximum chunk overlap
max_chunk_overlap = 20
prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)
print(prompt_helper)

custom_LLM_index = GPTVectorStoreIndex.from_documents(
    documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper
)

query = custom_LLM_index.as_query_engine()
response = query.query("Tell me industry in which 121G, LLC venture invest")
print(response.response)