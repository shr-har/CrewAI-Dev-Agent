import streamlit as st
import requests
import time

API_BASE_URL = "https://crewai-dev-agent-0e0f358e-1773-4c2c-bb30-20-e6402b3e.crewai.com"
BEARER_TOKEN = "e03db76ea59c"  # Replace with your actual token

HEADERS = {"Authorization": f"Bearer {BEARER_TOKEN}"}

def get_required_inputs():
    """Fetch required inputs for the CrewAI agent."""
    response = requests.get(f"{API_BASE_URL}/inputs", headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch inputs: {response.text}")
        return None

def kickoff_execution(inputs):
    """Start CrewAI execution."""
    payload = {"inputs": inputs}
    response = requests.post(f"{API_BASE_URL}/kickoff", json=payload, headers=HEADERS)
    
    if response.status_code == 200:
        return response.json().get("task_id")
    else:
        st.error(f"Error: {response.text}")
        return None

def check_status(task_id):
    """Check execution status until completion."""
    status_url = f"{API_BASE_URL}/status/{task_id}"
    while True:
        response = requests.get(status_url, headers=HEADERS)
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "completed":
                return result
            else:
                st.info("Processing... Checking again in 5 seconds.")
                time.sleep(5)
        else:
            st.error(f"Error checking status: {response.text}")
            return None

def main():
    st.title("CrewAI Developer Agent")

    # Fetch required inputs
    required_inputs = get_required_inputs()
    if required_inputs:
        st.subheader("Provide Inputs for CrewAI Execution")
        user_inputs = {}
        for key in required_inputs.get("inputs", {}):
            user_inputs[key] = st.text_input(f"Enter {key}:", "")

        if st.button("Run CrewAI Agent"):
            with st.spinner("Processing... Please wait."):
                task_id = kickoff_execution(user_inputs)
                if task_id:
                    st.success(f"Task started! Task ID: {task_id}")
                    result = check_status(task_id)
                    if result:
                        st.success("Execution Completed!")
                        st.text_area("Result:", str(result), height=300)

if __name__ == "__main__":
    main()
