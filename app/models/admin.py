from .funcionario import Funcionario

class Admin(Funcionario):

    _privilege = 4

    def remove_user(self, user_id, db):
        try:
            db.remove_user(user_id)
            
            return True

        except Exception as e:
            
            return e