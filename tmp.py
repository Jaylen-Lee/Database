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


# Placeholder for querying train information
@app.route('/Train/query', methods=['GET'])
def query_train():
    start_station = request.args.get('start_station')
    arrive_station = request.args.get('arrive_station')
    go_date = request.args.get('go_date')
    ticket_type = request.args.get('type')  # Correcting the parameter name

    # Connect to MySQL database
    connection = pymysql.connect(**db_config)
    print(start_station, arrive_station, go_date, ticket_type)

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
            print(train_info)

            # Adjust the price for student tickets
            for info in train_info:
                if info['type'] == '学生票':
                    info['price'] = info['price'] * 0.75

        return jsonify(train_info)
    except Exception as e:
        print("failed")
        return jsonify({'error': str(e)})
    finally:
        connection.close()


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
        payment_options = data.get('paymentOptions')
        count = data.get('count')
        id_list = data.get('id_list')
        pay_method = data.get('pay_method')
        identity_list = data.get('identity_list')

        # Connect to MySQL database
        connection = pymysql.connect(**db_config)

        try:
            with connection.cursor() as cursor:
                # Check if there are enough remaining seats
                cursor.execute("SELECT remaining_seats FROM seats WHERE train_number = %s AND date = %s",
                               (train_number, date))
                remaining_seats = cursor.fetchone()[0]

                if remaining_seats >= count:
                    # Calculate ticket price based on identity
                    # For simplicity, assuming the price is fixed
                    price = 100  # You can adjust this based on your pricing logic

                    # Insert into unpaid orders table
                    order_number = generate_order_number()
                    cursor.execute(
                        "INSERT INTO unpaid_order (order_number, account, date, train_number, count, payment_method, status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (order_number, account, date, train_number, count, pay_method, 'unpaid'))

                    # Insert into ticket table
                    for i in range(count):
                        ticket_number = generate_ticket_number()
                        cursor.execute(
                            "INSERT INTO ticket (ticket_number, train_number, date, id_number, order_number, fare) VALUES (%s, %s, %s, %s, %s, %s)",
                            (ticket_number, train_number, date, id_list[i], order_number,
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
                cursor.execute("UPDATE unpaid_order SET status = 'completed' WHERE order_number = %s", (order_number,))

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
                cursor.execute("UPDATE unpaid_order SET status = 'refund' WHERE order_number = %s", (order_number,))

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
                    {'ticket_number': ticket[0], 'train_number': ticket[1], 'date': ticket[2], 'id_number': ticket[3],
                     'order_number': ticket[4], 'fare': ticket[5]} for ticket in tickets]

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
                cursor.execute("SELECT * FROM unpaid_order WHERE account = %s", (account,))
                orders = cursor.fetchall()

                # Convert the result to a list of dictionaries
                result = [{'order_number': order[0], 'purchase_time': order[1], 'payment_amount': order[2],
                           'payment_method': order[3], 'status': order[4], 'user_account': order[5]} for order in
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
                    "SELECT train_number, station_name, arrival_time, stop_order, seats_num, mileage, train_type FROM train "
                    "JOIN arrival_time ON train.train_number = arrival_time.train_number "
                    "WHERE train.train_number = %s", (train_number,))
                train_info = cursor.fetchall()

                # Convert the result to a list of dictionaries
                result = [{'train_number': info[0],
                           'station_name': info[1],
                           'arrival_time': info[2],
                           'stop_order': info[3],
                           'seats_num': info[4],
                           'mileage': info[5],
                           'train_type': info[6]} for info in train_info]

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
                result = [{'account': user['account'], 'username': user['username'], 'password': user['password'], 'noOfOrder': user['noOfOrder']} for
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
