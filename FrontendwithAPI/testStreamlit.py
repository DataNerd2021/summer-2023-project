import streamlit as st
import pandas as pd
from google.cloud import bigquery
import os
import requests 

# set page configurations
st.set_page_config(layout="centered", page_title='Used Car App')
st.title('&ensp;&ensp;&ensp;Used Car Price Prediciton App with API')
st.text("")
st.text("")
st.text("")

def truelistingCalls(endpoint,data):
    base_url = "http://truelistingapi:2020"
    url = f"{base_url}/{endpoint}"
    response = requests.post(url,json=data)
    
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"extended-spark-381216-d0e2ae70606d.json"
client = bigquery.Client(project='extended-spark-381216')

main_table = '`training_data.filtered_training_data`'
st.header("Select Your Vehicle")

# Create Integer Object for Model Year
year_selector = st.number_input(label='Model Year', value=2023, min_value=1997, max_value=2024)

# Create Select Object for Makes
col1, col2, col3 = st.columns([1,1,1])
with col1:
    makes = pd.DataFrame(client.query(f'SELECT DISTINCT make FROM {main_table} WHERE year = {year_selector} ORDER BY make;').to_dataframe())
    makes = pd.Series(makes['make'])
    makes = makes.tolist()
    make_selector = st.selectbox(label='Make', options=[make for make in makes])
# Create Select Object for Models
with col2:
    try:
        models = pd.DataFrame(client.query(f'''SELECT DISTINCT model FROM {main_table} WHERE TRIM(make) = '{str(make_selector)}' AND year = {year_selector} ORDER BY model''').to_dataframe())
        models = pd.Series(models['model'])
        models = models.tolist()
        model_selector = st.selectbox(label='Model', options=[model for model in models])
    except:
        models = pd.DataFrame(client.query(f'SELECT DISTINCT model FROM {main_table} ORDER BY model').to_dataframe())
        models = pd.Series(models['model'])
        models = models.tolist()
        model_selector = st.selectbox(label='Model', options=[model for model in models])
# Create Select Object for Trims
with col3:
    try:
        trims = pd.DataFrame(client.query(f'''SELECT DISTINCT trim FROM {main_table} WHERE TRIM(make) = '{str(make_selector)}' AND TRIM(model) = '{str(model_selector)}' AND year = {year_selector} ORDER BY trim''').to_dataframe())
        trims = pd.Series(trims['trim'])
        trims = trims.tolist()
        trim_selector = st.selectbox(label='Trim', options=[trim for trim in trims])
    except:
        trims = pd.DataFrame(client.query(f'SELECT DISTINCT trim FROM {main_table} ORDER BY trim').to_dataframe())
        trims = pd.Series(trims['trim'])
        trims = trims.tolist()
        trim_selector = st.selectbox(label='Trim', options=[trim for trim in trims])
        
# Create Select Object for Transmission
st.text("")
st.text("")
st.header("Select Vehicle Specifications")
col4, col5 = st.columns([1,1])
with col4:
    mileage_selector = st.number_input(label='Mileage', value=0, min_value=0, max_value=412000, step=1000)
with col5:
    engines = pd.DataFrame(client.query(f'''SELECT DISTINCT engine FROM {main_table} WHERE TRIM(make) = '{str(make_selector)}' AND TRIM(model) = '{str(model_selector)}' AND TRIM(trim) LIKE '%{str(trim_selector)}%' AND year = {year_selector} ORDER BY engine''').to_dataframe())
    engines = pd.Series(engines['engine'])
    engines = engines.tolist()
    engine_selector = st.selectbox(label='Engine', options=[engine for engine in engines])
col6, col7, col8 = st.columns([1,1,1])
with col6:
    try:
        fuel_types = pd.DataFrame(client.query(f'''SELECT DISTINCT fuel_type FROM {main_table} WHERE TRIM(make) = '{str(make_selector)}' AND TRIM(model) = '{str(model_selector)}' AND TRIM(trim) LIKE '%{str(trim_selector)}%' AND year = {year_selector} ORDER BY fuel_type''').to_dataframe())
        fuel_types = pd.Series(fuel_types['fuel_type'])
        fuel_types = fuel_types.tolist()
        fuel_selector = st.selectbox(label='Fuel Type', options=[fuel_type for fuel_type in fuel_types])
    except:
        fuel_types = pd.DataFrame(client.query(f'''SELECT DISTINCT fuel_type FROM {main_table} WHERE TRIM(make) = '{str(make_selector)}' AND TRIM(make) = '{str(model_selector)}' ''').to_dataframe())
        fuel_types = pd.Series(fuel_types['fuel_type'])
        fuel_types = fuel_types.tolist()
        fuel_selector = st.selectbox(label='Fuel Type', options=[fuel_type for fuel_type in fuel_types])
with col7:
    try:
        transmissions = pd.DataFrame(client.query(f'''SELECT DISTINCT transmission FROM {main_table} ORDER BY transmission''').to_dataframe())
        transmissions = pd.Series(transmissions['transmission'])
        transmissions = transmissions.tolist()
        transmission_selector = st.selectbox(label='Transmission', options=[transmission for transmission in transmissions])
    except:
        transmissions = pd.DataFrame(client.query(f'SELECT DISTINCT transmission FROM {main_table} ORDER BY transmission').to_dataframe())
        transmissions = pd.Series(transmissions['transmission'])
        transmissions = transmissions.tolist()
        transmission_selector = st.selectbox(label='Transmission', options=[transmission for transmission in transmissions])
