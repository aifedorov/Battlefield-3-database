import MySQLdb
from flask import Flask, render_template, request

app = Flask(__name__)
app.config.from_object('config')

def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

@app.route('/')
def get_weclome():
    return render_template('base.html')

@app.route('/users',methods= ['GET', 'POST'])
def get_list_users():
        if request.method == 'POST':
            if(request.form['id_max'] > request.form['id_min']):
                id_min = request.form['id_min']
                id_max = request.form['id_max']
            else:
                id_min = request.form['id_max']
                id_max = request.form['id_min']
            db = MySQLdb.connect(host="localhost", user="root", passwd="qwert", db="my_db", charset='utf8')
            cursor = db.cursor()
            if(request.form.get('order_by_name')):
                sql = """select users.id, users.username as username, users.email as email, ranks.name as rank, \
                weapons.name as weapon, vehicles.name as vehicle, classplayer.name as classplayer \
                from users \
                join \
                ranks on ranks.id = users.rank_id \
                join \
                weapons on weapons.id = users.weapon_id \
                join \
                vehicles on vehicles.id = users.vehicle_id \
                join \
                classplayer on classplayer.id = users.classplayer_id \
                where users.id >= %s and users.id <= %s order by username limit 1000; """ % (id_min, id_max)
            else:
                sql = """select users.id, users.username as username, users.email as email, ranks.name as rank, \
                weapons.name as weapon, vehicles.name as vehicle, classplayer.name as classplayer \
                from users \
                join \
                ranks on ranks.id = users.rank_id \
                join \
                weapons on weapons.id = users.weapon_id \
                join \
                vehicles on vehicles.id = users.vehicle_id \
                join \
                classplayer on classplayer.id = users.classplayer_id \
                where users.id >= %s and users.id <= %s;""" % (id_min, id_max)
            cursor.execute(sql)
            records = dictfetchall(cursor)
            return render_template('users.html',
                           request = True,
                           control = False,
                           users_list = records
                           )
        else:
            return render_template('users.html',
                               request = False,
                               control = True
                               )

@app.route('/vehicle',methods= ['GET', 'POST'])
def get_list_vehicle():
        if request.method == 'POST':
            class_vehicle = request.form.items('class_vehicle')
            db = MySQLdb.connect(host="localhost", user="root", passwd="qwert", db="my_db", charset='utf8')
            cursor = db.cursor()
            sql = """select id, name from vehicles where class = '%s'; """ %(class_vehicle[0][1])
            cursor.execute(sql)
            records = dictfetchall(cursor)
            return render_template('vehicles.html',
                           request = True,
                           control = False,
                           vehicles_list = records
                           )
        else:
            return render_template('vehicles.html',
                               request = False,
                               control = True
                               )

@app.route('/weapons',methods= ['GET', 'POST'])
def get_list_weapon():
        if request.method == 'POST':
            selects = request.form.items('auto_fire')
            db = MySQLdb.connect(host="localhost", user="root", passwd="qwert", db="my_db", charset='utf8')
            cursor = db.cursor()
            sql = """select weapons.name as weapon, classplayer.name as classplayer, weapons.auto_fire, \
            weapons.burst_fire, weapons.range_fire, weapons.single_shot_fire, weapons.rate_of_fire from weapons \
            join classplayer on classplayer.id = weapons.classplayer_id   where weapons.auto_fire = '%s' \
            and weapons.burst_fire = '%s'  and weapons.range_fire = '%s' and \
            weapons.single_shot_fire = '%s'; """ %(selects[2][1], selects[3][1], selects[1][1], selects[0][1])
            cursor.execute(sql)
            records = dictfetchall(cursor)
            return render_template('weapons.html',
                           request = True,
                           control = False,
                           weapons_list = records
                           )
        else:
            return render_template('weapons.html',
                               request = False,
                               control = True
                               )

@app.route('/ranks',methods= ['GET', 'POST'])
def get_list_ranks():
            db = MySQLdb.connect(host="localhost", user="root", passwd="qwert", db="my_db", charset='utf8')
            cursor = db.cursor()
            sql = """select * from ranks order by id; """
            cursor.execute(sql)
            records = dictfetchall(cursor)
            return render_template('ranks.html',
                           ranks_list = records
                           )

@app.route('/class-player',methods= ['GET', 'POST'])
def get_list_class_player():
            db = MySQLdb.connect(host="localhost", user="root", passwd="qwert", db="my_db", charset='utf8')
            cursor = db.cursor()
            sql = """select * from classplayer limit 15; """
            cursor.execute(sql)
            records = dictfetchall(cursor)
            return render_template('classpalers.html',
                           classplayer_list = records
                           )

@app.route('/awards',methods= ['GET', 'POST'])
def get_list_awards():
        if request.method == 'POST':
            award_type = request.form.items('award_type')
            db = MySQLdb.connect(host="localhost", user="root", passwd="qwert", db="my_db", charset='utf8')
            cursor = db.cursor()
            if(request.form.get('order_by_name')):
                sql = """select * from awards where type = '%s' order by name limit 300; """ % (award_type[0][1])
            else:
                sql = """select * from awards where type = '%s' limit 300; """ % (award_type[0][1])
            cursor.execute(sql)
            records = dictfetchall(cursor)
            return render_template('awards.html',
                           request = True,
                           control = False,
                           awards_list = records
                           )
        else:
            return render_template('awards.html',
                               request = False,
                               control = True
                               )
@app.route('/maps',methods= ['GET', 'POST'])
def get_list_map():
        if request.method == 'POST':
            db = MySQLdb.connect(host="localhost", user="root", passwd="qwert", db="my_db", charset='utf8')
            cursor = db.cursor()
            if(request.form.get('order_by_area')):
                sql = """select name, area from maps order by area limit 100; """
            else:
                sql = """select name, area from maps order by name limit 100; """
            cursor.execute(sql)
            records = dictfetchall(cursor)
            return render_template('maps.html',
                           request = True,
                           control = False,
                           maps_list = records
                           )
        else:
            return render_template('maps.html',
                               request = False,
                               control = True
                               )
@app.route('/objects',methods= ['GET', 'POST'])
def get_list_object():
        if request.method == 'POST':
            db = MySQLdb.connect(host="localhost", user="root", passwd="qwert", db="my_db", charset='utf8')
            cursor = db.cursor()
            if(request.form.get('order_by_name') and request.form.get('order_by_height')):
                sql = """select name, area, height from objects order by name, height limit 100; """
            elif(request.form.get('order_by_name')):
                sql = """select name, area, height from objects order by name limit 100; """
            elif(request.form.get('order_by_height')):
                sql = """select name, area, height from objects order by height limit 100; """
            else:
                sql = """select name, area, height from objects limit 100; """
            cursor.execute(sql)
            records = dictfetchall(cursor)
            return render_template('objects.html',
                           request = True,
                           control = False,
                           objects_list = records
                           )
        else:
            return render_template('objects.html',
                               request = False,
                               control = True
                               )

if __name__ == '__main__':
    app.run()
