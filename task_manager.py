import streamlit as st
from pymongo import MongoClient
from datetime import datetime

# MongoDB Setup (Make sure MongoDB is running locally or use MongoDB Atlas)
client = MongoClient("mongodb://localhost:27017/")
db = client['task_manager']
collection = db['tasks']

# Function to add a task
def add_task(title, description, due_date, priority):
    task_data = {
        'title': title,
        'description': description,
        'due_date': due_date.isoformat(),  # Convert date to string
        'priority': priority
    }
    collection.insert_one(task_data)

# Function to retrieve all tasks
def get_tasks():
    tasks = collection.find()
    return list(tasks)

# Streamlit UI
st.title("Task Manager")

# Sidebar Menu
menu = ["Add Task", "View Tasks"]
choice = st.sidebar.selectbox("Menu", menu)

# Add Task Module
if choice == "Add Task":
    st.subheader("Add a New Task")
    
    with st.form(key='add_task_form'):
        title = st.text_input("Task Title")
        description = st.text_area("Task Description")
        due_date = st.date_input("Due Date", min_value=datetime.today())
        priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        submit_button = st.form_submit_button(label='Add Task')

    if submit_button:
        add_task(title, description, due_date, priority)
        st.success(f"Task added: {title} (Due: {due_date}, Priority: {priority})")

# View Tasks Module
elif choice == "View Tasks":
    st.subheader("View All Tasks")
    
    tasks = get_tasks()
    
    if len(tasks) > 0:
        for task in tasks:
            st.write(f"**Title:** {task['title']}")
            st.write(f"**Description:** {task['description']}")
            st.write(f"**Due Date:** {task['due_date']}")
            st.write(f"**Priority:** {task['priority']}")
            st.write("---")  # Separator line
    else:
        st.info("No tasks found!")