with col8:
    try:
        drivetrains = pd.DataFrame(client.query(f'''SELECT DISTINCT drivetrain FROM {main_table} WHERE TRIM(make) = '{str(make_selector)}' AND TRIM(model) = '{str(model_selector)}' AND year = {year_selector} ORDER BY trim''').to_dataframe())
        drivetrains = pd.Series(drivetrains['drivetrain'])
        drivetrains = drivetrains.tolist()
        drivetrain_selector = st.selectbox(label='Drivetrain', options=[drivetrain for drivetrain in drivetrains])
    except:
        drivetrains = pd.DataFrame(client.query(f"SELECT DISTINCT drivetrain FROM {main_table} WHERE model = '{model_selector}' AND year = {year_selector} ORDER BY drivetrain").to_dataframe())
        drivetrains = pd.Series(drivetrains['drivetrain'])
        drivetrains = drivetrains.tolist()
        drivetrain_selector = st.selectbox(label='Drivetrain', options=[drivetrain for drivetrain in drivetrains])
st.text("")
st.text("")
st.header('Select Vehicle Colors')
col9, col10, = st.columns([2,2])
with col9:
    try:
        exterior_colors = pd.DataFrame(client.query(f'''SELECT DISTINCT exterior_color FROM {main_table} WHERE TRIM(make) = '{str(make_selector)}' AND TRIM(model) = '{str(model_selector)}' AND trim LIKE '%{str(trim_selector)}%' AND year = {year_selector} ORDER BY exterior_color''').to_dataframe())
        exterior_colors = pd.Series(exterior_colors['exterior_color'])
        exterior_colors = exterior_colors.tolist()
        ex_color_selector = st.selectbox(label='Exterior Color', options=[ex_color for ex_color in exterior_colors])
    except:
        exterior_colors = pd.DataFrame(client.query(f'SELECT DISTINCT exterior_color FROM {main_table} ORDER BY exterior_color').to_dataframe())
        exterior_colors = pd.Series(exterior_colors['exterior_color'])
        exterior_colors = exterior_colors.tolist()
        ex_color_selector = st.selectbox(label='Exterior Color', options=[ex_color for ex_color in exterior_colors])
with col10:
    try:
        interior_colors = pd.DataFrame(client.query(f'''SELECT DISTINCT interior_color FROM {main_table} WHERE TRIM(make) = '{str(make_selector)}' AND TRIM(model) = '{str(model_selector)}' AND TRIM(trim) LIKE '%{str(trim_selector)}%' AND year = {year_selector} ORDER BY interior_color''').to_dataframe())
        interior_colors = pd.Series(interior_colors['interior_color'])
        interior_colors = interior_colors.tolist()
        int_color_selector = st.selectbox(label='Interior Color', options=[int_color for int_color in interior_colors])
    except:
        interior_colors = pd.DataFrame(client.query(f'SELECT DISTINCT interior_color FROM {main_table} ORDER BY interior_color').to_dataframe())
        interior_colors = pd.Series(interior_colors['interior_color'])
        interior_colors = interior_colors.tolist()
        int_color_selector = st.selectbox(label='Interior Color', options=[int_color for int_color in interior_colors])
st.text("")
st.text("")
st.header('Select Vehicle Location')
col11, col12, col13 = st.columns([1,0.2,3])
with col11:
    try:
        states = pd.DataFrame(client.query(f'''SELECT DISTINCT CASE WHEN state IS NULL THEN 'Online' ELSE state END state FROM {main_table} ORDER BY state''').to_dataframe())
        states = pd.Series(states['state'])
        states = states.tolist()
        state_selector = st.selectbox(label='State', options=[state for state in states])
    except:
        states = pd.DataFrame(client.query(f'''SELECT DISTINCT state FROM {main_table} ORDER BY state''').to_dataframe())
        states = pd.Series(states['state'])
        states = states.tolist()
        state_selector = st.selectbox(label='State', options=[state for state in states], disabled=True)
with col13:
    try:
        cities = pd.DataFrame(client.query(f'''SELECT DISTINCT CASE WHEN state IS NULL THEN NULL ELSE city END city FROM {main_table} WHERE TRIM(state) = '{str(state_selector)}' ORDER BY city''').to_dataframe())
        cities = pd.Series(cities['city'])
        cities = cities.tolist()
        city_selector = st.selectbox(label='City', options=[city for city in cities])
    except:
        cities = pd.DataFrame(client.query(f'''SELECT DISTINCT CASE WHEN state IS NULL THEN NULL ELSE city END city FROM {main_table} WHERE TRIM(state) = '{str(state_selector)}' ORDER BY city''').to_dataframe())
        cities = pd.Series(cities['city'])
        cities = cities.tolist()
        city_selector = st.selectbox(label='City', options=[city for city in cities], disabled=True)
            
test_model =  {
    "year": year_selector,
    "make": make_selector,
    "model": model_selector,
    "trim": trim_selector,
    "mileage": mileage_selector,
    "engine": engine_selector,
    "fuelType": fuel_selector,
    "transmission": transmission_selector,
    "drivetrain": drivetrain_selector,
    "exteriorColor": ex_color_selector,
    "interiorColor": int_color_selector,
    "state": state_selector,
    "city": city_selector,
}

# predicted_price = round(prediction_query['predicted_price'].values[0], 2)
with col11:
    prediction_btn = st.button(label='Get Prediction')
    
with col13:
    clear_btn = st.button(label='Clear Output')

if prediction_btn:
    truelistingCalls("pricing", test_model)
    #st.markdown("<h3>Predicted Price: <br><br> <h2>${:,.2f}</h2>".format(predicted_price), unsafe_allow_html=True)
elif clear_btn:
    st.markdown("")
