# Modules
import pyrebase
import streamlit as st
from datetime import datetime
from PIL import Image

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
    connectBtn = st.sidebar.button("Connect to Session")

elif user_type_choice == 'Host/Teacher':
    # Authentication
    choice = st.sidebar.selectbox('Please Login/Signup to continue...', ['Login', 'Sign Up'])

    # Obtain User Input for email and password
    email = st.sidebar.text_input('Please enter your email address')
    password = st.sidebar.text_input('Please enter your password',type = 'password')

    # Sign up Block
    if choice == 'Sign Up':
        handle = st.sidebar.text_input('Please enter your full name')
        submit = st.sidebar.button('Create Host Account')

        if submit:
            user = auth.create_user_with_email_and_password(email, password)
            st.sidebar.success('Your account is created successfully!')
            st.balloons()
            # Sign in
            user = auth.sign_in_with_email_and_password(email, password)
            db.child(user['localId']).child("Handle").set(handle)
            db.child(user['localId']).child("ID").set(user['localId'])
            st.title('Welcome ' + handle + '!')
            st.info('Login via login drop down selection')

    # Login Block
    if choice == 'Login':
        login = st.sidebar.checkbox('Login')
        if login:
            user = auth.sign_in_with_email_and_password(email, password)
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            bio = st.radio('Jump to',['Home','Workplace Feeds', 'Settings'])
            st.sidebar.success('Successfully authenticated...Welcome '+ email + '!')
            st.balloons()
            
    # SETTINGS PAGE 
            if bio == 'Settings':  
                # CHECK FOR IMAGE
                nImage = db.child(user['localId']).child("Image").get().val()    
                # IMAGE FOUND     
                if nImage is not None:
                    # We plan to store all our image under the child image
                    Image = db.child(user['localId']).child("Image").get()
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
                            db.child(user['localId']).child("Image").push(a_imgdata_url)
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
                        db.child(user['localId']).child("Image").push(a_imgdata_url)
    
    
    # HOME PAGE
            elif bio == 'Home':
                col1, col2 = st.columns(2)
                
                # col for Profile picture
                with col1:
                    nImage = db.child(user['localId']).child("Image").get().val()         
                    if nImage is not None:
                        val = db.child(user['localId']).child("Image").get()
                        for img in val.each():
                            img_choice = img.val()
                        st.image(img_choice,use_column_width=True)
                    else:
                        st.info("No profile picture yet. Go to Edit Profile and choose one!")
                    
                    post = st.text_input("Let's share my current mood as a post!",max_chars = 100)
                    add_post = st.button('Share Posts')
                if add_post:   
                    now = datetime.now()
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")              
                    post = {'Post:' : post,
                            'Timestamp' : dt_string}                           
                    results = db.child(user['localId']).child("Posts").push(post)
                    st.balloons()

                # This coloumn for the post Display
                with col2:
                    
                    all_posts = db.child(user['localId']).child("Posts").get()
                    if all_posts.val() is not None:    
                        for Posts in reversed(all_posts.each()):
                                #st.write(Posts.key()) # Morty
                                st.code(Posts.val(),language = '') 
    # WORKPLACE FEED PAGE
            else:
                all_users = db.get()
                res = []
                # Store all the users handle name
                for users_handle in all_users.each():
                    k = users_handle.val()["Handle"]
                    res.append(k)
                # Total users
                nl = len(res)
                st.write('Total users here: '+ str(nl)) 
                
                # Allow the user to choose which other user he/she wants to see 
                choice = st.selectbox('My Collegues',res)
                push = st.button('Show Profile')
                
                # Show the choosen Profile
                if push:
                    for users_handle in all_users.each():
                        k = users_handle.val()["Handle"]
                        # 
                        if k == choice:
                            lid = users_handle.val()["ID"]
                            
                            handlename = db.child(lid).child("Handle").get().val()             
                            
                            st.markdown(handlename, unsafe_allow_html=True)
                            
                            nImage = db.child(lid).child("Image").get().val()         
                            if nImage is not None:
                                val = db.child(lid).child("Image").get()
                                for img in val.each():
                                    img_choice = img.val()
                                    st.image(img_choice)
                            else:
                                st.info("No profile picture yet. Go to Edit Profile and choose one!")
    
                            # All posts
                            all_posts = db.child(lid).child("Posts").get()
                            if all_posts.val() is not None:    
                                for Posts in reversed(all_posts.each()):
                                    st.code(Posts.val(),language = '')

