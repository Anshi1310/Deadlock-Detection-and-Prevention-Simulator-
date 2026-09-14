# Deadlock Detection and Prevention Simulator
📌 Deadlock Detection & Prevention Simulator

An interactive web-based simulator built using HTML, CSS, JavaScript, and Flask (Python) to visualize deadlock detection, deadlock prevention, and Banker’s Algorithm.
This project was developed as part of a PBL (Project-Based Learning) Team Project, and I contributed the entire frontend interface and UI design.

## 🎯 Project Objective

The objective of this project is to provide an interactive learning environment for understanding deadlock detection and prevention in Operating Systems.

The simulator allows users to experiment with process and resource allocations and observe safety checks, safe sequences, deadlock states, and resource-request decisions.

## 🚀 Features

🔹 Deadlock Detection

Computes Need Matrix, Work Vector, and Safe Sequence

Generates Wait-For Graph (WFG)

Displays step-by-step simulation and visualization

Identifies deadlocked processes, if any

🔹 Deadlock Prevention

Handles resource request scenarios

Determines if allocation is safe or unsafe

Visual feedback with color-coded alerts

🔹 Dynamic Matrix Input

Auto-generates input tables based on number of processes & resources

Matrix validation and error handling


🔹 UI & Visualization

Modern, responsive UI with Bootstrap

Mermaid.js graphs for WFG

Downloadable simulation output



## 🧠 Algorithms Implemented

Banker’s Algorithm (Safety Check + Resource Allocation)

Deadlock Detection Algorithm

Wait-For Graph analysis

Need matrix calculation



## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- Bootstrap
- JavaScript
- Mermaid.js

### Backend
- Python
- Flask
- Jinja2


## 📂 Project Structure

```text
Deadlock-Detection-and-Prevention-Simulator/
│
├── static/
│   └── style.css
│
├── templates/
│   ├── index.html
│   └── result.html
│
├── screenshots/
│   ├── main-interface.png
│   ├── simulation-result.png
│   └── step-by-step.png
│
├── app.py
├── README.md
├── LICENSE
└── .gitignore
```


## 📸 Screenshots

### Main Interface
The simulator provides separate modes for deadlock detection and prevention, with dynamic process and resource matrix inputs.

![Main Interface](screenshots/main-interface.png)

### Simulation Result
The simulator calculates the Need Matrix and determines the Safe Sequence for the given system state.

![Simulation Result](screenshots/simulation-result.png)

### Step-by-Step Analysis
The simulator provides a step-by-step breakdown of the safety check, showing the Need Matrix, Work Vector, allocation decisions, and process completion.

![Step-by-Step Analysis](screenshots/step-by-step.png)



## ▶️ How to Run the Project Locally

### 1. Install dependencies

```bash
pip install flask
```
### 2. Run the Flask app
```bash
python app.py
```
### 3. Open the application

Open your browser and visit:
```bash
http://127.0.0.1:5050/
```

## 👩‍💻 My Contribution

I designed and developed the complete frontend interface and UI/UX for the project.

My contributions included:

- Designed the overall UI layout and responsive interface
- Developed dynamic process and resource matrix components
- Implemented frontend validation and error handling
- Integrated Flask/Jinja2 templates with the frontend
- Implemented Mermaid.js-based Wait-For Graph visualization
- Designed the simulation result and step-by-step analysis views
- Developed the user interaction workflow


## 📄 License

This project is licensed under the MIT License.
