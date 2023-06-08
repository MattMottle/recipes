from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash
class Recipe:
    db= "recipes"
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.cooked_at = data["cooked_at"]
        self.under_30 = data["under_30"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.creator = None

    @classmethod
    def get_all_recipes_with_users(cls):
        query = """
            SELECT * FROM recipes 
            LEFT JOIN users ON users.id = recipes.user_id;
            """
        results = connectToMySQL(cls.db).query_db(query)
        all_recipes =[]
        for row in results:
            all_recipes.append(row)
        return all_recipes
    
    @classmethod
    def create_recipe(cls,data):
        query = """
        INSERT INTO recipes (name, description, instructions, cooked_at, under_30, user_id) 
        VALUES (%(name)s, %(description)s, %(instructions)s, %(cooked_at)s, %(under_30)s, %(user_id)s);
        """
        print(query)
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_one_recipe(cls, id):
        query ="SELECT * FROM recipes WHERE id = %(id)s;"
        data = id
        print(data)
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_one_with_user(cls, data):
        query = """
            SELECT * FROM recipes 
            LEFT JOIN users ON users.id = recipes.user_id 
            WHERE recipes.id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        row = results[0]
        one_recipe = cls(results[0])
        user_data = {
            "id": row["id"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "email": row["email"],
            "password": row["password"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"]
        }
        one_recipe.creator = user.User(user_data)
        return one_recipe

    @classmethod
    def update(cls,data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, cooked_at=%(cooked_at)s, under_30=%(under_30)s, user_id=%(user_id)s WHERE recipes.id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def is_valid(recipe):
        is_valid = True
        if len(recipe["name"]) < 3:
            flash("Recipe name must be at least 3 characters")
            is_valid = False
        if len(recipe["description"]) < 3:
            flash("Recipe description must be at least 3 characters")
            is_valid = False
        if len(recipe["instructions"]) < 3:
            flash("Recipe instructions must be at least 3 characters")
            is_valid = False
        if len(recipe["cooked"]) < 3:
            flash("Date must not be blank")
            is_valid = False
        return is_valid

