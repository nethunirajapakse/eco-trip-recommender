# CeylonWild

A rule-based, light-weight expert recommender system designed to suggest **ecologically friendly Sri Lankan travel destinations** tailored to user constraints, preferences, and desired activities. 

Built combining deterministic expert system logic with a modern API layer, CeylonWild serves as an ideal framework for research, prototypes, and interactive pedagogy in **sustainable tourism** and **knowledge-based systems**.

---

## ✨ Key Features

* **Rule-Based Destination Scoring:** Utilizes a CLIPS-driven expert system engine to translate complex user profiles and environmental constraints into accurate destination suitability metrics.
* **Multi-Criteria Preference Engine:** Filters and ranks ecological sites dynamically based on:
  * **Geographical & Climatic Factors:** Region and climate alignment.
  * **Logistical Dimensions:** Physical difficulty thresholds and destination popularity levels.
* **Activity-Based Match Ranking:** Cross-references and sorts recommended locations by density of user-preferred activities.
* **Mathematical Normalization:** Outputs both raw rule-weights and normalized scores, allowing seamless, objective comparison across diverse ecological spots.
* **Rich Native Knowledge Base:** Backed by an extensible, cached knowledge base containing granular metadata (activities, specialized ecological features, regional data).
* **API-Driven Architecture:** Ready-to-consume Flask backend making it fully compatible with modern web or mobile user interfaces.

---

## ⚙️ Tech Stack

The repository features a decoupled architecture blending an algorithmic pythonic engine with a strongly-typed web interface/orchestration layer:

* **Backend Logic & Inference Engine:** Python, Flask, `clipspy` (CLIPS integration)
* **Type-Safe Application Layer:** TypeScript, JavaScript

---

## 🚀 Getting Started

### Prerequisites
* Python 3.9+
* Node.js & npm / yarn (for frontend/TypeScript tooling)
* [CLIPS core libraries](https://www.clipsrules.net/) (if compiling `clipspy` natively)

### Backend Installation & Setup
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/nethunirajapakse/CeylonWild.git](https://github.com/nethunirajapakse/CeylonWild.git)
   cd CeylonWild
   ```

2. **Set up a Python virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

```


3. **Install backend dependencies:**
```bash
pip install -r requirements.txt

```


4. **Run the Flask Development Server:**
```bash
flask run

```



### Frontend / Tooling Setup

Install the necessary Node modules for the TypeScript layer:

```bash
npm install
npm run build

```

---

## 🧠 Architecture Overview

CeylonWild separates data representation, expert inference, and user access into a clean three-tier pipeline:

```text
┌────────────────────────┐      ┌────────────────────────┐      ┌────────────────────────┐
│      User Input        │      │    CLIPS Inference     │      │   Normalized Output    │
│  (Climate, Activities, ├─────►│  Evaluates rules against│─────►│ Ranked Recommendations │
│  Difficulty Limits)    │      │  Destination Facts     │      │  via Flask REST API    │
└────────────────────────┘      └────────────────────────┘      └────────────────────────┘

```

1. **Facts (Knowledge Base):** Contains explicit metadata regarding Sri Lankan eco-destinations (e.g., Sinharaja Rain Forest, Ella, Horton Plains).
2. **Rules (Production System):** Production rules written in CLIPS determine how conflicting parameters (e.g., matching low difficulty against high terrain isolation) resolve into quantitative scores.
3. **Inference API:** Flask surfaces execution hooks to trigger the agenda, assert user tokens as temporary facts, run the rules, and extract the sorted results.

---


