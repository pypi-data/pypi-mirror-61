import pymysql

def get_conn(*,host,user,pwd,db,charset="utf8"):
    """
    :return: 连接，游标
    """
    # 创建连接
    conn = pymysql.connect(host=host,
                           user=user,
                           password=pwd,
                           db=db,
                           charset=charset)
    # 创建游标
    cursor = conn.cursor()# 执行完毕返回的结果集默认以元组显示
    # cursor = conn.cursor(cursor=pymysql.cursors.DictCursor) # 得到一个可以执行SQL语句并且将结果作为字典返回的游标
    return conn, cursor


def close_conn(conn, cursor):
    cursor.close()
    conn.close()


def query(sql, *args,host,user,pwd,db,charset="utf8"):
    
    conn, cursor = get_conn(host=host,user=user,pwd=pwd,db=db,charset="utf8")
    cursor.execute(sql,args)
    res = cursor.fetchall()
    close_conn(conn,cursor)
    return res


def modify(sql, *args,host,user,pwd,db,charset="utf8"):
    conn, cursor = get_conn(host=host,user=user,pwd=pwd,db=db,charset="utf8")
    # 受影响的行数
    rows = cursor.execute(sql, args)
    #提交事务 update delete insert操作
    conn.commit()
    close_conn(conn, cursor)
    return rows

if __name__ == "__main__":
    
    import configparser
    config = configparser.ConfigParser()
    config.read(r"C:\Users\admin\Desktop\notebook\mysql.ini")
    items = dict(config.items("settings"))

    sql = "select * from users"
    a = query(sql,**items)
    print(a)
