# services/cloudinary_service.py
import cloudinary.uploader
from fastapi import UploadFile


def upload_photo(file: UploadFile, description: str, user_id: int) -> str:
    
    """
    The upload_photo function takes in a file, description and user_id.
        It then uploads the image to cloudinary using the cloudinary library.
        The uploaded image is then returned as a secure url.
    
    :param file: UploadFile: Upload the file to cloudinary
    :param description: str: Store the description of the photo
    :param user_id: int: Identify the user who uploaded the photo
    :return: The secure_url of the image uploaded to cloudinary
    :doc-author: Trelent
    """
    uploaded_image = cloudinary.uploader.upload(file.file,
                                                folder="Webcore",
                                                transformation=[
                                                    {"width": 500, "height": 500, "crop": "fill"},
                                                    {"effect": "grayscale"},
                                                    {"quality": "auto"}
                                                ])
    return uploaded_image["secure_url"]

def update_photo(photo_id: int, file: UploadFile) -> str:
    
    # Логіка оновлення фото в Cloudinary
    """
    The update_photo function updates a photo in Cloudinary.
        Args:
            photo_id (int): The ID of the photo to update.
            file (UploadFile): The new image file to upload.
    
    :param photo_id: int: Specify the id of the photo that needs to be updated
    :param file: UploadFile: Pass the file to the function
    :return: A string with a link to the updated photo
    :doc-author: Trelent
    """
    pass
