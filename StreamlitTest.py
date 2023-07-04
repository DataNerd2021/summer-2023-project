import streamlit as st
import pandas as pd
import duckdb

# set page configurations
st.set_page_config(layout="centered", page_title='Used Car App')
st.title('&ensp;&ensp;&ensp;Used Car Price Prediciton App')
st.text("")
st.text("")
st.text("")

conn = duckdb.connect()

# declare main DataFrame
listings  = conn.sql('SELECT * FROM clean_training_data.csv').to_df()

# Create Integer Object for Model Year

year_selector = st.number_input(label='Model Year', value=2023, min_value=1997, max_value=2024)

# Create Select Object for Makes
col1, col2, col3 = st.columns([1,1,1])
with col1:
    makes = pd.DataFrame(conn.sql(f'SELECT DISTINCT make FROM listings WHERE year = {year_selector} ORDER BY make').to_df())
    makes = pd.Series(makes['make'])
    makes = makes.tolist()
    make_selector = st.selectbox(label='Make', options=[make for make in makes])
# Create Select Object for Models
with col2:
    try:
        models = pd.DataFrame(conn.sql(f'''SELECT DISTINCT model FROM listings WHERE TRIM(make) = '{str(make_selector)}' AND year = {year_selector} ORDER BY model''').to_df())
        models = pd.Series(models['model'])
        models = models.tolist()
        model_selector = st.selectbox(label='Model', options=[model for model in models])
    except:
        models = pd.DataFrame(conn.sql(f'SELECT DISTINCT model FROM listings ORDER BY model').to_df())
        models = pd.Series(models['model'])
        models = models.tolist()
        model_selector = st.selectbox(label='Model', options=[model for model in models])
# Create Select Object for Trims
with col3:
    try:
        trims = pd.DataFrame(conn.sql(f'''SELECT DISTINCT trim FROM listings WHERE TRIM(make) = '{str(make_selector)}' AND TRIM(model) = '{str(model_selector)}' AND year = {year_selector} ORDER BY trim''').to_df())
        trims = pd.Series(trims['trim'])
        trims = trims.tolist()
        trim_selector = st.selectbox(label='Trim', options=[trim for trim in trims])
    except:
        trims = pd.DataFrame(conn.sql(f'SELECT DISTINCT trim FROM listings ORDER BY trim').to_df())
        trims = pd.Series(trims['trim'])
        trims = trims.tolist()
        trim_selector = st.selectbox(label='Trim', options=[trim for trim in trims])
# Create Select Object for Transmission
st.text("")
st.text("")
col4, col5 = st.columns([2,2])
with col4:
    try:
        transmissions = pd.DataFrame(conn.sql(f'''SELECT DISTINCT transmission FROM listings ORDER BY transmission''').to_df())
        transmissions = pd.Series(transmissions['transmission'])
        transmissions = transmissions.tolist()
        transmission_selector = st.selectbox(label='Transmission', options=[transmission for transmission in transmissions])
    except:
        transmissions = pd.DataFrame(conn.sql(f'SELECT DISTINCT transmission FROM listings ORDER BY transmission').to_df())
        transmissions = pd.Series(transmissions['transmission'])
        transmissions = transmissions.tolist()
        transmission_selector = st.selectbox(label='Transmission', options=[transmission for transmission in transmissions])
with col5:
    try:
        drivetrains = pd.DataFrame(conn.sql(f'''SELECT DISTINCT drivetrain FROM listings WHERE TRIM(make) = '{str(make_selector)}' AND TRIM(model) = '{str(model_selector)}' AND year = {year_selector} ORDER BY trim''').to_df())
        drivetrains = pd.Series(drivetrains['drivetrain'])
        drivetrains = drivetrains.tolist()
        drivetrain_selector = st.selectbox(label='Drivetrain', options=[drivetrain for drivetrain in drivetrains])
    except:
        drivetrains = pd.DataFrame(conn.sql(f'SELECT DISTINCT drivetrain FROM listings ORDER BY drivetrain').to_df())
        drivetrains = pd.Series(drivetrains['drivetrain'])
        drivetrains = drivetrains.tolist()
        drivetrain_selector = st.selectbox(label='Drivetrain', options=[drivetrain for drivetrain in drivetrains])
