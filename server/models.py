from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    @validates('name')
    def validate_name(self, key, name):
        # names = Author.query(Author.name).all() # => TypeError: 'Query' object is not callable
        
        # names = Author.query.with_entities(Author.name).all()
        # names = [author.name for author in Author.query.all()]
        names = db.session.query(Author.name).all()
        if not name:
            raise ValueError('Must have a name.')
        elif name in names:
            raise ValueError("Name must be unique.")
        return name

    phone_number = db.Column()
    @validates('phone_number')
    def validate_phone_number(self, key, number):
        if len(number) != 10:
            raise ValueError('Failed phone number, must be 10 digits.')
        return number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text)
    category = db.Column(db.String)
    summary = db.Column(db.String)

    # @validates('title')
    # def validate_title(self, key, title):
    #     if not title:
    #         raise ValueError('Must have a title.')

    #     clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
    #     check = []     
    #     for bail in clickbait:
    #         if bail in title:
    #             check.append(True)
    #         check.append(False)
    #     if True not in check:   
    #         raise ValueError("No clickbait found")
            
    #     return title
    
    @validates('title')
    def validate_title(self, key, title):
        clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(substring in title for substring in clickbait):
            raise ValueError("No clickbait found")
        return title

    @validates("content", "summary")
    def validate_content_summary(self, key, string):
        if key == "content":
            if not len(string) >= 250:
                raise ValueError("Content must be at least 250 characters long")
        elif key == "summary":
            if not len(string) <= 250:
                raise ValueError("Summary must be a maximum of 250 characters")
        return string

    @validates("category")
    def validate_category(self, key, category):
        if category != "Fiction" and category != "Non-Fiction":
            raise ValueError("Summary must be Fiction or Non-Fiction.")
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title}, content={self.content}, summary={self.summary})'

# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import validates
# db = SQLAlchemy()

# class Author(db.Model):
#     __tablename__ = 'authors'

#     id = db.Column(db.Integer, primary_key=True)
#     name= db.Column(db.String, unique=True, nullable=False)
#     phone_number = db.Column(db.String)
#     # created_at = db.Column(db.DateTime, server_default=db.func.now())
#     # updated_at = db.Column(db.DateTime, onupdate=db.func.now())

#     def __repr__(self):
#         return f'Author(id={self.id}, name={self.name})'

#     @validates('name')
#     def validate_name(self, key, name):
#         names = db.session.query(Author.name).all()
#         if not name:
#             raise ValueError("Name field is required.")
#         elif name in names:
#             raise ValueError("Name must be unique.")
#         return name

#     @validates('phone_number')
#     def validate_phone_number(self, key, phone_number):
#         if len(phone_number) != 10:
#             raise ValueError("Phone number must be 10 digits.")
#         return phone_number

# class Post(db.Model):
#     __tablename__ = 'posts'

#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String, nullable=False)
#     content = db.Column(db.Text)
#     category = db.Column(db.String)
#     summary = db.Column(db.String)
#     # created_at = db.Column(db.DateTime, server_default=db.func.now())
#     # updated_at = db.Column(db.DateTime, onupdate=db.func.now())

#     @validates('title')
#     def validate_title(self, key, title):
#         raise ValueError("No clickbait found")
#         clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
#         if not any(substring in title for substring in clickbait):
#             raise ValueError("No clickbait found")
#         return title

#     @validates('content', 'summary')
#     def validate_length(self, key, string):
#         if( key == 'content'):
#             if len(string) <= 250:
#                 raise ValueError("Post content must be greater than or equal 250 characters long.")
#         if( key == 'summary'):
#             if len(string) >= 250:
#                 raise ValueError("Post summary must be less than or equal to 250 characters long.")
#         return string

#     @validates('category')
#     def validate_category(self, key, category):
#         if category != 'Fiction' and category != 'Non-Fiction':
#             raise ValueError("Category must be Fiction or Non-Fiction.")
#         return category

#     def __repr__(self):
#         return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'