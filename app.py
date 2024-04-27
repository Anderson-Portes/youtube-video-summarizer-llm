import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def get_youtube_video_id(youtube_video_url):
  video_url = youtube_video_url.split('v=')[1]
  return video_url.split('&')[0]
  

def get_transcript_from_youtube(youtube_video_url):
  video_id = get_youtube_video_id(youtube_video_url)
  response = YouTubeTranscriptApi.get_transcript(video_id, languages=['en','pt'])
  return ' '.join([x['text'] for x in response])

def generate_gemini_content(transcript):
  prompt = "Você é um resumidor de vídeos do YouTube. Você pegará o texto transcrito e resumirá todo o vídeo e fornecerá o resumo importante em pontos de até 250 palavras. Forneça o resumo do texto fornecido aqui:"
  model = genai.GenerativeModel('gemini-pro')
  response = model.generate_content(prompt+transcript)
  return response.text

st.title('Youtube Transcript to Detailed Notes Converter')
youtube_link = st.text_input('Enter Youtube Video Link: ')

if youtube_link:
  video_id = get_youtube_video_id(youtube_link)
  st.image(f'http://img.youtube.com/vi/{video_id}/0.jpg',use_column_width=True)

if st.button('Get Detailed Notes'):
  transcript = get_transcript_from_youtube(youtube_link)
  if transcript:
    summary = generate_gemini_content(transcript)
    st.markdown("## Detailed Notes")
    st.write(summary)
  else:
    st.write('No summary found')