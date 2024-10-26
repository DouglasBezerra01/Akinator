import json

# Carregar os dados do JSON
def carregar_personagens():
    with open("personagens.json", 'r') as f:
        dados = json.load(f)
    return dados

# Classe de Personagem
class Personagem:
    def __init__(self, dados):
        self.nome = dados["nome"]
        self.sexo = dados["sexo"]
        self.animacao = dados["animacao"]
        self.superpoder = dados["superpoder"]
        self.tipo = dados["tipo"]
        self.universo = dados["universo"]
        self.idade = dados["idade"]
        self.protagonista = dados["protagonista"]

# Classe para as perguntas da árvore de decisão
class Pergunta:
    def __init__(self, texto, chave, criterio=None):
        self.texto = texto
        self.chave = chave
        self.criterio = criterio
        self.sim = None
        self.nao = None

# Construir a árvore de perguntas
def construir_arvore():
    raiz = Pergunta("Seu personagem é do sexo masculino?", "sexo", "masculino")

    # Perguntas com base nos atributos dos personagens
    raiz.sim = Pergunta("Seu personagem é de um universo de super-heróis?", "tipo", "herói")
    raiz.nao = Pergunta("Seu personagem tem superpoderes?", "superpoder", True)

    raiz.sim.sim = Pergunta("Seu personagem é do universo Marvel?", "universo", "Marvel")
    raiz.sim.nao = Pergunta("Seu personagem é o protagonista?", "protagonista", True)
    
    raiz.nao.sim = Pergunta("Seu personagem aparece em animação?", "animacao", True)
    raiz.nao.nao = Pergunta("Seu personagem é jovem (idade < 25)?", "idade", "jovem")

    return raiz

# Classe do Jogo
class JogoAkinator:
    def __init__(self, personagens):
        self.personagens = [Personagem(p) for p in personagens]
        self.arvore = construir_arvore()

    def filtrar_personagens(self, chave, resposta, criterio):
        if chave == "idade":
            if resposta == "sim":
                self.personagens = [p for p in self.personagens if p.idade < 25]
            else:
                self.personagens = [p for p in self.personagens if p.idade >= 25]
        else:
            if resposta == "sim":
                self.personagens = [p for p in self.personagens if getattr(p, chave) == criterio]
            else:
                self.personagens = [p for p in self.personagens if getattr(p, chave) != criterio]

    def jogar(self):
        no = self.arvore

        while no and len(self.personagens) > 1:
            resposta = input(f"{no.texto} (sim/nao): ").strip().lower()
            if resposta not in ["sim", "nao"]:
                print("Por favor, responda apenas com 'sim' ou 'não'.")
                continue

            # Filtra personagens e avança para o próximo nó
            self.filtrar_personagens(no.chave, resposta, no.criterio)
            no = no.sim if resposta == "sim" else no.nao

        # Exibe resultado final
        if len(self.personagens) == 1:
            print(f"Acho que seu personagem é {self.personagens[0].nome}!")
        else:
            print("Não consegui adivinhar seu personagem. Tente novamente!")

# Execução do jogo
personagens = carregar_personagens()
jogo = JogoAkinator(personagens)
jogo.jogar()
