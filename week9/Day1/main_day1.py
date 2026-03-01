import asyncio
from agents.research_agent import research_agent
from agents.summarizer_agent import summarizer_agent
from agents.answer_agent import answer_agent


async def run_pipeline(user_query: str):
    print()
    research_result = await research_agent.run(task=user_query)
    research_text = research_result.messages[-1].content
    print("RESEARCH RESULT\n" , research_text )
    print()
    
    summary_result = await summarizer_agent.run(
        task=research_text
    )
    summary_text = summary_result.messages[-1].content
    print("SUMMARY RESULT : \n" ,summary_text )
    print()

    final_result = await answer_agent.run(
        task=summary_text
    )
    return final_result.messages[-1].content
    


if __name__ == "__main__":
    query = input("What would you like to research ? ")
    result = asyncio.run(run_pipeline(query))
    print("FINAL RESULT : \n" , result)