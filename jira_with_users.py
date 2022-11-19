from enum import Enum

from transitions import MachineError, Machine


class UserRoles(Enum):
    tester = 1
    developer = 2


class UserStorage():
    def __init__(self):
        self._users = [
            {'id': 'vt', 'name': 'Вася Тестировщиков', 'role': UserRoles.tester},
            {'id': 'np', 'name': 'Никола Программистиков', 'role': UserRoles.developer}
        ]

    def get_user_by_id(self, id):
        return next((item for item in self._users if item['id'] == id), None)

    def is_tester(self, id):
        user = self.get_user_by_id(id)
        if user:
            return user['role'] == UserRoles.tester
        return False

    def is_developer(self, id):
        user = self.get_user_by_id(id)
        if user:
            return user['role'] == UserRoles.developer
        return False


class JiraTask:
    def __init__(self, user_id):
        self._user_id = user_id

    def is_tester(self):
        return UserStorage().is_tester(self._user_id)

    def is_developer(self):
        return UserStorage().is_developer(self._user_id)


# Состояния остались теми же
states = ['open', 'closed', 'resolved', 'inprogress', 'reopened']

# Теперь задачи могут закрывать только тестировщики
transitions = [
    {'trigger': 'start_progress', 'source': 'open', 'dest': 'inprogress'},
    {'trigger': 'resolve_and_close', 'source': 'open', 'dest': 'closed', 'conditions': ['is_tester']},
    {'trigger': 'stop_progress', 'source': 'inprogress', 'dest': 'open'},
    {'trigger': 'resolve', 'source': 'inprogress', 'dest': 'resolved'},
    {'trigger': 'resolve_and_close', 'source': 'open', 'dest': 'closed', 'conditions': ['is_tester']},
    {'trigger': 'close', 'source': 'resolved', 'dest': 'closed', 'conditions': ['is_tester']},
    {'trigger': 'reopen', 'source': 'closed', 'dest': 'reopened'},
    {'trigger': 'resolve', 'source': 'reopened', 'dest': 'resolved'},
    {'trigger': 'resolve_and_close', 'source': 'reopened', 'dest': 'closed', 'conditions': ['is_tester']},
    {'trigger': 'start_progress', 'source': 'reopened', 'dest': 'inprogress'}
]

if __name__ == '__main__':
    task = JiraTask('np')
    machine = Machine(task, states=states, transitions=transitions, initial='open')
    try:
        if not task.start_progress():
            print('conditions fail')
        else:
            print(task.state)

        if not task.resolve():
            print('conditions fail')
        else:
            print(task.state)

        if not task.close():
            print('conditions fail')
        else:
            print(task.state)

    except MachineError as error:
        print(error)



