import os,requests,streamlit as st
st.set_page_config(page_title='Autonomous Enterprise AI Task Worker',page_icon='🤖',layout='wide')
API=os.getenv('API_URL','http://127.0.0.1:8000')
st.title('🤖 Autonomous Enterprise AI Task Worker');st.caption('Natural language → discovery → policy → execution → verification')
examples=['What is the name of employee EMP-20001?','What is the paycheck status for employee EMP-20001?','Check refund eligibility for order ORD-10001','Check low stock items','Show pending customer tickets']
with st.sidebar:
 st.header('Examples');c=st.selectbox('Choose an example',['Choose…']+examples)
 if c!='Choose…':st.session_state.task=c
t=st.text_area('What should I do?',st.session_state.get('task',''),height=120)
if st.button('▶ Run task',type='primary',use_container_width=True):
 try:
  d=requests.post(API+'/task',json={'task':t},timeout=120).json()
  st.subheader('Result');st.write(d.get('answer',''))
  st.subheader('Action');st.write(d.get('action',''))
  st.subheader('Evidence');st.write(', '.join(d.get('evidence',[])))
  det=d.get('details') or {}
  if 'items' in det:
   st.subheader(f"Low-stock items ({det['count']})")
   st.dataframe(det['items'],use_container_width=True,hide_index=True)
  elif 'decisions' in det:
   st.subheader('Refund decisions');st.dataframe(det['decisions'],use_container_width=True,hide_index=True)
  elif 'solved' in det or 'pending' in det:
   if det.get('solved'):st.subheader(f"Solved tickets ({len(det['solved'])})");st.dataframe(det['solved'],use_container_width=True,hide_index=True)
   if det.get('pending'):st.subheader(f"Pending tickets ({len(det['pending'])})");st.dataframe(det['pending'],use_container_width=True,hide_index=True)
  elif 'employee' in det:st.subheader('Employee data');st.dataframe([det['employee']],use_container_width=True,hide_index=True)
  elif 'customer' in det:st.subheader('Customer data');st.dataframe([det['customer']],use_container_width=True,hide_index=True)
  st.caption(f"Confidence: {d.get('confidence',0)*100:.0f}% · Status: {d.get('status','')}")
 except Exception as e:st.error(f'Could not reach worker API: {e}')
