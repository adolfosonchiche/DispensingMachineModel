import threading

class Rule:
    def __init__(self, action, id):
        self.action = action
        self.id = id
        
class State:
    def __init__(self, action, id):
        self.action = action
        self.id = id

class Model:
    def __init__(self, state,  action, perception):
        self.perception = perception
        self.state = state
        self.action = action

class Machine:
    def __init__(self):
        self.index = 0
        self.state = []
        self.perception = 'recibi-moneda'
        self.state.append(State( 'sin-moneda', 0))
        self.state.append(State( 'recibi-moneda', 1))  
        self.state.append(State( 'servido-c1', 2))
        self.state.append(State( 'servido-c2', 3))
        self.state.append(State( 'servido-c3', 4)) 
        
        self.rule = []
        self.rule.append(Rule( 'pedir-moneda', 'sin-moneda'))
        self.rule.append(Rule( 'pedir-codigo', 'moneda'))  
        self.rule.append(Rule( 'servir-c1-esperar', 'c1'))
        self.rule.append(Rule( 'servir-c2-esperar', 'c2'))
        self.rule.append(Rule( 'servir-c3-esperar', 'c3'))
        
        self.model = []
        self.model.append(Model('sin-moneda', 'pedir-moneda', "recibi-moneda"))
        self.model.append(Model('recibi-moneda', 'pedir-codigo', "servido-c1"))
        self.model.append(Model('recibi-moneda', 'pedir-codigo', "servido-c2"))
        self.model.append(Model('recibi-moneda', 'pedir-codigo', "servido-c3"))
        self.model.append(Model('servido-c1', 'servir-c1-esperar', "sin-moneda"))
        self.model.append(Model('servido-c2', 'servir-c2-esperar', "sin-moneda"))
        self.model.append(Model('servido-c3', 'servir-c3-esperar', "sin-moneda"))
        self.model.append(Model('recibi-moneda', 'pedir-codigo', "recibi-moneda"))
        self.currentModel = Model(self.state[0].action,  "pedir-moneda", "")       

    def rule_action(self, action):
        self.index = 0
        for i, objet in enumerate(self.rule):
            if objet.id == action and action == 'moneda':
                self.index = i
                break
            
        if self.index == 0:
            return Rule("pedir-moneda", "")            
        return self.rule[self.index]
    
    def verify_code(self, code):
        index = -1
        for i, objet in enumerate(self.rule):
            if objet.id == code and code != 'moneda':
                self.currentModel = Model(self.state[0].action,  self.rule[0].action, "")
                index = i
                break
            
        if index == -1 or index == 0:
            return Rule("pedir-codigo", "")            
        return self.rule[index]
    
    def update_status(self, state, action, perception):
        rule = self.rule_action(perception)
        state_rule = self.state[self.index]
        if(self.exist_model(state, action, state_rule.action)):            
            self.currentModel = Model(state_rule.action, rule.action, "")
            return state_rule
                  
        return state
    
    def exist_model(self, state, action, perception):
        model_received = Model(state, action, perception)
        for i, objet in enumerate(self.model):
            if objet.perception == model_received.perception:
                return True                  
        return False 
        


class User(threading.Thread):
    def __init__(self, machine):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            init_action = machine.currentModel
            print('\nIngrese  una moneda') 
            percepcion = input()
            
            status = machine.update_status(init_action.state, init_action.action, percepcion)
            
            action = machine.rule[status.id]
            if action.id == 'moneda':
                soft_drink_served = True
                while soft_drink_served:
                    print('\nIngrese codigo de refresco:') 
                    code = input()
                    action = machine.verify_code(code)
                    if action.action!= 'pedir-codigo':
                        soft_drink_served = False
                    if soft_drink_served:
                        print(action.action + '\n')    
            print(action.action + '\n')
            
            threading.Event().wait(2)
            
            
machine = Machine()

user = User(machine)
user.start()