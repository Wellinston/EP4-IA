import skfuzzy as fz
from skfuzzy import control as ctrl
import numpy as np

class Fuzzy:
    def __init__(self):
        self.text = None
        self.point = 0
        self.positiveWords = ["feliz", "bom", "ótimo", "alegre", "maravilhoso", "encantador", "fantástico", "adorável", "excelente", "bonito", "lindo", "incrível"]
        self.negativeWords = ["raiva", "ódio", "desespero", "mágoa", "desgosto", "desânimo", "amargura", "frustração", "desapontamento", "ressentimento", "solidão", "inveja"]
        self.intensifiers = ["muito", "extremamente", "absolutamente", "completamente", "altamente", "bastante", "totalmente"]
        self.negations = ["não", "nunca", "jamais", "nada", "ninguém", "nem"]
        
        PosWord = ctrl.Antecedent(np.arange(0, 2, 1), "FP")
        NegWord = ctrl.Antecedent(np.arange(0, 2, 1), "FN")
        IntensWord = ctrl.Antecedent(np.arange(0, 2, 1), "I")
        NegationWord = ctrl.Antecedent(np.arange(0, 2, 1), "N")

        PosWord.automf(names=["Não", "Sim"])
        NegWord.automf(names=["Não", "Sim"])
        IntensWord.automf(names=["Não", "Sim"])
        NegationWord.automf(names=["Não", "Sim"])
        
        sentiment = ctrl.Consequent(np.arange(0, 11, 1), "Sentimento")
        
        sentiment["Negativo"] = fz.trimf(sentiment.universe, [0, 2, 3])
        sentiment["Neutro"] = fz.trimf(sentiment.universe, [2, 4, 6])
        sentiment["Positivo"] = fz.trimf(sentiment.universe, [4, 7, 10])
        
        rule1 = ctrl.Rule(PosWord["Sim"], sentiment["Positivo"])
        rule2 = ctrl.Rule(NegWord["Sim"] & NegationWord["Sim"], sentiment["Positivo"])
        rule3 = ctrl.Rule(NegWord["Não"] & PosWord["Não"], sentiment["Neutro"])
        rule4 = ctrl.Rule(PosWord["Sim"] & NegationWord["Sim"], sentiment["Negativo"]) 
        rule5 = ctrl.Rule(NegWord["Sim"] & IntensWord["Sim"], sentiment["Negativo"])
        
        rules = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
        self.sys = ctrl.ControlSystemSimulation(rules)
      
    def setText(self, text):
        self.text = text
        wordList = text.split(" ")
        
        self.sys.input["FP"] = 0 
        self.sys.input["FN"] = 0  
        self.sys.input["I"] = 0   
        self.sys.input["N"] = 0   
        
        for i in range(len(wordList)):
            if wordList[i] in self.positiveWords:
                self.sys.input["FP"] = 1
                if i >= 1:
                    if wordList[i-1] in self.intensifiers:
                        self.sys.input["I"] = 1
                        return
                    elif wordList[i-1] in self.negations:
                        self.sys.input["N"] = 1
                        return
                if i+1 < len(wordList):
                    if wordList[i+1] in self.intensifiers:
                        self.sys.input["I"] = 1
                        return
                    elif wordList[i+1] in self.negations:
                        self.sys.input["N"] = 1
                        return
            elif wordList[i] in self.negativeWords:
                self.sys.input["FN"] = 1
                if i >= 1:
                    if wordList[i-1] in self.intensifiers:
                        self.sys.input["I"] = 1
                        return
                    elif wordList[i-1] in self.negations:
                        self.sys.input["N"] = 1
                        return
                if i+1 < len(wordList):
                    if wordList[i+1] in self.intensifiers:
                        self.sys.input["I"] = 1
                        return
                    elif wordList[i+1] in self.negations:
                        self.sys.input["N"] = 1
                        return

    def compute(self):
        self.sys.compute()
        self.point = self.sys.output["Sentimento"]

    def showRaw(self):
        print(self.point)

    def polaritySentiment(self):
        if 0 < self.point < 3:
            print("Negativo")
        elif 2 < self.point < 6:
            print("Neutro")
        elif 4 < self.point < 10:
            print("Positivo")


if __name__ == "__main__":
    fuzzy = Fuzzy()
    phrases = [
        "Estou extremamente feliz com os resultados do meu trabalho. É absolutamente maravilhoso!",
        "Nada pode me deixar completamente triste hoje. Estou altamente alegre!",
        "Sou completamente grato pela oportunidade incrível que me foi dada.",
        "Nunca vi um dia tão bom como hoje. É fantástico!",
        "A experiência que tive no parque de diversões foi muito intensa e adorável.",
        "Não existe nada melhor do que passar um tempo com amigos e se divertir muito. É ótimo!",
        "Estou profundamente encantado com o pôr do sol que vi na praia. É realmente maravilhoso.",
        "De jeito nenhum vou esquecer a sensação de completude que sinto quando estou com minha família.",
        "Essa viagem foi além das minhas expectativas. Estou completamente satisfeito!",
        "Nem consigo expressar o quão excelente foi o concerto que assisti ontem. Foi incrível!"
    ]
    
    for phrase in phrases:
        print("___________________________")
        print("___________________________")
        fuzzy.setText(phrase)
        fuzzy.compute()
        print("Sentença:\n" + phrase + "")
        fuzzy.showRaw()
        print("______________")
        print("Sentimento:")
        fuzzy.polaritySentiment()
        
        
