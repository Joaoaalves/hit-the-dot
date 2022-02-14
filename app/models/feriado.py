from datetime import datetime

class Feriado():

    def __init__(self, data):
        if 'id' in data:
            self.id = data['id']
        self.nome = data['nome']
        self.dia = int(data['dia'])
        self.mes = int(data['mes'])

        self.repete = data['repete'] == True
        if not self.repete:
            self.ano = int(data['ano'])
    
    def get_date(self):
        now = datetime.now()
        if self.repete:
            return datetime(now.year, self.mes, self.dia)

        return datetime(self.ano, self.mes, self.dia)

    def get_formated_date(self):
        return self.get_date().strftime('%d/%m/%Y')

    def get_html_date(self):
        return self.get_date().strftime('%Y-%m-%d')

    def to_json(self):

        if self.repete:
            return {
                'nome' : self.nome,
                'dia' : self.dia,
                'mes' : self.mes,
                'repete' : True
            }
        
        else:
            return {
                'nome' : self.nome,
                'dia' : self.dia,
                'mes' : self.mes,
                'ano' : self.ano,
                'repete' : False
            }