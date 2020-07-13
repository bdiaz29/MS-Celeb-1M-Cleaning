import sqlite3
import time
import numpy as np
import os
import glob

# create string to send insert command
values_string = "INSERT INTO embeddings(ident,file_path,score,check_flag"
for i in range(128):
    values_string = values_string + "," + "vec_" + str(i)
values_string = values_string + ")\n"
values_string = values_string + "VALUES(?"
for j in range(128 + 3):
    values_string = values_string + ",?"
values_string = values_string + ")"
P = 0


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except:
        print("error connecting to database")
    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except:
        print("error creating a table")


def create_project(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    global values_string
    sql = ''' INSERT INTO celeb(ident,file_path,score,check_flag,face_embeddings)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    return cur.lastrowid


def chunk_insert(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    global values_string
    sql = ''' INSERT INTO celeb(ident,file_path,score,check_flag,face_embeddings)
              VALUES(?,?,?,?,?) '''

    cur = conn.cursor()
    cur.execute("begin;")
    for i in range(len(project)):
        proj = project[i]
        cur.execute(sql, proj)
    cur.execute("commit;")
    return cur.lastrowid


def update_project(conn, task):
    sql = ''' UPDATE tasks
                  SET priority = ? ,
                      begin_date = ? ,
                      end_date = ?
                  WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()


def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")

    rows = cur.fetchall()
    return rows


"""p = 0
insert = (folder, path, .5, 1, test_2)
p = 0
with connection:
    project_id = create_project(connection, insert)
    p = 0"""
connection = create_connection("G:/machine learning/Celeb1M.db")
folder_list = glob.glob("G:/machine learning/Celeb 1M cleaned no relabeling/*/")
c = 0
d = 0
c0 = 0
insert=[]
for i in range(len(folder_list)):
    opened_folder = folder_list[i]
    folder = os.path.basename(os.path.normpath(opened_folder))
    a = time.time()
    identity_grp = np.load(opened_folder + "vec.npy")
    file_list = np.load(opened_folder + "file_list.npy")
    b = time.time()
    for j in range(len(identity_grp)):
        c0 = time.time()
        face_embedding = identity_grp[j].tobytes()
        insert += [(folder, file_list[j], 1, 0, face_embedding)]
    if len(insert)>=50000:
        with connection:
            c = time.time()
            project_id = chunk_insert(connection, insert)
            d = time.time()
            print(str(i), str(b - a), str(c - c0), str(d - c))
            insert=[]
