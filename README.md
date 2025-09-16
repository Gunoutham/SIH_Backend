### AI-Powered Rainwater & Groundwater Calculator`


### A smart FastAPI backend for sustainable water management.

-----

#### **Section 2: Introduction**

**(Create a new text block below the header with a short, engaging paragraph.)**

**Text:**
`This project provides a secure, multilingual API for calculating rainwater harvesting potential and financial payback. The core of the application is a specialized AI chatbot, built with Google Gemini, that guides users through a complex data collection process to deliver a comprehensive environmental and financial report.`

-----

#### **Section 3: Key Features**

**(Use an icon-based layout. Find icons in Canva for "API", "Security", "AI Bot", and "Globe".)**

  * **[Icon for API]**
    **FastAPI Backend:** High-performance, modern API for user management and AI interaction.
  * **[Icon for Security Shield]**
    **Secure Authentication:** User registration and login with secure password hashing (`werkzeug`).
  * **[Icon for Chat Bot]**
    **Specialist AI Assistant:** A rule-following Gemini chatbot that collects 11 data points for detailed calculations.
  * **[Icon for Globe/Languages]**
    **Full Multilingual Support:** Automatically detects user language and translates the entire conversation for a seamless experience.

-----

#### **Section 4: Technology Stack**

**(Use the official logos for each technology. You can search for these in Canva under "Elements".)**

`[Python Logo] [FastAPI Logo] [PostgreSQL Logo] [Google Gemini Logo] [LangChain Logo] [Werkzeug Logo]`

-----

#### **Section 5: Setup & Installation**

**(Create a step-by-step numbered list. Use a different background color for this section to make it stand out.)**

**1. Clone & Install**

  - Create a `requirements.txt` file and run `pip install -r requirements.txt`.

**2. Configure Database**

  - Ensure your PostgreSQL server is running.
  - Run the following SQL command to prepare your `userdata` table:
    ```sql
    ALTER TABLE userdata
    ADD COLUMN username VARCHAR(255) UNIQUE,
    ADD COLUMN email VARCHAR(255) UNIQUE,
    ADD COLUMN password VARCHAR(255);
    ```

**3. Set API Keys**

  - Create a `.env` file in the main project folder.
  - Add your secret keys:
    ```
    GEMINI_API_KEY=YOUR_GEMINI_KEY
    DETECTION_API_KEY=YOUR_DETECTLANGUAGE.COM_KEY
    ```

**4. Run the Server**

  - Launch the application from your terminal:
    `uvicorn main:app --reload`
  - Access the API docs at `http://12до7.0.0.1:8000/docs`.

-----

#### **Section 6: API Endpoints**

**(Create three distinct sections for each endpoint, using a "POST" tag for each.)**

**`POST` /register**
Creates a new user.
`{ "username": "newuser", "email": "user@email.com", "password": "securepassword123" }`

**`POST` /** (Login)
Logs in a user.
`{ "username": "newuser", "password": "securepassword123" }`

**`POST` /ask**
The main stateless chat endpoint. Sends the new user message and the entire chat history.
`{ "user_input": "My roof is 100 sq meters.", "chat_history": [...] }`
