class TipoTarefa():
    
    def __init__(self, data):
        
        self.id = data['id']
        self.nome = data['nome']
        self.pontuacao = data['pontuacao']
        self.horas_planejadas = data['horas_planejadas']
    