# Website Change Monitor

This is a lightweight yet powerful project designed to monitor websites for changes. It leverages Python and Selenium to check for updates and includes a GitHub Actions workflow that automates the process on a defined schedule.

I use this project to track changes on my university portal for grade updates, but it can be adapted to monitor any website where tracking changes is important.

---

## Features
- Monitors a specified website for changes.
- Sends email notifications when changes are detected.
- Includes a GitHub Actions workflow to automate the monitoring process on a schedule.
- Flexible and easy to set up for your own use cases.

---

## Use Cases
- Monitoring a university portal for grade updates.
- Tracking updates to a blog or news page.
- Keeping an eye on price changes for a product.
- Monitoring any webpage for changes in content.

---

## How to Fork and Use This Project

### Step 1: Fork the Repository
1. Click the **Fork** button at the top-right corner of this repository to create your own copy.

### Step 2: Clone Your Forked Repository
```bash
git clone https://github.com/your-username/website-change-monitor.git
cd website-change-monitor
```

### Step 3: Create the `Test` Environment
1. Navigate to **Settings** > **Environments** in your forked repository.
2. Click **New environment** and name it `Test`.

### Step 4: Set Up Secrets
<ol>
<li>Generate the encryption secret. For that, run the following code:<br>
   Terminal: `pip3 install cryptography`, place in the venv if needed.<br>
   Script:<br>
<pre>
from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(key.decode())
</pre>
or just comment out these lines from the end.</li>
<li>Copy the generated code from the console to use it in the step 4.</li>
<li>Navigate to **Settings** > **Environments** > **Test** > **Add environment secret**.</li>
<li>Add the following secrets:

   | Secret Name      | Description                             |
   |------------------|-----------------------------------------|
   | `EMAIL`          | Your email address                     |
   | `EMAIL_PASSWORD` | Password or app-specific password for your email |
   | `LOGIN_USERNAME` | Username for the website to monitor     |
   | `LOGIN_PASSWORD` | Password for the website to monitor     |
   | `ENCRYPTION_KEY` | Key, generated in Step 1                |
   </li>
<li>The workflow will start atomatically and the script will be run every 20 Minutes (you can find the runs under **Actions**), the time can be changed at .github/workflows/run_script.yml, line 5. </li>
</ol>

### Step 6: Allow Github Actions to read and write artefacts
It is needed to update content_file.txt every run.
For that, go to Settings -> Actions -> General -> Scroll to the bottom to 'Workflow permissions' and select 'Read and write permissions'.

### [optional] Step 7: Run the Workflow manually
1. Go to the **Actions** tab in your repository.
2. Select the **Run Python Script** Workflow at the top left and click **Run workflow** to start the monitoring process. Without it, the process

### Step 8: Set Up the Project to Test Locally

1. **Create a Virtual Environment**: Run `venv create` to set up a virtual environment.
2. **Install Dependencies**: Import the required packages by running `requirements.txt`.
3. **Add a `.env` File**: Create a file named `.env` and add your secrets in the following format:
   <pre>
   EMAIL='vika.vovchenkoo@gmail.com'
   EMAIL_PASSWORD='password from email address to send emails'
   LOGIN_USERNAME='login from the website'
   LOGIN_PASSWORD='password from the website'
   </pre>
4. **Run the Script**: Execute the script to test its functionality.
5. **Adapt to Your Needs**: Modify the script according to the documentation provided below.

---

## Technical Overview

### How the Project Works
The main script, `script.py`, orchestrates the entire process. Here's an outline of its functionality:

1. **Fetch Website Content**
   - The script logs into a website and retrieves the required elements.
   - For websites requiring authentication, login steps are included. If you do not need a login or any steps, you can remove lines 50–71 in the script.
   - Customize the steps based on your needs. You can add more URLs, steps, fields, or anything necessary to extract the desired data. Remove 'options=options' from line 42 to remove headless mode and allow to see the steps if needed.
   - For element selection, the script uses XPath. To find an XPath:
     - Open developer tools in your browser (F12).
     - Select the desired element.
     - Right-click and choose "Copy > XPath".
   - Update `XPATH_TRACK_AREA` to match the parent element containing the information you want to track (e.g., a price field, a feed, or a table with university marks).
   - Adjust `.github/workflows/run_script.yml` for your requirements:
     - Modify check intervals (line 5).
     - Update the GitHub environment name (line 11).
     - Configure environment variables (lines 79-82). If login isn't needed, remove those variables or add new ones if required.
   - Keep `.env` listed in `.gitignore` to prevent exposing sensitive data.

2. **Compare Content**
   - The script compares the current website content with the previous content stored locally.

3. **Save Content**
   - Any changes are saved to `content_file.txt`. The format it outerHTML of the parent element (`XPATH_TRACK_AREA`).

---

## Contributing
Contributions are welcome! If you have ideas for improvements, feel free to:
- Fork the repository.
- Create a new branch for your changes.
- Submit a pull request.

---

## License
This project is open-source and available under the [MIT License](LICENSE).

---

Feel free to adapt this project to your own needs and use it for tracking changes on your favorite websites! If you find it helpful or have suggestions, I'd love to hear from you. 😊
