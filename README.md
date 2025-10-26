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


### ERD Overview




# Figma Prototype – User Flow (Pick-and-Pack Journey)

The following section presents the visual flow of TrolleyFlow’s Pick-and-pack interface, built in Figma.
Each frame represents a key step in the operator’s interaction.

## Frame 1 – Login & Airline Selection

(Insert screenshot of Frame 1)

![Frame 1 - Login & Airline Selection](https://github.com/yourusername/TrolleyFlow2025/blob/main/assets/figma_frame1.png)


Explanation:
The Pick-and-packer logs into the system and selects their assigned airline.
The interface automatically loads the airline’s policies and assigned flights.

## Frame 2 – Flight Overview & Inventory Load

(Insert screenshot of Frame 2)

![Frame 2 - Flight Overview](https://github.com/yourusername/TrolleyFlow2025/blob/main/assets/figma_frame2.png)


Explanation:
The operator views the upcoming flight list and the expected bottle inventory.
They can confirm quantities and check compliance warnings.

## Frame 3 – Bottle Scanning

(Insert screenshot of Frame 3)

![Frame 3 - Bottle Scanning](https://github.com/yourusername/TrolleyFlow2025/blob/main/assets/figma_frame3.png)


Explanation:
Each bottle is scanned.
The system identifies whether the bottle should be reused, refilled, or discarded based on its current level and reuse policy.

## Frame 4 – AI Decision Suggestion

(Insert screenshot of Frame 4)

![Frame 4 - AI Suggestion](https://github.com/yourusername/TrolleyFlow2025/blob/main/assets/figma_frame4.png)


Explanation:
The AI system provides the recommended action instantly, reducing manual judgment.
Pick-and-packers confirm or override decisions with a single tap.

## Frame 5 – Summary & Sync

(Insert screenshot of Frame 5)

![Frame 5 - Summary](https://github.com/yourusername/TrolleyFlow2025/blob/main/assets/figma_frame5.png)


Explanation:
A summary of actions taken (reuse, discard, refill) is displayed for confirmation.
Data is automatically logged for the airline and GateGroup dashboards.

## Frame 6 – Forecast & Report Generation

(Insert screenshot of Frame 6)

![Frame 6 - Forecast](https://github.com/yourusername/TrolleyFlow2025/blob/main/assets/figma_frame6.png)


Explanation:
The system uses the forecasting API to predict upcoming bottle requirements per route and destination.
Reports are generated for future planning and cost optimization. And 

## How to View the Figma Prototype

You can access the interactive Figma prototype here:



