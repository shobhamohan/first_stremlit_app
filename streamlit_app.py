import streamlit
import requests
import snowflake.connector
import pandas
from urllib.error import URLError

# new section to display api response
streamlit.header('Fruity Vice Advice!')
#create a funtion 
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    #streamlit.write('The user entered ', fruit_choice)
    #import requests
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function) 
except URLError as e:
    streamlit.error()
    
#streamlit.text(fruityvice_response.json())
 my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"]) 
 my_cur = my_cnx.curor()
 my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
 stremlit.stop()


streamlit.header("DATA")
streamlit.button("get fruit load list")
def get_fruit_load_list():
    with my_cnx.cursor() as  my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()
    #add button to load fruit list
    try:
        if streamlit.button('get fruit load list'):
            my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
            my_data_rows = get_fruit_load_list()
            my_cnx.close()
            streamlit.dataframe(my_data_rows)
    except URLError as e:
        streamlit.error()

streamlit.header("DATA end ")     
streamlit.title('My parents New Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥤Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list =my_fruit_list.set_index ('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
# streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)

# take the json response  
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# display in the frame
#streamlit.dataframe(fruityvice_normalized)
#import snowflake.connector
# snowflake related funcitons

#streamlit.stop() 

#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor as my_cur:
        my_cur.execute("insert into fruit_load_list values ('test')")
        return "Thanks for adding " + new_fruit
add_my_fruit = streamlit.text_input('What fruit you would like add?')
try:
    if not add_my_fruit:
        streamlit.error("Please enter fruit")
    else:
        streamlit.button('add a fruit to the list')
        my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
        back_from_function = insert_row_snowflake(add_my_fruit)
        streamlit.text(back_from_function)
except URLError as e:
    streamlit.error()


#streamlit.write('The user entered ', fruit_choice2)
