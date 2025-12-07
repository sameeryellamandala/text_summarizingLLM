import validators,traceback
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader

st.set_page_config( page_title = "langChain: Summarize Text from YT or website ")
st.title( "Langchain : Summarize Text")
st.subheader('Summarize URL')

with st.sidebar :
    groq_api_key = st.text_input("GROQ API KEY" , value = "" , type = "password")


prompt_template = ChatPromptTemplate.from_messages([
    ("system", "summarize the following text :"),
    ("human", "{text}")
])
gurl = st.text_input( "URL" ,label_visibility= "collapsed")

if st.button("Summarize the content from YT or Website ") :

    if not groq_api_key.strip() or not gurl.strip():
        st.error("please enter full information to start !")
    elif not validators.url(gurl):
        st.error("please enter valid url it should be  any website or YT url")

    else:
        try:
            with st.spinner("waiting..."):
                llm = ChatGroq(model = "llama-3.3-70b-versatile",groq_api_key = groq_api_key)
                docs = []
                if "youtube.com" in gurl  or "youtu.be" in gurl :
                    if "&" in gurl:
                        gurl = gurl.split("&")[0]
                    loader = YoutubeLoader.from_youtube_url(gurl,add_video_info=False)
                else :
                    loader = UnstructuredURLLoader(urls = [gurl], ssl_verify = False, headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}
)
                docs = loader.load()

                chain = prompt_template | llm | StrOutputParser()
                result = chain.invoke({"text" : docs})

                st.success(result)
        except Exception as e:
            st.error(f" An error occured during processing :{str(e)}")
            st.code(traceback.format_exc(),language='python')

            
