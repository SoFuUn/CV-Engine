# Automated Python CV Creator 📄🚀

An automated Python tool for dynamically generating modern, professional CVs in PDF format. The entire application is data-driven and controlled through a central JSON file. The layout adapts automatically: page one features a left-hand sidebar, while page two seamlessly switches to a mirrored right-hand sidebar to provide additional space for an extended technical profile.

The project is implemented using advanced object-oriented Python design principles, following clean architecture and maintainable coding standards.

## Features ✨

* **100% Data-Driven:** No code modifications are required for content or structural updates. Everything is managed through a single JSON configuration file.
* **Intelligent Multi-Page Layout:** Automatically detects the transition to page two, mirrors the sidebar to the right, and displays an extended technical profile.
* **Modern Text Rendering:** Produces clean, left-aligned text layouts that eliminate large spacing gaps commonly found in justified column text.
* **Custom Assets:** Easily replace the profile picture and contact icons through the `assets` folder. Supports automatic detection of `.png`, `.jpg`, and `.jpeg` files.
* **Cascading Fallback System:** A three-stage fallback mechanism (primary data → template file → built-in memory dictionary) prevents application crashes even if the data directory is missing.
* **Integrated Logging:** Comprehensive file and console logging with timestamps and line numbers for efficient debugging and error tracking.

---

# Project Structure 📂

```text
├── assets/                  # Visual assets (images & icons)
│   ├── mail.png             # Email icon (supports PNG, JPG, JPEG)
│   ├── phone.png            # Phone icon
│   ├── pin.png              # Address / location icon
│   └── portrait.jpg         # Profile picture (automatically detected via glob)
├── data/                    # Data input & templates
│   ├── cv_data.json         # Main content file
│   └── template_data.json   # Local backup template (fallback)
├── logs/                    # Automatically generated log files
│   └── cv_generator.log     # Error and system logs
├── output/                  # Output directory
│   └── Resume.pdf           # Generated multi-page PDF
├── main.py                  # Main application (execution, validation & orchestration)
├── lebenslauf.py            # PDF class architecture (FPDF2 extension with event handling)
└── README.md                # Project documentation
```

---

# Installation ⚙️

## 1. Requirements

Make sure Python **3.8 or later** is installed.

## 2. Install Dependencies

The project is built on the modern **fpdf2** library.

Install the required package:

```bash
pip install fpdf2
```

---

# Configuration & Customization 🛠️

## 1. Edit Resume Content (`data/cv_data.json`)

All resume content is maintained inside `cv_data.json`.

The logical section `technical_profile` is used to populate the extended sidebar on the second page.

Example structure:

```json
{
    "contact": {
        "name": "John Doe",
        "jobtitle": "Python Developer",
        "certificate": "PCEP, PCAP, PCPP1",
        "address": ["123 Example Street"],
        "email": ["john@example.com"],
        "phone": ["+1 555 123456"]
    },
    "profile_summary": "Passionate Python developer focused on clean software architecture...",
    "sections": {
        "Internships": [
            {
                "period": "2024 - Present",
                "title": "Senior Python Engineer",
                "company": "Tech Solutions Ltd."
            }
        ]
    },
    "technical_profile": {
        "programming_languages": [
            {"name": "Python", "level": 5},
            {"name": "SQL", "level": 4},
            {"name": "JavaScript", "level": 3}
        ],
        "tools_frameworks": [
            "Git & GitHub",
            "Docker",
            "Django",
            "Flask"
        ],
        "focus_areas": [
            "Object-Oriented Programming (OOP)",
            "Clean Code & PEP 8",
            "Test-Driven Development (TDD)"
        ]
    }
}
```

## 2. Replace Design Assets (`assets/`)

### Profile Picture

Replace the existing image inside the `assets` folder.

The script automatically detects any image whose filename begins with:

```
portrait.
```

Supported formats:

* PNG
* JPG
* JPEG

### Contact Icons

Replace the address, email, and phone icons with your own PNG or JPG files named:

* `pin`
* `mail`
* `phone`

Filename capitalization is ignored.

### Fault Tolerance

If any assets are missing, the application automatically generates simple geometric placeholders, ensuring that PDF generation never fails.

---

# Usage 🚀

Run the main application:

```bash
python main.py
```

After successful execution, your generated resume can be found at:

```text
output/Resume.pdf
```

---

# Robust Error Handling & Logging 📋

The application is designed for reliable production use.

* **JSON Validation:** Invalid JSON inside the primary data file is detected and results in a controlled error message instead of a Python crash.
* **Hierarchical Data Fallback:** If `cv_data.json` is unavailable, the application loads `template_data.json`. If that file is also missing, it automatically generates data from a built-in Python dictionary.
* **Logging:** All warnings and runtime events (such as missing images) are written to `logs/cv_generator.log` with precise timestamps and source line numbers, making debugging straightforward.
