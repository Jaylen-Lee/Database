from flask import Flask, request, jsonify
import pymysql
from pymysql.cursors import DictCursor

app = Flask(__name__)

# Your database connection information
db_config = {
    'host': 'localhost',
    'user': 'sola',  # Replace with your username
    'password': 'kaimo1234',  # Replace with your password
    'database': 'train_system',  # Replace with your database name
    'charset': 'utf8mb4',
    'cursorclass': DictCursor
}

# Placeholder for user registration
@app.route('/User/register', methods=['POST'])
def user_register():
    data = request.json
    account = data.get('account')
    username = data.get('username')
    password = data.get('password')

    # Connect to MySQL database
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:
            # Insert new user information into the 'user' table
            cursor.execute("INSERT INTO `user` (account, username, password, noOfOrder) VALUES (%s, %s, %s, 0)",
                           (account, username, password))
            # Commit the transaction
            connection.commit()

        return jsonify({'message': 'User registered successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        connection.close()

# Placeholder for querying user's added passengers
@app.route('/Passenger/findbyuser', methods=['POST'])
def find_passengers_by_user():
    data = request.json
    account = data.get('account')

    # Connect to MySQL database
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:
            # Query the 'person_info' and 'passenger' tables to get user's added passengers
            cursor.execute("SELECT p.name, p.id_number, p.phone, p.identity FROM person_info pi "
                           "JOIN passenger p ON pi.id_number = p.id_number "
                           "WHERE pi.account = %s", (account,))
            passengers = cursor.fetchall()

        return jsonify(passengers)
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        connection.close()

# Placeholder for adding a new passenger
@app.route('/Passenger/add', methods=['POST'])
def add_passenger():
    data = request.json
    id_number = data.get('id_number')
    name = data.get('name')
    phone = data.get('telphone')  # Correcting the parameter name
    identity = data.get('indentity')  # Correcting the parameter name

    # Connect to MySQL database
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:
            # Insert new passenger information into the 'passenger' table
            cursor.execute("INSERT INTO passenger (name, id_number, phone, identity) VALUES (%s, %s, %s, %s)",
                           (name, id_number, phone, identity))
            # Insert new passenger information into the 'person_info' table
            cursor.execute("INSERT INTO person_info (account, id_number) VALUES (%s, %s)",
                           (account, id_number))
            # Commit the transaction
            connection.commit()

        return jsonify({'message': 'Passenger added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        connection.close()

# Placeholder for querying all user accounts
@app.route('/User/findall_account', methods=['GET'])
def find_all_accounts():
    # Connect to MySQL database
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:
            # Query all user accounts from 'user' table
            cursor.execute("SELECT account FROM user")
            user_accounts = cursor.fetchall()

            # Query all administrator accounts from 'administrator' table
            cursor.execute("SELECT account FROM administrator")
            admin_accounts = cursor.fetchall()

            # Combine user and administrator accounts
            all_accounts = [account['account'] for account in user_accounts] + [admin['account'] for admin in admin_accounts]

            # file_path = "output.txt"
            # with open(file_path, "w") as file:
            #     # Write each account on a new line
            #     for account in all_accounts:
            #         file.write(account + "\n")

        return jsonify(all_accounts)
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        connection.close()

# Placeholder for querying user/administrator information by account
@app.route('/User/findby_account', methods=['GET'])
def find_user_by_account():
    is_admin = request.args.get('is_ad') == 'true'
    account = request.args.get('account')

    # Connect to MySQL database
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:
            if is_admin:
                # Query administrator information by account from 'administrator' table
                cursor.execute("SELECT * FROM administrator WHERE account = %s", (account,))
            else:
                # Query user information by account from 'user' table
                cursor.execute("SELECT * FROM user WHERE account = %s", (account,))

            user_info = cursor.fetchone()

            if user_info:
                # If the user is not an administrator, set 'name' and 'phone' to empty strings
                if not is_admin:
                    user_info['name'] = ''
                    user_info['phone'] = ''

        return jsonify(user_info)
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        connection.close()

# Placeholder for querying train information
@app.route('/Train/query', methods=['GET'])
def query_train():
    start_station = request.args.get('start_station')
    arrive_station = request.args.get('arrive_station')
    go_date = request.args.get('go_date')
    ticket_type = request.args.get('type')  # Correcting the parameter name

    # Connect to MySQL database
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:
            # Query train information based on parameters
            cursor.execute("SELECT t.start_station, t.arrive_station, t.go_time, t.arrival_time, t.train_number, "
                           "t.type, t.price, t.go_date, s.remaining_seats "
                           "FROM train t "
                           "JOIN seats s ON t.train_number = s.train_number "
                           "WHERE t.start_station = %s AND t.arrive_station = %s AND t.go_date = %s "
                           "AND t.type = %s", (start_station, arrive_station, go_date, ticket_type))

            train_info = cursor.fetchall()

            # Adjust the price for student tickets
            for info in train_info:
                if info['type'] == '学生票':
                    info['price'] = info['price'] * 0.75

        return jsonify(train_info)
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        connection.close()

# Route for modifying user/administrator information
@app.route('/User/modify', methods=['POST'])
def modify_user_info():
    is_admin = request.form.get('is_ad') == 'true'
    account = request.form.get('account')
    username = request.form.get('username')
    name = request.form.get('name') if not is_admin else None
    password = request.form.get('password')
    phone = request.form.get('phone') if not is_admin else None

    # Connect to MySQL database
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:
            if is_admin:
                # Update administrator information in 'administrator' table
                cursor.execute("UPDATE administrator SET username = %s, password = %s, phone = %s WHERE account = %s",
                               (username, password, phone, account))
            else:
                # Update user information in 'user' table
                cursor.execute("UPDATE user SET username = %s, password = %s WHERE account = %s",
                               (username, password, account))

            connection.commit()

        return jsonify({'message': 'User/Administrator information updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        connection.close()

# Route for finding all station names
@app.route('/Station/findall', methods=['GET'])
def find_all_stations():
    # Connect to MySQL database
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:
            # Query all station names from the 'station' table
            cursor.execute("SELECT station_name FROM arrival_time")
            station_names = [result['station_name'] for result in cursor.fetchall()]

        return jsonify(station_names)
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
