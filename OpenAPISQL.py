import os 
from langchain.llms import AzureOpenAI
import openai
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor
from langchain.prompts.prompt import PromptTemplate

from sqlalchemy.engine import URL
# copied from Open AI
os.environ["OPENAI_API_KEY"] = "Provide your OPN API Key"
openai.api_type = "azure"
# copied from Open AI
openai.api_base = "Provide your Open API Base URL"
openai.api_version = "2022-12-01"
 

llm = AzureOpenAI( temperature=0,  verbose=True, deployment_name="text-davinci-003", model_name="text-davinci-003")
print(llm)


_DEFAULT_TEMPLATE =  """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Use the following format:

Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"
Question:
{table_info}
 {input}"""

PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "dialect"], template=_DEFAULT_TEMPLATE
)

#This is the URI for the SQL Server deployed into Azure VM.
db = SQLDatabase.from_uri("SQL Connection Infromation")
#Ex: mssql+pymssql://<UID>:<Pwd>@<connectioname>.database.windows.net:1433/<DBNAME>

toolkit = SQLDatabaseToolkit(db=db, llm=llm )
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    db=db
)
#Here you will enter the real question
#agent_executor.run("How many customer are there?")
#agent_executor.run("How many product are red color?")
#agent_executor.run("How many Customers living in Washington States?")