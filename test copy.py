import os
import gradio as gr

os.environ["GROQ_API_KEY"] = "gsk_BQoQcim65HBqtG4u4FCNqyXpHG"
os.environ["TAVILY_API_KEY"] = "tvly-TB0Ps3C2LkebdDQ"
os.environ["LANGCHAIN_API_KEY"] = "lsv2_pt_20fcc2e58441ecd"
os.environ["LANGCHAIN_PROJECT"] = "sql_langchain"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_TRACING_V2"] = "True"

import langchain
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI 
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
import ast
import re
import pandas as pd
from langchain_core.prompts import PromptTemplate
from langchain import LLMChain
from typing import Annotated
from langchain_experimental.utilities import PythonREPL
import io
from PIL import Image

llm = ChatOpenAI(api_key="sk-proj-Cr6RALcomvgi",model="gpt-3.5-turbo", temperature=0)
db_username = "chatbot-demo-backend"
db_password = "bemedicrlpravLchukix"
db_host = "13.201.41.83"
db_name = "eda"
db = SQLDatabase.from_uri(f"mysql+mysqlconnector://{db_username}:{db_password}@{db_host}/{db_name}")

repl = PythonREPL()
def python_repl(
    code: Annotated[str, "The python code to execute to generate your chart."]
):
    """Use this to execute python code. If you want to see the output of a value,
    you should print it out with `print(...)`. This is visible to the user."""
    try:
        result = repl.run(code)
    except BaseException as e:
        return f"Failed to execute. Error: {repr(e)}"
    result_str = f"Successfully executed:\n```python\n{code}\n```\nStdout: {result}"
    return (
        result_str + "\n\nIf you have completed all tasks, respond with FINAL ANSWER."
    )

template = """
    You are a helpful assistant to create chart python code in matplotlib.
    Give me only and only code to directly execute in pyhtorepl no other text rather than code.
    try to create minimum two plot if possible like pie chart and bar plot in single image
    and don't use plt.show() 
    just save in last plt.savefig('bar_chart.png')

    And This is Data: {data}
"""

promp = PromptTemplate(template=template,input_variables=['data'])
llm_chain = LLMChain(llm=llm, prompt=promp)


generate_query = create_sql_query_chain(llm, db)
execute_query = QuerySQLDataBaseTool(db=db)
# Replace Decimal('...') with corresponding float values
def replace_decimals(match):
    return str(float(match.group(1)))

def answer_from_sql(question):
    query = generate_query.invoke({"question": f'{question}'})
    print(query)
    data=execute_query.invoke(query)
    cleaned_output_str = re.sub(r"Decimal\('([\d.]+)'\)", replace_decimals, data)
    # Convert the cleaned string to a Python list
    dat = ast.literal_eval(cleaned_output_str)

    column_name = llm.invoke(f"""create only column names list for use in pandas according to sql queary : {query}""")

    cleaned_output_str = re.sub(r"Decimal\('([\d.]+)'\)", replace_decimals, column_name.content)
    # Convert the cleaned string to a Python list
    col_list = ast.literal_eval(cleaned_output_str)
    print(col_list)
    data=pd.DataFrame(dat,columns=col_list)
    data.to_csv('01.csv',index=False)
    data1 = pd.read_csv('E:/practice/sql_langgraph/01.csv')

    result = llm_chain.run(data=dat)
    print('<<<<',result,'>>>>>>>>>')
    python_repl(result)

    img = 'E:/practice/sql_langgraph/bar_chart.png'
    return data1 , img

with gr.Blocks() as iface:
    csv_input = gr.Text(label="Ask Sql related Question")
    submit_button = gr.Button("Submit")

    with gr.Tabs():
        with gr.Tab("DataFrame"):
            dataframe_output = gr.DataFrame()
        
    with gr.Tab("Plot"):
        plot_output = gr.Image()
    
    submit_button.click(
        fn=answer_from_sql,
        inputs=csv_input,
        outputs=[dataframe_output, plot_output]
    )

iface.launch(server_port=7851)