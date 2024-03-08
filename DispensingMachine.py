import threading

class Rule:
    def __init__(self, action, id):
        self.action = action
        self.id = id

class Machine:
    def __init__(self):
        self.rule = []
        self.rule.append(Rule( 'pedir-codigo', 'moneda'))  
        self.rule.append(Rule( 'servir refresco 1', 'c1'))
        self.rule.append(Rule( 'servir refresco 2', 'c2'))
        self.rule.append(Rule( 'servir refresco 3', 'c3'))            

    def rule_action(self, action):
        index = -1
        for i, objet in enumerate(self.rule):
            if objet.id == action:
                index = i
                break
            
        if index == -1:
            return Rule("percepcion incorrecto!!", "")            
        return self.rule[index]
    
    def verify_code(self, code):
        index = -1
        for i, objet in enumerate(self.rule):
            if objet.id == code:
                index = i
                break
            
        if index == -1 or index == 0:
            return Rule("codigo invalido!!", "")            
        return self.rule[index]
        


class User(threading.Thread):
    def __init__(self, machine):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            print('\nIngrese una percepcion:') 
            percepcion = input()
            
            action = machine.rule_action(percepcion)
            
            if action.id == 'moneda':
                print('\nIngrese codigo de refresco:') 
                code = input()
                action = machine.verify_code(code)
            print(action.action)
            
            threading.Event().wait(2)
            
            
machine = Machine()

user = User(machine)
user.start()