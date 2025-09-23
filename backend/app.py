from fastapi import FastAPI, Request
from pydantic import BaseModel
from langchain_community.document_loaders import WebBaseLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import uvicorn

app = FastAPI()

class SummarizeRequest(BaseModel):
    url: str

@app.post("/summarize")
async def summarize(req: SummarizeRequest):
    loader = WebBaseLoader(req.url)
    documents = loader.load()
    page_text = "\n".join([doc.page_content for doc in documents])

    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    summary_prompt = PromptTemplate(
        template="Summarize the following web page in under 200 words:\n{text}",
        input_variables=['text']
    )
    summarize_chain = summary_prompt | model | StrOutputParser()
    summary = summarize_chain.invoke({"text": page_text})
    return {"summary": summary}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)