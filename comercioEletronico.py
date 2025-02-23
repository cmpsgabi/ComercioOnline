from maspy import *
from maspy.learning import *

class ComercioOnline(Environment):
    def __init__(self, env_name = None):
        super().__init__(env_name)

        for i in range(1, 3):
            self.create(Percept(f"Produto_{i}", 
                                ("0,0,0", "0,1,0", "0,1,1", "0,1,0", "0,0,1", 
                                "1,0,0", "1,1,0", "1,1,1", "1,0,1"), listed))
        
        for i in range(1, 3):
            self.possible_starts[f"Produto_{i}"] = (5, 5, 5)

    def sugestao_compra(self, state: dict, produto_cliente: tuple[str, tuple]):
        produto, cliente = produto_cliente #acao que se quer realizar

        produto_state: str = state[produto] #estado atual do produto

        media, promocao, repetido = int = cliente.split(',')
        mediaAtual, promocaoAtual, repetidoAtual = int = produto_state.split(',')

        #se a ação quer sugerir pro mesmo cliente já sugerido ou se o produto já foi sugerido e a ação quer sugerir ele de novo
        if produto_state == cliente or (mediaAtual or promocaoAtual or repetidoAtual) != 5:
            reward = -6
            terminated = True
        else:
            state[produto] = cliente

            if media or promocao or repetido == 5:
                reward = -6
            else:
                if media + promocao + repetido == 0:
                    reward = -4
                if media + promocao + repetido == 1:
                    reward = +2
                if media + promocao + repetido == 2:
                    reward = +4
                if media + promocao + repetido == 3:
                    reward = +6
    
            terminated = False

        for value in state.values():
            mediaAtual, promocaoAtual, repetidoAtual = int = value.split(',')

            if mediaAtual or promocaoAtual or repetidoAtual != 5:
                continue
            break
        else:
            terminated = True
        
        return state, reward, terminated
    
    
    @action(cartesian, (("Produto_1", "Produto_2"), 
                        ("0,0,0", "0,1,0", "0,1,1", "0,1,0", "0,0,1", 
                         "1,0,0", "1,1,0", "1,1,1", "1,0,1")), sugestao_compra)
    def sugestao(self, agt, produto_cliente: tuple[str, tuple]):
        produto, cliente = produto_cliente

        produtopercepcao = self.get(Percept(produto, Any))
        assert isinstance(produtopercepcao, Percept)

        self.print(f"{agt} ta sugerindo {produto} pro {cliente}")

class Cliente(Agent):
    def __init__(agt_name):
        super().__init__(agt_name)

        agt_name.media = 0
        agt_name.promocao = 0
        agt_name.repetido = 1
        


class Vendedor(Agent):

    @pl(gain, Goal("criar_modelo", Any))
    def criarModelo(self, src, model_list: list[EnvModel]):
        model = model_list[0]

        model.learn(qlearning, num_episodes = 20)
        ag.auto_action = True
        ag.add_policy(model)
        
if __name__ == "__main__":
    env = ComercioOnline()
    model = EnvModel(env)
    ag = Vendedor()
    ag.add(Goal("criar_modelo", [model]))
    
    Admin().start_system