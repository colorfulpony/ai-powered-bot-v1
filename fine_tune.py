import os
from langchain.chat_models import ChatOpenAI
from llama_index.output_parsers import LangchainOutputParser
from llama_index.prompts.prompts import QuestionAnswerPrompt, RefinePrompt
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from llama_index import SimpleDirectoryReader, LLMPredictor, PromptHelper, GPTVectorStoreIndex
from llama_index.llm_predictor import StructuredLLMPredictor
from llama_index.prompts.default_prompts import DEFAULT_TEXT_QA_PROMPT_TMPL

os.environ["OPENAI_API_KEY"] = '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'

def add_quotes_and_replace_semicolons_in_dir(dir_path):
    # iterate over each file in the directory
    for filename in os.listdir(dir_path):
        # get the full path of the file
        file_path = os.path.join(dir_path, filename)
        if os.path.isfile(file_path):
            # read the contents of the file into a list
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.read().splitlines()

            # delete all existing quotes from each line
            lines = [line.replace('"', '') for line in lines]

            # add quotes and replace semicolons in each line
            modified_lines = ['"' + line.strip().replace(';', '","') + '"' for line in lines]

            # write the modified lines back to the file
            with open(file_path, 'w', encoding='utf-8-sig') as file:
                file.write('\n'.join(modified_lines))

def construct_index(directory_path):
    max_input_size = 8192
    num_outputs = 4096
    max_chunk_overlap = 20
    chunk_size_limit = 600
    
    # add_quotes_and_replace_semicolons_in_dir(directory_path)
        
    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", max_tokens=num_outputs))

    documents = SimpleDirectoryReader(directory_path).load_data()

    index = GPTVectorStoreIndex.from_documents(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    
    return index


if __name__ == '__main__':
    
    llm_predictor = StructuredLLMPredictor()
    
    response_schemas = [
        ResponseSchema(
            name="Investment fund name", 
            description="Write name of the investment fund"
        ),
        ResponseSchema(
            name="Investment fund website", 
            description="Write the website url of the investment fund"
        ),
        ResponseSchema(
            name="Analyst name", 
            description="Write name of the analyst of the investment fund"
        ),
        ResponseSchema(
            name="Analyst linkedin", 
            description="Write linkedin url of the analyst of the investment fund"
        ),
        ResponseSchema(
            name="Individual email to the analyst to get an investment from fund", 
            description="Write a personalized email to the analyst of an investment fund so that the user can receive investments from this fund (main part up to 3 sentences). One of the sentences should be about startups that this investment fund has invested in before (include the exact names and website urls of the startups), which are in a similar field to the user's startup so that the investor is interested."
        )
    ]
    
    lc_output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    output_parser = LangchainOutputParser(lc_output_parser)
    
    fmt_qa_tmpl = output_parser.format(DEFAULT_TEXT_QA_PROMPT_TMPL)

    qa_prompt = QuestionAnswerPrompt(fmt_qa_tmpl, output_parser=output_parser)
    
    directory_path = "Scrap Website Recursively/work/docs"
    index = construct_index(directory_path)
    query = index.as_query_engine(
        text_qa_template=qa_prompt,
        llm_predictor=llm_predictor
    )

    print("Bot is ready to chat. Type 'exit' to stop chatting.")
    while True:
        # Prompt user for startup details
        startup_name = input("Enter the startup name: ")
        if startup_name.lower() == "exit":
            break
        startup_industry = input("Enter the startup industry: ")
        if startup_industry.lower() == "exit" :
            break
        startup_stage = input("Enter the startup stage: ")
        if startup_stage.lower() == "exit" :
            break
        problems_solved = input("Enter the problems solved by the startup: ")
        if problems_solved.lower() == "exit":
            break

        # Construct input prompt for GPT chat
        startup_info = f"""{startup_name} is a startup that works at {startup_stage} stage(s) in the {startup_industry} industry(s) that solves the following problems: {problems_solved}."""
        prompt = f"""{startup_info}
Based on the information about the ventures I gave you, find the best one of them that is likely to invest in the described startup. Use only startups that I gave you.'"""
        
        response = query.query(prompt).response
        print("Bot:", response)
