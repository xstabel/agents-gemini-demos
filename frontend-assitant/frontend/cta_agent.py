"""! @brief: Implementation of the Agent using LangChain."""

from langchain.agents.format_scratchpad import (
    format_to_openai_function_messages,
)
from langchain_google_vertexai import ChatVertexAI
from langchain_core.messages import SystemMessage
from langchain_core.pydantic_v1 import BaseModel
#from state import AssistantAgentState
import streamlit as st
from langchain_core.tools import tool
from datetime import datetime
from langchain_core.messages.base import BaseMessage, BaseMessageChunk
from typing import Literal
from langgraph.graph import MessageGraph, START , END , StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
import google.auth.transport.requests
import google.oauth2.id_token
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import ToolMessage
import json
import urllib
import os

@tool
def get_weather(city: str = "Lima") -> str:
    """
    This function get updated weather information for a given city and dates. 
    Useful for clothing advice and planning activities. If a city is not given then ask for it to complete your request. 
    :param city: A string with the name of a city to get the weather for and call the weather API
    :return: a string containing the response
    """
    print("@@@@@@@@@@")
    print("@@@@@@@@@@" + city)
    url_api = os.environ.get("API_WEATHER_URL")
    if not url_api:
        raise Exception("API_WEATHER_URL missing")
    url=f"{url_api}/meteocris"

    req = urllib.request.Request( url+'?cityname='+city.upper() )
    # add the logic to call the remote authentication when running in cloud run or from local development
    if google.auth.default()[0].requires_scopes:        
        auth_req = google.auth.transport.requests.Request()
        target_audience = url
        id_token = google.oauth2.id_token.fetch_id_token(auth_req, target_audience)
        req.add_header("Authorization", f"Bearer {id_token}")
    else:
        print("@@@@@@@@@@ from local")
    response = urllib.request.urlopen(req)
    jsonloads= json.loads(response.read())
    print(f"***agent.py 3 in new_request controller.py response.read - {response.read()} !") 
    jsondumps=json.dumps(jsonloads)
    print(f"***agent.py 4 in new_request controller.py response - {jsondumps} !") 
    dataweather = {}
    dataweather['city'] = city
    dataweather['weather'] = jsondumps
    print(f"***agent.py 5 in new_request data - {dataweather} !") 
    return dataweather 

@tool
def get_ctaciaInfo(question: str = "emKszv8xjISy446FJNmK") -> str:
    """
    This function Get info about a term related to the company cta-cia, its history and human team, but also the capabilities and details about the cta-cia's AI: Ken."
    :param question: A question posed by a user that requires answering
    :return: a dictionary containing the information about Meteo
    """
    print("@@@@@@@@@@")
    print(question)
    return {"Info": "cta-cia es una empresa dedicada a dar información útil del tiempo ..."}


@tool
def get_meteoGlossary(getconcept: str):
    """
    This function Get definitions of meteorological concepts
    :param getconcept: the concept to obtain a definition
    :return: all the information about that concept
    """
    print("@@@@@@@@@@")
    print(getconcept)
    return {"getconcept": "Concepto 1 de metereología"}

# NEW TOOL REF #REQ-TEC-123
@tool
def get_temperature(city: str):
    """
    This function get the temperature for a given city. 
    Useful for clothing advice and planning activities.
    :param city: A string with the name of a city to get the temperature for and call the temperature API
    :return: a string containing the response
    """
    print("@@@@@@@@@@")
    print("@@@@@@@@@@" + city)
   
    url_api = os.environ.get("API_WEATHER_URL")
    if not url_api:
        raise Exception("API_WEATHER_URL missing")
    url=f"{url_api}/get_temperature"

    req = urllib.request.Request( url+'?cityname='+city.upper() )
    # add the logic to call the remote authentication when running in cloud run or from local development
    if google.auth.default()[0].requires_scopes:
        print("@@@@@@@@@@ from local")
        auth_req = google.auth.transport.requests.Request()
        target_audience = url
        id_token = google.oauth2.id_token.fetch_id_token(auth_req, target_audience)
        req.add_header("Authorization", f"Bearer {id_token}")
    else:
        print("@@@@@@@@@@ from local")
    response = urllib.request.urlopen(req)
    response = urllib.request.urlopen(req)
    jsonloads= json.loads(response.read())
    print(f"***agent.py  3 in get_temperature controller.py response.read - {response.read()} !") 
    jsondumps=json.dumps(jsonloads)
    print(f"***agent.py  4 in get_temperature controller.py response - {jsondumps} !") 
    dataweather = {}
    # default data
    dataweather['city'] = city
    dataweather['weather'] = jsondumps
    print(f"***agent.py 5 in get_temperature data - {dataweather} !") 
    return dataweather #

@tool
def get_supportTool(getsupport: str):
    """
    This function Get technical support about the app or handle"
    :param getsupport: the concept to ask for help
    :return: all the information for helping the user about the concept {getsupport}
    """
    print("@@@@@@@@@@")
    print(getsupport)
    return {"getsupport": "Nuestro servicio de soporte está disponible!"}


TOOLS = [get_weather, get_ctaciaInfo, get_meteoGlossary, get_supportTool, get_temperature]
llm = ChatVertexAI(model_name="gemini-2.0-flash-exp")
llm_with_tools = llm.bind_tools(TOOLS)


# --- Define State and Graph ---
class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)


def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"], prompt=prompt)]}


graph_builder.add_node("chatbot", chatbot)


class BasicToolNode:
    """A node that runs the tools requested in the last AIMessage."""

    def __init__(self, tools: list) -> None:
        self.tools_by_name = {tool.name: tool for tool in tools}

    def __call__(self, inputs: dict):
        if messages := inputs.get("messages", []):
            message = messages[-1]
        else:
            raise ValueError("No message found in input")
        outputs = []
        for tool_call in message.tool_calls:
            tool_result = self.tools_by_name[tool_call["name"]].invoke(
                tool_call["args"]
            )
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": outputs}


tool_node = BasicToolNode(tools=TOOLS)
graph_builder.add_node("tools", tool_node)


def route_tools(
    state: State,
) -> Literal["tools", "__end__"]:
    """
    Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route to the end.
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return "__end__"


graph_builder.add_conditional_edges(
    "chatbot",
    route_tools,
    {"tools": "tools", "__end__": "__end__"},
)
# Any time a tool is called, we return to the chatbot to decide the next step
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
graph = graph_builder.compile()

# --- Streamlit App ---
st.title("Tempo Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Process user input with the LangGraph
    full_response = ""
    with st.chat_message("assistant"):      
        message_placeholder = st.empty()
        for event in graph.stream({"messages": [("user", prompt)]}):
            for value in event.values():
                if isinstance(value["messages"][-1], BaseMessage):
                   response = value["messages"][-1].content
                   full_response += response
                   message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
