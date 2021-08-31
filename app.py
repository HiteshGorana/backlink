import base64
import datetime
import io
import os
import re
from time import gmtime, strftime
from urllib.parse import urlsplit

import pandas as pd
import requests
import streamlit as st
import yagmail
from bs4 import BeautifulSoup

from mail import send_email
from utility import stqdm

STYLE = """
<style>
img {
    max-width: 100%;
}
</style>
"""

FILE_TYPES = ["csv"]

TEXT = """
A platform to enable brands & agencies for ensuring their investment of time & money in getting quality backlinks, high authority linkages and affiliate partnership is live. 

How does it work 
- Register your brand 
- Upload a list of URLs to watch 
- Set frequency to ping 
- Get regular Summary on mail 
"""
def check_backlink(url, backlink):
    request = requests.get(url)
    if request.ok:
        raw = request.text
        soup = BeautifulSoup(raw, "html.parser")
        anchors = soup.find_all('a')  # find all anchor tag
        flag = False
        herf_same = []
        for anchor in anchors:
            herf = anchor.attrs.get('href')
            try:
                if urlsplit(herf).netloc == urlsplit(backlink).netloc:
                    herf_same.append(herf)
            except:
                pass
            if herf == backlink:  # extract herf link and compare
                flag = True
        return flag, herf_same
    else:
        return False, []


def status_code(list_):
    status_ = []
    for i in list_:
        if i:
            try:
                request = requests.get(i, timeout=60)
                status_.append(request.status_code)
            except:
                status_.append(404)
        else:
            status_.append(None)
    return status_

# import yagmail
# import io
# towrite = io.BytesIO()
# # yag = yagmail.register('info.opositive@gmail.com', 'Obbserv@123')
# import pandas as pd
# yag = yagmail.SMTP('info.opositive@gmail.com', 'Obbserv@123')
# data = pd.read_csv('sample_input.csv')
# data.to_csv(towrite)
# towrite.seek(0)
# yag.send(to='hitesh.obbserv@gmail.com',
#          subject='Test',
#          contents="Test",
#          attachments=towrite
#          )

