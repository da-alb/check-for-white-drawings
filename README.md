# PDF Analyzer for white drawings and small files

This Python script analyzes PDF files within a specified folder (including subfolders) to identify two main issues:

1.  **PDFs containing white drawings:** It detects PDFs that contain completely white images with a width greater than 1200 pixels. This can be indicative of scanning or conversion errors where blank pages or drawings are not rendered properly.
2.  **PDFs smaller than 20 KB:** It flags PDF files that are smaller than 20 kilobytes, which might suggest incomplete or empty documents.

**Key Features:**

*   **Date Filtering:** The script processes only PDF files created on a specific date (by default, today's date). You can override this to process files from a different date if needed for debugging.
*   **Recursive Folder Traversal:** It analyzes all PDF files within a specified folder and its subfolders, making it easy to process a large number of documents.
*   **File Size Check:** It efficiently identifies and skips files smaller than 20 KB, avoiding unnecessary processing.
*   **Image Analysis:** It utilizes the PyMuPDF (fitz) and Pillow (PIL) libraries to extract images from PDFs and determine if they are entirely white and larger than 1200px in width.
*   **Email Reporting:** If any issues are found, the script sends an email report containing two HTML tables: one listing the PDFs with large white images and another listing the small-size PDFs. The report includes both the full path and the filename for each problematic PDF.
*   **Email CC Support:** You can specify multiple CC recipients in the email report.
*   **Execution Time:** The report also includes the script's execution time in seconds.

**Dependencies:**

*   **PyMuPDF (fitz):**  A powerful PDF manipulation library. Install it via pip:
    ```bash
    pip install pymupdf
    ```
*   **Pillow (PIL):** A library for image processing. Install it via pip:
    ```bash
    pip install pillow
    ```

**How to Use:**

1.  **Install Dependencies:** Make sure you have installed PyMuPDF and Pillow.
2.  **Configure Parameters:**
    *   **`folder_path`:** Modify this variable in the `__main__` section to point to the root folder you want to analyze (e.g., `"M:\\FileTec\\PDF\\2025"`).
    *   **`target_date`:** By default, it processes today's files. For debugging, you can uncomment and set `target_date` to a specific date (e.g., `datetime.date(2025, 1, 20)`).
    *   **Email Configuration:** Update the following variables in the `__main__` section with your email settings:
        *   `sender_email`
        *   `recipient_email`
        *   `cc_emails` (a list of email addresses)
        *   `smtp_server`
        *   `smtp_port`
        *   `smtp_password`
3.  **Run the Script:** Execute the Python script.
    ```bash
    python your_script_name.py
    ```

**Output:**

*   **Console:** The script will print "Email sent successfully." if issues are found and an email report is sent. Otherwise, it will print "No issues found for PDFs created on \[date]."
*   **Email:** If any problematic PDFs are found, an email will be sent to the specified recipients, including the CC addresses. The email will contain two HTML tables:
    *   **PDFs with white images:** Lists the full path and filename of PDFs containing large white images.
    *   **PDFs smaller than 20 KB:** Lists the full path and filename of PDFs smaller than 20 KB.
    *   **Execution Time:** Shows how long the script took to run.

**Example Email Report:**

The email subject will be "PDF con problemi". The body will contain the following (if issues are detected):

```html
<html>
<body>
    <p><strong>Execution Time:</strong> 12.34</p>
    <p>Ecco i PDF con problemi:</p>
    <h3>PDF con disegni bianchi:</h3>
    <table border="1" style="border-collapse: collapse;">
        <tr>
            <th>Full Path</th>
            <th>Filename</th>
        </tr>
        <tr><td>M:\FileTec\PDF\2025\example1.pdf</td><td>example1.pdf</td></tr>
        <tr><td>M:\FileTec\PDF\2025\subdir\example2.pdf</td><td>example2.pdf</td></tr>
    </table>
    <h3>PDF più piccoli di 20 KB:</h3>
    <table border="1" style="border-collapse: collapse;">
        <tr>
            <th>Full Path</th>
            <th>Filename</th>
        </tr>
        <tr><td>M:\FileTec\PDF\2025\small.pdf</td><td>small.pdf</td></tr>
    </table>
</body>
</html>