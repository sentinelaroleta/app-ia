import streamlit as st
import os
from groq import Groq

# Configuração da página
st.set_page_config(page_title="Meu Chatbot IA")

st.title("🤖 Chatbot Independente (Llama 3)")

# Pega a chave que vamos configurar no Render depois
api_key = os.environ.get("GROQ_API_KEY")

# Se não achar a chave, avisa o usuário
if not api_key:
    st.warning("⚠️ Chave de API não encontrada. Configure no painel do Render.")
    st.stop()

# Conecta na Groq
client = Groq(api_key=api_key)

# Cria a memória do chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostra as mensagens antigas na tela
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Caixa de texto para você digitar
if prompt := st.chat_input("Escreva sua mensagem..."):
    # 1. Mostra o que você digitou
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Manda para a IA e pega a resposta
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=st.session_state.messages,
            temperature=0.7,
            max_tokens=1024,
            stream=True,
        )

        # 3. Mostra a resposta da IA digitando em tempo real
        with st.chat_message("assistant"):
            response = st.write_stream(completion)
        
        # 4. Guarda a resposta na memória
        st.session_state.messages.append({"role": "assistant", "content": response})

    except Exception as e:
        st.error(f"Erro ao conectar: {e}")