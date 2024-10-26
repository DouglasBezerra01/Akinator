import json
from collections import Counter

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

    def __repr__(self):
        return self.nome

# Classe do Jogo
class JogoAkinator:
    def __init__(self, personagens):
        self.personagens = [Personagem(p) for p in personagens]
        self.caracteristicas = {
            "sexo": "Seu personagem é do sexo masculino?",
            "animacao": "Seu personagem é de uma animação?",
            "superpoder": "Seu personagem tem superpoderes?",
            "tipo": "Seu personagem é do tipo {}?",
            "universo": "Seu personagem é do universo {}?",
            "protagonista": "Seu personagem é o protagonista?"
        }

    # Filtrar personagens com base em uma característica
    def filtrar_personagens(self, chave, resposta):
        self.personagens = [p for p in self.personagens if getattr(p, chave) == resposta]

    # Escolher a próxima característica para perguntar
    def proxima_pergunta(self):
        # Conta os valores mais comuns para cada característica
        contadores = {caract: Counter(getattr(p, caract) for p in self.personagens) for caract in self.caracteristicas}

        # Escolher a característica com mais variação
        for caract, contador in contadores.items():
            if len(contador) > 1:  # Há variação suficiente para fazer uma pergunta
                valor_comum = contador.most_common(1)[0][0]  # Valor mais frequente
                return caract, valor_comum
        return None, None

    def jogar(self):
        while len(self.personagens) > 1:
            caract, valor = self.proxima_pergunta()
            if caract is None:
                break  # Se não há mais perguntas úteis, finaliza

            # Perguntar ao usuário sobre a característica com uma pergunta intuitiva
            pergunta = self.caracteristicas[caract].format(valor)
            resposta = input(f"{pergunta} (sim/nao): ").strip().lower()
            if resposta not in ["sim", "nao"]:
                print("Por favor, responda apenas com 'sim' ou 'não'.")
                continue

            # Filtrar com base na resposta do usuário
            if resposta == "sim":
                self.filtrar_personagens(caract, valor)
            else:
                self.personagens = [p for p in self.personagens if getattr(p, caract) != valor]

        # Resultado final
        if len(self.personagens) == 1:
            print(f"Acho que seu personagem é {self.personagens[0].nome}!")
        else:
            print("Não consegui adivinhar seu personagem. Tente novamente!")

# Execução do jogo
personagens = carregar_personagens()
jogo = JogoAkinator(personagens)
jogo.jogar()
