import random
registred_states = {}
global num
global transId

def get_state(state_id):
    return registred_states[state_id]

class Transition:

    def __init__(self, to_id, synonims):
        self.to_id = to_id
        self.synonims = synonims
    
    def must_go(self, user_text):
        return user_text in self.synonims

    def get_dest_id(self):
        return self.to_id

class State:
    
    def __init__(self, id, text, transitions, default_transitions, is_end = False):
        self.id = id
        self.text = text
        self.transitions = transitions
        self.default_transitions = default_transitions
        self.is_end = is_end
    
    def get_next_state(self, user_input):
        for transitions in self.transitions:
            if transitions.must_go(user_input):
                return get_state(transitions.to_id)
        return get_state(self.default_transitions)
    
    def register(self):
        global registred_states
        registred_states[self.id] = self
    
    def get_id(self):
        return self.id

    def get_text(self):
        return self.text()

    def is_end_state(self):
        return self.is_end()

def init():
    global root_state_id

    State("100", "Привет! Давайте сыграем в игру чётное/нечётное", 
    [
        Transition("900", ["нет", "не хочу", "не давайте", "не надо", "не буду"])
    ]
    , "101").register()
    
    num = random.randint(1, 101)

    if num % 2 == 0:
        transId = "200"
    else: 
        transId = "300"

    State("101", "Отлично! Я задумала число, какое оно? ", [], transId).register()

    State("200", "", 
    [
        Transition("400", ["чётное", "делится на два", "делится на 2"])
    ]
    , "500").register()
    
    State("300", "", 
    [
        Transition("400", ["не чётное", "нечётное", "не делится на 2", "не делится на два"])
    ]
    , "500").register()

    State("400", f"Вы правы! Моим числом было {num} \nХотите продолжить?", [Transition("101", ["да", "хочу"])], "900").register()
    State("500", f"Вы не угадали! Моим числом было {num} \nХотите продолжить?", [Transition("101", ["да", "хочу"])], "900").register()

    State("900", "Хорошо поиграли!", [], None, True).register()

    root_state_id = "100"

init()
