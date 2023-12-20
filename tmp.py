from flask import Flask, request, jsonify
import pymysql
from pymysql.cursors import DictCursor
import arrow
from hashlib import md5

app = Flask(__name__)

# Your database connection information
db_config = {
    'host': 'localhost',
    'port':3306,
    'user': 'root',  # Replace with your username
    'password': '123456',  # Replace with your password
    'database': 'dazuoye',  # Replace with your database name
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
    account = data.get('account')
    id_number = data.get('id_number')
    name = data.get('name')
    phone = data.get('phone')  # Correcting the parameter name
    identity = data.get('identity')  # Correcting the parameter name

    # Connect to MySQL database
    connection = pymysql.connect(**db_config)

    print(account, id_number, name, phone, identity)

    try:
        with connection.cursor() as cursor:
            # Check if the passenger already exists
            cursor.execute("SELECT * FROM passenger WHERE id_number = %s", (id_number,))
            existing_passenger = cursor.fetchone()

            if existing_passenger:
                print("Passenger already exists")
                return jsonify({'message': 'Passenger already exists'})

            # Insert new passenger information into the 'passenger' table
            cursor.execute("INSERT INTO passenger (name, id_number, phone, identity) VALUES (%s, %s, %s, %s)",
                           (name, id_number, phone, identity))
            # Insert new passenger information into the 'person_info' table
            cursor.execute("INSERT INTO person_info (account, id_number) VALUES (%s, %s)",
                           (account, id_number))
            # Commit the transaction
            connection.commit()

            print("Passenger added successfully")

        return jsonify({'message': 'Passenger added successfully'})
    except Exception as e:
        print("fail")
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
            all_accounts = [account['account'] for account in user_accounts] + [admin['account'] for admin in
                                                                                admin_accounts]

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

            print(user_info)

            # if user_info:
            #     # If the user is not an administrator, set 'name' and 'phone' to empty strings
            #     if not is_admin:
            #         user_info['name'] = ''
            #         user_info['phone'] = ''

        return jsonify(user_info)
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        connection.close()


# Define price coefficients for each train type
TRAIN_TYPE_COEFFICIENTS = {
    '普慢': 1.0,
    '普快': 1.2,
    '空调普快': 1.5,
    '城际列车': 1.8,
    '城际高速': 2.0,
}


# Route for querying train information
@app.route('/Train/query', methods=['GET'])
def query_train_info():
    try:
        # Get parameters from the request
        start_station = request.args.get('start_station')
        arrive_station = request.args.get('arrive_station')
        go_date = request.args.get('go_date')

        # Connect to MySQL database
        connection = pymysql.connect(**db_config)
        print(start_station, arrive_station, go_date)

        try:
            with connection.cursor() as cursor:
                # First query: Find train information for the start station
                start_station_query = """
                    SELECT train_number, arrival_time, stop_order
                    FROM arrival_time
                    WHERE station_name = %s
                """
                cursor.execute(start_station_query, (start_station,))
                start_station_info = cursor.fetchall()

                # Second query: Find train information for the arrival station
                arrive_station_query = """
                    SELECT train_number, arrival_time, stop_order
                    FROM arrival_time
                    WHERE station_name = %s
                """
                cursor.execute(arrive_station_query, (arrive_station,))
                arrive_station_info = cursor.fetchall()

                # Filter the trains with the correct stop_order for arrival station
                valid_trains = [
                    {
                        'train_number': start_info['train_number'],
                        'start_station': start_station,
                        'arrive_station': arrive_station,
                        'go_time': format_time(start_info['arrival_time']),
                        'arrive_time': format_time(arrive_info['arrival_time']),
                        'price': 50,  # You need to calculate the price based on your logic
                        'go_date': str(go_date),
                        'remain': get_remaining_seats(connection, start_info['train_number'], go_date)
                    }
                    for start_info in start_station_info
                    for arrive_info in arrive_station_info
                    if start_info['train_number'] == arrive_info['train_number']
                       and start_info['stop_order'] < arrive_info['stop_order']
                ]

                # Query the train table to get train_type
                train_type_query = """ 
                    SELECT train_number, train_type
                    FROM train
                    WHERE train_number IN (%s)
                """
                train_numbers = [train['train_number'] for train in valid_trains]
                in_clause = ', '.join(['%s'] * len(train_numbers))
                train_type_query = train_type_query % in_clause
                cursor.execute(train_type_query, tuple(train_numbers))
                train_types = cursor.fetchall()

                # Map train types to the valid trains
                train_type_dict = {train['train_number']: train['train_type'] for train in train_types}
                for train in valid_trains:
                    train_type = train_type_dict.get(train['train_number'], 'Unknown')
                    # Calculate running time in minutes
                    # pdb.set_trace()
                    running_time_minutes = (arrow.get(train['arrive_time'], 'HH:mm:ss') - arrow.get(train['go_time'],
                                                                                                    'HH:mm:ss')
                                            ).seconds // 60

                    # Determine base price based on running time
                    base_price = calculate_base_price(running_time_minutes)

                    # Get train type and apply price coefficient
                    price_coefficient = TRAIN_TYPE_COEFFICIENTS.get(train_type, 1.0)

                    # Calculate final ticket price
                    ticket_price = base_price * price_coefficient

                    # Update the train dictionary with the calculated price
                    train['price'] = round(ticket_price, 2)

                return jsonify(valid_trains)

        except Exception as e:
            print("failed")
            return jsonify({'error': str(e)})
        finally:
            connection.close()

    except Exception as e:
        return jsonify({'error': str(e)})


def calculate_base_price(running_time_minutes):
    # based on the running time. This is just a placeholder
    return max(50, running_time_minutes * 0.1)  # Adjust as needed


def get_remaining_seats(connection, train_number, go_date):
    with connection.cursor() as cursor:
        remaining_seats_query = """
            SELECT remaining_seats
            FROM seats
            WHERE train_number = %s AND date = %s
        """
        cursor.execute(remaining_seats_query, (train_number, go_date))
        result = cursor.fetchone()
        return result['remaining_seats'] if result else 0


def format_time(raw_time):
    # Assuming raw_time is a timedelta object
    hours, remainder = divmod(raw_time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    formatted_time = "{:02}:{:02}:{:02}".format(hours, minutes, seconds)
    return formatted_time


# Route for modifying user/administrator information
@app.route('/User/modify', methods=['POST'])
def modify_user_info():
    # print("Request Parameters:", request.form.to_dict())
    is_admin = request.form.get('id_ad') == 'true'
    account = request.form.get('id')
    username = request.form.get('username')
    name = request.form.get('name') if not is_admin else None
    password = request.form.get('password')
    phone = request.form.get('phone') if not is_admin else None

    # Connect to MySQL database
    connection = pymysql.connect(**db_config)

    print(account, username, password)

    try:
        with connection.cursor() as cursor:
            if is_admin:
                # Update administrator information in 'administrator' table
                cursor.execute("UPDATE administrator SET username = %s, password = %s, phone = %s WHERE account = %s",
                               (username, password, phone, account))
                # print("SQL Query:", cursor.mogrify("UPDATE administrator SET username = %s, password = %s, phone = %s WHERE account = %s",
                #                (username, password, phone, account)))
            else:
                # Update user information in 'user' table
                cursor.execute("UPDATE user SET username = %s, password = %s WHERE account = %s",
                               (username, password, account))
                # print("SQL Query:", cursor.mogrify("UPDATE user SET username = %s, password = %s WHERE account = %s",
                #                (username, password, account)))

            connection.commit()
            print("updated successfully")

        return jsonify({'message': 'User/Administrator information updated successfully'})
    except Exception as e:
        print("failed")
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
            cursor.execute("SELECT DISTINCT station_name FROM arrival_time")
            station_names = [result['station_name'] for result in cursor.fetchall()]

        return jsonify(station_names)
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        connection.close()


# Route for modifying passenger information for a specific user
@app.route('/Passenger/modify', methods=['POST'])
def modify_passenger_info():
    # Get JSON data from the request
    data = request.json

    # Extract parameters from JSON data
    name = data.get('name')
    phone = data.get('phone')
    identity = data.get('identity')
    id_number = data.get('id_number')

    # Connect to MySQL database
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:
            # Update the personal information table
            cursor.execute(
                "UPDATE passenger SET name = %s, phone = %s, identity = %s WHERE id_number = %s",
                (name, phone, identity, id_number))

            # print("SQL Query:", cursor.mogrify(
            #     "UPDATE passenger SET name = %s, phone = %s, identity = %s WHERE id_number = %s",
            #     (name, phone, identity, id_number)))

            print("updated successfully")

        # Commit the changes to the database
        connection.commit()

        return jsonify({'message': 'Passenger information updated successfully'})
    except Exception as e:
        print("failed")
        return jsonify({'error': str(e)})
    finally:
        connection.close()


# Route for deleting passenger information for a specific user
@app.route('/Passenger/delete', methods=['POST'])
def delete_passenger_info():
    try:
        # Get JSON data from the request
        data = request.json

        # Extract parameters from JSON data
        account = data.get('account')
        id_number = data.get('id_number')

        # Connect to MySQL database
        connection = pymysql.connect(**db_config)

        try:
            with connection.cursor() as cursor:
                # Delete from the personal information table
                cursor.execute("DELETE FROM person_info WHERE account = %s AND id_number = %s", (account, id_number))

            # Commit the changes to the database
            connection.commit()

            return jsonify({'message': 'Passenger information deleted successfully'})
        except Exception as e:
            return jsonify({'error': str(e)})
        finally:
            connection.close()
    except Exception as e:
        return jsonify({'error': str(e)})


def generate_order_number(account, pay_amount, date):
    return md5(f'{account}'.encode(encoding='utf-8')).hexdigest()[:5] + md5(
        f'{pay_amount}'.encode(encoding='utf-8')).hexdigest()[:5] + \
           md5(f'{date}'.encode(encoding='utf-8')).hexdigest()[:5]


def generate_ticket_number(train_number, id_number, order_number, date):
    return md5(f'{train_number}'.encode(encoding='utf-8')).hexdigest()[:5] + md5(
        f'{id_number}'.encode(encoding='utf-8')).hexdigest()[:5] + md5(
        f'{order_number}'.encode(encoding='utf-8')).hexdigest()[:5] + md5(
        f'{date}'.encode(encoding='utf-8')).hexdigest()[:5]


# Route for purchasing tickets based on selected train
@app.route('/Ticket/choose', methods=['POST'])
def purchase_tickets():
    try:
        # Get JSON data from the request
        data = request.json
        # Extract parameters from JSON data
        account = data.get('account')
        date = data.get('date')
        train_number = data.get('train_number')
        start_station = data.get("start_station")
        arrive_station = data.get("arrive_station")
        start_time = data.get("start_time")
        arrive_time = data.get("arrive_time")
        payment_options = data.get('paymentOptions')
        count = data.get('count')
        id_list = data.get('id_list')
        for dic in payment_options:
            if dic['checked']:
                pay_method = dic['name']
                break
        identity_list = data.get('identity_list')

        # Connect to MySQL database
        connection = pymysql.connect(**db_config)

        try:
            with connection.cursor() as cursor:
                # Check if there are enough remaining seats
                cursor.execute("SELECT remaining_seats FROM seats WHERE train_number = %s AND date = %s",
                               (train_number, date))
                remaining_seats = cursor.fetchall()
                remaining_seats = remaining_seats[0]['remaining_seats']
                if remaining_seats >= count:
                    # Calculate ticket price based on identity
                    # For simplicity, assuming the price is fixed
                    price = 100  # You can adjust this based on your pricing logic
                    order_price = price * len(identity_list) - 0.25 * (sum(identity_list))
                    # Insert into unpaid orders table
                    order_number = generate_order_number(account, order_price, date)
                    cursor.execute(
                        "INSERT INTO `order` (order_number, user_account, purchase_time, payment_amount, payment_method, status) VALUES (%s, %s, %s, %s, %s, %s)",
                        (order_number, account, date, order_price, pay_method, 'unpaid'))
                    # Insert into ticket table
                    for i in range(count):
                        ticket_number = generate_ticket_number(train_number, id_list[i], order_number, date)
                        cursor.execute(
                            "INSERT INTO ticket (ticket_number, train_number,departure_station,destination_station,departure_time,arrival_time, date, id_number, order_number, fare) VALUES (%s, %s,%s,%s,%s,%s, %s, %s, %s, %s)",
                            (ticket_number, train_number, start_station,arrive_station,start_time,arrive_time,date, id_list[i], order_number,
                             price * (0.75 if identity_list[i] == 1 else 1)))

                    # Commit the changes to the database
                    connection.commit()
                    return jsonify({'success': True, 'order_number': order_number})
                else:
                    return jsonify({'success': False, 'message': 'Not enough remaining seats'})
        except Exception as e:
            return jsonify({'error': str(e)})
        finally:
            connection.close()
    except Exception as e:
        return jsonify({'error': str(e)})


# Route for handling payment completion
@app.route('/Order/completed', methods=['POST'])
def complete_payment():
    try:
        # Get JSON data from the request
        data = request.json

        # Extract parameters from JSON data
        order_number = data.get('order_number')

        # Connect to MySQL database
        connection = pymysql.connect(**db_config)

        try:
            with connection.cursor() as cursor:
                # Update order status to 'completed'
                cursor.execute("UPDATE `order` SET status = 'completed' WHERE order_number = %s", (order_number,))

                # Commit the changes to the database
                connection.commit()

                return jsonify({'success': True, 'message': 'Payment completed successfully'})
        except Exception as e:
            return jsonify({'error': str(e)})
        finally:
            connection.close()
    except Exception as e:
        return jsonify({'error': str(e)})


# Route for handling refund
@app.route('/Order/refund', methods=['POST'])
def refund_order():
    try:
        # Get JSON data from the request
        data = request.json

        # Extract parameters from JSON data
        order_number = data.get('order_number')

        # Connect to MySQL database
        connection = pymysql.connect(**db_config)

        try:
            with connection.cursor() as cursor:
                # Update order status to 'refund'
                cursor.execute("UPDATE `order` SET status = 'refund' WHERE order_number = %s", (order_number,))

                # Commit the changes to the database
                connection.commit()

                return jsonify({'success': True, 'message': 'Refund completed successfully'})
        except Exception as e:
            return jsonify({'error': str(e)})
        finally:
            connection.close()
    except Exception as e:
        return jsonify({'error': str(e)})


# Route for finding tickets by order number
@app.route('/Ticket/findbyId', methods=['POST'])
def find_tickets_by_order():
    try:
        # Get JSON data from the request
        data = request.json

        # Extract parameters from JSON data
        order_number = data.get('order_number')

        # Connect to MySQL database
        connection = pymysql.connect(**db_config)

        try:
            with connection.cursor() as cursor:
                # Query tickets based on order number
                cursor.execute("SELECT * FROM ticket WHERE order_number = %s", (order_number,))
                tickets = cursor.fetchall()

                # Convert the result to a list of dictionaries
                result = [
                    {'ticket_number': ticket['ticket_number'], 'train_number': ticket['train_number'],
                     'date': str(ticket['date']), 'id_number': ticket['id_number'],
                     'order_number': ticket['order_number'], 'fare': ticket['fare'],
                     'arrival_time': str(ticket['arrival_time']), 'departure_time': str(ticket['departure_time']),
                     'departure_station': ticket['departure_station'],
                     'destination_station': ticket['destination_station']} for
                    ticket in tickets]

                return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)})
        finally:
            connection.close()
    except Exception as e:
        return jsonify({'error': str(e)})


