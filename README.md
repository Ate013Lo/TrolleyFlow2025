# TrolleyFlow 2025  
**Optimizing GateGroup’s airline catering through intelligent automation and AI forecasting**

---

## Overview  
**TrolleyFlow** optimizes GateGroup’s catering operations by guiding operators with **real-time decisions** on alcohol bottles and other onboard items.  
It minimizes waste, ensures regulatory compliance, and transforms manual inspection tasks into a **smart, data-driven operation**.

---

## Key Features
- Intelligent decision system for **reuse, refill, discard, or replace** actions.  
- Airline-specific policies and regional compliance built into every workflow.  
- Forecasting API (built with **Google AI Studio**) to predict bottle usage and optimize supply.  
- Scanning interface for **Pick-and-packers**, reducing manual judgment and error.  
- Scalable architecture to extend beyond liquids — napkins, plates, and perishable items.  

---

## Tech Stack  
| Layer | Technology |
|-------|-------------|
| **Frontend / UI** | Figma Prototype |
| **Backend** | Python / Visual Studio Code |
| **AI Forecasting** | Google AI Studio |
| **Data Storage** | Excel + Custom Dataset |
| **Version Control** | GitHub |

---

## How It Works
1. The **Pick-and-packer** logs in and selects the assigned airline.  
2. The system loads the flight’s inventory and policies.  
3. Each bottle is scanned; the system recommends the correct action.  
4. Forecasting API predicts next-flight consumption and refilling needs.  
5. Decisions are logged for performance tracking and sustainability metrics.  

---

## ERD

## Clone the repository
git clone https://github.com/Ate013Lo/TrolleyFlow2025.git
cd TrolleyFlow2025


---

## Future Scope

- Integrate live data with GateGroup systems for automated inventory sync.

- Expand forecasting model for food and packaging materials.

- Deploy full cloud-based dashboard for analytics and sustainability tracking.

## Contributors

| Name | Role |
|-------|-------------|
| **Luis Angelo Zapata Jimenez** |  Frontend / UI |
| **José Ángel Rodriguez Chairez** | Backend  |
| **Maximo Diego Gamon Simental** | Backend |
| **Atenea López Corona** | AI Forecasting |

# TrolleyFlow – System Architecture & User Manual

---

## Entity Relationship Diagram (ERD)

Below is the entity-relationship model that structures the **TrolleyFlow** data ecosystem.  
It represents how airlines, bottles, policies, and pick-and-pack decisions are connected.


# Figma Prototype – User Flow (Pick-and-Pack Journey)

The following section presents the visual flow of TrolleyFlow’s Pick-and-pack interface, built in Figma.
Each frame represents a key step in the operator’s interaction.

## Frame 1 – Login & Airline Selection

![Imagen de WhatsApp 2025-10-26 a las 06 06 22_ee4d488e](https://github.com/user-attachments/assets/8f880ccd-4abf-44e7-8477-873999c95f07)

Explanation:
The Pick-and-packer logs into the system and selects their assigned airline.


## Frame 2 – Flight Overview & Inventory Load

![Imagen de WhatsApp 2025-10-26 a las 06 08 32_51420382](https://github.com/user-attachments/assets/de392a7a-de08-4092-8af5-62f6058aed2f)

Explanation:
The operator views the upcoming flight list and the expected bottle inventory.
The interface automatically loads the airline’s policies and assigned flights.

## Frame 3 – Flight Operations Screen

![Imagen de WhatsApp 2025-10-26 a las 06 19 07_20c648ea](https://github.com/user-attachments/assets/7245032c-ee05-41d6-97da-c8675bf36a8b)

Explanation:
This screen represents the central operational interface of TrolleyFlow, designed for GateGroup operators and pick-and-packers to monitor and make quick decisions about onboard alcohol supplies.

## Frame 4 – Bottle Scanning

![Imagen de WhatsApp 2025-10-26 a las 06 21 46_56860aea](https://github.com/user-attachments/assets/885750c9-bddc-4820-b58c-b43fd3fd192a)

Explanation:
Each bottle is scanned.
The system identifies whether the bottle should be reused, refilled, or discarded based on its current level and reuse policy.

## Frame 5 – AI Forecasting

![Imagen de WhatsApp 2025-10-26 a las 06 21 46_820beccc](https://github.com/user-attachments/assets/47bf9bca-1554-4914-b6c9-8ef51653a2af)

Explanation:
The system uses the forecasting API to predict upcoming bottle requirements per route and destination.
Reports are generated for future planning and cost optimization. And 

## How to View the Figma Prototype

You can access the interactive Figma prototype here: https://www.figma.com/design/5oBhpS9leX2ZZ81B6QjyXs/Sin-t%C3%ADtulo?node-id=0-1&t=T2QRnGNrupw8Ioq2-1 

## Assumptions

To build the TrolleyFlow system and forecasting logic, several operational and data assumptions were made based on the available information and realistic conditions observed in GateGroup’s processes.

---

### 1. Airline Assignment and Staff Rotation
We assumed that each **Pick-and-packer** is primarily assigned to handle **one or two airline lines** at most.  
Typically, one or two employees are responsible for preparing trolleys for a single airline within an airport.  
However, staff rotation may occur occasionally to help employees gain experience with different airline procedures and policies.

---

### 2. Policy and Destination-Based Decision Rules
In our latest dataset, we defined specific **conditional rules** for bottle-handling decisions:
- If the **destination** is a country with strict alcohol regulations (e.g., **Hong Kong** or the **United States**), the bottle is **automatically discarded**, regardless of its remaining content.  
- Each airline also has defined tolerance thresholds based on the **alcohol percentage remaining** in the bottle.  
  For example, if the leftover content falls below the allowed threshold, the system recommends **reuse or refill**, otherwise **discard**.
- These decision trees assume that airlines are already aware of their **regulatory compliance limits**, and the system automates the decision accordingly.

---

### 3. Class-Based Bottle Distribution
To simulate realistic onboard inventory, we assumed bottle distribution according to **aircraft class segmentation**:
- **First Class (10%)** — includes trolleys with **1-liter wine bottles**.  
- **Business / Premium Economy (20%)** — primarily contains **small spirits bottles** and mixed beverages.  
- **Economy Class (70%)** — standard service area, mainly stocked with miniatures and economy-serving bottles.

This class-based ratio (10%-20%-70%) reflects the typical passenger distribution and directly influences the **forecasting API** when estimating total bottle quantities required per flight.

---

### 4. Pick-and-Packer Operation Assumptions
From a human resource perspective, we assumed that:
- The Pick-and-packer is equipped with a **tablet interface** to operate nearby the trolley.  
- The system allows for **scanning each bottle directly from the tablet**, which then displays the automated action (reuse, discard, refill).  
- The employee has sufficient **training and capacity** to execute this process without assistance.

This setup minimizes physical effort and enables faster, more consistent operations across different flight preparations.

---

### 5. Forecasting and Data Limitations
The forecasting API was developed using **GateGroup’s provided datasets**, which are relatively **small in size**.  
Because the dataset does not qualify as *Big Data*, the machine learning model operates on **limited sample variance**, meaning that:
- The predictive accuracy is not yet fully optimized.  
- The model still provides reliable short-term forecasts based on **historical patterns of bottle usage per flight**.  
- The API is designed to scale as more data becomes available, improving performance over time.

---

**Summary:**  
These assumptions form the foundation for our decision logic, forecasting model, and interface behavior.  
They ensure that TrolleyFlow remains **realistic, scalable, and adaptable** to real-world airline operations.


