import asyncio
from pydantic import ValidationError

from loader import LLMclient
from orchestrator.planner import Planner, PlannerResult
from agents.worker_agents import WorkerAgent
from agents.validator_agent import ValidatorAgent, ValidationResult

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import DiGraphBuilder, GraphFlow


WORKER_LIMIT = 3


def build_execution_graph(plan: PlannerResult, llm_client):
    builder = DiGraphBuilder() ## In this graph each node represent one agent instance ... 

    reflector = AssistantAgent(
        name="reflector",
        model_client=llm_client,
        system_message=(
            "You are a Reflection Agent.\n"
            "Synthesize worker outputs into one coherent answer.\n"
            "Improve clarity and structure.\n"
            "Do NOT add new facts.\n"
            "Do NOT validate correctness."
        ),
    )

    validator = ValidatorAgent().agent

    builder.add_node(reflector)
    builder.add_node(validator)

    workers = []

    for task in plan.tasks:
        worker = WorkerAgent(
            task.worker_name,
            task.task,
            task.instructions,
        )
        workers.append(worker.agent)
        builder.add_node(worker.agent)
        builder.add_edge(worker.agent, reflector)

    builder.add_edge(reflector, validator)

    return builder.build(), workers, reflector, validator


def parse_validation_output(raw_text: str) -> ValidationResult:
    cleaned = raw_text.strip().replace("```json", "").replace("```", "") ## Converts the string response to JSON format ... 
    try:
        return ValidationResult.model_validate_json(cleaned)
    except ValidationError as e:
        raise ValueError(
            f"Validator returned invalid JSON:\n{cleaned}\n\nError:\n{e}"
        )


def print_execution_tree(plan: PlannerResult):
    print("\nEXECUTION TREE\n")
    print("START → Planner")
    for i, task in enumerate(plan.tasks):
        print(f"   |-- Worker {i}: {task.worker_name} → Reflector")
    print("   |-- Reflector → Validator")
    print("   |-- FINAL OUTPUT\n")


async def main():
    query = input("What would you like to perform today? ")

    llm_client = LLMclient().llmclient

   
    plan = await Planner(WORKER_LIMIT).run(query)


    graph, workers, reflector, validator = build_execution_graph(plan, llm_client)


    team = GraphFlow(
        participants=[*workers, reflector, validator],
        graph=graph,
    )

    result = await team.run(task=query)

    reflector_output = None
    validator_raw_output = None

   
    for msg in result.messages:
        if msg.source == reflector.name:
            reflector_output = msg.content
        elif msg.source == validator.name:
            validator_raw_output = msg.content

    if reflector_output is None or validator_raw_output is None:
        raise RuntimeError("Missing output from reflector or validator")


    validation = parse_validation_output(validator_raw_output)


    if validation.is_valid: ## If validation is true show the reflector_output ... 
        print("\nFINAL ANSWER\n")
        print(reflector_output)
    else:
        print("\nVALIDATION FAILED\n")
        print(reflector_output)
        print("\nIssues:")
        for issue in validation.issues:
            print("-", issue)

    print_execution_tree(plan)


if __name__ == "__main__":
    asyncio.run(main())