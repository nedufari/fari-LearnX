import streamlit as st
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder




# Load the data

# Load the data
df = pd.read_csv('learnxds.csv')

# check for missing values
df.isnull().sum()

# drop missing values
df.dropna(inplace=True)

# check for duplicates
df.duplicated().sum()

# drop duplicates
df.drop_duplicates(inplace=True)

# Initialize the label encoder
le = LabelEncoder()

df_encoded = pd.get_dummies(df,columns=['Coursecode','Coursetitle','Subtopic'], drop_first=True)
df_encoded.drop(['id','isObjective'], axis=1, inplace=True)
df_encoded = df.apply(le.fit_transform)
# df_encoded.groupby(['Coursecode','Coursetitle','Subtopic']).count()

# Extract the questions and answers from the data
questions = df['Question']
answers = df['Answerkey']

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(questions)
y = answers

#feature engineering 


# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = DecisionTreeClassifier()
model.fit(X_train, y_train)



# Fit the model
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# evaluate the model on the test set
from sklearn.metrics import accuracy_score
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Generate a question for the user to answer
with st.container():

    st.info("""  #  120 QUESTIONS QUIZ GENERATED TO TEST YOUR PREPAREDNESS FOR THE SECOND SEMESTER EXAMS 
The questions would be auto refreshed in an hour from now and the student is expected to have been done and graded before the questions are being refreshed. """)
    st.warning("PLEASE BEFORE ATTEMPTING THIS QUIZ ENSURE YOU HAVE COVERED ALL THE MATERIALS, THE QUIZ WOULD CUT ACCROSS ALL THE THREE COURSES IN OUR COURSE LIST. THANKS ")

# Create a progress bar
progress_bar = st.progress(0)

# Initialize counters for correct answers and total questions
# calculate the number of correct answers
num_correct = (y_pred == y_test).sum()
num_questions =120
user_answers=[None for _ in range(num_questions)]
correct_answers=[]

# Create a table to store the answers
answers_df = pd.DataFrame(columns=["Question", "Correct Answer", "User Answer"])

# Generate a question for the user to answer

@st.cache(ttl=1800,suppress_st_warning=True, show_spinner=True, allow_output_mutation=True)

def generate_questions():
    
    return questions.sample(120,replace=False)
    
    # code to generate questions

unique_question=generate_questions()

score = 0


for i, question in enumerate(unique_question):
    # Use the model to predict the correct answer
    prediction = model.predict(vectorizer.transform([question]))[0]
    correct_answers.append(prediction)
    
    st.write(f"Question {i+1} of {num_questions} attempted")

    # Use a consistent layout
    st.subheader(f"Question {i+1}")
    
    # Display the generated question to the user
    st.markdown(question)
    
    
    # Use more dynamic inputs
    user_answer = st.text_input("please input your answer",key = f"question_{i+1}")
    # options = ['PICK ONE','A','B','C','D']
    # user_answer = st.selectbox("please choOse your answer",options, key=f"question_{i+1}")
    if user_answer:
        progress_bar.progress((i+1)/num_questions)
        st.write(f"{(i+1)/num_questions*100:.1f}% of questions answered, {num_questions-(i+1)} remaining")
        user_answers.append(user_answer)
        if user_answer == prediction:
            score += 1

       
    # Use error handling
    if user_answer == "":
        st.error("You must provide an answer, and please in capital letters")
        continue
        
    # Grade the user's answer and provide feedback
    if user_answer == prediction:
        num_correct += 1
        st.success("Correct! Great job.")
    else:
        st.error("oops!, incorrect")
    
    # Update the answers_df DataFrame with the user's answer
    answers_df = answers_df.append({'Question':question,'Correct Answer':prediction,'User Answer':user_answer},ignore_index=True)

st.subheader("Score")
st.write(f"Your score is {score:.1f} out of {num_questions}")

# Provide feedback and suggestions
if score >= 10.0:
    st.write("Great job! Keep up the good work.")
elif score <= 9.0:
    st.write("You're doing well, but there's still room for improvement.")
else:
    st.write("You'll need to work a bit harder to improve your score.")


# Show the answers table
st.write("Answers:")
st.table(answers_df)

df_encoded['Question'] = question
df_encoded['Answerkey'] = prediction
df_encoded['User_Answer'] = user_answer
grouped_df = df.groupby(['Question', 'Coursecode', 'Coursetitle', 'Subtopic']).size().reset_index(name='number of questions')

st.info("TABLE CONTAINING ALL THE QUESTIONS AND THEIR CATEGORIES")
st.write(grouped_df)

# Use the merge function to join the grouped_df DataFrame with the answers_df DataFrame on the 'Question' column
merged_df = pd.merge(answers_df, grouped_df, left_on='Question', right_on='Question')

