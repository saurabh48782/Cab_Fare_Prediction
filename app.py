import pickle
import math
import streamlit as st
import pandas as pd

"""
Created By: Saurabh Gupta
"""

# A function to round-off fares
def round5(number):
    dec_part = number%math.floor(number)
    if dec_part>0.00 and dec_part< 0.5:
        number = math.floor(number)+0.5
    elif dec_part == 0.5:
        number = number
    else:
        number = math.ceil(number)
    return number

# loading the trained model 
pickle_in = open('xgbr.pkl', 'rb') 
regressor = pickle.load(pickle_in)
  
# defining the function which will make the prediction using the data which the user inputs 
def prediction(Cab_Organization, Source, Destination, Distance, Surge_Multiplier,Cab_type):   
 
    # Pre-processing user input    
    if Cab_Organization == "Uber":
        Cab_Organization = 0
    else:
        Cab_Organization = 1
        
    # Source    
    if Source == "North End":
        Source = 0
    elif Source == "Financial District":
        Source = 1
    elif Source == "Theatre District":
        Source = 2
    elif Source == "South Station":
        Source = 3
    elif Source == "Back Bay":
        Source = 4
    elif Source == "Haymarket Square":
        Source = 5
    elif Source == "Northeastern University":
        Source = 6
    elif Source == "Beacon Hill":
        Source = 7
    elif Source == "Fenyway":
        Source = 8
    elif Source == "Boston University":
        Source = 9
    elif Source == "West End":
        Source = 10
    else:
        Source = 11
        
    # Destination    
    if Destination == "Back Bay":
        Destination = 0
    elif Destination == "North End":
        Destination = 1
    elif Destination == "Financial District":
        Destination = 2
    elif Destination == "Theatre District":
        Destination = 3
    elif Destination == "North Station":
        Destination = 4
    elif Destination == "Fenyway":
        Destination = 5
    elif Destination == "West End":
        Destination = 6
    elif Destination == "Northeastern University":
        Destination = 7
    elif Destination == "South Station":
        Destination = 8
    elif Destination == "Boston University":
        Destination = 9
    elif Destination == "Haymarket Square":
        Destination = 10 
    else:
        Destination = 11
    if Distance == 0:
        Distance = 1
        print("Distance can't be set to zero")
    else:
        Distance = Distance   
 
    if Surge_Multiplier == "1.0":
        Surge_Multiplier = 0
    elif Surge_Multiplier == "1.25":
        Surge_Multiplier = 1
    elif Surge_Multiplier == "1.5":
        Surge_Multiplier = 2
    elif Surge_Multiplier == "1.75":
        Surge_Multiplier = 3
    elif Surge_Multiplier == "2.0":
        Surge_Multiplier = 4
    elif Surge_Multiplier == "2.50":
        Surge_Multiplier = 5
    else:
        Surge_Multiplier = 6
    
    if Cab_type == "WAV":
        Cab_type = 0
    elif Cab_type == "UberXL":
        Cab_type = 1
    elif Cab_type == "UberX":
        Cab_type = 2
    elif Cab_type == "Black":
        Cab_type = 3
    elif Cab_type == "Black SUV":
        Cab_type = 4
    elif Cab_type == "UberPool":
        Cab_type = 5
    elif Cab_type == "Lyft":
        Cab_type = 6
    elif Cab_type == "Lux Black":
        Cab_type = 7
    elif Cab_type == "Shared":
        Cab_type = 8
    elif Cab_type == "Lyft XL":
        Cab_type = 9
    elif Cab_type == "Lux":
        Cab_type = 10
    else:
        Cab_type = 11

    test_data = pd.DataFrame({ 'cab_provider':[Cab_Organization], 'source':[Source], 'destination':[Destination],
                              'distance':[Distance], 'surge_multiplier':[Surge_Multiplier], 'cab_type':[Cab_type] })
    # Making predictions 
    prediction = regressor.predict(test_data)
     
    return round5(prediction[0])
      
  
# this is the main function in which we define our webpage  

def main():       
    # front end elements of the web page 
    html_temp = """ 
    <div style ="background-color:yellow;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Streamlit Cab Fare Prediction ML App</h1> 
    </div> 
    """
      
    # display the front end aspect
    st.markdown(html_temp, unsafe_allow_html = True) 
     

    # following lines create boxes in which user can enter data required to make prediction 
    Cab_Organization = st.selectbox('Cab Provider',("Lyft","Uber"))
    if Cab_Organization == "Uber":
        Cab_type = st.selectbox('Cab Type',("UberPool","UberX","WAV","Black","Black SUV","Uber XL"))
    else:
        Cab_type = st.selectbox('Cab Type',("Shared","Lyft","Lux","Lux Black","Lux Black XL","Lyft XL"))
    # Input box for distance    
    Distance = st.number_input("Enter distance (if set to zero, by default it will be 1)")
    
    Source = st.selectbox('Source',("North End","Financial District","Theatre District","South Station", "Black Bay",
                                    "Haymarket Square","Northeastern University","Beacon Hill","Fenway","Boston University",
                                    "West End","North Station"))
    
    Destination = st.selectbox('Destination',("Back Bay","North End","Financial District","Theatre District",
                                              "North Station","Fenway","West End","Northeastern University","Beacon Hill",
                                              "Boston University","Haymarket Square","South Station"))
    
    if Cab_Organization == "Uber":
        Surge_Multiplier = st.selectbox('Surge Multiplier',("1.0"))
    else:
        Surge_Multiplier = st.selectbox('Surge Multiplier',("1.0","1.25","1.5","1.75","2.0","2.50","3.00"))
    
    result =""
      
    # when 'Predict' is clicked, make the prediction and store it 
    if st.button("Predict"): 
        result = prediction(Cab_Organization,Source, Destination, Distance, Surge_Multiplier, Cab_type) 
        st.success('Your predicted fare is USD {}'.format(result))
     
if __name__=='__main__': 
    main()
