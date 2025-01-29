# PDF Analyzer for White Drawings and Small Files

This Python script analyzes PDF files within a specified folder (including subfolders) to identify two main issues:

1.  **PDFs containing white drawings:** It detects PDFs that contain completely white images with a width greater than 1200 pixels. This can be indicative of scanning or conversion errors where blank pages or drawings are not rendered properly.
2.  **PDFs smaller than 20 KB:** It flags PDF files that are smaller than 20 kilobytes, which might suggest incomplete or empty documents.

**Project Structure:**
```
pdf_analyzer/
├── config.py
├── config.yaml
└── main.py
```
**Key Features:**

*   **Date Filtering:** The script processes only PDF files created on a specific date. The date is configurable via a `config.yaml` file and defaults to today's date.
*   **Recursive Folder Traversal:** It analyzes all PDF files within a specified folder and its subfolders, making it easy to process a large number of documents.
*   **File Size Check:** It efficiently identifies and skips files smaller than 20 KB, avoiding unnecessary processing.
*   **Image Analysis:** It utilizes the PyMuPDF and Pillow (PIL) libraries to extract images from PDFs and determine if they are entirely white and larger than 1200px in width.
*   **Email Reporting:** If any issues are found, the script sends an email report containing two HTML tables: one listing the PDFs with large white images and another listing the small-size PDFs. The report includes both the full path and the filename for each problematic PDF.
*   **Email CC Support:** You can specify multiple CC recipients in the email report by configuring the `cc` array in the `config.yaml` file.
*   **Execution Time:** The report also includes the script's execution time in seconds, passed as a parameter to the email function.

**Dependencies:**

*   **PyMuPDF:** A powerful PDF manipulation library. Install it via pip:

    ```bash
    pip install pymupdf
    ```
*   **Pillow (PIL):** A library for image processing. Install it via pip:

    ```bash
    pip install pillow
    ```
*   **PyYAML:** A library for parsing YAML files. Install it via pip:

    ```bash
    pip install pyyaml
    ```

**How to Use:**

1.  **Install Dependencies:** Make sure you have installed PyMuPDF, Pillow, and PyYAML.
2.  **Configure Parameters (`config.yaml`):**
    *   **`folder.path`:** Modify this parameter in the `config.yaml` file to specify the root folder you want to analyze (e.g., `"C:\\PDF"`). **Important:** You will need to manually update the year in this path each year as needed.
    *   **`date_settings`:**
        *   To process today's files, set `use_today: true`.
        *   To process files from a specific date, set `use_today: false` and `specific_date: landlab-MM-DD` (e.g., `specific_date: 2023-12-20`).
        *   To process files from a certain number of days before today, set `use_today: false` and `days_offset: -N` (e.g., `days_offset: -7` for a week ago).
    *   **Email Configuration:** Update the following parameters in `config.yaml` with your email settings:
        *   `email.sender`
        *   `email.recipient`
        *   `email.cc` (an array of email addresses)
        *   `email.smtp_server`
        *   `email.smtp_port`
        *   `email.smtp_password`

    *   See [sample-config.yaml](sample-config.yaml) for a template.

3.  **Run the Script:**

    ```bash
    python main.py
    ```

**Output:**

*   **Console:** The script will print "Email sent successfully." if issues are found and an email report is sent. Otherwise, it will print "No issues found for PDFs created on \[date]."
*   **Email:** If any problematic PDFs are found, an email will be sent to the specified recipients, including the CC addresses. The email will contain two HTML tables:
    *   **PDFs with white images:** Lists the full path and filename of PDFs containing large white images.
    *   **PDFs smaller than 20 KB:** Lists the full path and filename of PDFs smaller than 20 KB.
    *   **Execution Time:** Shows how long the script took to run.

**Example Email Report:**

The email subject will be "PDF con problemi per il giorno \[date]" (PDF issues for \[date]). The body will contain the following (if issues are detected):

```html
<html>
<body>
    <p><strong>Execution Time:</strong> 12.34</p>
    <p>Here are the PDFs with issues:</p>
    <h3>PDFs with white drawings:</h3>
    <table border="1" style="border-collapse: collapse;">
        <tr>
            <th>Full Path</th>
            <th>Filename</th>
        </tr>
        <tr><td>C:\PDF\example1.pdf</td><td>example1.pdf</td></tr>
        <tr><td>C:\PDF\subdir\example2.pdf</td><td>example2.pdf</td></tr>
    </table>
    <h3>PDFs smaller than 20 KB:</h3>
    <table border="1" style="border-collapse: collapse;">
        <tr>
            <th>Full Path</th>
            <th>Filename</th>
        </tr>
        <tr><td>C:\PDF\small.pdf</td><td>small.pdf</td></tr>
    </table>
</body>
</html>

** TODO **

* Add an option to exclude certain subfolders.
* Manually update the 'folder.path' in config.yaml each year.
* Implement logging to a file for debugging purposes.
* Improve error handling for incorrect SMTP credentials.
* Allow configuration of the threshold for white image detection (currently set at 1200px width).