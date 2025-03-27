import azure.functions as func
import logging
from PIL import Image
import io
import os

app = func.FunctionApp()

@app.function_name(name="ImageProcessor")
@app.blob_trigger(
    arg_name="myblob",
    path="uploads/{name}",
    connection="AzureWebJobsStorage"
)
@app.blob_output(
    arg_name="outputBlob",
    path="processed/{name}",
    connection="AzureWebJobsStorage"
)
def process_image(myblob: func.InputStream, outputBlob: func.Out[bytes]):
    """Processes uploaded images by converting them to grayscale"""
    
    try:
        # 1. التحقق من نوع الملف
        if not myblob.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            logging.warning(f"Unsupported file type: {myblob.name}")
            return

        logging.info(f"Processing image: {myblob.name}, Size: {myblob.length} bytes")

        # 2. معالجة الصورة
        with Image.open(myblob) as image:
            # تحويل إلى تدرج الرمادي مع التحكم بالجودة
            grayscale_image = image.convert("L")
            
            # 3. حفظ النتيجة
            with io.BytesIO() as output:
                grayscale_image.save(
                    output,
                    format="PNG",
                    optimize=True,
                    quality=85  # مناسب للتوازن بين الجودة والحجم
                )
                output.seek(0)
                outputBlob.set(output.read())

        logging.info(f"Successfully processed {myblob.name}")

    except Image.UnidentifiedImageError:
        logging.error(f"Invalid image file: {myblob.name}")
    except Exception as e:
        logging.error(f"Unexpected error processing {myblob.name}: {str(e)}", exc_info=True)
        raise
