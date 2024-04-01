import streamlit as st
import re
import sqlite3
import pandas as pd
import pickle
import bz2
st.set_page_config(page_title="instgram spammer",page_icon="fevicon.jpg",layout="centered",initial_sidebar_state="auto",menu_items=None)
def set_bg_hack_url():
     '''
     A function to unpack an image from url and set as bg.
     Returns
     -------
     The background.
     '''
        
     st.markdown(
           f"""
           <style>
          .stApp {{
              background: url("https://images.rawpixel.com/image_800/cHJpdmF0ZS9sci9pbWFnZXMvd2Vic2l0ZS8yMDIyLTA1L3Y1NDZiYXRjaDMtbXludC0zMS1iYWRnZXdhdGVyY29sb3JfMS5qcGc.jpg");
              background-size: cover
          }}
          </style>
          """,
          unsafe_allow_html=True
      )
set_bg_hack_url()

conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(FirstName TEXT,LastName TEXT,Mobile TEXT,City TEXT,Email TEXT,password TEXT,Cpassword TEXT)')
def add_userdata(FirstName,LastName,Mobile,City,Email,password,Cpassword):
    c.execute('INSERT INTO userstable(FirstName,LastName,Mobile,City,Email,password,Cpassword) VALUES (?,?,?,?,?,?,?)',(FirstName,LastName,Mobile,City,Email,password,Cpassword))
    conn.commit()
def login_user(Email,password):
    c.execute('SELECT * FROM userstable WHERE Email =? AND password = ?',(Email,password))
    data = c.fetchall()
    return data
def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data



menu = ["Home","Login","SignUp","Contact us"]
choice = st.sidebar.selectbox("Menu",menu)


if choice=="Home":
    st.markdown(
        """
        <h2 style="color:black">Welcome To Website</h2>
        <h1>    </h1>
        <p align="justify">
        <b style="color:black">This project introduces a Python-based web application designed for classifying fake Instagram accounts. The increasing prevalence of fraudulent accounts on social media platforms poses a significant threat to user privacy and security. Leveraging machine learning techniques, the web app employs a trained model to analyze various features associated with Instagram profiles and determine the likelihood of an account being fake.</b>
        </p>
        """
        ,unsafe_allow_html=True)
if choice=="SignUp":
        Fname = st.text_input("First Name")
        Lname = st.text_input("Last Name")
        Mname = st.text_input("Mobile Number")
        Email = st.text_input("Email")
        City = st.text_input("City")
        Password = st.text_input("Password",type="password")
        CPassword = st.text_input("Confirm Password",type="password")
        b2=st.button("SignUp")
        if b2:
            pattern=re.compile("(0|91)?[7-9][0-9]{9}")
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if Password==CPassword:
                if (pattern.match(Mname)):
                    if re.fullmatch(regex, Email):
                        create_usertable()
                        add_userdata(Fname,Lname,Mname,City,Email,Password,CPassword)
                        st.success("SignUp Success")
                        st.info("Go to Logic Section for Login")
                    else:
                        st.warning("Not Valid Email")         
                else:
                    st.warning("Not Valid Mobile Number")
            else:
                st.warning("Pass Does Not Match")
if choice=="Login":
    Email = st.sidebar.text_input("Email")
    Password = st.sidebar.text_input("Password",type="password")
    b1=st.sidebar.checkbox("Login")
    
   
    if b1:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, Email):
            result = login_user(Email,Password)
            if result:
                if Email=="a@a.com":
                   st.success("Logged In as {}".format(Email))
                   user_result = view_all_users()
                   clean_db = pd.DataFrame(user_result,columns=["FirstName","LastName","Mobile","City","Email","password","Cpassword"])
                   st.dataframe(clean_db)
                else:
                    st.success("Logged In as {}".format(Email))
                    menu2 = ["SVM","K-Nearest Neighbors", "Naive Bayes",
                             "Decision Tree", "Random Forest",
                             "ExtraTreesClassifier"]
                    choice2 = st.selectbox("Select ML",menu2)

                    edge_followed_by=float(st.slider('edge_followed_by', 0, 1000))
                    edge_follow=float(st.slider('edge_follow', 0,1000))
                    username_length=int(st.slider('username_length', 0,15))
                    username_has_number=int(st.slider('username_has_number', 0,1))
                    full_name_has_number=int(st.slider('full_name_has_number', 0,1))
                    full_name_length=int(st.slider('full_name_length', 0,1))
                    is_private=int(st.slider('is_private', 0,1))
                    is_joined_recently=int(st.slider('is_joined_recently', 0,1))
                    has_channel=int(st.slider('has_channel', 0,1))
                    is_business_account=int(st.slider('is_business_account', 0,1))
                    has_guides=int(st.slider('has_guides', 0,1))
                    has_external_url=int(st.slider('has_external_url', 0,1))
                    my_array=[edge_followed_by,edge_follow,username_length,username_has_number,
                              full_name_has_number,full_name_length,is_private,
                              is_joined_recently,has_channel,is_business_account,
                              has_guides,has_external_url] 
                    b2=st.button("Predict")
                    model=pickle.load(open("models.pkl",'rb'))
                    if b2:  
                        tdata=[my_array]
                       
                        #st.write(tdata)
                        if choice2=="K-Nearest Neighbors":
                            test_prediction = model[0].predict(tdata)
                            query=test_prediction[0]
                            #st.success(query)
                        if choice2=="SVM":
                            test_prediction = model[1].predict(tdata)
                            query=test_prediction[0]
                            #st.success(query)                 
                        if choice2=="Decision Tree": 
                            test_prediction = model[2].predict(tdata)
                            query=test_prediction[0]
                            #st.success(query)
                        if choice2=="Random Forest":
                            test_prediction = model[3].predict(tdata)
                            query=test_prediction[0]
                            #st.success(query)
                        if choice2=="Naive Bayes":
                            test_prediction = model[4].predict(tdata)
                            query=test_prediction[0]
                            #st.success(query)
                        if choice2=="ExtraTreesClassifier":
                            test_prediction = model[5].predict(tdata)
                            query=test_prediction[0]
                            #st.success(query)
                        if str(query)=="1":
                            st.error("Fake User")
                        else:
                            st.success("Real User")
                            
                            
                            
                    
            else:
                st.warning("Incorrect Email/Password")
        else:
            st.warning("Not Valid Email")    

if choice=="Contact us":
    st.text("NAME-HETVI SHAH")
    st.text("MOBILE NO.-7016694557")
    
