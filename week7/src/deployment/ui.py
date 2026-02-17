import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import os

API_BASE="http://localhost:8000"

st.set_page_config(
    page_title="Multimodal RAG Assistant",
    layout="centered",
)

st.title("Multimodal RAG Assistant")

mode=st.radio(
    "Select mode",
    ["Text RAG","Image RAG","SQL RAG"],
    horizontal=True,
)

st.divider()

def render_evaluation(evaluation:dict):
    st.caption("Evaluation")
    st.write(f"Faithfulness: {evaluation.get('faithfulness')}")
    st.write(f"Confidence: {evaluation.get('confidence')}")
    st.write(f"Hallucination Risk: {evaluation.get('hallucination_risk')}")

def render_image(source:str,caption:str|None=None):
    try:
        if source.startswith("http"):
            resp=requests.get(source,timeout=10)
            resp.raise_for_status()
            img=Image.open(BytesIO(resp.content))
        else:
            if not os.path.exists(source):
                st.warning(f"Image not found: {source}")
                return
            img=Image.open(source)
        st.image(img,caption=caption,width=700)
    except Exception as e:
        st.warning(f"Could not render image: {e}")

if mode=="Image RAG":
    st.subheader("Image-based RAG")

    image_mode=st.radio(
        "Select Image Mode",
        [
            "Image → Image (Find similar images)",
            "Image → Text (Extract text from image)",
            "Text → Image (Find images from text)",
        ],
    )

    question=None
    image=None

    if image_mode=="Text → Image (Find images from text)":
        question=st.text_area("Enter text query",height=100)
    else:
        image=st.file_uploader(
            "Upload an image",
            type=["jpg","jpeg","png"],
        )

    if st.button("Run Image Query"):
        with st.spinner("Processing..."):
            data={}
            files={}

            if question:
                data["question"]=question

            if image:
                files["image"]=(
                    image.name,
                    image.getvalue(),
                    image.type,
                )

            if image_mode=="Image → Image (Find similar images)":
                endpoint="/ask-image-image"
            else:
                endpoint="/ask-image"

            resp=requests.post(
                f"{API_BASE}{endpoint}",
                data=data,
                files=files,
                timeout=1000,
            )

        if resp.status_code!=200:
            st.error(resp.text)
        else:
            result=resp.json()

            st.success("Answer")
            st.write(result.get("answer",""))

            context=result.get("context_used",[])

            if context:
                st.subheader("Retrieved Results")

                for item in context:
                    if item.get("source"):
                        render_image(
                            item["source"],
                            caption=item.get("caption",""),
                        )

                    if item.get("ocr_text"):
                        st.caption("OCR Text")
                        st.code(item["ocr_text"])

                    st.caption(f"Score: {item.get('score',0.0)}")
                    st.divider()
            else:
                if image_mode!="Image → Text (Extract text from image)":
                    st.warning("No results found.")

            if "evaluation" in result:
                render_evaluation(result["evaluation"])

elif mode=="Text RAG":
    st.subheader("Text Retrieval (RAG)")

    question=st.text_area("Enter your question",height=120)

    if st.button("Ask"):
        with st.spinner("Thinking..."):
            resp=requests.post(
                f"{API_BASE}/ask",
                params={"question":question},
                timeout=600,
            )

        if resp.status_code!=200:
            st.error(resp.text)
        else:
            data=resp.json()
            st.success("Answer")
            st.write(data.get("answer",""))

            if "evaluation" in data:
                render_evaluation(data["evaluation"])

else:
    st.subheader("SQL Assistant")

    question=st.text_area("Ask a question about the database",height=120)

    if st.button("Run SQL Query"):
        with st.spinner("Running SQL query..."):
            resp=requests.post(
                f"{API_BASE}/ask-sql",
                params={"question":question},
                timeout=600,
            )

        if resp.status_code!=200:
            st.error(resp.text)
        else:
            st.success("SQL Result")
            st.write(resp.json())
