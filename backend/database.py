# 导入 SQLAlchemy 的工具，它帮我们把 Python 代码翻译成数据库语句
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. 告诉它：我要在当前文件夹建一个名叫 competitor.db 的 SQLite 数据库
# check_same_thread=False 是为了让 FastAPI 的并发请求都能连上它
DATABASE_URL = "sqlite:///./competitor.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 2. 创建一个“会话”工厂。想象成你每次去仓库拿东西，都要推个手推车（Session）
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. 创建一个基础类，所有的表都要继承它
Base = declarative_base()