
def user_is_judge(user):
    return user.roles.filter(name="Judge").exists()

def user_is_superior_judge(user):
    return user.roles.filter(name="Superior Judge").exists()

def user_is_tabulator(user):
    return user.roles.filter(name="Tabulator").exists()

def user_is_kct(user):
    return user.roles.filter(name="KCT").exists()
