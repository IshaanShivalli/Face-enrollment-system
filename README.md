# Face Attendance System

A Windows desktop application for enrolling faces with a webcam, training a face-recognition model, recording attendance, and viewing or exporting records.

## Requirements

- Windows with a working webcam
- Python 3.12 (the repository includes a Windows CPython 3.12 `dlib` wheel)
- The packages listed in `requirements.txt`

Tkinter is included with the standard Windows Python installer.

## Installation

From the project directory, create and activate a virtual environment, then install the dependencies:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Create the directory used for generated model files:

```powershell
New-Item -ItemType Directory -Force output
```

The default settings are in `config/config.json`. Paths in that file are relative to the project directory. The enrollment application creates the dataset directories as needed.

## Workflow

Run these commands from the project directory, in order:

1. Enroll a person and capture face images:

   ```powershell
   python enroll.py
   ```

   Enter the person's numeric ID, name, and `config/config.json` in the application. Use the application controls to start or stop capture.

   Repeat enrollment for each person to recognize. Model training requires face images for at least two different people, each enrolled with a different ID.

2. Encode the captured faces:

   ```powershell
   python encode_faces.py
   ```

   Encodings are labeled from person-ID subfolders under `dataset/PROJECT`. If you add or recapture faces, run the encoder again before training.

3. Train the recognition model:

   ```powershell
   python train_model.py
   ```

4. Start attendance recognition:

   ```powershell
   python recognition.py
   ```

   Select **Start** to begin webcam recognition and **Exit** to close the application.

5. View attendance and enrollment records or export them as CSV:

   ```powershell
   python attendance_enroll_info_check_and_delete_id.py
   ```

The optional `unknown_face_enroll.py` script accepts an ID and name on the command line:

```powershell
python unknown_face_enroll.py --id 123 --name "Example Person"
```

It reads source images from the `unknown` directory. A different configuration file can be supplied with `--conf`.

## Configuration

The default `config/config.json` settings specify:

- `dataset_path` and `class`: where captured face images are stored
- `face_count`: the number of images captured for an enrollment
- `db_path`: the TinyDB enrollment database
- `encodings_path`, `recognizer_path`, and `le_path`: generated model files
- `detection_method`: the face-location method (`hog` by default)

## Generated and personal data

The dataset, enrollment database, attendance log, and generated model files can contain biometric or identifying information. Keep them private and handle them according to your organization's privacy requirements. These runtime files are excluded from Git by `.gitignore`.
