import pymupdf
from PIL import Image
import io
import os
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from config import load_config

def is_white_image(image):
    # Check if an image is completely white and its width is larger than 1200px
    if image.width > 1200:
        img = image.convert("L")  # Convert to grayscale
        pixels = img.getdata()
        return all(p == 255 for p in pixels)
    return False


def process_pdfs_in_folder(folder_path, target_date):
    """
    Analyze PDFs in the folder and subfolders:
    1. Process only files with the creation date matching `target_date`.
    2. Skip files smaller than 20 KB.
    3. Check for white images larger than 1200px width.
    """
    pdfs_with_white_images = []
    small_size_pdfs = []

    # Iterate through all files in the folder and subfolders
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_path = os.path.join(root, file)

                # Check file creation date
                file_creation_date = datetime.date.fromtimestamp(os.path.getctime(pdf_path))
                if file_creation_date != target_date:
                    continue  # Skip files not created on the target date

                # Check file size
                file_size_kb = os.path.getsize(pdf_path) / 1024  # Size in KB
                if file_size_kb < 20:
                    small_size_pdfs.append(pdf_path)
                    continue  # Skip further processing for this file

                # Open the PDF and check for white images

                doc = pymupdf.open(pdf_path)
                has_large_white_image = False

                for page_num in range(len(doc)):
                    page = doc[page_num]
                    images = page.get_images(full=True)

                    for img_index, img in enumerate(images):
                        xref = img[0]
                        base_image = doc.extract_image(xref)
                        image_bytes = base_image["image"]
                        image = Image.open(io.BytesIO(image_bytes))

                        if is_white_image(image):
                            has_large_white_image = True
                            break  # Stop checking further images in this PDF

                    if has_large_white_image:
                        break  # Stop checking further pages in this PDF

                if has_large_white_image:
                    pdfs_with_white_images.append(pdf_path)

    return pdfs_with_white_images, small_size_pdfs

def send_email_with_results(white_image_results, small_size_results, sender_email, recipient_email, cc_emails, smtp_server, smtp_port, smtp_password):
    
    global target_date

    # Send an email with the results in a table format and CC recipients
    # Create the email content
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Cc"] = ", ".join(cc_emails)  # Add CC recipients
    message["Subject"] = f"PDF con problemi per il giorno {target_date}"

    # Build the HTML table for white image PDFs
    white_image_rows = "".join(
        f"<tr><td>{pdf}</td><td>{os.path.basename(pdf)}</td></tr>" for pdf in white_image_results
    )
    small_size_rows = "".join(
        f"<tr><td>{pdf}</td><td>{os.path.basename(pdf)}</td></tr>" for pdf in small_size_results
    )

    html_content = f"""
    <html>
    <body>
        <p><strong>Tempo di esecuzione:</strong> {execution_time}</p>
        <p>Ecco i PDF con problemi:</p>
        <h3>PDF con disegni bianchi:</h3>
        <table border="1" style="border-collapse: collapse;">
            <tr>
                <th>Full Path</th>
                <th>Filename</th>
            </tr>
            {white_image_rows}
        </table>
        <h3>PDF più piccoli di 20 KB:</h3>
        <table border="1" style="border-collapse: collapse;">
            <tr>
                <th>Full Path</th>
                <th>Filename</th>
            </tr>
            {small_size_rows}
        </table>
    </body>
    </html>
    """
    # Attach the HTML content to the email
    message.attach(MIMEText(html_content, "html"))
    
    # Send the email
    all_recipients = [recipient_email] + cc_emails
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, smtp_password)
        server.sendmail(sender_email, all_recipients, message.as_string())

# Main function
if __name__ == "__main__":
    #Load configuration
    config = load_config()
    if not config:
        exit(1)  # Exit if configuration loading fails

    # Get settings from the config dictionary
    sender_email = config['email']['sender']
    recipient_email = config['email']['recipient']
    cc_emails = config['email']['cc']
    smtp_server = config['email']['smtp_server']
    smtp_port = config['email']['smtp_port']
    smtp_password = config['email']['smtp_password']
    folder_path = config['folder']['path']
    
    # Get target_date from config
    target_date = config.get('target_date', datetime.date.today())

    # Measure start time
    start_time = time.time()

    # Process PDFs
    white_image_results, small_size_results = process_pdfs_in_folder(folder_path, target_date)

    # Measure end time and calculate execution duration
    end_time = time.time()
    execution_time = round(end_time - start_time, 2)  # Execution time in seconds

    if white_image_results or small_size_results:

        # Send the email
        send_email_with_results(white_image_results, small_size_results, sender_email, recipient_email, cc_emails, smtp_server, smtp_port, smtp_password)

        print("Email sent successfully.")
    else:
        print(f"No issues found for PDFs created on {target_date}.")