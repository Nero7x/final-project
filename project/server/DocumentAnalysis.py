import io
from PyPDF2 import PdfReader 
import spacy
import nltk as nltk
from server import ElemenrsFinder as EF
from server import ReletionshipFinder as RF
from server import GenerateDiagram as Gen

class DocumentAnalysis:

    def dataInitialization(file,file_extension,diagram_type):
        
        texts = ""
        if file_extension == ".txt":
            text = file.read().decode('utf-8') 
            texts = nltk.sent_tokenize(text)

        elif file_extension ==".pdf":
            reader = PdfReader(io.BytesIO(file.read()))
            text = ""
            for page in range(len(reader.pages)):
                text += reader.pages[page].extract_text()
            texts = nltk.sent_tokenize(text)
        nlp = spacy.load('en_core_web_sm')

        results = {}

        for text in texts:
            actor = []
            usecase = []
            ucr = []
            clas = []
            attr = []
            method = []
            doc = nlp(text)
            if diagram_type == 'usecase':
                actor = EF.ElementsFinder.findActor(doc)
                usecase = EF.ElementsFinder.findUsecase(doc,actor)
                ucr = RF.RelationshipFinder.findUsecaseRelationship(doc, actor)
            elif diagram_type == 'class':
                actor = EF.ElementsFinder.findActor(doc)
                clas = EF.ElementsFinder.findClass(doc)
                attr = EF.ElementsFinder.findAttributes(doc)
                method = EF.ElementsFinder.findMethod(doc,actor)

            results[text] = {
            'actors': actor,
            'usecases': usecase,
            'usecase relationship': ucr,
            'class': clas,
            'attributes': attr,
            'method' : method,
            }

        cleanResults = DocumentAnalysis.cleanDuplicates(results,texts)

        #for i,result in enumerate(results):
            #print(f"{i}- {result}: {results[result]}")
        if diagram_type == 'usecase':
            Gen.GenerateDiagram.GenerateUsecase(cleanResults)
        elif diagram_type == 'class': 
            Gen.GenerateDiagram.GenerateClassDiagram(cleanResults, results, texts)



    def cleanDuplicates(results, texts):
        cleanResults = {'actors':set(),
                        'usecases': set(),
                        'usecase relationship': set(),
                        'class': set(),
                        'attributes': set(),
                        'method' : set()}
        for text in texts:
            for actor in results[text]['actors']:
                cleanResults['actors'].add(actor)
            for actor in results[text]['usecases']:
                cleanResults['usecases'].add(actor)
            for actor in results[text]['usecase relationship']:
                cleanResults['usecase relationship'].add(actor)
            for actor in results[text]['class']:
                cleanResults['class'].add(actor)
            for actor in results[text]['attributes']:
                cleanResults['attributes'].add(actor)
            for actor in results[text]['method']:
                cleanResults['method'].add(actor)
        return cleanResults
