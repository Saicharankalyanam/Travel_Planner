import streamlit as st
import google.generativeai as genai

import os

image_path = r"C:\Users\saich\streamlit\envi\travel_image1.jpg"
st.image(image_path)
st.title('🤖SmartTrip AI: Plan, Pack & Go!🌍 ')
# st.write('Enter your Trip details :')


#logic-1 
from langchain_core.prompts import ChatPromptTemplate

prompt_template = ChatPromptTemplate.from_messages([
                                              ('system','''you are helpful AI Assist which guide trip of National trips & International trips and who gives approximate the cost of ticket options based on mode of transport 
                                               & helpful Travel guide who suggests best places to visit by day wise with expertise in travel details, destinations & trip planner
                                               by considering travel style (Budget, Comfortable & Expensive ), type of passangers(Kids, Famliy vacation, couple) and gives the total cost of trip
                                               also suggest if any other trip based on mentioned dates & details on sesional tourism'''),
                                              ('human','Book a ticket from {Source} to {Destination}, Mode of transport{Transportation_Options}, travel style {travel_style} for number of {Passengers}, Time{Date}')])

#logic-2
#choosing a best model for step-2
# import google.generativeai as genai
# genai.configure(api_key="AIzaSyBhTcKEi5DmBT4SQoBR9-hpW7f7VcL5yqg")

#step-1 : importing google genAI chat model
from langchain_google_genai import ChatGoogleGenerativeAI

#step-2 : setting google API to the model  
# chat_model = ChatGoogleGenerativeAI(model = 'models/gemini-1.5-pro-latest',google_api_key='')

with open("google_api.txt", "r") as file:
    # Read the entire content of the file
    GOOGLE_API_KEY = file.read().strip()

# Set up Google GenAI Chat Model
if GOOGLE_API_KEY:
    chat_model = ChatGoogleGenerativeAI(model='models/gemini-1.5-pro-latest', google_api_key=GOOGLE_API_KEY)
else:
    st.error("❌ API Key Missing! Set GOOGLE_API_KEY in Hugging Face Secrets.")


#logic-3
from langchain_core.output_parsers import StrOutputParser
output_parser = StrOutputParser()

#langchain pipeline
chain = prompt_template | chat_model | output_parser


#input data
col1,col2 = st.columns(2)
with col1:
    Source = st.text_input('From Location :', placeholder = 'e.g., Hyderabad')
    Passengers = st.number_input('No.of Pasengers :', min_value=1,value=1)
with col2:    
    Destination = st.text_input('To Location:',placeholder='e.g., Manali')
    Date  = st.date_input('Date')

Transportation_Options = st.selectbox('Choose Transportation' , ['suitable','Car', 'Bus', 'Train', 'Flight'])
travel_style = st.selectbox('Travel style',['Budget', 'Mid-Range', 'Luxury'])

#logic-4
if st.button('Make my trip!'):
    if Source.strip() == "" or Destination.strip() == "":
            st.warning("Please enter location details📍")

    else:
        with st.spinner("Making a best plan..."): 
            input_ = {'Source':Source, 'Destination': Destination,'Transportation_Options':Transportation_Options,'Passengers': Passengers,  'Date': Date, 'travel_style': travel_style}
            st.write(chain.invoke(input_))

