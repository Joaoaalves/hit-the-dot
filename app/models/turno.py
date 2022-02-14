from datetime import datetime, timedelta

class Turno:
    _horas_totais = timedelta(seconds=0)
    _segundos_totais = 0
    def __init__(self, data):
        if 'id' in data:
            self.id = data['id']

        self.dia = data['dia']
        self.hora_entrada = data['hora_entrada']
        self.current_status = data['current_status']
        self.user_id = int(data['user_id'])
        self.almocou = False
        
        if 'turno_funcionario':
            self.turno_funcionario = data['turno_funcionario']
        
        if 'hora_saida' in data:
            self.hora_saida = data['hora_saida']

        if 'inicio_almoco' in data:
            self.inicio_almoco = data['inicio_almoco']
            self.almocou = data['almocou'] == 1

        if 'fim_almoco' in data:
            self.fim_almoco = data['fim_almoco']

    def set_tempo_total(self):
        self._segundos_totais = (self.hora_saida.seconds - self.hora_entrada.seconds) - self.get_tempo_almoco().seconds
        self._horas_totais = self._segundos_totais // 3600
        
    def get_tempo_almoco(self):
        if self.almocou:
            return self.fim_almoco - self.inicio_almoco
            
        return timedelta(seconds=0)
        
    def get_total_time_str(self):


        total_time = (self.hora_saida - self.hora_entrada) - self.get_tempo_almoco()
                
        return str(total_time) 
 
    def get_month(self):
        return datetime.strptime(self.dia, '%d/%m/%Y').month
        
    def converter_str_datetime(self, dt):
        return datetime.strptime(dt, '%H:%M:%S')
    
    def get_formated_date(self):
        return datetime.strftime(self.dia, '%d/%m/%Y')

    def to_json(self):
        if self.almocou:
            return {
                'dia' : datetime.strptime(self.dia, '%d/%m/%Y').strftime('%Y-%m-%d'),
                'hora_entrada' : str(self.hora_entrada),
                'hora_saida' : str(self.hora_saida),
                'inicio_almoco' : str(self.inicio_almoco),
                'fim_almoco' : str(self.fim_almoco),
                'user_id' : self.user_id,
                'current_status' : self.current_status,
                'almocou' : int(self.almocou),
                'turno_funcionario' : self.turno_funcionario
            }
        else:
            return {
                'dia' : datetime.strptime(self.dia, '%d/%m/%Y').strftime('%Y-%m-%d'),
                'hora_entrada' : str(self.hora_entrada),
                'hora_saida' : str(self.hora_saida) if self.hora_saida else None,
                'user_id' : self.user_id,
                'current_status' : self.current_status,
                'almocou' : int(self.almocou),
                'turno_funcionario' : self.turno_funcionario
            }