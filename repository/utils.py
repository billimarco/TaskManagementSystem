def get_user_permissions(user_roles):
    user_permissions = set()
    
    for role in user_roles:
        if role.role.can_change_status_if_task_assigned and 'can_change_status_if_task_assigned' not in user_permissions:
            user_permissions.add('can_change_status_if_task_assigned')
        if role.role.can_manage_tasks and 'can_manage_tasks' not in user_permissions:
            user_permissions.add('can_manage_tasks')
        if role.role.can_manage_users and 'can_manage_users' not in user_permissions:
            user_permissions.add('can_manage_users')
        if role.role.can_manage_roles and 'can_manage_roles' not in user_permissions:
            user_permissions.add('can_manage_roles')
        if role.role.can_cancel_repo and 'can_cancel_repo' not in user_permissions:
            user_permissions.add('can_cancel_repo')
    
    return user_permissions