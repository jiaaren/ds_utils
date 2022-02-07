import numpy as np

'''
Returns sum of all dataframes inputted as arguments
Returns size in megabyes (MB)
'''
def calc_df_size(*args):
    tot_size = 0
    for df in args:
        tot_size += df.memory_usage().sum()
    return tot_size/1000000

'''
Accepts dataframe and outputs schema in indented python dictionary format
'''
def schema_output(df):
    print('_SCHEMA = {')
    for col in df.columns:
        print(f'\t"{col}":', '{')
        print("\t\t\"title\": \"\",")
        print("\t\t\"data_type\": \"\"")
        print("\t}", end='')
        if df.columns[len(df.columns) - 1] != col:
            print(',', end='')
        print()
    print('}')
        
'''
# to time delta
# https://pandas.pydata.org/docs/reference/api/pandas.to_timedelta.html
Helper function to convert columns to relevant datatype specified in schema
To be used in conjunction with type_cast_df below
'''
def type_cast_column(col, schema):
    # search through schema to confirm title is present
    found_dtype = schema[col.name]
    if found_dtype == int:
        return col.astype(np.int32)
    elif found_dtype == float:
        return col.astype(np.float32)
    elif found_dtype == 'datetime':
        return pd.to_datetime(col)
    elif found_dtype == 'timedelta':
        # convert to timedelta seconds
        return pd.to_timedelta(col, unit='S')
    else:
        return col
    
'''
Accepts dataframe and outputs a copy based on updated datatypes specified in schema
Converts schema to a new dictionary which only contains updated titles/names
Uses type_cast_column helper function above
'''
def type_cast_df(df, schema):
    cpy = df.copy()
    # update column names as there are issues with unicode issues with title for video performance metrics
    new_col_names = [item['title'] for key, item in schema.items()]
    cpy.columns = new_col_names
    # create new dict from schema
    schema_upt = {item['title']:item['data_type'] for key, item in schema.items()}
    for col in cpy.columns:
        cpy[col] = type_cast_column(cpy[col], schema_upt)
    return cpy

