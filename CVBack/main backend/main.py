from fastapi.middleware.cors import CORSMiddleware
import requests
from fastapi import FastAPI, File, UploadFile ,Query,Form
from pydantic import BaseModel
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io
import spacy
import re
from typing import List, Dict, Optional
import pyrebase
import json
from datetime import datetime
import joblib
# Load spaCy model
nlp = spacy.load('en_core_web_sm')


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"], 
    allow_headers=["*"], 
    allow_credentials=True,
)

firebaseConfig = {
  "apiKey": "AIzaSyAWDV1ewlU5Je_BXLAyYMP2haBc-_MGx7k",
  "authDomain": "jobseeker-34ae4.firebaseapp.com",
  "databaseURL": "https://jobseeker-34ae4-default-rtdb.firebaseio.com",
  "projectId": "jobseeker-34ae4",
  "storageBucket": "jobseeker-34ae4.appspot.com",
  "messagingSenderId": "664053320393",
  "appId": "1:664053320393:web:6b8d7685ab616b92ca1b18",
  "measurementId": "G-R676D6RNT5"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
auth = firebase.auth()


class jobDetail(BaseModel):
    user:str
    title:str
    skils:str
    description:str
    location:str

@app.post('/addJob')
def addJob(jobDetails:jobDetail):
    current_time = datetime.now().isoformat()
    data = {
        "user":jobDetails.user,
        "title": jobDetails.title,
        "skils":jobDetails.skils,
        "description":jobDetails.description,
        "location":jobDetails.location,
        "date_time": current_time
        }
    db.child("Jobs").child("jobPost").push(data)

    return {"status":"Uploaded"}


class jobUserDetail(BaseModel):
    user:str

@app.post('/getUserJobPosts')
def getUserJobs(userDetails:jobUserDetail):
    # Query to filter by user
    jobs = db.child("Jobs").child("jobPost").order_by_child("user").equal_to(userDetails.user).get()
    
    if jobs.each() is None:
        return {"status": "No jobs found for the user"}
    
    user_jobs = []
    for job in jobs.each():
        user_jobs.append(job.val())

    return {"status": "success", "data": user_jobs}


class userDetails(BaseModel):
    username: str

@app.post("/user_recomdation_jobs")
def user_recomdation_jobs(userData: userDetails):
    prefer_job_title = db.child("Users").child(userData.username).child("info").child("prefer_job_title").get().val()
    Skills = db.child("Users").child(userData.username).child("info").child("Skills").get().val()
    output_list = Skills.split(',')
    # Transform skills to features
    skills_features = vectorizer.transform([' '.join(output_list)])

    # Predict job title
    predicted_title = rf.predict(skills_features)
    print("predicted_title")
    print(predicted_title)

    return {"prefer_job_title":prefer_job_title,"predicted_title":predicted_title[0]}

@app.post('/getUserData')
def getUserData(userData: userDetails):
    user = db.child("Users").child(userData.username).child("info").get().val()
    return {"userData":user}

class userSelecttedJob(BaseModel):
    username: str
    jobName: str

@app.post('/apply_job')
def apply_job(ujdata: userSelecttedJob):
    selectted_job = db.child("Jobs").child("jobPost").order_by_child("title").equal_to(ujdata.jobName).get().val()
    # Extract the first item from the OrderedDict
    first_key, first_job = next(iter(selectted_job.items()))
    # Get the candidates from the job data
    candidates = first_job['candinates']
    candidates.append(ujdata.username)
    db.child("Jobs").child("jobPost").child(first_key).update({"candinates": candidates})
    return {"update":"update"}

@app.post('/getAllJobs')
def getAllJobs():
    jobs = db.child("Jobs").child("jobPost").get()
    
    if jobs.each() is None:
        return {"status": "No jobs found"}
    
    all_jobs = []
    for job in jobs.each():
        all_jobs.append(job.val())
        
    print(all_jobs)

    return {"status": "success", "data": all_jobs}

class UserLogin(BaseModel):
    email: str
    password: str

@app.post("/login")
def login_user(userData: UserLogin):
    print(userData);
    try:
        user = auth.sign_in_with_email_and_password(userData.email, userData.password)
        print(f"Login successful. User ID: {user['localId']}")
        if user:
            print(user['displayName'])
            userType = db.child("Users").child(user['displayName']).child("info").child("user_type").get().val()
            return {"userdata":user['displayName'],"userType":userType}
        else:
            print("no user")
    except Exception as e:
        print(f"Login failed: {e}")
        return {"userdata":"error"}
    
class UserRegister(BaseModel):
    email: str
    username:str
    password: str
    prefer_job_title: str
    Skills: str
    user_type:str

@app.post("/register")
def register_user(userData:UserRegister):
    print(userData.email, userData.password,userData.username)
    try:
        user1 = auth.create_user_with_email_and_password(userData.email, userData.password)
        # check this
        user1= auth.update_profile(display_name=userData.username,id_token=user1['idToken'])
        data = {"prefer_job_title": userData.prefer_job_title,"Skills":userData.Skills,"user_type":userData.user_type}
        db.child("Users").child(user1['displayName']).child("info").set(data)

        if user1:
            print(user1['displayName'])
            userType = db.child("Users").child(user1['displayName']).child("info").child("user_type").get().val()
            return {"userdata":user1['displayName'],"newUser":"1","userType":userType}
        else:
            print("no user")
    except Exception as e:
        print(f"Registration failed: {e}")

# Define the request body schema
class InputData(BaseModel):
    text: str
    user: str

@app.post("/process-message/")
async def process_message(input_data: InputData):
    # Make a POST request to the Rasa webhook
    rasa_response = requests.post('http://localhost:5005/webhooks/rest/webhook', 
                                  json={"sender": input_data.user, "message": input_data.text})
    
    # Extract the bot response from Rasa
    bot_messages = [i['text'] for i in rasa_response.json()]
    
    return {"bot_responses": bot_messages}


# Define a model for the response
class ExtractedData(BaseModel):
    names: List[str]
    roles: List[str]
    nic_numbers: List[str]
    ofz: List[str]
    date_ranges: List[str]
    validation: Optional[Dict[str, str]]


def extract_text_from_pdf(pdf_file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, codec='utf-8', laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    
    pdf_text = ""
    with pdf_file as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
            pdf_text += fake_file_handle.getvalue()
    
    converter.close()
    fake_file_handle.close()
    
    return pdf_text

def change_month_to_number(text):
    month_dict = {
        'JANUARY': '01',
        'FEBRUARY': '02',
        'MARCH': '03',
        'APRIL': '04',
        'MAY': '05',
        'JUNE': '06',
        'JULY': '07',
        'AUGUST': '08',
        'SEPTEMBER': '09',
        'OCTOBER': '10',
        'NOVEMBER': '11',
        'DECEMBER': '12'
    }
    for month, value in month_dict.items():
        text = re.sub(r'\b{}\b'.format(month), value, text.upper())
    return text

def extract_data_from_text(text,ofz_term):
    tt = change_month_to_number(text)
    tt = re.sub(r'(\d{2})(?:ST|ND|RD|TH) (\d{2}) (\d{4})', r'\1 \2 \3', tt)
    tt = re.sub(r'\.', ' ', tt)
    
    names = [ent.text for ent in nlp(text).ents if ent.label_ == "PERSON"]
    
    roles = re.findall(r'\b(?:Production Associator|Manager Administration|Developer|Analyst|Engineer|Ml Engineer|Software Engineer)\b', text)
    
    nic_pattern = r'\bNIC\s*(\d{9,12}[A-Z]?)\b|\b(\d{9,12}[A-Z]?)\s*NIC\b'
    matches = re.findall(nic_pattern, text)
    nic_numbers = [match[0] or match[1] for match in matches]
    
    # ofz_pattern = r'\b(?:Sadisa Management & Technologies)\b'
    # ofz = re.findall(ofz_pattern, text)

    # Extract "ofz" specific term
    ofz_pattern = r'\b(?:{})\b'.format(re.escape(ofz_term))
    ofz = re.findall(ofz_pattern, text)

    # Extract date ranges
    lines = tt.split("\n")
    date_ranges = []
    for line in lines:
        if " TO " in line:
            dates = re.findall(r'\b\d{2} \d{2} \d{4}\b', line)
            if dates and len(dates) == 2:
                date_ranges.append(f"Date range: {dates[0]} to {dates[1]}")
    
    return {
        "names": names,
        "roles": roles,
        "nic_numbers": nic_numbers,
        "ofz": ofz,
        "date_ranges": date_ranges
    }

class ValidationInput(BaseModel):
    names: str
    roles: str
    nic_numbers: str
    date_ranges: str


def parse_date_range(date_range_str):
    start_str, end_str = date_range_str.split(' to ')
    start_date = datetime.strptime(start_str.strip(), '%d %m %Y')
    end_date = datetime.strptime(end_str.strip(), '%d %m %Y')
    return start_date, end_date


@app.post("/extract-data/")
async def extract_data(
    pdf_file: UploadFile = File(...),
    # ofz_term: str = Query(...),
    validation_input: str = Form(...), 
):
    print(validation_input)
    validation_input = json.loads(validation_input)
    pdf_text = extract_text_from_pdf(pdf_file.file)
    extracted_data = extract_data_from_text(pdf_text, "ofz_term")
    print(extracted_data)
    
    # Perform validation
    validations = {
        "Name" : "Invalid",
        "Role" : "Invalid",
        "Nic Number" : "Invalid",
        "Date Range": "Invalid"
    }
    print("xd")
    # Check if the validation_input name is in the extracted_data names
    if any(name in extracted_data['names'] for name in validation_input['names']):
        print("Valid")
        validations["Name"] = "Valid"
    if any(nic in extracted_data['roles'] for nic in validation_input['roles']):
        print("Valid")
        validations["Role"] = "Valid"
    if any(nic in extracted_data['nic_numbers'] for nic in validation_input['nic_numbers']):
        print("Valid")
        validations["Nic Number"] = "Valid"

    # Parse validation_input date range
    val_start, val_end = parse_date_range(validation_input['date_ranges'][0])

    # Check if the validation_input date range is found in any extracted_data date ranges
    for range_str in extracted_data['date_ranges']:
        # Extract date range from the string (removing 'Date range:' prefix)
        extracted_range = range_str.replace('Date range:', '').strip()
        ext_start, ext_end = parse_date_range(extracted_range)
        
        # Check for overlap or exact match
        if val_start <= ext_end and val_end >= ext_start:
            validations["Date Range"] = "Valid"
            break
    
    if all(status == "Valid" for status in validations.values()):
        return {"validation": validations, "status": "accepted"}
    else:
        return {"validation": validations, "status": "rejected"}

# Load the model and vectorizer
rf = joblib.load('random_forest_model.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')

class Skills(BaseModel):
    skills: list[str]

@app.post("/predict_job")
def predict_job_title(skills: Skills):
    try:
        # Transform skills to features
        skills_features = vectorizer.transform([' '.join(skills.skills)])

        # Predict job title
        predicted_title = rf.predict(skills_features)
        
        return {"recommended_job_title": predicted_title[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
