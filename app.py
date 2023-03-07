import pandas as pd, duckdb, streamlit as st

def app(DB_PATH=':memory:'):
    # Config
    st.set_page_config(layout="wide")
    
    # Header
    st.markdown('<h1 align="center"><b> File Query App </b></h1>', unsafe_allow_html=True)

    # User input
    SELECT_FILES = st.file_uploader(
        label='UPLOAD FILE', 
        accept_multiple_files=True,
        type=['csv', 'parquet'], )

    # DATABASE
    DATABASE = duckdb.connect(DB_PATH)

    if len(SELECT_FILES) > 0:
        for file in SELECT_FILES:
            tmp_name, tmp_type = file.name.split('.')

            if tmp_type.lower() == 'csv':
                tmp = pd.read_csv(file)

            if tmp_type.lower() == 'parquet':
                tmp = pd.read_parquet(file)
            
            DATABASE.execute(f'CREATE OR REPLACE TABLE {tmp_name} AS SELECT * FROM tmp;')
    
    # Query Input
    if len(SELECT_FILES) == 0:
        st.markdown('<h4 align="center"><b> Upload A File To Enter Query Mode </b></h4>', unsafe_allow_html=True)
    else:
        st.markdown('---')
        USER_QUERY = st.text_area(label='ENTER QUERY', height=200)
    
        if USER_QUERY:
            USER_RESULT = DATABASE.execute(USER_QUERY).df()
            
            # Download results
            st.download_button(
                label='Download Result', 
                data=USER_RESULT.to_csv().encode('utf-8'),
                file_name='USER_QUERY.csv')
            
            # Show results
            st.markdown('---')
            st.write('QUERY RESULTS')
            st.dataframe(USER_RESULT, use_container_width=True)

            # Plot option 
            st.markdown('---')
            st.write('PLOT OPTIONS') 
            col_x, col_y, col_t, col_a = st.columns(4)

            X_LABEL = col_x.selectbox(label='X-Axis', options=USER_RESULT.columns)
            Y_LABEL = col_y.selectbox(label='Y-Axis', options=USER_RESULT.columns)
            CHART_TYPE = col_t.selectbox(label='Chart Type', options=['area', 'bar', 'line'])
            AGG_TYPE = col_a.selectbox(label='Aggregation', options=['sum', 'mean', 'count', 'max', 'min', 'std'])
     
            try:
                DATA = USER_RESULT.groupby(X_LABEL)[Y_LABEL].agg(AGG_TYPE).round(1)
            except TypeError:
                st.markdown('<h4 align="center"><b>SELECTION CANNOT BE PLOTTED</b></h4>', unsafe_allow_html=True)
            else:
                getattr(st, f'{CHART_TYPE}_chart')(data=DATA, height=500)
                
if __name__ == "__main__":
    app()