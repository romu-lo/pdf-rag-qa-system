from fastapi import FastAPI

from app.api.routes import router
from app.domain import answer_question, upload_files

app = FastAPI()
app.include_router(router)


# path1 = "../../resources/case_files/MN414_0224.pdf"
# path2 = "resources/case_files/WEG-CESTARI-manual-iom-guia-consulta-rapida-50111652-pt-en-es-web.pdf"

# result = upload_files([path2])
# print(result)

# answer = answer_question("What is the main purpose of the WEG Cestari manual?")
# print(answer)