st.text("")
st.text("")
col6, col7, = st.columns([2,2])
with col6:
    try:
        exterior_colors = pd.DataFrame(conn.sql(f'''SELECT DISTINCT exterior_color FROM listings WHERE TRIM(make) = '{str(make_selector)}' AND TRIM(model) = '{str(model_selector)}' AND trim LIKE '%{str(trim_selector)}%' AND year = {year_selector} ORDER BY exterior_color''').to_df())
        exterior_colors = pd.Series(exterior_colors['exterior_color'])
        exterior_colors = exterior_colors.tolist()
        ex_color_selector = st.selectbox(label='Exterior Color', options=[ex_color for ex_color in exterior_colors])
    except:
        exterior_colors = pd.DataFrame(conn.sql(f'SELECT DISTINCT exterior_color FROM listings ORDER BY exterior_color').to_df())
        exterior_colors = pd.Series(exterior_colors['exterior_color'])
        exterior_colors = exterior_colors.tolist()
        ex_color_selector = st.selectbox(label='Exterior Color', options=[ex_color for ex_color in exterior_colors])
with col7:
    try:
        interior_colors = pd.DataFrame(conn.sql(f'''SELECT DISTINCT interior_color FROM listings WHERE TRIM(make) = '{str(make_selector)}' AND TRIM(model) = '{str(model_selector)}' AND TRIM(trim) LIKE '%{str(trim_selector)}%' AND year = {year_selector} ORDER BY interior_color''').to_df())
        interior_colors = pd.Series(interior_colors['interior_color'])
        interior_colors = interior_colors.tolist()
        int_color_selector = st.selectbox(label='Interior Color', options=[int_color for int_color in interior_colors])
    except:
        interior_colors = pd.DataFrame(conn.sql(f'SELECT DISTINCT interior_color FROM listings ORDER BY interior_color').to_df())
        interior_colors = pd.Series(interior_colors['interior_color'])
        interior_colors = interior_colors.tolist()
        int_color_selector = st.selectbox(label='Interior Color', options=[int_color for int_color in interior_colors])
col8, col9, col10 = st.columns([1,0.2,3])
with col8:
    try:
        states = pd.DataFrame(conn.sql(f'''SELECT DISTINCT CASE WHEN state IS NULL THEN 'Online' ELSE state END state FROM listings ORDER BY state''').to_df())
        states = pd.Series(states['state'])
        states = states.tolist()
        state_selector = st.selectbox(label='State', options=[state for state in states])
    except:
        states = pd.DataFrame(conn.sql(f'''SELECT DISTINCT state FROM listings ORDER BY state''').to_df())
        states = pd.Series(states['state'])
        states = states.tolist()
        state_selector = st.selectbox(label='State', options=[state for state in states], disabled=True)
with col10:
    try:
        cities = pd.DataFrame(conn.sql(f'''SELECT DISTINCT CASE WHEN state IS NULL THEN NULL ELSE city END city FROM listings WHERE TRIM(state) = '{str(state_selector)}' ORDER BY city''').to_df())
        cities = pd.Series(cities['city'])
        cities = cities.tolist()
        city_selector = st.selectbox(label='City', options=[city for city in cities])
    except:
        cities = pd.DataFrame(conn.sql(f'''SELECT DISTINCT CASE WHEN state IS NULL THEN NULL ELSE city END city FROM listings WHERE TRIM(state) = '{str(state_selector)}' ORDER BY city''').to_df())
        cities = pd.Series(cities['city'])
        cities = cities.tolist()
        city_selector = st.selectbox(label='City', options=[city for city in cities], disabled=True)