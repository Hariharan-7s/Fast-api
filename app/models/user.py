from sqlmodel import Field, SQLModel


# Define SQLModel for testing
class User(SQLModel):
    first_name: str
    last_name: str
    email: str
