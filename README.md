# TaskManagementSystem

For using this web application you need at least:
 - sign up
 - log in in your account
 - create a repository
After this you can do what you want essentially:
 - from the menu where you see the button for creating a repository there are two options:
   . you can see your assigned task from every repository ( you can only modify or see status either if you have permissions for manage tasks of a certain repo).
   . you can see the list of repositories you are signed in.
 - you can manage with your repository in few ways:
   . you can create, delete and modify tasks if you have the permission to manage tasks.
   . you can remove or add people if you have the permission to manage users (That's don't have the confirmation from the other user. Maybe in a next implementation).
   . you can remove, assign or create a role if you have the permission to manage roles. At the start of the repo; there are two roles: superadmin and user. 
     Superadmin have all the permissions in the repo (also deleting her), instead user have only the permission to change status to tasks which he's assigned.
     The user who created the repo is assigned superadmin by default.
 - for track the status I create a history for all tasks which is a pseudo tracking where everytime you changed status is recorded in history.

That's all. Have fun.
