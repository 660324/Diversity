import pandas as pd
import streamlit as st
import io
import requests
pd.set_option('display.max_columns', None)
st.set_page_config(layout="centered")  #use 'wide' mode and use column controls to make it two-column website?

# original_df = pd.read_excel('C:/Users/yuhao1/Desktop/diversity/data.xlsx',sheet_name='Form1')
# original_df.to_pickle('C:/Users/yuhao1/Desktop/diversity/data.pkl')
#streamlit run "C:/Users/yuhao1/Desktop/diversity/diversity1.py"

# link = '[GitHub](http://github.com)'
# st.markdown(link, unsafe_allow_html=True)


url='https://github.com/660324/Diversity/blob/main/data.pkl?raw=true'
original_df=pd.read_pickle(url)
#print (original_df)

response = requests.get('https://github.com/660324/Diversity/blob/main/logo.png?raw=true')
logo=io.BytesIO(response.content)
st.sidebar.image(logo)

response1= requests.get("https://github.com/660324/Diversity/blob/main/DEIBInventoryForm.pdf?raw=true")
DEIBInventoryForm = io.BytesIO(response1.content)



st.title('DEIB Resources Inventory')
st.text("")

######sort##########
st.sidebar.text("")
st.sidebar.text("")
option1 = st.sidebar.selectbox('Sort by',('Title', 'Submitter', 'Location'))
st.sidebar.write('You selected:', option1)

if option1=='Submitter' :
    option1='Name'
if option1=='Location' :
    option1='Location of effort (city/state/country/etc.)'

option1_1 = st.sidebar.radio("Order", ('Ascending','Descending'))
if option1_1=='Ascending' :
    option1_1=True
if option1_1=='Descending' :
    option1_1=False
########################


######tag##########
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
option2=st.sidebar.multiselect('Select All Tags that apply',
                               ['Age','Culture' ,'Different Ideas and Perspectives','Disability','Ethnicity','First Generation Status','Familial Status',
                                'Gender Identity and Expression','Geographic Background','Marital Status','National Origin','Race', 'Religious and Spiritual Beliefs'
                                ,'Sex','Sexual Orientation','Socioeconomic Status','Student Organization','Veteran Status'],default=None, help='Select as many tags as you want')
########################


###########download form##########
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.write("To submit your events, visit the link: https://www.k-state.edu/diversity-inclusion; Or click the button below to download the application form")
st.sidebar.download_button(
    label="Download Form",
    data=DEIBInventoryForm,
    file_name='form.pdf')
########################


######search and check##########
search1 = st.text_input('Search Title and Description')

c1, c2 = st.columns([3, 2])
with c1:
    cka = st.checkbox('Expand All')
with c2:
    mhk = st.checkbox('See Manhattan Campus Only',help='Check this box to ignore events in Salina and Olathe campus')
st.text("")

if cka:
    check1=True
else:
    check1=False

if mhk:
    check2='Manhattan'
else:
    check2=','
########################



df=original_df.sort_values(by=option1, ascending=option1_1)

df=df[df[['Title', 'Brief Description for Listing']].apply(lambda x: x.str.contains(search1, case=False)).any(axis=1)
& df['Location of effort (city/state/country/etc.)'].str.contains(check2,case=False)
& df['Tags (Please select all categories that apply)'].apply(lambda x: all(word in x for word in option2))]
# df=df[df['Location of effort (city/state/country/etc.)'].str.contains(check2,case=False)]


for i,j in df.iterrows():  # i is index, j is the row content
    #print (j)
    # print (j['Title'])
    # print ('Organized by: '+j['Name']+'   ' + 'At: '+str(j['Location of effort (city/state/country/etc.)']))
    # print (j['Brief Description for Listing'])
    # print ('Web: '+j['Website'])
    # print ('Full Description: '+j['Description'].replace("\n", " ")+'\nFrequency: '+j['Frequency']+'\nSubmitted at: '+str(j['Completion time'])
    #        +'\nContact: '+j['Contact (please provide principle contact name and email/preferred contact number)']+'\nUnit: '+j['College/Academic Unit/Office'])
    # print (u'\u2500' * 50)   #print a horizon line

    st.subheader(j['Title'])

    col1, col2 = st.columns([1, 1])
    with col1:
        st.caption('Submitted by: ' + j['Name'])
    with col2:
        st.caption('At: '+str(j['Location of effort (city/state/country/etc.)']))

    st.write(j['Brief Description for Listing'])

    st.write('Web: '+j['Website'])

    with st.expander("See more details", expanded=check1):
        st.write('Full Description: '+j['Description'].replace("\n", " "))
        st.write('Contact: '+j['Contact (please provide principle contact name and email/preferred contact number)'])
        st.write('Tag: ' + j['Tags (Please select all categories that apply)'].replace(";", ", ").rstrip(', '))
        st.write('Audience: ' + j['Audience (Please select all that apply)'].replace(";", ", ").rstrip(', '))
        st.text('Frequency: '+j['Frequency']+'\nSubmitted at: '+str(j['Completion time'])+'\nUnit: '+j['College/Academic Unit/Office']
                + '\nEffort Dates: ' + str(j["This Year's Effort Dates (Start Date)"])+'\nPartners: ' +str(j['Collaborative Partner(s)'])
                + '\nNumber of Participants: ' + str(j['Number of Participants (please provide your best estimate if/when applicable)'])
                + '\nEffort Type: ' + j['Effort Type (Please select all categories that apply)'].replace(";", ", ").rstrip(', '))

    st.write (u'\u2500' * 62)   #print a horizon line

