from agent_swarm.agents.routeragent import RouterAgent
from agent_swarm.agents.knowledgeagent import KnowledgeAgent
from agent_swarm.agents.costumeragent import CostumerAgent
from agent_swarm.agents.pokemonagent import PokemonAgent
from agent_swarm.utils.personality import Personalities

class Manager:
    def __init__(self, key):
        self.RA = RouterAgent(key)
        self.KA = KnowledgeAgent(key)
        self.CA = CostumerAgent(key)
        self.PA = PokemonAgent(key)
        self.Personalities = Personalities(key)

    async def chat(self, message: str):
        raw_agent_response = ""
        personality_response = ""
        agent_workflow = []
        route = await self.RA.route(message)
        if route == 'knowledge':
            raw_agent_response = await self.KA.chat(message)
            personality_response = await self.Personalities.apply_knwoledge_personality(message, raw_agent_response)
            agent_workflow.append({
                "agent_name": "KnowledgeAgent",
                "tool_calls": {}
            })
        elif route == 'costumer':
            raw_agent_response = await self.CA.chat(message)
            personality_response = await self.Personalities.apply_costumer_personality(message, raw_agent_response)
            agent_workflow.append({
                "agent_name": "CostumerAgent",
                "tool_calls": {}
            })
        elif route == 'pokemon':
            raw_agent_response = await self.PA.chat(message)
            personality_response = await self.Personalities.apply_pokemon_personality(message, raw_agent_response)
            agent_workflow.append({
                "agent_name": "PokemonAgent",
                "tool_calls": {}
            })
        else:
            personality_response = "Sorry, I couldn't understand the request."
            agent_response = personality_response
            agent_workflow.append({
                "agent_name": "RouterAgent",
                "tool_calls": {"routing": "Unrecognized route"}
            })
        return {
            "response": personality_response,
            "source_agent_response": agent_response,
            "agent_workflow": agent_workflow
        }