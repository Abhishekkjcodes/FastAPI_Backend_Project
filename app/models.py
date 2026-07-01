from .database import Base
from sqlalchemy import TIMESTAMP, ForeignKey, Integer, String, text,CheckConstraint
from sqlalchemy.orm import Mapped, Relationship,mapped_column
class Post(Base):
    __tablename__="posts"

    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    title:Mapped[str]=mapped_column(String,nullable=False)
    content:Mapped[str]=mapped_column(nullable=False)
    published:Mapped[bool]=mapped_column(server_default=text('true'))
    created_at=mapped_column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    user_id:Mapped[int]=mapped_column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)

    user_info=Relationship("User")

class User(Base):
    __tablename__="users"

    id:Mapped[int]=mapped_column(primary_key=True)
    email:Mapped[str]=mapped_column(nullable=False,unique=True)
    password:Mapped[str]=mapped_column(nullable=False)

class Like(Base):
    __tablename__="likes"
    post_id:Mapped[int]=mapped_column(ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)
    user_id:Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    direction:Mapped[int]=mapped_column(CheckConstraint(sqltext="direction IN (-1,1)",name="chk_likes_direction"),nullable=False)


