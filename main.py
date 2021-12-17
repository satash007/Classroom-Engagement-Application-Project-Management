# Modules
import pyrebase
import streamlit as st
from datetime import datetime
from PIL import Image
import base64
import datetime
from datetime import datetime
import time

# Generates random strings
import secrets

# Load the fav icon image from the res folder in project
img = Image.open('res/videoconference2.png')

# Config function
st.set_page_config(page_title='Classroom Engagement Application', page_icon=img)

#Set background image
st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://github.com/satash007/Classroom-Engagement-Application-Project-Management/blob/main/res/bg_img_main.jpg?raw=true")
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Configuration Key
firebaseConfig = {
    'apiKey': "AIzaSyDm9i_Wbq737WWGapfpVVz27vu7mg3Tqhs",
    'authDomain': "classroomengagementapp.firebaseapp.com",
    'projectId': "classroomengagementapp",
    'databaseURL': "https://classroomengagementapp-default-rtdb.firebaseio.com/",
    'storageBucket': "classroomengagementapp.appspot.com",
    'messagingSenderId': "987739429861",
    'appId': "1:987739429861:web:1ade3cdf0749913f4b2d0c",
    'measurementId': "G-EHF9HLVEBZ"
}

# Minimalize the default features by hiding main menu and footer elements
hide_menu_style= """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide_menu_style, unsafe_allow_html=True)

#Modify default attributes for alert elements
st.markdown(
    """
    <style>
        .stAlert {
            background-color: white;
            opacity: 0.8;
        }
        .stAlert:hover {
        opacity: 1.0;
        }
    </style>""",
    unsafe_allow_html=True,
)

# Firebase Authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Database
db = firebase.database()
storage = firebase.storage()
st.sidebar.title("Welcome!")

st.sidebar.image(
    "res/CEA-Sidebar-Image-white-txt2.png",
    width=300
)

#Define the user types
user_types = ['Student', 'Host/Teacher']

user_type_choice = st.sidebar.radio('I would like to use this application as a...', user_types)

#st.sidebar.markdown("[![Foo](http://www.google.com.au/images/nav_logo7.png)](http://google.com.au/)")

if user_type_choice == 'Student':
    student_name = st.sidebar.text_input('Please enter your full name')
    student_ID = st.sidebar.text_input('Please enter your student ID')
    session_code = st.sidebar.text_input('Please enter the session code')
    connectBtn = st.sidebar.checkbox("Connect to Session")
    

    if 'firstConnect' not in st.session_state:
        st.session_state.firstConnect = 0

    if connectBtn:
        st.sidebar.success('Connected...Welcome '+ student_name + '!')
        #Set background image
        st.markdown(
            """
            <style>
            .reportview-container {
                background: url("https://github.com/satash007/Classroom-Engagement-Application-Project-Management/blob/main/res/bg_img_dark.jpg?raw=true")
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        all_sessions = db.child("Sessions").get()
        if all_sessions.val() is not None:    
            for sessions in reversed(all_sessions.each()):
                #st.write(Posts.key()) # Morty
                if sessions.val()["Session Code"] == session_code:
                    session_host_val = sessions.val()["Host"]
                    datetime_obj = datetime.strptime(sessions.val()["Session Date"], 
                                "%d/%m/%Y %H:%M:%S")
                    start_time_obj = datetime.strptime(sessions.val()["Session Time Start"], 
                                "%H:%M:%S")
                    end_time_obj = datetime.strptime(sessions.val()["Session Time End"], 
                                "%H:%M:%S")
                   
                    session_current_time = '-'
                    session_state = '-'
                    session_current_time_min = '-'
                   
                    if datetime.now().date() == datetime_obj.date():
                      
                        if  datetime.now().time().hour < start_time_obj.time().hour:
                            session_current_time = '-'
                            session_state = 'Not Started Yet'
                            session_duration_val = sessions.val()["Session Duration"]
                        elif datetime.now().time().hour > start_time_obj.time().hour and datetime.now().time().hour < end_time_obj.time().hour:
                            session_current_time = str(end_time_obj.time().hour - datetime.now().time().hour) + 'hr'
                            session_current_time_min = str(end_time_obj.time().minute - datetime.now().time().minute) + 'mins'
                            session_state = 'Active'
                            session_duration_val = sessions.val()["Session Duration"]
                        else:
                            session_current_time = '-'
                            session_state = 'Ended'
                            session_duration_val = sessions.val()["Session Duration"]

                    if datetime.now().date() > datetime_obj.date():
                        session_current_time = '-'
                        session_state = 'Ended'
                        session_duration_val = sessions.val()["Session Duration"]

                    if datetime.now().date() < datetime_obj.date():
                        session_current_time = '-'
                        session_state = 'Not Started Yet'
                        session_duration_val = sessions.val()["Session Duration"]


        # only display balloons animation once using Session State
        if st.session_state.firstConnect == 0:
            st.balloons()
            st.session_state.firstConnect += st.session_state.firstConnect + 1; 
        
        session_remaining_time2 = end_time_obj.time().hour - datetime.now().time().hour
        session_remaining_time = session_current_time + session_current_time_min
        st.title('Session('+ session_code + ') Information')
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Session State", session_state)
        col2.metric("Session Duration", session_duration_val)
        col3.metric("Remaining Time", str(session_remaining_time))
        col4.metric("Hosted By", 'John K.')

        st.markdown('<hr style="width:100%;text-align:left;margin:0; padding-top:0;">',unsafe_allow_html=True)
        my_bar = st.progress(0)
        for percent_complete in range(session_remaining_time2):
            time.sleep(0.1)
            my_bar.progress(percent_complete + 1)

        st.title("Hi " + student_name) 
        """## Share Your Impression""" 
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            feeling = st.radio('How are you feeling?',['😊Happy','🤔Confused', '😲Wowed', '😂Amused', '😞Sad', '🧐Inquisitive', '😠Angry'])
            btnClickShareImpression = st.button('Submit Impression')
            if btnClickShareImpression:
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")  
                        
                impression = {'Feeling' : feeling,
                        'Timestamp' : dt_string}  
                
                studentInfo = {
                'Student ID': student_ID,
                'Student Name': student_name,
                'Session Code': session_code,
                'Impression': impression
                }
                db.child("Students").push(studentInfo)
                st.balloons()

        with col2:
            if feeling == '😊Happy':
                st.markdown('<h3 style="color: white; padding: 0">I\'m feeling Happy</h3>',
                                unsafe_allow_html=True)
                st.image("https://media.giphy.com/media/QWvra259h4LCvdJnxP/giphy.gif", width=150)

            if feeling == '🤔Confused':
                st.markdown('<h3 style="color: white; padding: 0">I\'m feeling Confused</h3>',
                                unsafe_allow_html=True)
                st.image("https://media.giphy.com/media/USUIWSteF8DJoc5Snd/giphy.gif", width=150)
        
            if feeling == '😲Wowed':
                st.markdown('<h3 style="color: white; padding: 0">I\'m feeling Wowed</h3>',
                                unsafe_allow_html=True)
                st.image("https://media.giphy.com/media/WprjTWyCWtfbJ11WEM/giphy.gif", width=150)
            
            if feeling == '😂Amused':
                st.markdown('<h3 style="color: white; padding: 0">I\'m feeling Amused</h3>',
                                unsafe_allow_html=True)
                st.image("https://media.giphy.com/media/QX1vLPZxlUh1bzbgbq/giphy.gif", width=150)
        
            if feeling == '😞Sad':
                st.markdown('<h3 style="color: white; padding: 0">I\'m feeling Sad</h3>',
                                unsafe_allow_html=True)
                st.image("https://media.giphy.com/media/IzcFv6WJ4310bDeGjo/giphy.gif", width=150)
        
            if feeling == '🧐Inquisitive':
                st.markdown('<h3 style="color: white; padding: 0">I\'m feeling Inquisitive</h3>',
                                unsafe_allow_html=True)
                st.image("https://media.giphy.com/media/cOiuXv4agUAEa4EosP/giphy.gif", width=150)
        
            if feeling == '😠Angry':
                st.markdown('<h3 style="color: white; padding: 0">I\'m feeling Angry</h3>',
                                unsafe_allow_html=True)
                st.image("https://media.giphy.com/media/j5E5qvtLDTfmHbT84Y/giphy.gif", width=150)
        
        with col3:
            st.markdown('<h4 style="color: white; padding: 0">Impression Log:</h4>',
                                unsafe_allow_html=True)
            st.caption('Session Code: ' + session_code)

            all_impressions = db.child("Students").get()
            if all_impressions.val() is not None:    
                for Posts in reversed(all_impressions.each()):
                    #st.write(Posts.key()) # Morty
                    if Posts.val()["Session Code"] == session_code:
                        datetime_obj = datetime.strptime(Posts.val()["Impression"]["Timestamp"], 
                                 "%d/%m/%Y %H:%M:%S")
                        time = datetime_obj.time()
                        #print(time)
                        st.write('You were ' + Posts.val()["Impression"]["Feeling"] + ' at ', time, language = '')
    else:
        st.sidebar.info('Status: Not Connected.')        

elif user_type_choice == 'Host/Teacher':
    # Authentication
    choice = st.sidebar.selectbox('Please Login/Signup to continue...', ['Login', 'Sign Up'])

    # Obtain User Input for email and password
    email = st.sidebar.text_input('Please enter your email address')
    password = st.sidebar.text_input('Please enter your password',type = 'password')

    # Sign up Block
    if choice == 'Sign Up':
        name = st.sidebar.text_input('Please enter your full name')
        submit = st.sidebar.button('Create Host Account')

        if submit:
            user = auth.create_user_with_email_and_password(email, password)
            st.sidebar.success('Your account was created successfully!')
            st.balloons()
            # Sign in
            user = auth.sign_in_with_email_and_password(email, password)
            db.child("Hosts").child(user['localId']).child("fullName").set(name)
            db.child("Hosts").child(user['localId']).child("ID").set(user['localId'])
            host_name = db.child("Hosts").child(user['localId']).child("fullName").get().key() 
            st.title('Welcome ' + name + '!')
            st.info('Thank you for creating an account. To proceed, please login with the credentials chosen.')

    # Login Block
    if choice == 'Login':
        login = st.sidebar.checkbox('Login')
        if 'firstConnect' not in st.session_state:
            st.session_state.firstConnect = 0

        if login:
            user = auth.sign_in_with_email_and_password(email, password)
            #if user['localId'] is None:
                #st.sidebar.success('Incorrect login details entered. Please try again.')    
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            page = st.radio('Go to',['Home', 'Create Session', 'View Analytics', 'Settings'])
            host_name = db.child("Hosts").child(user['localId']).child("fullName").get().key() 
            st.sidebar.success('Connected...Welcome '+ email + '!')
            
            # only display balloons animation once using Session State
            if st.session_state.firstConnect == 0:
                st.balloons()
                st.session_state.firstConnect += st.session_state.firstConnect + 1; 
        
            #Set background image
            st.markdown(
                """
                <style>
                .reportview-container {
                    background: url("https://github.com/satash007/Classroom-Engagement-Application-Project-Management/blob/main/res/bg_img_dark.jpg?raw=true")
                }
                </style>
                """,
                unsafe_allow_html=True
            )   
        
    # SETTINGS PAGE 
            if page == 'Settings':  
                # CHECK FOR IMAGE
                nImage = db.child("Hosts").child(user['localId']).child("Image").get().val()    
                # IMAGE FOUND     
                if nImage is not None:
                    # We plan to store all our image under the child image
                    Image = db.child("Hosts").child(user['localId']).child("Image").get()
                    for img in Image.each():
                        img_choice = img.val()
                        #st.write(img_choice)
                    st.image(img_choice, width=300)
                    exp = st.expander('Change Bio and Image')  
                    # User plan to change profile picture  
                    with exp:
                        #newImgPath = st.text_input('Enter full path of your profile imgae')
                        newImgPath = st.file_uploader("Upload File",type=['png','jpg'])
                        upload_new = st.button('Upload')
                        if upload_new:
                            uid = user['localId']
                            fireb_upload = storage.child(uid).put(newImgPath.getvalue(),user['idToken'])
                            a_imgdata_url = storage.child(uid).get_url(fireb_upload['downloadTokens']) 
                            db.child("Hosts").child(user['localId']).child("Image").push(a_imgdata_url)
                            st.success('Success!') 
                # IF THERE IS NO IMAGE
                else:    
                    st.info("No profile picture yet")
                    #newImgPath = st.text_input('Enter full path of your profile image')
                    newImgPath = st.file_uploader("Upload File",type=['png','jpg'])
                    upload_new = st.button('Upload')
                    if upload_new:
                        uid = user['localId']
                        # Stored Initated Bucket in Firebase
                        fireb_upload = storage.child(uid).put(newImgPath.getvalue(),user['idToken'])
                        # Get the url for easy access
                        a_imgdata_url = storage.child(uid).get_url(fireb_upload['downloadTokens']) 
                        # Put it in our real time database
                        db.child("Hosts").child(user['localId']).child("Image").push(a_imgdata_url)
    
    
    # HOME PAGE
            elif page == 'Home':
                st.title('Hi ' + email + '!')
                col1, col2 = st.columns(2)
                # col for Profile picture
                with col1:
                    nImage = db.child("Hosts").child(user['localId']).child("Image").get().val()         
                    if nImage is not None:
                        val = db.child("Hosts").child(user['localId']).child("Image").get()
                        for img in val.each():
                            img_choice = img.val()
                        st.image(img_choice,use_column_width=True)
                    else:
                        st.image('res/videoconference2.png',use_column_width=True)
                        st.info("No profile picture set yet. Go to Settings and choose one!")

                # This coloumn for the post Display
                with col2:
                    all_posts = db.child("Hosts").child(user['localId']).child("Posts").get()
                    if all_posts.val() is not None:    
                        for Posts in reversed(all_posts.each()):
                                #st.write(Posts.key()) # Morty
                                st.code(Posts.val(),language = '') 
            elif page == 'Create Session':
                 # Create Session
                st.subheader('Create New Session')

                #randomly generate session code using the token hex method of the secrets library
                session_code = secrets.token_hex(nbytes=3).upper() 

                st.write('**Session Code:** ' + session_code + ' _(Randomly generated)_')
                with st.form(key='sessionForm', clear_on_submit=True):
                    session_name = st.text_input("Please enter a session name",max_chars = 100)
                    session_duration = st.selectbox('Choose Session Duration', ['1 Hour', '2 Hours', '3 Hours', '4 Hours'])
                    session_date = st.date_input('Session Date', datetime.now())
                    session_time_start = st.time_input('What time will this session begin?', datetime.now())
                    session_time_end = st.time_input('What time will this session end?')
                    #TODO
                    create_session = st.form_submit_button('Create Session')
                if create_session: 
                    
                    dt_string = session_date.strftime("%d/%m/%Y %H:%M:%S")
                    ts_string = session_time_start.strftime("%H:%M:%S")  
                    te_string = session_time_end.strftime("%H:%M:%S") 
                    host_name = db.child("Hosts").child(user['localId']).child("fullName").get().key() 
                    sessionInfo = {
                    'Session Code': session_code,
                    'Session Name': session_name,
                    'Session Duration': session_duration,

                    'Session Date': dt_string,
                    'Session Time Start': ts_string,
                    'Session Time End': te_string,
                    'Host' : host_name,
                    'Host Email': email
                    }
                    db.child("Sessions").push(sessionInfo)
                    #print(sessionInfo)
                    st.success('Session(' + session_code + ') Created Successfully!')  
                    st.balloons()

                
    # WORKPLACE FEED PAGE
            else:
                all_users = db.child("Students").get()
                res = []
                # Store all the users full name
                for username in all_users.each():
                    k = username.val()["Student Name"]
                    res.append(k)
                # Total users
                totalStudents = len(res)
                st.write('Total Students: '+ str(totalStudents)) 
                
                # Allow the user to choose which other user he/she wants to see 
                choice = st.selectbox('Students List',res)
                btnProfile = st.button('Show Profile')
                
                # Show the choosen Profile
                if btnProfile:
                    for username in all_users.each():
                        k = username.val()["Student Name"]
                        # 
                        if k == choice:
                            lid = username.val()["Student ID"]
                            
                            #username = db.child("Students")..child("fullName").get().val()             
                            
                            st.markdown(username, unsafe_allow_html=True)
                            
                            nImage = db.child("Students").child("Image").get().val()         
                            if nImage is not None:
                                val = db.child("Students").child("Image").get()  
                                for img in val.each():
                                    img_choice = img.val()
                                    st.image(img_choice)
                            else:
                                st.info("No profile picture yet. Go to Edit Profile and choose one!")
    
                            # All posts
                            all_posts = db.child("Students").child("Impression").get()
                            if all_posts.val() is not None:    
                                for Posts in reversed(all_posts.each()):
                                    st.code(Posts.val()["Feeling"],language = '')
        else:
            st.sidebar.info('Status: Not Connected.')       
