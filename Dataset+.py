import psycopg2

conn = psycopg2.connect("dbname=dataset user=postgres password=1234")
cur = conn.cursor()
for i in range(10):
    print(f"\nВвод № {i + 1}")    
    inp = input('\nВходные данные: ')
    out = input('\nВыходные данные: ')

    cur.execute("INSERT INTO trainingdataset (input, output) VALUES (%s, %s) RETURNING id", (inp, out))
    conn.commit()

    print("\nДанные успешно добавлены в базу.")

cur.execute("SELECT id, input, output FROM trainingdataset")
records = cur.fetchall()

#for record in records:
    #print(f"\nID: {record[0]}\n\n Входные данные: {record[1]}\n\n Выходные данные: {record[2]}\n")

cur.close()
conn.close()

