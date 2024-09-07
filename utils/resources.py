from fastapi import HTTPException, status, UploadFile
import os
from unstructured.partition.pdf import partition_pdf
import pytesseract
import base64



output_path = os.path.join(os.getcwd(), "output")

def extract_text_from_docs(docs:list):
    try:
        elements=extract_elements(docs=docs)
        text_elements, table_elements, image_elements=extract_text_from_elements(doc_elements=elements)
        return text_elements, table_elements, image_elements
    except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=e.args)
    
    
def extract_elements(docs:list):
    try:
        doc_elememnts=list()
        for doc in docs:
            element = partition_pdf(
                filename=os.path.join(doc),
                extract_images_in_pdf=True,
                infer_table_structure=True,
                chunking_strategy="by_title",
                max_characters=4000,
                new_after_n_chars=3800,
                combine_text_under_n_chars=2000,
                image_output_dir_path=output_path,
            )
            
            doc_elememnts.append(element)
        return doc_elememnts
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=e.args)
        
    
    

def extract_text_from_elements(doc_elements:list): 
    try:
        text_elements = []
        table_elements = []
        image_elements = []

        # Function to encode images
        def encode_image(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')

        for element in doc_elements:
            if 'CompositeElement' in str(type(element)):
                text_elements.append(element)
            elif 'Table' in str(type(element)):
                table_elements.append(element)
                
                
        for image_file in os.listdir(output_path):
            if image_file.endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(output_path, image_file)
                encoded_image = encode_image(image_path)
                image_elements.append(encoded_image)
                

        table_elements = [i.text for i in table_elements]
        text_elements = [i.text for i in text_elements]

        return text_elements, table_elements, image_elements
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=e.args)
        