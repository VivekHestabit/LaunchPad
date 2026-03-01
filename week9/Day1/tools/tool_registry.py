from autogen_core.tools import FunctionTool
from tools.web_search import search_and_clean

web_search_tool = FunctionTool(
    search_and_clean,
    description = (
        "Search the web using the EXACT FULL USER QUESTION. "
        "Do not shorten, abstract, or redefine the query. "
        "Return information ONLY about the given topic."
    ),
)
