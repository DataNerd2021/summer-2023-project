import streamlit as st
import pandas as pd
import duckdb

# set page configurations
st.set_page_config(layout="centered", page_title='Used Car App')

conn = duckdb.connect()

# declare main DataFrame
listings  = conn.sql('SELECT * FROM clean_training_data.csv').to_df()

# Create Slider Object for Model Year
min_year = conn.sql('SELECT MIN(year) AS min_year FROM listings').to_df()
min_year = int(min_year['min_year'][0])

max_year = conn.sql('SELECT MAX(year) AS max_year FROM listings').to_df()
max_year = int(max_year['max_year'][0])

year_selector = st.slider(label='Model Year', min_value=min_year, max_value=max_year, value=(min_year,max_year))

# Create Multi-Select Object for Makes
col1, col2, col3 = st.columns([1,1,1])
with col1:
    makes = pd.DataFrame(conn.sql('SELECT DISTINCT make FROM listings ORDER BY make').to_df())
    makes = pd.Series(makes['make'])
    makes = makes.tolist()
    make_selector = st.multiselect(label='Make', options=[make for make in makes])
# Create Multi-Select Object for Models
with col2:
    try:
        models = pd.DataFrame(conn.sql(f'SELECT DISTINCT model FROM listings WHERE make IN ({str(make_selector)[1:-1]}) ORDER BY model').to_df())
        models = pd.Series(models['model'])
        models = models.tolist()
        model_selector = st.multiselect(label='Model', options=[model for model in models])
    except:
        models = pd.DataFrame(conn.sql(f'SELECT DISTINCT model FROM listings ORDER BY model').to_df())
        models = pd.Series(models['model'])
        models = models.tolist()
        model_selector = st.multiselect(label='Model', options=[model for model in models])
# Create Multi-Select Object for Trims
with col3:
    try:
        trims = pd.DataFrame(conn.sql(f'SELECT DISTINCT trim FROM listings WHERE make IN ({str(make_selector)[1:-1]}) AND model IN({str(model_selector)[1:-1]}) ORDER BY model').to_df())
        trims = pd.Series(trims['trim'])
        trims = trims.tolist()
        trim_selector = st.multiselect(label='Trim', options=[trim for trim in trims])
    except:
        trims = pd.DataFrame(conn.sql(f'SELECT DISTINCT trim FROM listings ORDER BY trim').to_df())
        trims = pd.Series(trims['trim'])
        trims = trims.tolist()
        trim_selector = st.multiselect(label='Trim', options=[trim for trim in trims])
# Create Multi-Select Object for Transmission
col4, col5, col6 = st.columns([1,1,1])
with col4:
    try:
        transmissions = pd.DataFrame(conn.sql(f'SELECT DISTINCT transmission FROM listings WHERE make IN ({str(make_selector)[1:-1]}) AND model IN({str(model_selector)[1:-1]}) AND trim IN({str(trim_selector)[1:-1]}) ORDER BY transmission').to_df())
        transmissions = pd.Series(transmissions['transmission'])
        transmissions = transmissions.tolist()
        transmission_selector = st.multiselect(label='Transmission', options=[transmission for transmission in transmissions])
    except:
        transmissions = pd.DataFrame(conn.sql(f'SELECT DISTINCT transmission FROM listings ORDER BY transmission').to_df())
        transmissions = pd.Series(transmissions['transmission'])
        transmissions = transmissions.tolist()
        transmission_selector = st.multiselect(label='Transmission', options=[transmission for transmission in transmissions])
with col5:
    try:
        drivetrains = pd.DataFrame(conn.sql(f'SELECT DISTINCT drivetrain FROM listings WHERE make IN ({str(make_selector)[1:-1]}) AND model IN({str(model_selector)[1:-1]}) AND trim IN({str(trim_selector)[1:-1]}) AND transmission IN({str(transmission_selector)[1:-1]}) ORDER BY drivetrain').to_df())
        drivetrains = pd.Series(drivetrains['drivetrain'])
        drivetrains = drivetrains.tolist()
        drivetrain_selector = st.multiselect(label='Drivetrain', options=[drivetrain for drivetrain in drivetrains])
    except:
        drivetrains = pd.DataFrame(conn.sql(f'SELECT DISTINCT drivetrain FROM listings ORDER BY drivetrain').to_df())
        drivetrains = pd.Series(drivetrains['drivetrain'])
        drivetrains = drivetrains.tolist()
        drivetrain_selector = st.multiselect(label='Drivetrain', options=[drivetrain for drivetrain in drivetrains])
# Create Output DataFrame
try:
    try:
        query = conn.sql(f'''SELECT FORMAT(price, 'N') AS price, year, make, model, trim, mileage, engine, fuel_type, drivetrain, transmission, exterior_color, interior_color, city, state FROM listings WHERE year BETWEEN {min_year} AND {max_year} AND make IN({str(make_selector)[1:-1]}) AND model IN({str(model_selector)[1:-1]}) AND trim IN({str(trim_selector)[1:-1]}) AND transmission IN({str(transmission_selector)[1:-1]})''').to_df()
        results = st.dataframe(query)
        try:
            st.write(f'{len(query)} Results')
        except:
            st.write()
    except:
        query = conn.sql(f'''SELECT FORMAT(price, 'N') AS price, year, make, model, trim, mileage, engine, fuel_type, drivetrain, transmission, exterior_color, interior_color, city, state FROM listings WHERE year BETWEEN {min_year} AND {year_selector} AND make IN({str(make_selector)[1:-1]}) AND model IN({str(model_selector)[1:-1]}) AND trim IN({str(trim_selector)[1:-1]})''').to_df()
        results = st.dataframe(query)
        st.write(f'{len(query)} Results')
        try:
            query = conn.sql(f'''SELECT ROUND(price, 2) AS price, year, make, model, trim, mileage, engine, fuel_type, drivetrain, transmission, exterior_color, interior_color, city, state FROM listings WHERE year BETWEEN {min_year} AND {year_selector} AND make IN({str(make_selector)[1:-1]}) AND model IN({str(model_selector)[1:-1]})''').to_df()
            results = st.dataframe(query)
            st.write(f'{len(query)} Results')
        except:
            results = st.dataframe(conn.sql(f'''SELECT ROUND(price, 2) AS price, year, make, model, trim, mileage, engine, fuel_type, drivetrain, transmission, exterior_color, interior_color, city, state FROM listings WHERE year BETWEEN {min_year} AND {year_selector} AND make IN({str(make_selector)[1:-1]})''').to_df())
            st.write(f'# of Results: {len(results)}')
except:
    results = st.dataframe(conn.sql(f'''SELECT ROUND(price, 2) AS price, year, make, model, trim, mileage, engine, fuel_type, drivetrain, transmission, exterior_color, interior_color, city, state FROM listings WHERE year BETWEEN {min_year} AND {year_selector}''').to_df())
    try:
        st.write(f'# of Results: {len(results)}')
    except:
        st.write()