import streamlit as st
import pandas as pd

upload = st.file_uploader('Upload your unedited .csv from CC. It will not leave your private instance of this website, meaning nobody will have access to it.')

if upload != None:
    df = pd.read_csv(upload)

def process(df=df):
    for postcode in df.postcode.unique():
        _ = df[df.postcode == postcode].ward.value_counts()
        if len(_) > 1:
            while _.iloc[-1] < _.sum()/3:
                _ = df[df.postcode == postcode].ward.value_counts()
                df.drop(df[(df.postcode == postcode) & (df.ward == _.index[-1])].index, inplace=True)

    output = pd.DataFrame()

    for ward in df.ward.unique():
        _ = df[df.ward == ward].postcode.unique()
        _ = pd.Series(_, name=ward)
        output = output.join(_, how='outer')
    
    return output

if st.button('Process!'):
    output = process()
    st.table(output)
    st.download_button("Press to Download", output.to_csv(), "postcodesByWard.csv", "text/csv", key='download-csv')

