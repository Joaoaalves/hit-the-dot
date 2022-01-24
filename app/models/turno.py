from datetime import datetime, timedelta

from flask.helpers import total_seconds
class Turno:
    _horas_totais = timedelta(seconds=0)
    _segundos_totais = 0
    def __init__(self, data):
        
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
            self.almocou = True

        if 'fim_almoco' in data:
            self.fim_almoco = data['fim_almoco']

    
    
    def set_tempo_total(self):
        str_horas_totais = self.get_total_time_str()
        self._horas_totais = self.converter_str_datetime(str_horas_totais)
        self._segundos_totais = self._horas_totais.second + self._horas_totais.minute * 60 + self._horas_totais.hour * 3600
        
    def get_tempo_almoco(self):
        if self.almocou:
            breakin_time = self.converter_str_datetime(self.inicio_almoco)
            breakout_time = self.converter_str_datetime(self.fim_almoco)
            total_time = breakout_time - breakin_time
            return timedelta(seconds=total_time.seconds)
            
            
        return timedelta(seconds=0)
        
    def get_total_time_str(self):
        initial_time = self.converter_str_datetime(self.hora_entrada)
        final_time = self.converter_str_datetime(self.hora_saida)

        total_time = (final_time - initial_time) - self.get_tempo_almoco()
                
        return str(total_time) 
 
    def get_month(self):
        return datetime.strptime(self.dia, '%d/%m/%Y').month
        
    def converter_str_datetime(self, dt):
        return datetime.strptime(dt, '%H:%M:%S')
    
    def get_dia_html(self):
        return f'{self.dia[-4:]}-{self.dia[3:5]}-{self.dia[:2]}'

    def to_json(self):
        if self.almocou:
            return {
                'dia' : self.dia,
                'hora_entrada' : self.hora_entrada,
                'hora_saida' : self.hora_saida,
                'inicio_almoco' : self.inicio_almoco,
                'fim_almoco' : self.fim_almoco,
                'user_id' : self.user_id,
                'current_status' : self.current_status,
                'almocou' : self.almocou
            }
        else:
            return {
                'dia' : self.dia,
                'hora_entrada' : self.hora_entrada,
                'hora_saida' : self.hora_saida,
                'user_id' : self.user_id,
                'current_status' : self.current_status,
                'almocou' : self.almocou
            }