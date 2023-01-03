import streamlit as st
import pandas as pd
import time

# Add Title to your website
st.title("Startup Dashboard")

# Add header
st.header(" I am learning streamlit")

# Add sub header
st.subheader(" I am loving it")

# Write (Print paragraph)
st.write("This is a normal text")

# Markdown
st.markdown(""" My favourite stocks
- KPITech   
- Persistent
- Medanta
""")
# Here - will create bullet points

# Write code
st.code("""
# Square of any number
def func(x):
return x**2

y = func(2)
""")

# Write Latex
st.latex("""
 x^2 + y^2 + 2 = 0
 sin^2(x) + cos^2(x) = 1
""")

# Add DataFrame
import pandas as pd
df = pd.DataFrame({"Name":["A","B","C"],
                   "Marks":[1,2,3]})
st.dataframe(df)

# Add Metric
st.metric('Revenue: ','Rs 3,00,000','2%')
st.metric('Cost: ','Rs 1,00,000','-2%')

# Add Json
st.json({"Name":["A","B","C"],
                   "Marks":[1,2,3]})

# Displaying Media :-
# Add Image
#st.image('Path Name')

# Add Video
#st.video("Video Name")

# Creating Layout:-
# Add Sidebar
st.sidebar.title("SideBar Title")
st.sidebar.write("Stocks")
st.sidebar.markdown("""Top Picks
- IT
- Metal
""")

# Add columns:-
col1, col2 = st.columns(2)
with col1:
    st.image("output_0_1.png")
with col2:
    st.image("output_9_1.png")


# Showing Status:-

# Error Message
st.error("Login Failed")
st.success("Login Successful")
st.warning("Warning Message")
st.info("Information")

# Progress Bar
bar = st.progress(0)

for i in range(1,10):
    time.sleep(0.001)
    bar.progress(i)

st.write("File Upload Successful")


# Take Input from User
Name = st.text_input("Enter Name")
Age = st.number_input("Enter Age")
st.write(Name, Age)
st.date_input("Enter Date")

email = st.text_input("Enter email")
password = st.text_input("Enter password")
btn = st.button("Login Please")

if btn:
    if email == 'dadhich.grv@gmail.com' and password == '123':
        st.success("Login Successful")
        st.balloons()
    else:
        st.error("Login Fail")

# DropDown
gender = st.selectbox("Enter Gender",['M','F'])
st.write(gender)

# Upload file
file = st.file_uploader("Upload csv file")
if file is not None:
    df = pd.read_csv(file)
    st.dataframe(df.describe())


