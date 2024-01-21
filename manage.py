from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db  # your_app은 Flask 애플리케이션 객체입니다.

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()