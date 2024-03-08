import threading

class State:
    def __init__(self, action, id):
        self.action = action
        self.id = id

class Rule:
    def __init__(self, state, action):
        self.state = state
        self.action = action
        
class Model:
    def __init__(self, state,  action, perception):
        self.perception = perception
        self.state = state
        self.action = action
        

class Machine:
    def __init__(self):
        
        self.state = []
        self.state.append(State( 'sin-moneda', 0))
        self.state.append(State( 'recibi-moneda', 1))  
        self.state.append(State( 'servido-c1', 2))
        self.state.append(State( 'servido-c2', 3))
        self.state.append(State( 'servido-c3', 4)) 
        
        self.rule = []
        self.rule.append(Rule(self.state[0], 'pedir-moneda'))
        self.rule.append(Rule(self.state[1], 'pedir-codigo'))
        self.rule.append(Rule(self.state[2], 'servir-c1-esperar'))
        self.rule.append(Rule(self.state[3], 'servir-c2-esperar'))
        self.rule.append(Rule(self.state[4], 'servir-c3-esperar'))
        
        self.model = []
        self.model.append(Model('sin-moneda', 'pedir-moneda', "recibi-moneda"))
        self.model.append(Model('recibi-moneda', 'pedir-codigo', "servido-c1"))
        self.model.append(Model('recibi-moneda', 'pedir-codigo', "servido-c2"))
        self.model.append(Model('recibi-moneda', 'pedir-codigo', "servido-c3"))
        self.model.append(Model('servido-c1', 'servir-c1-esperar', "sin-moneda"))
        self.model.append(Model('servido-c2', 'servir-c2-esperar', "sin-moneda"))
        self.model.append(Model('servido-c3', 'servir-c3-esperar', "sin-moneda"))
        self.model.append(Model('recibi-moneda', 'pedir-codigo', "recibi-moneda"))
        self.currentModel = Model(self.state[0],  "pedir-moneda", "recibi-moneda")
        
    def update_status(self, state, action, perception):
        if(self.exist_model(state, action, perception)):
            print('existe')
            return self.currentModel
                  
        return self.model[0]
    
    def exist_model(self, state, action, perception):
        model_received = Model(state, action, perception)
        for i, objet in enumerate(self.model):
            if objet == model_received:
                for i, objet_rule in enumerate(self.rule):
                    if objet_rule.state == perception:
                        self.currentModel = Model(model_received.perception, objet_rule.action, "" )
                       #self.currentModel = Model(model_received.perception, )
                    return True
                  
        return False 

    
        


class User(threading.Thread):
    def __init__(self, machine):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            init_action = machine.currentModel
            print('\nIngrese una ' + init_action.action) 
            percepcion = input()
            
            action = machine.update_status(machine.currentModel.state, machine.currentModel.action, percepcion)
            
            
            print(action.action)
            
            
            threading.Event().wait(2)
            
            
machine = Machine()

user = User(machine)
user.start()