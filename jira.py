from transitions import Machine, MachineError


class JiraTask:
    pass

task = JiraTask()

# init jira task states and transitions

# Все возможные состояния
states = ['open', 'closed', 'resolved', 'inprogress', 'reopened']

# Описание переходов
# trigger - действие, которое может привести к смене состояния объекта
# source - исходное состояние объекта
# dest - целевое состояние объекта
transitions = [
    {'trigger': 'start_progress', 'source': 'open', 'dest': 'inprogress'},
    {'trigger': 'resolve_and_close', 'source': 'open', 'dest': 'closed'},
    {'trigger': 'stop_progress', 'source': 'inprogress', 'dest': 'open'},
    {'trigger': 'resolve', 'source': 'inprogress', 'dest': 'resolved'},
    {'trigger': 'resolve_and_close', 'source': 'open', 'dest': 'closed'},
    {'trigger': 'close', 'source': 'resolved', 'dest': 'closed'},
    {'trigger': 'reopen', 'source': 'closed', 'dest': 'reopened'},
    {'trigger': 'resolve', 'source': 'reopened', 'dest': 'resolved'},
    {'trigger': 'resolve_and_close', 'source': 'reopened', 'dest': 'closed'},
    {'trigger': 'start_progress', 'source': 'reopened', 'dest': 'inprogress'}
]

# Initialize fsm and bind it
machine = Machine(task, states=states, transitions=transitions, initial='open')

# Тестирование
if __name__ == '__main__':
    # Позитивный сценарий
    try:
        task.start_progress()
        print(task.state)

        task.resolve()
        print(task.state)

        task.close()
        print(task.state)

    except MachineError as error:
        print(error)

    # Негативный сценарий
    try:
        task.start_progress()
        print(task.state)

        task.close() # exception - there is no such transition in model
        print(task.state)

        task.resolve()
        print(task.state)

        task.close()
        print(task.state)

    except MachineError as error:
        print(error)