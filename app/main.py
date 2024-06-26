import fastapi as _fastapi
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.analyzer import Analyzer as TextHandler, CorpusManager
from app.crud import create_text, get_text, get_text_by_id, set_buffer
from app.database import SessionLocal, engine, Base
from app.schemas import Text, CurrentTable
from app.llm_api import get_synonyms, get_antonyms, chatting, get_definition

Base.metadata.create_all(bind=engine)
app = _fastapi.FastAPI(debug=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


templates = Jinja2Templates("templates")

manager = CorpusManager()
@app.get("/", response_class=HTMLResponse)
def index(request: _fastapi.Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

@app.get("/view/{text_name}", response_class=HTMLResponse)
def index(request: _fastapi.Request):
    return templates.TemplateResponse(
        request=request, name="text_page.html"
    )

@app.get("/get_info/{text_name}")
def get_data(text_name: str, db: Session = _fastapi.Depends(get_db)):
    text = get_text_by_id(db=db, name=text_name)
    if text:
        return text

@app.get("/get_texts")
def get_texts(db: Session = _fastapi.Depends(get_db)):
    return get_text(db)

@app.post("/upload")
def upload(file: _fastapi.UploadFile = _fastapi.File(...), db: Session = _fastapi.Depends(get_db)):
    handler = TextHandler()
    text = Text(name=file.filename, raw_text=file.file.read())
    current_table = CurrentTable(name=text.name)
    set_buffer(db=db, current_table=current_table)
    text.tokens = handler.leksems(text.raw_text)
    text.collocations = handler.analyze(text.raw_text)
    create_text(text_new=text, db=db)
    return text.model_dump_json()

@app.post("/save_data")
def save_data(text: Text, db: Session = _fastapi.Depends(get_db)):
    handler = TextHandler()
    text.tokens = handler.leksems(text.raw_text)
    text.collocations = handler.analyze(text.raw_text)
    create_text(text_new=text, db=db)

@app.get("/generate_markup")
def generate_markup(text_name: str, db: Session = _fastapi.Depends(get_db)):
    text = get_text_by_id(db=db, name=text_name)
    xml = manager.generate_xml(text)
    manager.db_manager.create_xml(xml=xml, db=db)
    return xml.model_dump_json()

@app.get("/corpus/{text_name}")
def manager_main(text_name: str, db: Session = _fastapi.Depends(get_db)):
    return (manager.db_manager.read_xml(db=db, name=text_name)).model_dump_json()

@app.get("/corpus/{text_name}/view", response_class=HTMLResponse)
def index(request: _fastapi.Request):
    return templates.TemplateResponse(
        request=request, name="xml_viewer.html"
    )

@app.get("/corpus/{text_name}/search")
def search(text_name, tag: str, db: Session = _fastapi.Depends(get_db)):
    xml = manager.db_manager.read_xml(name=text_name, db=db)
    return manager.search(tag=tag, xml=xml)

@app.get("/gpt/get_synonyms_antonyms/{word}")
def semantic_analysis(word: str):
    index = word.index('Слово')
    res = word[:index]
    definition = (manager.get_definition(word=res))
    if definition == None:
        definition = get_definition(word=res)
    print(definition)
    synonyms = get_synonyms(word=res)
    antonyms = get_antonyms(word=res)
    return definition, synonyms, antonyms

@app.get("/gpt/chatting/{message}")
def gpt_chat(message: str):
    response = chatting(message)
    return(response)

@app.get("/gpt/chatting", response_class=HTMLResponse)
def index(request: _fastapi.Request):
    return templates.TemplateResponse(
        request=request, name="test.html"
    )
