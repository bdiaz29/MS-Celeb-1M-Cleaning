import sqlite3
import numpy as np
import tensorflow as tf
import time
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except:
        print("error connecting to database")
    return conn


def get_ident_index(conn):
    command = """SELECT DISTINCT ident from celeb where ident!='unknown'"""
    cur = conn.cursor()
    cur.execute(command)
    rows = cur.fetchall()
    rows = np.ndarray.flatten(np.array(rows))
    return rows


def get_group_face_embeddings(ident, conn):
    command = "SELECT  face_embeddings,id from celeb where ident=\'" + ident + "\'"
    cur = conn.cursor()
    cur.execute(command)
    rows = cur.fetchall()
    # convert into 1d vectors
    vectors = []
    ids = []
    for i in range(len(rows)):
        temp = np.frombuffer(rows[i][0], dtype=np.float32)
        vectors += [temp]
        ids += [rows[i][1]]
    return vectors, ids


# test how similar the group is
def test_group(ident, conn, model, samples):
    group_arr, ids = get_group_face_embeddings(ident, conn)
    group = []
    group_length = len(group_arr)
    samples_ = min(samples, group_length-1)
    # take random samples
    c=len(group_arr)-1
    s_list = np.random.choice(c, replace=False,size=samples_)
    sample_list=[]
    for k in range(len(s_list)):
        sample_list+=[group_arr[s_list[k]]]

    for i in range(len(sample_list)):

        sample = sample_list[i]
        for j in range(group_length):
            test_case = group_arr[j]
            temp = np.concatenate([sample, test_case])
            group += [temp]

    if group_length == 1:
        temp = np.concatenate([group_arr[0], group_arr[0]])
        group += [temp]
    group = np.array(group)
    pred = model.predict(group)
    avg = np.mean(pred)
    return avg

def remove_group(ident,conn):
    command = "UPDATE celeb SET ident='unknown' WHERE ident=\'" + ident + "\'"+";"
    cur = conn.cursor()
    cur.execute(command)

vec_nn = tf.keras.models.load_model("faces3.h5",
                                    custom_objects={
                                        'LeakyReLU': tf.keras.layers.LeakyReLU(),
                                        'GlorotUniform': tf.keras.initializers.glorot_uniform()}, compile=True)

connection = create_connection("G:/machine learning/Celeb1M.db")
# read entire ll valid identities
idents = get_ident_index(connection)
count=0
threshold=.7
length=len(idents)
for i in range(len(idents)):
    a = test_group(idents[i], connection, vec_nn, 10)
    if a<=threshold:
        count+=1
        remove_group(idents[i],connection)
        ratio = ((count) / (i + 1)) * 100
        print(i,str(a),str(ratio),"group removed")
    else:
        ratio = ((count) / (i + 1)) * 100
        print(i, str(a), str(ratio))
connection.commit()
connection.close()

print(count," groups removed")
