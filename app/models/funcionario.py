from .user import User
from datetime import timedelta, datetime

class Funcionario(User):

    _privilege = 2
    def __init__(self, data):
        self.name = data['name']
        self.id = data['id']
        self.email = data['email']
        self.cargo = data['cargo']
        self.turno = data['turno']
        
        if 'inicio_trabalho' in data:
            try:
                if '-' in data['inicio_trabalho']:
                    ano,mes,dia = data['inicio_trabalho'].split('-')
                    
                else:
                    dia,mes,ano = data['inicio_trabalho'].split('/')
                    
                self.inicio_trabalho = f'{dia}/{mes}/{ano}'
            
            except:
                self.inicio_trabalho = None
                
        if 'celular' in data:
            self.celular = data['celular']
            
        else:
            self.celular = None
            
        if 'dias_trabalho' in data:
            self.dias_trabalho = data['dias_trabalho']
        
    def set_turnos(self, turnos):
        self.turnos = turnos
        
        for turno in self.turnos:
            turno.set_tempo_total()
            
    def get_datetime_inicio_trabalho(self):
        ano,mes,dia = self.inicio_trabalho.split('/')
        return datetime(year=int(ano), month=int(mes), day=int(dia))
    
    def worked_this_date(self, date):
        for turno in self.turnos:
            dt = datetime.strptime(turno.dia, '%d/%m/%Y')
            
            if dt == date:
                return True
            
        return False
    def get_tempo_total_trabalho_mes(self, mes):
        if self.turnos:
            horas_totais = timedelta(seconds = 0)
            for turno in self.turnos:
                if int(turno.dia[3:5]) == mes:
                    horas = turno._horas_totais
                    horas_totais += timedelta(hours=horas.hour, minutes=horas.minute, seconds=horas.second)
                    
            return horas_totais 
            
        else:
            return None
    
    def get_month_total_shift(self, month):
        total_shift_time = 0
        
        for turno in self.turnos:
            t_month = turno['current_date'][3:5]
            if t_month == month:
                t_time = turno['total_shift_time']
                horas = int(t_time[:2])
                minutos = int(t_time[3:5])
                segundos = int(t_time[6:])
                total_shift_time += (horas * 3600) + (minutos * 60) + segundos
                
        return total_shift_time