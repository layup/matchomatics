import os 
import numpy as np  
import random
import pdfkit
import names 

from numpy import dot
from numpy.linalg import norm 
from jinja2 import Environment, FileSystemLoader

#preferences 

#personality  
PERSONALITY_TYPE = {
    'e': 'extraversion', 
    'a': 'agreeableness', 
    'o': 'openness',
    'c': 'conscientiousness',
    'n': 'neuroticism'
}
CHARACTERS = ['e', 'a', 'o', 'c', 'n'] 

# Define weights for each trait (you can adjust these based on importance)
#TODO: i can adjust the weights based on some intial questions that can help determine which they weight as more important then others
# basic user information, preferences, trait weight, questions answers 
TRAIT_WEIGHTS = {'e': 1, 'a': 1, 'o': 1, 'c': 1, 'n': 1}
TEMPLATE_NAME = 'template.html'

TOTAL_TRAIT_QUESTIONS = 5
MAX_QUESTION_POINTS = 5
TOTAL_POINTS = TOTAL_TRAIT_QUESTIONS * MAX_QUESTION_POINTS


def userInfo(): 
    
    user = {
        'first':'', 
        'last': '', 
        'gender':'', 
        'birthday':'', 
    }

def generateArray():
    result_array = []
    
    for character in CHARACTERS:
        for _ in range(TOTAL_TRAIT_QUESTIONS):
            number = random.randint(1, MAX_QUESTION_POINTS)
            result_array.append((number, character))

    return result_array

def generateFakeUserInfo(amount):
    fakeNames = []
    
    for i in range(amount): 
        random_name = names.get_full_name()
        fakeNames.append(random_name)
       
    return fakeNames

def compatabilitySorter():  
    pass; 

def calculateStats(data):
    characters = {
        'e':0, 
        'a':0,
        'o':0, 
        'c':0, 
        'n':0, 
    }
    temp = []
     
    for value, char in data: 
        characters[char] += value 
        
    for char, value in characters.items(): 
        percentageData = value/TOTAL_POINTS
        characters[char] = percentageData
        temp.append(percentageData)
 
    return characters
        
def euclideanDistance(arr1, arr2): 
    array1 = np.array(arr1)
    array2 = np.array(arr2)

    distance = np.linalg.norm(array1 - array2)
    return distance 

def similarityPercentage(distance, max_distance): 
    return (1- distance/max_distance) *100

def compareCloseness(arr1, arr2): 
    cos_sin = dot(arr1, arr2)/(norm(arr1) * norm(arr2))

    return cos_sin; 

def calculate_trait_similarity(trait1, trait2):

    # Use normalized Likert scale values for sensitivity
    normalized_trait1 = normalize_likert_scale(trait1)
    normalized_trait2 = normalize_likert_scale(trait2)
    
    # You can use different similarity measures here
    # For simplicity, I'll use absolute difference as a similarity measure
    return 1 - abs(trait1 - trait2)

def calculate_overall_compatibility(user1_data, user2_data, trait_weights):
    total_weight = sum(trait_weights.values())
    overall_similarity = 0

    for trait, weight in trait_weights.items():
        similarity_score = calculate_trait_similarity(user1_data[trait], user2_data[trait])
        overall_similarity += (weight / total_weight) * similarity_score

    return overall_similarity

def normalize_likert_scale(value, min_value=1, max_value=5):
    return (value - min_value) / (max_value - min_value)

def printScore(users, userInfo,  showDetailed=False): 
    for i, user in enumerate(users): 
        currentUser = users[i]
        currentData = userInfo[currentUser]
        print(f'***Current user: {currentUser}')
        
        for char, value in currentData.items(): 
            charName = PERSONALITY_TYPE[char]
            print(f'{charName:<20}: {value}')
        
        print('')
        for j in range(len(users)): 
            if(i != j): 
                comparingUser = users[j]
                compareData = userInfo[comparingUser]
            
                # Calculate overall compatibility
                overall_compatibility = calculate_overall_compatibility(currentData, compareData, TRAIT_WEIGHTS)

                # Calculate the similiarity 
                similarityScore = calculate_overall_compatibility(currentData, compareData, TRAIT_WEIGHTS) 
                
                # Print the results
                print(f'{comparingUser:<20} Similarity Score: {similarityScore:.2%}')
                if(showDetailed): 
                    print()
                    print(f"Trait Similarity Scores:")
                    for trait in currentData:
                        similarity_score = calculate_trait_similarity(currentData[trait], compareData[trait])
                        print(f"{trait}: {similarity_score:.2%}")

                    print("\nOverall Compatibility:")
                    print(f"{overall_compatibility:.2%}")
                
        print('-----------------------------------------') 

def generateTemplate(outputName, userInfo): 
    # Load the template
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(TEMPLATE_NAME)

    # Data to be inserted into the template
    e = userInfo['e'] * 100
    a = userInfo['a'] * 100 
    o = userInfo['e'] * 100 
    c = userInfo['c'] * 100 
    n = userInfo['n'] * 100
    
    data = {
        'name': outputName, 
        'age': 26, 
        'sign': 'cancer',
        'e': f'{e:.1f}', 
        'a': f'{a:.1f}',
        'o': f'{o:.1f}',
        'c': f'{c:.1f}',
        'n': f'{n:.1f}',
    }

    # Render the template with data
    output_html = template.render(data)

    templateName = outputName + '.html'
    pdfName = outputName + '.pdf'
    
    filePath = os.path.join('results/', templateName)
    filePath2 = os.path.join('results/', pdfName)
     
    # Save the rendered HTML to a file
    with open(filePath, 'w') as f:
        f.write(output_html)
        
    #write the pdf
    #pdfkit.from_string(output_html, filePath2) 

        
def basicInfo(): 
    pass; 


if __name__ == '__main__': 
    
    users = ['Shelley', 'Eric', 'Ben', 'Jordan', 'Evan', 'Marc', 'Rebecca', 'Jonah', 'Rhett', 'Sam', 
             'Connor', 'Maja', 'Emma', 'Kayleigh', 'Andrew']
    
    #users = ['Jonah', 'Rebecca', 'Rhett', 'LJ']

    users = generateFakeUserInfo(20)

    userInfo = {}
    
    #general information 
    totalUsers = len(users)


    print('**USER DATA')
    for user in users: 
        rawData = generateArray() 
        results = calculateStats(rawData)
        userInfo[user] = results 
        
        print(f'{user}: {results}')
    
    print()
 
    for i, user in enumerate(users): 
        currentUser = users[i]
        currentData = userInfo[currentUser]
        #print(f'***Current user: {currentUser} results: {currentData}')

    printScore(users, userInfo, False)
    
    for userName, data in userInfo.items(): 
       generateTemplate(userName, data) 
                

                
            
        

            
    
        
        
    

 
