from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.core.config import settings
from app.models.workflow import AgentState
from app.agents.prompts import DRAFTER_PROMPT, CRITIC_PROMPT
from app.core.logging import logger

# Initialize LLM
llm = ChatOpenAI(
    api_key=settings.OPENAI_API_KEY,
    model=settings.OPENAI_MODEL_ID,
    temperature=0.2 # Low temperature for factual consistency
)

def drafter_node(state: AgentState) -> AgentState:
    """
    Generates or revises the technical draft.
    """
    logger.info("✍️ Drafter Agent is working...")
    
    # Format the prompt with current state
    context_str = "\n".join(state.get("context", []))
    draft = state.get("draft", "")
    critique = state.get("critique", "")
    
    formatted_prompt = DRAFTER_PROMPT.format(
        context=context_str,
        query=state["query"],
        current_draft=draft if draft else "None",
        critique=critique if critique else "None"
    )
    
    response = llm.invoke([HumanMessage(content=formatted_prompt)])
    
    # Update state
    return {
        "draft": response.content,
        "revision_count": state.get("revision_count", 0) + 1
    }

def critic_node(state: AgentState) -> AgentState:
    """
    Reviews the draft against guidelines.
    """
    logger.info("🧐 Critic Agent is reviewing...")
    
    context_str = "\n".join(state.get("context", []))
    draft = state.get("draft", "")
    
    formatted_prompt = CRITIC_PROMPT.format(
        context=context_str,
        draft=draft
    )
    
    response = llm.invoke([HumanMessage(content=formatted_prompt)])
    
    return {
        "critique": response.content
    }