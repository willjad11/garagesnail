from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime

class Post:

    def __init__(self, data):

        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.address = data['address']
        self.city = data['city']
        self.state = data['state']
        self.placeid = data['placeid']
        self.saledate = data['saledate']
        self.saletime = data['saletime']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_post_by_id(cls, data):
        query = "SELECT * FROM posts WHERE id = %(id)s;"
        result = connectToMySQL('garagesnail').query_db(query, data)
        if not result:
            return False
        return cls(result[0])

    @classmethod
    def get_all(cls):
        query = '''
                SELECT * FROM posts
                ORDER BY created_at DESC;
                '''
        results = connectToMySQL('garagesnail').query_db(query)
        posts = []
        if results:
            for post in results:
                posts.append(cls(post))
            return posts
        else:
            print("No results")

    @staticmethod
    def search(data):
        posts = []
        query = '''
                SELECT id, GROUP_CONCAT(city,', ', state) AS citystate FROM posts
                GROUP BY posts.id
                '''
        results = connectToMySQL('garagesnail').query_db(query)
        if results:
            for post in results:
                if post['citystate'] == data:
                    posts.append(Post.get_post_by_id({"id": post['id']}))
            return posts
        else:
            print("No results")
    
    @staticmethod
    def index_locations():
        locations = []
        query = '''
                SELECT GROUP_CONCAT(city,', ', state) AS citystate FROM posts
                GROUP BY posts.id
                '''
        results = connectToMySQL('garagesnail').query_db(query)
        if results:
            for post in results:
                if post['citystate'] not in locations:
                    locations.append(post['citystate'])
            return locations
        else:
            print("No results")

    @staticmethod
    def create_new(data):
        query = '''
                INSERT INTO posts ( title, description, address, city, state, placeid, user_id, saledate, saletime, created_at, updated_at ) 
                VALUES ( %(ptitle)s , %(pdesc)s , %(padd)s , %(pcity)s , %(pstate)s , %(plid)s , %(uid)s , %(pdate)s, %(ptime)s, NOW() , NOW() );
                '''
        return connectToMySQL('garagesnail').query_db(query, data)

    @staticmethod
    def get_author(data):
        query = '''
                SELECT *
                FROM users
                JOIN posts ON posts.user_id = users.id
                WHERE posts.id = %(pid)s
                '''
        result = connectToMySQL('garagesnail').query_db(query, data)
        print(result)
        if not result:
            return False
        return result[0]

    @staticmethod
    def edit(data):
        query = '''
                UPDATE posts SET title = %(ptitle)s, description = %(pdesc)s, address = %(padd)s, city = %(pcity)s, state = %(pstate)s, 
                placeid = %(plid)s, saledate = %(pdate)s, saletime = %(ptime)s, updated_at = NOW() WHERE id = %(pid)s;
                '''
        return connectToMySQL('garagesnail').query_db(query, data)
    
    @staticmethod
    def validate_post(form):
        valid = True
        form['pdate'].lower()
        form['ptime'].lower()
        if len(form['ptitle']) < 3 or len(form['ptitle']) > 45:
            flash("Your title must be between 3-45 characters in length.", 'post1')
            valid = False
        if len(form['pdesc']) < 3 or len(form['pdesc']) > 255:
            flash("Your description must be between 3-255 characters in length.", 'post2')
            valid = False
        if len(form['pdate']) != 10 or form['pdate'].islower() or not Post.datecheck(form['pdate']):
            flash("The date must be on or after today's date.", 'post3')
            valid = False
        if len(form['ptime']) != 5 or form['ptime'].islower():
            flash("You must enter a valid time.", 'post4')
            valid = False
        if len(form['plid']) < 25 or ", USA" not in form['padd'] or not Post.commacheck(form['padd']):
            flash("You must choose a valid address within the USA.", 'post5')
            valid = False
        return valid
    
    @staticmethod
    def commacheck(form):
        valid = True
        count = 0
        for char in form:
            if char == ",":
                count += 1
        if count != 3:
            valid = False
        return valid
    
    @staticmethod
    def delete(data):
        query = '''
                DELETE FROM posts WHERE posts.id = %(pid)s;
                '''
        return connectToMySQL('garagesnail').query_db(query, data)
    
    @staticmethod
    def extract_state(data):
        return data[-13:-11]
    
    @staticmethod
    def extract_city(data):
        newStr = ""
        for i in range(len(data) - 16, 0, -1):
            if data[i] == " " and data[i - 1] == ",":
                break
            newStr += data[i]
        return newStr[::-1]
    
    @staticmethod
    def datetimeconvert(date, time):
        newDatetime = datetime.strptime(date + " " + time, "%Y-%m-%d %H:%M")
        return 'This garage sale is scheduled to begin on <b>{0:%b}. {0:%d}</b> at <b>{0:%I:%M%p}</b>.'.format(newDatetime)
    
    @staticmethod
    def datecheck(date):
        now = datetime.now().date()
        if date < str(now):
            return False
        return True
