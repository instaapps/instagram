import streamlit as st
import re
import sqlite3
import pandas as pd

conn = sqlite3.connect('instadata.db')
c = conn.cursor()
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(FirstName TEXT,LastName TEXT,Mobile TEXT,City TEXT,email TEXT,Password TEXT,Cpassword TEXT)')
def add_userdata(FirstName,LastName,Mobile,City,email,Password,Cpassword):
    c.execute('INSERT INTO userstable(FirstName,LastName,Mobile,City,email,Password,Cpassword) VALUES (?,?,?,?,?,?,?)',(FirstName,LastName,Mobile,City,email,Password,Cpassword))
    conn.commit()
def login_user(email,Password):
    c.execute('SELECT * FROM userstable WHERE email =? AND Password = ?',(email,Password))
    data = c.fetchall()
    return data
def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data
def delete_user(Email):
    c.execute("DELETE FROM userstable WHERE Email="+"'"+Email+"'")
    conn.commit()

choice = st.sidebar.selectbox("home page:",
                     ['Home','Signup','Login','Contact us'])

if choice == 'Home':
    st.title("Instagram Fack Account")
    st.text("Implemented advanced content analysis for improved detection of fake Instagram accounts.")
if choice == 'Signup':
    FirstName = st.text_input("FIRST NAME")
    LastName = st.text_input("LAST NAME")
    Mobile = st.text_input("MOBILE NUMBER")
    City = st.text_input("City")
    email = st.text_input("EMAIL")
    Password = st.text_input("PASSWORD",type="password")
    Cpassword = st.text_input("CONFIRM PASSWORD",type="password")
    b2 = st.button('Signup')
    if b2:
        pattern=re.compile("(0|91)?[7-9][0-9]{9}")
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if Password==Cpassword:
            if (pattern.match(Mobile)):
                if re.fullmatch(regex, email):
                    create_usertable()
                    add_userdata(FirstName,LastName,Mobile,City,email,Password,Cpassword)
                    st.success("SignUp Success")
                    st.info("Go to Logic Section for Login")
                else:
                    st.warning("Not Valid Email")         
            else:
                st.warning("Not Valid Mobile Number")
        else:
            st.warning("Pass Does Not Match")
if choice == 'Login':
    email=st.sidebar.text_input("EMAIL")
    Password=st.sidebar.text_input("PASSWORD",type="password")
    if st.sidebar.checkbox('login'):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, email):
            result = login_user(email,Password)
            if result:
                if email== 'a@a.co':
                    st.success("Logged In as {}".format(email))
                    demail=st.text_input("Enter Delete EMAIL")
                    if st.button("Delete"):
                        delete_user(demail)
                    user_result = view_all_users()
                    clean_db = pd.DataFrame(user_result,columns=["FirstName","LastName","Mobile","City","Email","Password","Cpassword"])
                    st.dataframe(clean_db)
                else:
                    st.success("Logged In as {}".format(email))
                    choice3 = st.selectbox("Select ML:",
                                         ["SVM","NB","KNN","DT","RF","ET"])
                    
                    import pickle
                    model=pickle.load(open("model_instagram.pkl","rb"))
                    efb=float(st.slider("Enter edge_followed_by=",0.005))
                    ef=float(st.slider("Enter edge_follow =",0.999,0.001))
                    ul=(st.slider("Enter username_length =",1,19))
                    uhn = (st.selectbox("Enter username_has_number:",
                                         ['Yes','No']))
                    if uhn == 'Yes':
                        uhn=0
                    else:
                        uhn = 1
                
                    fnhn= (st.selectbox("Enter full_name_has_number:",
                                         ['Yes','No']))
                    if fnhn == 'Yes':
                        fnhn=0
                    else:
                        fnhn = 1
                    fnl=float(st.slider("Enter full_name_length=",0,19))
                    
                    ip= (st.selectbox("Enter is_private:",
                                         ['Yes','No']))
                    if ip == 'Yes':
                        ip=0
                    else:
                        ip = 1
                 
                    ijr= (st.selectbox("Enter is_joined_recently:",
                                         ['Yes','No']))
                    if ijr == 'Yes':
                        ijr=0
                    else:
                        ijr = 1
                    
                    iba= (st.selectbox("Enter is_business_account:",
                                         ['Yes','No']))
                    if iba == 'Yes':
                        iba=0
                    else:
                        iba = 1
                    
                    heu= (st.selectbox("Enter has_external_url:",
                                         ['Yes','No']))
                    if heu == 'Yes':
                        heu=0
                    else:
                        heu = 1
                    if st.button('Predict'):
                        if choice3=="SVM":
                            PE = model[0].predict([[efb,ef,ul,uhn,fnhn,fnl,ip,ijr,iba,heu]])[0]
                        if choice3=="NB":
                            PE = model[1].predict([[efb,ef,ul,uhn,fnhn,fnl,ip,ijr,iba,heu]])[0]
                        if choice3=="KNN":
                           PE =  model[2].predict([[efb,ef,ul,uhn,fnhn,fnl,ip,ijr,iba,heu]])[0]
                        if choice3=="DT":
                            PE = model[3].predict([[efb,ef,ul,uhn,fnhn,fnl,ip,ijr,iba,heu]])[0]
                        if choice3=="RF":
                            PE = model[4].predict([[efb,ef,ul,uhn,fnhn,fnl,ip,ijr,iba,heu]])[0]
                        if choice3=="ET":
                            PE = model[5].predict([[efb,ef,ul,uhn,fnhn,fnl,ip,ijr,iba,heu]])[0]
                        #st.write(PE)
                        if(str(PE)=="1"):
                                    st.success('Yes')
                        else:
                                    st.warning('No')
            else:
                st.warning("Incorrect Email/Password")
        else:
            st.warning("Not Valid Email")       
if choice == 'Contact us':
    st.text("NAME:- HETVI SHAH")
    st.text("EMAIL ID:- hetvishah3412@gmail.com")
    st.text("ADDRESS:- Manjalpur,VADODARA")
    