# Create a new column that shows the student's score for each question
merged_df['Score'] = (merged_df['User Answer'] == merged_df['Correct Answer']).astype(int)

# Group the merged_df DataFrame by the Coursecode, Coursetitle, and Subtopic columns and calculate the student's score for each group
performance_df = merged_df.groupby(['Coursecode', 'Coursetitle', 'Subtopic']).agg({'number of questions': 'first', 'Score': 'mean'}).reset_index()

# Calculate the total number of questions for each group
# performance_df['total number of questions'] = performance_df['number of questions'].sum()

# Create a new column that shows the student's percentage score for each group
performance_df['Overall Percentage Score'] = performance_df['Score']/ performance_df['number of questions'] * 100

# Group the performance_df DataFrame by the Coursetitle column and calculate the number of questions answered for each coursetitle
courses_df = performance_df.groupby('Coursetitle').agg({'number of questions': 'sum', 'Score': 'sum'}).reset_index()

# Create a new column that shows the student's percentage score for each coursetitle
courses_df['Overall Percentage Score'] = courses_df['Score'] / courses_df['number of questions'] * 100

# Group the performance_df DataFrame by the Subtopic column and calculate the number of questions answered for each subtopic
subtopics_df = performance_df.groupby('Subtopic').agg({'number of questions': 'sum', 'Score': 'sum'}).reset_index()

# Create a new column that shows the student's percentage score for each subtopic
subtopics_df['Overall Percentage Score'] = subtopics_df['Score'] / subtopics_df['number of questions'] * 100

# Display the results to the user

import plotly.express as px

# Create a new DataFrame that only contains the 'Coursetitle' and 'Percentage Score' columns
pie_dfy = performance_df[['Subtopic', 'Overall Percentage Score']]
pie_dfy = pie_dfy.dropna()
print (pie_dfy.columns)
print(pie_dfy)

# Use the pivot_table function to create a new DataFrame with one row for each Coursetitle and one column for each Percentage Score
pie_dfy = pie_dfy.pivot_table(index='Subtopic', values=['Overall Percentage Score'], aggfunc='sum')

# Extract the values of the 'Percentage Score' column from the `pie_df` DataFrame
valuesy= pie_dfy['Overall Percentage Score'].tolist()
# Create a pie chart using Plotly
if pie_dfy.empty:
    st.write("no data to display")
else:
    figy = px.pie(pie_dfy, values=valuesy, names=pie_dfy.index, title='Percentage of Questions Answered Correctly by Subtopic')
    figy.update_traces(textposition='inside', textinfo='percent+label')

# Display the pie chart in Streamlit
    st.plotly_chart(figy)


# Calculate the percentage of correct answers for each course
performance_df['Overall Percentage Score'] = performance_df['Overall Percentage Score'] / performance_df['number of questions']*100

# Group the performance_df DataFrame by the Coursecode column and sum the Percentage Score column
course_scores = performance_df.groupby('Coursecode')['Overall Percentage Score'].sum().reset_index()




# Create a new DataFrame that only contains the 'Coursetitle' and 'Percentage Score' columns
pie_dfy = performance_df[['Coursecode', 'Overall Percentage Score']]
pie_dfy = pie_dfy.dropna()
print (pie_dfy.columns)
print(pie_dfy)

# Use the pivot_table function to create a new DataFrame with one row for each Coursetitle and one column for each Percentage Score
pie_dfy = pie_dfy.pivot_table(index='Coursecode', values=['Overall Percentage Score'], aggfunc='sum')

# Extract the values of the 'Percentage Score' column from the `pie_df` DataFrame
valuesy= pie_dfy['Overall Percentage Score'].tolist()
# Create a pie chart using Plotly
if pie_dfy.empty:
    st.write("no data to display")
else:
    figy = px.pie(pie_dfy, values=valuesy, names=pie_dfy.index, title='Percentage of Questions Answered Correctly by Coursecode')
    figy.update_traces(textposition='inside', textinfo='percent+label')

# Display the pie chart in Streamlit
    st.plotly_chart(figy)
    st.info("The percentage allocated to each category is done based on the real time data being processed. The category with the highest percentage shows where your stregnth lies and in that order the data shows you areas where you performed well and areas where you need to improve more on. The table above containing all questions is there to assist you in knowing the category the questions you got wrongly or correctly falls under. ")


# Calculate the percentage of correct answers for each course
performance_df['Overall Percentage Score'] = performance_df['Overall Percentage Score'] / performance_df['number of questions']*100

# Group the performance_df DataFrame by the Coursecode column and sum the Percentage Score column
course_scores = performance_df.groupby('Coursecode')['Overall Percentage Score'].sum().reset_index()

