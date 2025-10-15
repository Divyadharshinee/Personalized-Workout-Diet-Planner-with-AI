# Setup guide (Windows PowerShell)

This repo has a small helper script to create the backend virtual environment and install Python dependencies.

Backend (PowerShell)
1. Open PowerShell and go to the backend folder:
   ```powershell
   cd "c:\Users\Divyadharshinee\OneDrive\Desktop\IBM - AI & Cloud\personalized-fit\backend"
   ```

2. Run the setup script. To recreate the venv use the `-Recreate` flag:
   ```powershell
   .\setup-env.ps1
   # or to force recreation
   .\setup-env.ps1 -Recreate
   ```

3. Activate the venv (if not already activated):
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

4. Initialize the DB and start the backend:
   ```powershell
   python db_init.py
   python app.py
   ```

Frontend (PowerShell)
1. Open a new PowerShell window and go to the frontend folder:
   ```powershell
   cd "c:\Users\Divyadharshinee\OneDrive\Desktop\IBM - AI & Cloud\personalized-fit\frontend"
   ```

2. Install dependencies and start the dev server:
   ```powershell
   npm install
   npm start
   ```

Notes & troubleshooting
- If Pillow fails to build on your Python version, either:
  - Create the venv with Python 3.11 (recommended), or
  - Install Visual Studio "Build Tools for Visual Studio" with the C++ workload.
- If PowerShell complains about script execution when activating venv, run:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
  .\.venv\Scripts\Activate.ps1
  ```
