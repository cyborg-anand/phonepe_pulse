import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import fiona
fiona.drvsupport.supported_drivers['ESRI Shapefile'] = 'rw'

def show_page():
    st.title("Page 1")
    
    india_states = gpd.read_file('D:\\Projects\\phonepe_pulse\\india_st.shx')


    # Read shapefile for India's districts
    #india_districts = gpd.read_file('path_to_districts_shapefile.shp')

    # Plotting India's states
    fig, ax = plt.subplots(1, 1)
    india_states.plot(ax=ax, color='white', edgecolor='black')
    ax.set_title('India States')

    # Plotting India's districts
    # fig, ax = plt.subplots(1, 1)
    # india_districts.plot(ax=ax, color='blue', edgecolor='black')
    # ax.set_title('India Districts')

    st.pyplot(fig)
