# 📦 StockFlow – Backend Engineering Case Study

Welcome! 👋  
This repository contains my solution for the **StockFlow Inventory Management System** case study as part of the Backend Engineering Intern assessment.

---



## ✅ Case Study Parts

1. **Code Review & Debugging**
   - Cleaned up and improved the given product creation API.
   - Added proper validation, error handling, and transaction safety.

2. **Database Design**
   - Designed a scalable relational schema using MySQL.
   - Covered support for warehouses, inventory, suppliers, and bundled products.

3. **API Implementation**
   - Wrote logic for a low-stock alert API with conditions like recent sales, thresholds, and supplier info.

---

## 💾 How to Run the Code (Optional)

> Only if you want to test it locally.

1. Make sure Python 3.x and MySQL are installed.
2. Install Flask and SQLAlchemy:
   ```bash
   pip install Flask SQLAlchemy
   ```
3. Set up your database using the SQL file:
   ```bash
   mysql -u your_user -p < stockflow_schema.sql
   ```
4. Run the Flask app files (e.g.):
   ```bash
   python product_create_api.py
   ```

---

## 🙋 Assumptions Made

- Products can exist in multiple warehouses.
- Some fields (e.g., description) are optional during product creation.
- Sales are considered “recent” if they happened within the last 30 days.
- SKU is globally unique.
- Bundles can be static or dynamically calculated.

> For a full list of assumptions, check the end of `stockflow_case_study_solution.md`.

---



Thanks for reviewing the project! 
