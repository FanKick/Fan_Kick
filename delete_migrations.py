import os

apps_path = 'apps'

for app in os.listdir(apps_path):
    app_migrations_path = os.path.join(apps_path, app, 'migrations')

    if not os.path.exists(app_migrations_path):
        print(f"No migrations directory found for {app}")
    else:
        for filename in os.listdir(app_migrations_path):
            if '_initial.py' in filename or 'alter' in filename:
                file_path = os.path.join(app_migrations_path, filename)
                os.remove(file_path)
                print(f"Deleted: {file_path}")
