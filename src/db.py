

import mysql.connector

def connect_to_database():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="mayankbiker44",
        database="mi_task"   
    )
    
def video_history(video_tag, video_summery,video_visual,output_image_path,filename):
    #return (answer)
    try:
        mydb = connect_to_database()
        mycursor = mydb.cursor()
        sql1 = "INSERT INTO mi_task.video_data (video_tag, video_summery,video_visual,image,video_name) VALUES (%s, %s, %s ,%s ,%s)" 
        val1 = (video_tag, video_summery,video_visual,output_image_path,filename)

        mycursor.execute(sql1, val1)
        mydb.commit()

        return 'yess'

    except Exception as e:
        print('Error checking user existence: ', e)
        return False
    
def user_history():
    try:
        mydb = connect_to_database()
        mycursor = mydb.cursor()

        sql =  f"""SELECT video_name,video_tag,image FROM mi_task.video_data"""
        mycursor.execute(sql)
        result = mycursor.fetchall()
        
        # Check if the user exists and is a seller
        print('allll new',result)
        return  result #[0] 

    except Exception as e:
        print('Error checking user existence: ', e)
        return False
    
