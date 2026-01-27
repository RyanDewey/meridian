# Meridian 🧭

**Meridian** is an end-to-end data pipeline for measuring, analyzing, and visualizing **local business demand**.

Built as a portfolio-grade systems project, Meridian ingests raw public data, performs spatial and statistical transformations, and produces actionable demand signals that help entrepreneurs and operators answer a fundamental question:

> *Where should a business open next — and why?*

The project is designed to mirror **real-world data engineering workflows**, combining Python-based ingestion and transformation with SQL-driven analytics and geospatial reasoning.

---

## 🎯 Purpose

Meridian was created to:

* Quantify unmet demand for specific business types in a city
* Combine disparate public datasets into a unified analytical model
* Explore how data pipelines evolve into decision-making systems
* Serve as a foundation for future ML-driven location intelligence

---

## ✨ Core Features

* 🗺️ **Geospatial demand modeling** using real geographic boundaries
* 📊 **Multi-source data ingestion** (demographics, POIs, zoning)
* 🧮 **Demand scoring formulas** per location
* 🧹 **Clean transform layer** separating raw and analytical data
* 🧠 **SQL-driven insights** for transparency and iteration

---

## 🧠 System Overview

Meridian follows a classic analytical data pipeline architecture:

1. **Extract**
   Raw datasets are pulled from public sources such as:

   * Census / demographic data
   * Points-of-interest (business listings)
   * Geographic boundary files (ZIPs, tracts, regions)

2. **Load**
   Raw data is loaded into a relational database with spatial support.

3. **Transform**
   Transformations are applied to:

   * Normalize schemas
   * Perform spatial joins
   * Aggregate metrics per geographic unit

4. **Analyze**
   SQL queries compute demand signals such as:

   * Business density vs population
   * Demand-per-capita ratios
   * Underserved area indicators

5. **Output**
   Results are surfaced as:

   * Tables for analysis
   * Heatmap-ready datasets

---

## 🧱 Project Structure

```
meridian/pipeline
├── /extract         # Data extraction scripts
├── transform/       # Cleaning and transformation logic
    └── sql/         # Analytical SQL queries
├── utils/           # Helper files
├── main.py          # Entry point
└── README.md
```

---

## 🗺️ Geospatial Focus

Meridian makes heavy use of spatial reasoning:

* Point-in-polygon joins (businesses → regions)
* Area-based normalization
* Geographic aggregation (ZIP, tract, neighborhood)

Spatial accuracy and interpretability are prioritized over black-box scoring.

---

## 📈 Example Demand Signals

Meridian can produce insights such as:

* High population, low business density zones
* Areas with strong demographic fit but weak supply
* Comparative rankings of regions within a city

These signals are intentionally explainable and tunable.

---

## 🔧 Design Principles

* **Transparency over magic** – Clear formulas instead of opaque models
* **SQL-first analytics** – Easy iteration and validation
* **Incremental complexity** – Built to evolve toward ML, not start there
* **Realistic data workflows** – Mirrors industry data pipelines

---

## 🛣️ Roadmap

* [ ] Expand to multiple cities
* [ ] Add more business categories
* [ ] Improve demand formulas
* [ ] Introduce ML-assisted demand prediction
* [ ] Interactive visualization layer

---

## 🎓 Why This Project Matters

Meridian demonstrates:

* End-to-end **data pipeline design**
* Practical **geospatial analytics**
* Strong separation of concerns (ingest, transform, analyze)
* How data engineering supports **real business decisions**

