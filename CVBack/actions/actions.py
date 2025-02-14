from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import os
# from pyresparser import ResumeParser
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pickle
# import json
import pyrebase

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


class getBestCandidate:
    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer()
        self.tfidf_matrix = None
        self.candidate_skills = None

    def build_model(self, candidate_skills):
        self.candidate_skills = candidate_skills
        self._create_tfidf_matrix()

    def _create_tfidf_matrix(self):
        self.candidate_skills['Features'] = self.candidate_skills['Skills']
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.candidate_skills['Features'])

    def recommend_candidates(self, job_skills, num_recommendations=5):
        job_profile = self.tfidf_vectorizer.transform([job_skills])
        cosine_similarities = linear_kernel(job_profile, self.tfidf_matrix).flatten()
        self.candidate_skills['score'] = cosine_similarities
        recommended_candidates_profile = self.candidate_skills.sort_values(by='score', ascending=False).head(num_recommendations)
        # return recommended_candidates_profile[['name', 'Skills', 'score']]
        return recommended_candidates_profile[['name', 'score']]

    def save_model(self, file_path):
        with open(file_path, 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def load_model(cls, file_path):
        with open(file_path, 'rb') as file:
            return pickle.load(file)
        
# Candidates_data = pd.DataFrame({
#     'name': ['shehan', 'krishan', 'gayan', 'amal'],
#     'Skills': ['python, machine learning, data analysis', 'java, c++, software development', 'html, css, javascript, web development', 'machine learning, python, data engineering'],
# })


job_data_db={
    'Skills_Required': ['python', "machine" "learning", "data analysis"]
}
# cv_db = {
#     'shehan': 'Curriculum Vitae -Shehan Krishan.pdf', 
# }

# data = ResumeParser('Curriculum Vitae -Shehan Krishan.pdf').get_extracted_data()
# print(data['skills'])

applicant_data = pd.DataFrame(columns=['name', 'working_arrangement_type', 'device_check', 'working_experience', 'role_due','start_When'])


class get_cv_info(Action):
    def name(self) -> Text:
        return "get_cv_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        name = [e['value'] for e in entities if e['entity'] == 'name']
        applicant_data.loc[0, 'name'] = name[0]
        msg = f"Hello! {name[0]} Thank you for applying for  this position. I have a few questions to help us understand your preferences and suitability for the role. Let's get started!"
        dispatcher.utter_message(text=msg)
        return []
    
class working_arrangement(Action):
    def name(self) -> Text:
        return "working_arrangement"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        msg = f"Great! First, what is your preferred working arrangement? (Remote,Physical,Hybrid)"
        dispatcher.utter_message(text=msg)
        return []
    
class device_check(Action):
    def name(self) -> Text:
        return "device_check"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        text = tracker.latest_message['text']
        applicant_data.loc[0, 'working_arrangement_type'] = text
        msg = f"Noted! Next, do you have the necessary device to work efficiently in your preferred setup?"
        dispatcher.utter_message(text=msg)
        return []
    
class working_experience(Action):
    def name(self) -> Text:
        return "working_experience"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        text = tracker.latest_message['text']
        applicant_data.loc[0, 'device_check'] = text
        msg = f"Could you also tell me about your previous working experience?"
        dispatcher.utter_message(text=msg)
        return []

class role_due(Action):
    def name(self) -> Text:
        return "role_due"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        text = tracker.latest_message['text']
        applicant_data.loc[0, 'working_experience'] = text
        msg = f"That's excellent. Thank you for sharing. One more question: How long would you ideally like to stay in this role?(Less than 1 year,1-2 years,3-5 years,More than 5 years)"
        dispatcher.utter_message(text=msg)
        return []
    
class available_start_date(Action):
    def name(self) -> Text:
        return "available_start_date"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        text = tracker.latest_message['text']
        applicant_data.loc[0, 'role_due'] = text
        msg = f"Thank you for letting us know! Now, could you please tell us when you would be available to start if selected for this role?"
        dispatcher.utter_message(text=msg)
        return []

class get_start_When(Action):
    def name(self) -> Text:
        return "get_start_When"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        text = tracker.latest_message['text']
        print(text)
        applicant_data.loc[0, 'available_start_date'] = text
        msg = f"Okay! Thank you for your time. We will consider you, along with the other applicants, and let you know if we will be proceeding.Have a great day!"
        print(applicant_data)
        applicant_data.to_csv('applicant_data.csv', index=False)
        dispatcher.utter_message(text=msg)
        return []


class get_age(Action):
    def name(self) -> Text:
        return "get_age"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        age = [e['value'] for e in entities if e['entity'] == 'age']
        print(age)
        applicant_data.loc[0, 'age'] = age[0]
        msg = f"What do you do Currenty?"
        dispatcher.utter_message(text=msg)
        return []
    
class get_current_activity(Action):
    def name(self) -> Text:
        return "get_current_activity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        text = tracker.latest_message['text']
        print(text)
        applicant_data.loc[0, 'current_activity'] = text
        msg = f"Why do you want to leave your current job?"
        print(applicant_data)
        dispatcher.utter_message(text=msg)
        return []
    
class get_reason_leave(Action):
    def name(self) -> Text:
        return "get_reason_leave"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        text = tracker.latest_message['text']
        print(text)
        applicant_data.loc[0, 'reason_leave'] = text
        msg = f"Why are you interested in this position?"
        print(applicant_data)
        dispatcher.utter_message(text=msg)
        
        return []
    
class get_interest_in_position(Action):
    def name(self) -> Text:
        return "get_interest_in_position"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        text = tracker.latest_message['text']
        print(text)
        applicant_data.loc[0, 'interest_in_position'] = text
        msg = f"Thats Great ! So.. This job can involve writing code, testing, debugging, and collaborating with other team members to ensure the success of a project. It often requires strong problem-solving skills, proficiency in programming languages, and the ability to adapt to new technologies and frameworks."
        
        dispatcher.utter_message(text=msg)
        return []
    
# class get_start_When(Action):
#     def name(self) -> Text:
#         return "get_start_When"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         text = tracker.latest_message['text']
#         print(text)
#         applicant_data.loc[0, 'start_When'] = text
#         msg = f"Okay! Thank you for your time. We will consider you, along with the other applicants, and let you know if we will be proceeding.Have a great day!"
#         print(applicant_data)
#         applicant_data.to_csv('applicant_data.csv', index=False)
#         dispatcher.utter_message(text=msg)
#         return []


def getCandinatesData():
    df = pd.read_csv("applicant_data.csv")
    
    names = []
    skills_list = []
    # Loop through each name in the CSV file
    for name in df['name']:
        # Fetch skills from Firebase for the current name
        skills = db.child("Users").child(name).child("info").child("Skills").get().val()
        
        # Append name and skills to the lists
        names.append(name)
        skills_list.append(skills if skills else "No skills found")  # Handle case if skills are missing

    # Create the DataFrame with names and skills
    Candidates_data = pd.DataFrame({
        'name': names,
        'Skills': skills_list,
    })
    
    return Candidates_data


    
class give_best_candidates(Action):
    def name(self) -> Text:
        return "give_best_candidates"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        model = getBestCandidate()
        
        Candidates_data = getCandinatesData()
        model.build_model(Candidates_data)

        # Sample job skills
        job_skills = "java ,software development, database management"

        # Get recommendations
        recommendations = model.recommend_candidates(job_skills)
        print("Recommended Jobs:")
        print(recommendations)
        
        msg = f"{recommendations}"
        dispatcher.utter_message(text=msg)
        return []

userName = "amal"
import re

class get_selectted_candidate(Action):
    def name(self) -> Text:
        return "get_selectted_candidate"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global userName
        entities = tracker.latest_message['entities']
        df = pd.read_csv("applicant_data.csv")
        name = [e['value'] for e in entities if e['entity'] == 'name']
        print(f"name is : {name}")
        user_row = df[df['name'] == name[0]]
        user_row_current_activity = user_row['working_experience'].values[0]
        role_pattern = re.compile(r'(as|working as|employed as|role of|position of)\s+(an?\s+)?([A-Za-z\s]+?)(?=\s+for|,|$)', re.IGNORECASE)
        # experience_pattern = re.compile(r'for\s+(\d+)\s+(years?|months?)', re.IGNORECASE)
        experience_pattern = re.compile(r'(\d+)\s+(years?|months?)', re.IGNORECASE)
        role_match = role_pattern.search(user_row_current_activity)
        role = role_match.group(3) if role_match else "unknown role"
        experience_match = experience_pattern.search(user_row_current_activity)
        if experience_match:
            duration = experience_match.group(1) + " " + experience_match.group(2)
        else:
            duration = "unknown duration"
            
        role = role.strip(), 
        experience = duration.strip()
        
        user_device_check = user_row['device_check'].values[0]
        
        devise = ""
        if "yes" in user_device_check:
            devise = "he is comfortable using his own devices."
        else:
            devise =  "he might need devices."
        
        # applicant_data.loc[0, 'name'] = name[0]
        userName = name[0] 
        msg = f"{userName} has {experience} of experience in {role}. {devise}"
        dispatcher.utter_message(text=msg)
        return []

class give_reason_role(Action):
    def name(self) -> Text:
        return "give_reason_role"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global userName
        df = pd.read_csv("applicant_data.csv")
        
        name = tracker.get_slot("callname")
        print("slotNAme")
        print(name)
        
        user_row = df[df['name'] == userName]
        user_row_current_activity = user_row['role_due'].values[0]

        msg = f"indicated that he would ideally like to stay in this role for {user_row_current_activity}."
        dispatcher.utter_message(text=msg)
        return []

class give_candidate_current_activity(Action):
    def name(self) -> Text:
        return "give_candidate_current_activity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global userName
        df = pd.read_csv("applicant_data.csv")
        
        name = tracker.get_slot("callname")
        print("slotNAme")
        print(name)
        
        user_row = df[df['name'] == userName]
        user_row_current_activity = user_row['current_activity'].values[0]

        msg = f"This is what he said : {user_row_current_activity}"
        dispatcher.utter_message(text=msg)
        return []

class give_candidate_reason_to_leave(Action):
    def name(self) -> Text:
        return "give_candidate_reason_to_leave"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global userName
        df = pd.read_csv("applicant_data.csv")
        
        name = tracker.get_slot("callname")
        print("slotNAme")
        print(name)
        
        user_row = df[df['name'] == userName]
        user_row_reason_leave = user_row['reason_leave'].values[0]

        msg = f"This is what he said : {user_row_reason_leave}"
        dispatcher.utter_message(text=msg)
        return []

class give_candidate_interest_in_position(Action):
    def name(self) -> Text:
        return "give_candidate_interest_in_position"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global userName
        df = pd.read_csv("applicant_data.csv")
        
        name = tracker.get_slot("callname")
        print("slotNAme")
        print(name)
        
        user_row = df[df['name'] == userName]
        user_row_interest_in_position = user_row['interest_in_position'].values[0]

        msg = f"This is what he said : {user_row_interest_in_position}"
        dispatcher.utter_message(text=msg)
        return []
    
class give_candidate_start_job(Action):
    def name(self) -> Text:
        return "give_candidate_start_job"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global userName
        df = pd.read_csv("applicant_data.csv")
        
        name = tracker.get_slot("callname")
        print("slotNAme")
        print(name)
        
        user_row = df[df['name'] == userName]
        user_row_start_When = user_row['start_When'].values[0]

        msg = f"This is what he said : {user_row_start_When}"
        dispatcher.utter_message(text=msg)
        return []

#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


