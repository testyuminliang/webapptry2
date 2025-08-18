# seed.py
from faker import Faker
from app import create_app, db
from app.models import User

# 创建一个Faker实例
fake = Faker()

# 创建app实例并进入应用上下文
app = create_app()
with app.app_context():
    # 清空旧数据（可选，每次运行脚本时都会重置数据库）
    print("Deleting old users...")
    db.session.query(User).delete()

    print("Creating 100 new fake users...")
    # 创建100个虚拟用户
    for _ in range(100):
        new_user = User(
            username=fake.user_name(),
            email=fake.unique.email() # unique确保email不重复
        )
        db.session.add(new_user)

    # 一次性提交所有新用户到数据库
    db.session.commit()
    print("Database has been seeded with 100 users!")