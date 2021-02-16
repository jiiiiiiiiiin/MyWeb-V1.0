from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db
from scripts import script_user


manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)
manager.add_command('user', script_user.user_manager)

# python user_manage.py db init    # 只需要运行一次
# python user_manage.py db migrate # model改变的时候运行
# python user_manage.py db upgrade # 更行数据库


if __name__ == '__main__':
    manager.run()
