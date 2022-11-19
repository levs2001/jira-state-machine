from transitions.extensions import GraphMachine

from jira_with_users import JiraTask, states, transitions

if __name__ == '__main__':
    task = JiraTask('np')  # Никола Программистиков
    machine = GraphMachine(task, states=states, transitions=transitions, initial='open')
    machine.get_graph().draw('/Users/lev.saskov/Documents/Study/AutomatesPres/jira_task_state_diagram.png', prog='dot')
