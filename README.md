🎬 YouTube Multi-Agent Chatbot using AutoGen + Streamlit
This project is an intelligent, multi-agent chatbot interface that lets you chat with any YouTube video. Built using the powerful AutoGen framework and Streamlit, the app extracts video transcripts and enables interactive Q&A about the video content.


✍️ How It Works

agent.py:
Defines two tools:

getVideoTranscript: Returns plain transcript

getVideoTranscriptWithTimeStamps: Returns transcript with timestamps

Uses AssistantAgent from AutoGen to decide which tool to use based on the user's question.

app.py:
Collects the video URL and question using Streamlit UI

Streams messages between user and agent

Saves and displays full chat history

Provides buttons to clear chat 

