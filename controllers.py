from views import render_template

from models import User, Phone


def default_controller(data=None, cls=True):
    """Default controller"""
    render_template(context={}, template="default.jinja2", cls=cls)
    return (input(), None)


def exit_controller(data=None, cls=True):
    render_template(context={}, template="exit.jinja2", cls=cls)
    exit()


def all_users_controller(data=None, cls=True):
    users = User.all()
    render_template(context={'users': users}, template="all_users.jinja2",
                    cls=cls)
    input("Do u want to continue? ")
    return 'main', None  # (next state, data)


def add_user_controller(data=None, cls=True):
    render_template(context={}, template="add_user.jinja2", cls=cls)
    username = input()
    user = User.add(username)
    return 21, user  # (next state, data)


def add_phone_controller(user, cls=True):
    render_template(context={}, template="add_phone.jinja2", cls=cls)
    phone_number = input()
    phone = Phone.add(phone_number, user)
    return 212, user  # (next state, data)


def add_more_controller(user, cls=True):
    render_template(context={}, template="add_more.jinja2", cls=cls)
    answer = input()
    if answer == 'Y':
        return 21, user
    return 51, user  # (next state, data)


def update_user_controller(data=None, cls=True):
    users = User.all()
    choice = input('Enter n, if u want to change the name, enter p, if u want \
to change the phone number: ')
    if choice == 'n':
        render_template(context={'users': users},
                        template="update_name.jinja2",
                        cls=cls)
        old_name = input()
        new_name = input("Ur new name: ")
        user = User.update(old_name, new_name)
        return '51', user
    if choice == 'p':
        render_template(context={'users': users},
                        template="user_delete.jinja2",
                        cls=cls)
        username_upd = input("Enter user's name, that phone's u want to  \
update: ")
        phones = Phone.all()
        for i in range(len(users)):
            if users[i].name == username_upd:
                numberline = ''
                for y in users[i].phones:
                    numberline += y.phone + ' '
                print(f'All numbers belonging to this user: \
{users[i].name}: {numberline}')
        old_phone = input("Enter the number, that u want to change: ")
        new_phone = input("Enter ur new number: ")
        phone = Phone.update(old_phone, new_phone)
        return '51', phone


def delete_user_controller(data=None, cls=True):
    users = User.all()
    render_template(context={'users': users}, template="user_delete.jinja2",
                    cls=cls)
    username = input("Enter user's name, that u want to delete: ")
    user = User.delete(username)
    return '51', user


def get_controller(state):
    return controllers_dict.get(state, default_controller)


controllers_dict = {  # use dict type instead of if else chain
    '0': exit_controller,
    '1': all_users_controller,
    '2': add_user_controller,
    '3': update_user_controller,
    '4': delete_user_controller,
    21: add_phone_controller,  # user can't enter 21 of int type
    212: add_more_controller
}
