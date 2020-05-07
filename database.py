import sqlite3
from process import Proc

# Things to do: Create a checking mechanism in insert to check if the data with the same name is already there
# If so update the database instead

#Close the connection then reestablish it
def create_connecton(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn

    except Error as e:
        print(e)

    return conn

#Create the table in the database for processes
def create_table(conn):
    try:
        c = conn.cursor()
        c. execute("""CREATE TABLE processes (
                        id integer,
                        name text,
                        appname text,
                        create_time integer,
                        time_used integer
                        ) """)

        conn.commit()

    except Error as e:
        print(e)

def get_entry(conn, process):
    c = conn.cursor()
    c.execute("SELECT * FROM processes WHERE id = :id", {'id': process.id})
    return c.fetchone()

def insert_entry(conn, process):
    c = conn.cursor()
    c.execute("SELECT * FROM processes WHERE id = :id", {'id': process.id})
    # nothing happens if you select a null entry, produces no errors

    process_attributes = list(c.fetchall())
    if len(process_attributes) != 0:
        if process_attributes[0][0] == process.id or process_attributes[0][2] == process.appname:
            print("Process already exists in database!")
            return
        else:
            pass

    c.execute("INSERT INTO processes VALUES(:id, :name, :appname, :create_time, :time_used)",
              {'id': process.id, 'name': process.name, 'appname': process.appname,
               'create_time': process.create_time, 'time_used': process.time_used})

#updates the entry for create_time and time_used
def update_entry(conn, process):
    c = conn.cursor()
    c.execute ("SELECT * FROM processes WHERE id = :id", {'id': process.id})
    try:
        time_added = c.fetchall()[0][4]
        total_time_used = process.time_used + time_added
        c.execute("UPDATE processes SET create_time = :create_time, time_used = :total_time_used WHERE id = :id",
                  {'id': process.id, 'create_time': process.create_time, 'total_time_used': total_time_used})

    except:
        print("Entry does not exist in database")

def get_all(conn):
    c = conn.cursor()
    c.execute('SELECT * FROM processes')
    return c.fetchall()

def show_all(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM processes")
    print(c.fetchall())

def delete_all(conn):
    c = conn.cursor()
    c.execute("DELETE FROM processes")

def main():
    conn = create_connecton('database.db')
    #create_table(conn)

    # test to see if insert entry function works
    p2 = Proc(0, 'newprocessA', 'NewProcessA', 0 , 0)
    p3 = Proc(1, 'newprocessB', 'NewProcesssB', 0, 0)

    insert_entry(conn, p2)
    insert_entry(conn, p3)

    show_all(conn)
    delete_all(conn)

    #test to see if update_entry works
    p4 = Proc(0, 'newprocessA', 'NewProcessA', 0 , 1)
    p5 = Proc(0, 'newprocessA', 'NewProcessA', 1 , 2)
    insert_entry(conn, p4)
    update_entry(conn, p5)

    show_all(conn)
    delete_all(conn)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()