import streamlit as st
import requests

API_URL = "http://localhost:5000/api/configurations"

def get_configurations():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch configurations")
        return []

def add_configuration(key, value):
    response = requests.post(API_URL, json={"key": key, "value": value})
    if response.status_code == 201:
        st.success("Configuration added successfully")
    else:
        st.error("Failed to add configuration")

def delete_configuration(config_id):
    response = requests.delete(f"{API_URL}/{config_id}")
    if response.status_code == 204:
        st.success("Configuration deleted successfully")
    else:
        st.error("Failed to delete configuration")

st.title("Configuration Management")

st.header("Add Configuration")
key = st.text_input("Key")
value = st.text_input("Value")
if st.button("Add"):
    add_configuration(key, value)

st.header("Existing Configurations")
configurations = get_configurations()
for config in configurations:
    st.write(f"ID: {config['id']}, Key: {config['key']}, Value: {config['value']}")
    if st.button(f"Delete {config['id']}"):
        delete_configuration(config['id'])
        st.experimental_rerun()