class Tarefa:
    
    def __init__(self, data):
        
        self.nome = data['nome']
        
        try:
            self.id = int(data['id'])
            self.tipo = int(data['tipo'])
            
        except Exception as e:
            raise e