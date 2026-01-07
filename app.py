import streamlit as st
import os
from groq import Groq

# Configuração da página
st.set_page_config(page_title="Sentinela IA", page_icon="🤖")

st.title("🤖 Sentinela (Llama 3.3)")

# Pega a chave da API
api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("⚠️ Chave de API não encontrada. Configure no Render.")
    st.stop()

client = Groq(api_key=api_key)

# Inicializa histórico
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostra histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- A MÁGICA ACONTECE AQUI ---
def gerar_resposta_limpa(chat_completion):
    """Filtra o código feio e entrega só o texto"""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

if prompt := st.chat_input("Digite sua mensagem..."):
    # Mostra mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Chama a IA
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            model="llama-3.3-70b-versatile", # Modelo Novo
            stream=True,
        )

        # Mostra resposta limpa
        with st.chat_message("assistant"):
            # Aqui usamos a função de limpeza
            response = st.write_stream(gerar_resposta_limpa(chat_completion))
            
        st.session_state.messages.append({"role": "assistant", "content": response})

    except Exception as e:
        st.error(f"Erro: {e}")
