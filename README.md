
# **VeinPay — Contactless Palm Vein Authentication System**

VeinPay is a next-generation biometric authentication platform that replaces physical cards, cash, smartphones, and PIN-based systems with **AI-powered contactless palm-vein recognition**.  
Using advanced image preprocessing, deep neural embeddings, and secure database storage, VeinPay enables **fast, private, and fraud-proof identity verification**.

---

## 🚀 **Key Features**

- **Contactless Palm Vein Authentication**  
  Uses NIR/RGB images to extract unique sub-dermal vein patterns.

- **MobileNetV2 Neural Embeddings**  
  Deep learning–based feature extraction ensures high accuracy and reliability.

- **Advanced Preprocessing Pipeline**  
  Includes contrast enhancement, ROI selection, normalization, and vein map extraction.

- **FastAPI Backend**  
  High-performance API for registration, matching, and storage.

- **MongoDB (Local or Cloud) Integration**  
  Secure storage of vector embeddings for user identification.

- **Modern Streamlit Frontend**  
  Includes custom dark UI, glass cards, gradient buttons, animations, and camera input.

- **Modular & Extensible Architecture**  
  Easily extendable for edge devices, NIR hardware, or FPGA acceleration.

---

##  **How VeinPay Works**

### 1️⃣ Image Acquisition  
User captures a palm image using:
- RGB camera (prototype)
- NIR camera (hardware-ready)

### 2️⃣ Preprocessing  
Pipeline includes:
- ROI extraction  
- Noise reduction  
- Level-set filtering  
- Histogram equalization  
- Vein map enhancement  

### 3️⃣ Feature Extraction  
MobileNetV2 generates a **1280-dimensional embedding vector**.

### 4️⃣ Storage  
Embeddings stored in MongoDB with a user ID.

### 5️⃣ Authentication  
Cosine similarity between new & stored embeddings →  
If score ≥ threshold → **Match**

---

##  **System Architecture**

```

```
         ┌──────────────────────┐
         │      Streamlit UI    │
         │  (Register / Match)  │
         └───────────┬──────────┘
                     │
                     ▼
         ┌──────────────────────┐
         │      FastAPI         │
         │ (Preprocess + ML)    │
         └───────────┬──────────┘
                     │
                     ▼
         ┌──────────────────────┐
         │     MobileNetV2      │
         │   Feature Embedding  │
         └───────────┬──────────┘
                     │
                     ▼
         ┌──────────────────────┐
         │       MongoDB        │
         │ (User + Embeddings)  │
         └──────────────────────┘
```

```

---

##  **Tech Stack**

### **Backend**
- FastAPI  
- Python 3.13  
- OpenCV  
- scikit-image  
- TensorFlow (MobileNetV2)  
- NumPy  

### **Database**
- MongoDB Atlas (Cloud)  
- MongoDB Local (Docker)  

### **Frontend**
- Streamlit  
- Custom CSS  
- Camera input  

---

## 📁 **Project Structure**

```

VeinPay/
│
├── backend/
│   ├── main.py
│   ├── utils/
│   │   ├── mobilenet.py
│   │   ├── preprocess.py
│   │   └── extract_vein.py
│   └── db/
│       └── database.py
│
├── streamlit_app/
│   ├── app.py
│   ├── register_page.py
│   ├── match_page.py
│   ├── utils.py
│   ├── config.py
│   └── styles.css
│
└── README.md

````

---

##  **Setup Instructions**

### **1. Clone the Repository**
```bash
git clone https://github.com/nikhilanandd/Veinpay.git
cd VeinPay
````

### **2. Create a Virtual Environment**

```bash
uv venv
source .venv/bin/activate
```

### **3. Install Dependencies**

```bash
uv sync
```

### **4. Setup MongoDB**

#### **Option A — Local (Docker)**

```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

#### **Option B — Cloud**

Add your connection string in `.env`:

```
MONGO_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/
```

### **5. Run the Backend**

```bash
uvicorn backend.main:app --reload
```

### **6. Run the Frontend**

```bash
cd streamlit_app
streamlit run app.py
```

---

## 🧪 **API Endpoints**

### **Register User**

```
POST /register?user_id=<id>
```

### **Match User**

```
POST /match?user_id=<id>
```

### **Health Check**

```
GET /
```

---

## 🔒 **Security Advantages**

| Risk in Existing Systems             | How VeinPay Solves It                              |
| ------------------------------------ | -------------------------------------------------- |
| Cards/phones can be stolen or cloned | Internal sub-dermal vein patterns cannot be forged |
| PIN theft & skimming attacks         | No PINs or physical devices needed                 |
| Spoofing fingerprints                | Requires live blood flow                           |
| Privacy concerns                     | No raw images stored — embeddings only             |
| Dependence on physical tokens        | Authentication is inherent to the user             |

---

##  **Future Scope**

* Custom NIR palm-vein sensor hardware
* FPGA/TPU acceleration
* Zero-knowledge biometric verification
* Merchant SDK (web, mobile, kiosk)
* Federated learning for privacy-preserving training
* Blockchain-based identity ledger
* Multi-modal biometrics (vein + gait + voice)

---

## 🤝 **Contributors**

* **Nikhil Anand** — Lead Developer & Architect
* Open for research & collaboration

---

## 📜 **License**

This project is licensed under the **GNU AFFERO GENERAL PUBLIC LICENSE**.

---

## ⭐ **Support the Project**

If you like this project, consider starring the repository:


⭐️ Star this repo to show your support!



