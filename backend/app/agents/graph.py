from langgraph.graph import StateGraph, END
from app.models.workflow import AgentState
from app.agents.nodes import drafter_node, critic_node
from app.core.logging import logger

def should_continue(state: AgentState):
    """
    Router logic: Decides whether to loop back or finish.
    """
    critique = state.get("critique", "")
    count = state.get("revision_count", 0)
    
    # Condition 1: Approved
    if "APPROVE" in critique.upper():
        logger.info("✅ Draft Approved!")
        return "end"
    
    # Condition 2: Max retries reached (Safety Break)
    if count >= 3:
        logger.warning("⚠️ Max revisions reached. Stopping loop.")
        return "end"
    
    # Condition 3: Needs revision
    logger.info(f"🔄 Revision needed. Loop {count}/3. Feedback: {critique[:50]}...")
    return "revise"

# 1. Initialize Graph
workflow = StateGraph(AgentState)

# 2. Add Nodes
workflow.add_node("drafter", drafter_node)
workflow.add_node("critic", critic_node)

# 3. Define Edges
# Start -> Drafter
workflow.set_entry_point("drafter")

# Drafter -> Critic
workflow.add_edge("drafter", "critic")

# Critic -> Conditional (Approve or Revise?)
workflow.add_conditional_edges(
    "critic",
    should_continue,
    {
        "end": END,
        "revise": "drafter"
    }
)

# 4. Compile
app = workflow.compile()