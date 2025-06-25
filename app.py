import streamlit as st
import asyncio
from autogen_agentchat.messages import ToolCallRequestEvent, ToolCallExecutionEvent
from agent import configAgent, askAgent

st.set_page_config(page_title="🎬 Multi-Agent YouTube Assistant", layout="wide")

st.title("🎥 Multi-Agent YouTube Assistant")
st.caption("🤖 Powered by AutoGen ")


with st.sidebar:
    st.header("🛠️ Controls")


    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.agent_state = None
        st.experimental_rerun()


    if 'messages' in st.session_state and st.session_state.messages:
        chat_log = "\n\n".join(
            msg.to_text() if hasattr(msg, "to_text") else str(msg)
            for msg in st.session_state.messages
        )
        st.download_button(
            label="💾 Download Chat Log",
            data=chat_log,
            file_name="chat_log.txt",
            mime="text/plain",
            use_container_width=True
        )


url = st.text_input('Enter the URL of the YouTube video:')
chat_container = st.container()
prompt = st.chat_input('Ask a question about the video:')


def showMessage(chat_container, message):
    with chat_container:
        if isinstance(message, str):
            if message.startswith('User:'):
                with st.chat_message("user"):
                    st.markdown(message)
            else:
                with st.chat_message("ai"):
                    st.markdown(message)
        elif isinstance(message, ToolCallRequestEvent):
            with st.expander("🛠️ Tool Call Request"):
                st.markdown(message.to_text())
        elif isinstance(message, ToolCallExecutionEvent):
            with st.expander("📄 Tool Call Execution"):
                st.markdown(message.to_text())


if 'messages' not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    showMessage(chat_container, message)


if prompt and url:
    st.session_state.messages.append(f'User: {prompt}')
    showMessage(chat_container, f'User: {prompt}')

    async def main(url, prompt):
        agent = configAgent()
        if 'agent_state' in st.session_state:
            await agent.load_state(st.session_state.agent_state)

        async for message in askAgent(agent, url, prompt):
            st.session_state.messages.append(message)
            showMessage(chat_container, message)

        agent_state = await agent.save_state()
        return agent_state

    with st.spinner("💬 Thinking..."):
        st.session_state.agent_state = asyncio.run(main(url, prompt))