# Route for finding all orders for a specific user
@app.route('/Order/findbyaccount', methods=['GET'])
def find_orders_by_account():
    try:
        # Get parameters from the request
        account = request.args.get('account')

        # Connect to MySQL database
        connection = pymysql.connect(**db_config)

        try:
            with connection.cursor() as cursor:
                # Query orders based on user account
                cursor.execute("SELECT * FROM `order` WHERE user_account = %s", (account,))
                orders = cursor.fetchall()

                # Convert the result to a list of dictionaries
                result = [{'order_number': order['order_number'], 'purchase_time': str(order['purchase_time']),
                           'payment_amount': order['payment_amount'],
                           'payment_method': order['payment_method'], 'status': order['status'],
                           'user_account': order['user_account']} for order in
                          orders]

                return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)})
        finally:
            connection.close()
    except Exception as e:
        return jsonify({'error': str(e)})


# Route for finding information about a specific train for an administrator
@app.route('/Train/findbyid', methods=['GET'])
def find_train_by_id():
    try:
        # Get parameters from the request
        train_number = request.args.get('train_number')

        # Connect to MySQL database
        connection = pymysql.connect(**db_config)

        try:
            with connection.cursor() as cursor:
                # Query train information based on train number
                cursor.execute(
                    "SELECT arrival_time.train_number, station_name, arrival_time, stop_order, seats_num, mileage, train_type FROM train "
                    "JOIN arrival_time ON train.train_number = arrival_time.train_number "
                    "WHERE train.train_number = %s ORDER BY stop_order", (train_number,))
                train_info = cursor.fetchall()

                # Convert the result to a list of dictionaries
                result = [{'train_number': info['train_number'],
                           'station_name': info['station_name'],
                           'arrival_time': str(info['arrival_time']),
                           'stop_order': info['stop_order'],
                           'seats_num': info['seats_num'],
                           'mileage': info['mileage'],
                           'train_type': info['train_type']} for info in train_info]

                return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)})
        finally:
            connection.close()
    except Exception as e:
        return jsonify({'error': str(e)})


# Route for finding users with a given account (admin operation)
@app.route('/Ad/finduser', methods=['GET'])
def find_users_by_account():
    try:
        # Get parameters from the request
        account = request.args.get('account')

        # Connect to MySQL database
        connection = pymysql.connect(**db_config)

        try:
            with connection.cursor() as cursor:
                # Fuzzy search for users based on account
                cursor.execute("SELECT * FROM user WHERE account LIKE %s", ('%' + account + '%',))
                users = cursor.fetchall()

                # Convert the result to a list of dictionaries
                result = [{'account': user['account'], 'username': user['username'], 'password': user['password'],
                           'noOfOrder': user['noOfOrder']} for
                          user in users]

                return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)})
        finally:
            connection.close()
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