def check(data):
    status = []
    Links = []
    for index, info in stqdm(data.iterrows(), total=len(data)):
        try:
            stat, links = check_backlink(info['AWU'], info['BU'])
            status.append(stat)
            links += [None] * (5 - len(links))
            Links.append(links)
        except:
            status.append('No')
            Links.append([None] * 5)
    data['Time-Initiation'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    data['Brand URLs Present'] = status
    data['Brand URLs Present'] = data['Brand URLs Present'].apply(lambda x: 'Yes' if x else 'No')
    data['AWU http response code'] = status_code(data['AWU'].tolist())
    data = data[['Time-Initiation', 'BU', 'AWU', 'Brand URLs Present', 'AWU http response code']]
    l1 = []
    l2 = []
    l3 = []
    l4 = []
    l5 = []
    for _l1, _l2, _l3, _l4, _l5 in Links:
        l1.append(_l1)
        l2.append(_l2)
        l3.append(_l3)
        l4.append(_l4)
        l5.append(_l5)
    data['Brand URLs 1'] = l1
    data['Brand URLs 1 http response code'] = status_code(l1)
    data['Brand URLs 2'] = l2
    data['Brand URLs 2 http response code'] = status_code(l2)
    data['Brand URLs 3'] = l3
    data['Brand URLs 3 http response code'] = status_code(l3)
    data['Brand URLs 4'] = l4
    data['Brand URLs 4 http response code'] = status_code(l4)
    data['Brand URLs 5'] = l5
    data['Brand URLs 5 http response code'] = status_code(l5)
    try:
        for i in [1, 2, 3, 4, 5]:
            data[f'Brand URLs {i}'] = data[f'Brand URLs {i}'].astype(int)
        data['AWU http response code'] = data['AWU http response code'].astype(int)
    except:
        pass
    return data


def download(text, csvstr):
    text = text.encode()
    b64 = base64.b64encode(text).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{csvstr}.csv" target="_blank">Download</a>'
    return href


def isValid(s):
    # 1) Begins with 0 or 91
    # 2) Then contains 7 or 8 or 9.
    # 3) Then contains 9 digits
    Pattern = re.compile("(0|91)?[7-9][0-9]{9}")
    return Pattern.match(s)


def main():
    # st.markdown(f"""<span style="color:red; font-size: 50px"><title>Keep it live<title></span>""",
    #             unsafe_allow_html=True)
    st.markdown(STYLE, unsafe_allow_html=True)
    st.write(TEXT)
    placeholder = st.sidebar.empty()
    form = placeholder.form(key='my_form')
    name_ = form.text_input(label='Name')
    email = form.text_input(label='Email')
    number = form.text_input(label='Mobile')
    brand_name = form.text_input(label='Brand name')
    plain = form.selectbox('Frequency', ('onetime', 'weekly', 'monthly'))
#     way = form.selectbox('Output', ('Download'))
    way = 'Download'
    tick = form.checkbox('Subscribe For Free Tools Update')
    if (not str(number).isdigit()) and (number != ''):
        st.sidebar.error('Invalid number')
    json_data = {
        "name": name_,
        "email": email,
        "mobile number": number,
        "brand name": brand_name,
        "output": way,
        "frequency": plain,
        "subscribe": tick
    }
    if '@' not in email and email != '':
        st.sidebar.error('Invalid Email')
        email = 'invalid'
    submit_button = form.form_submit_button(label='Submit')
    mydate = datetime.datetime.now()
    csvstr = datetime.datetime.strftime(mydate, '%Y-%m%d-%H-%M-%S')
    df = pd.read_csv('sample_input.csv')
    file = st.file_uploader("", type=FILE_TYPES)
    if not file:
        st.error('File not Uploaded')
    st.write('Input Format')
    st.write('BU : Brand URL (Service/Product) page')
    st.write('AWU : Authority Website URL (Published Authority Post URL)')
    st.table(df.head(1))
    if submit_button and email != 'invalid':
        try:
            data = pd.read_csv(file)
            if data.columns[0] != 'BU' and data.columns[0] != 'AWU':
                st.error('Wrong format csv file')
            data = check(data)
            st.success('success')
            st.dataframe(data.head())
            # data.to_csv(csvstr + '.csv', index=False)
            a = len(data)
            b = len(data[data['Brand URLs Present'] == 'Yes'])
            c = len(data[data['Brand URLs Present'] == 'No'])
            bodyText = f"""\
                Hey {name_}, 
                Thanks for using Keep it live! 
                Your Backlink audit has been ready. Here are some insights of your audit.
                
                
                Total URLs | Live Links | Broken Links | Link Removed
                    {a}        |     {b}        |      {c}          |      {c}
                
                Please download full backlinks audit report.
                Thank You! 
                Keep It Live 
                
                Copyright © 2021 Keep It Live, All rights reserved. 
                """
            if way == 'Email':
#                 towrite = io.BytesIO()
#                 data.to_csv(towrite)
#                 towrite.seek(0)
#                 yag.send(to=email,
#                          subject='Backlink',
#                          contents=bodyText,
#                          attachments=towrite
#                          )
                st.success('Data has been send to your Email Address')
            elif way == 'Download':
                st.markdown(download(data.to_csv(index=False), csvstr), unsafe_allow_html=True)
            file.close()
            try:
                os.remove(csvstr)
            except:
                pass
        except Exception as e:
            _ = e
    # st.markdown(f"""<span style="color:red; font-size: 50px"><title>Keep it Alive<title></span>""",
    # unsafe_allow_html=True)
    # st.image('MarineGEO_logo.png')


LOGO_IMAGE = "Final Logo_01.png"

if __name__ == "__main__":
    # st.markdown("""
    #                 <style>
    #                 MainMenu {visibility: hidden;}
    #                 </style>
    #                 """, unsafe_allow_html=True)
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>

    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    # MainMenu {visibility: hidden;}
    st.markdown(
        """
        <style>
        .container {
            display: flex;
        }
        .logo-text {
            font-weight:700 !important;
            font-size:50px !important;
            color: #f9a01b !important;
            padding-top: 75px !important;
        }
        .logo-img {
            float:right;
            height:70px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        f"""
        <div class="container">
            <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
        </div>
        """,
        unsafe_allow_html=True
    )
    main()
