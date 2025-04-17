# 📚 Library Management System

A fully functional Library Management System with distinct access for **Admin** and **User**. It supports book management, memberships, transactions, and reporting with robust validation and user-friendly design.

---

## 🚀 Modules Overview

### 1. Maintenance Module *(Admin Only)*

- **Add/Update Book**
  - Type: Book/Movie (default: Book)
  - All fields mandatory
  - Shows errors on the same page

- **Add/Update Membership**
  - Duration: 6 months / 1 year / 2 years (default: 6 months)
  - All fields mandatory

- **User Management**
  - User Type: New / Existing (default: New)
  - Name: Mandatory
  - Validates all relevant fields

---

### 2. Reports Module *(Admin & User)*

- Search for available books
- **Validation**: At least one input (textbox or dropdown) is required
- **Errors**: Displayed on the same page
- **Results**: Table view with radio button selection

---

### 3. Transactions Module *(Admin & User)*

#### 📘 Book Issue
- **Book Name**: Required  
- **Author Name**: Auto-filled, non-editable  
- **Issue Date**: Cannot be earlier than today  
- **Return Date**: Auto = 15 days ahead (can be set earlier)  
- **Remarks**: Optional  

#### 📗 Return Book
- **Book Name**: Required  
- **Author & Issue Date**: Auto-filled  
- **Serial Number**: Required  
- **Return Date**: Editable  
- Submit navigates to **Fine Pay Page**

#### 💵 Fine Pay
- All fields auto-filled except:
  - **Fine Paid** (Checkbox)
  - **Remarks**
- **Validation**: Fine checkbox must be ticked if fine is due

---

## 🔐 Authentication

- Separate login pages for Admin and User  
- Password input is masked during typing

---

## 👥 Access Control

| Module       | Admin Access | User Access |
|--------------|--------------|-------------|
| Maintenance  | ✅ Yes       | ❌ No       |
| Reports      | ✅ Yes       | ✅ Yes      |
| Transactions | ✅ Yes       | ✅ Yes      |

---

## ✅ Global Features

- Basic UI formatting acceptable  
- Radio buttons for single-choice fields  
- Checkboxes for Yes/No inputs  
- Persistent “Chart” link on all pages (for navigation only, non-functional)

---

## 📌 Assumptions

- **Author Name**: Auto-filled, based on selected book  
- **Serial Number**: Unique for each book copy  
- **Return Date (in Return form)**: Editable to any date  
- **Fine Calculation**: Logic handled externally (outside this scope)

---

> ⚠️ All form inputs are validated. Errors are shown immediately on the same page if fields are missing or incorrect.
