from agent_swarm.agents.routeragent import RouterAgent
from agent_swarm.agents.knowledgeagent import KnowledgeAgent
from agent_swarm.agents.costumeragent import CostumerAgent
from agent_swarm.agents.pokemonagent import PokemonAgent

class Manager:
    def __init__(self):
        self.RA = RouterAgent()
        self.KA = KnowledgeAgent()
        self.CA = CostumerAgent()
        self.PA = PokemonAgent()

    async def chat(self, message: str):
        route = self.RA.route(message)
        if route == 'knowledge':
            self.KA.chat(message)
        elif route == 'costumer':
            self.CA.chat(message)
        elif route == 'pokemon':
            self.PA.chat(message)