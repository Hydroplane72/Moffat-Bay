# Introduction
 
## 1.1 Purpose
The **Technical Design Document (TDD)** defines the architectural and functional requirements for the **Moffat Bay Lodge Reservation System**.

This document serves as a technical blueprint for the team by detailing terminology, design, user personas, and work estimations.

The primary objective is to deliver a seamless, responsive, and secure web application that enables prospective guests to explore lodge attractions, register customer accounts, check room availability, compare room rates, and manage reservations efficiently.

## 1.2 Terminology
| Terms / Abbreviations | Description |
| ---- | ---- |
| Moffat Bay Lodge | The business and web application entity for which the reservation system is built for. |
| TDD | Technical Design Document - A document detailing software workflows and technical implementation plans. |
| WIP | Work in Process - A DevOps metric limiting active tasks to optimize workflow efficiency and reduce context switching. |

## 1.3 User Personas & 1.4 User Stories
Each user persona is its own file, at least 3 user stories each.

**[Persona 1: Vacation Planner](UserPersona1.md) (`Lucia Collins`)** - 
1. As a vacation planner, I want to explore lodge amenities and island attractions (hiking, kayaking, whale watching) without logging in, so I can evaluate if Moffat Bay fits my family's trip preferences.
2. As a guest planning a trip, I want to view room types, guest capacities, and price rates upfront on the reservation page, so I can select an option that fits my budget.
3. As a busy mother, I want to navigate the Lodge's webpages easily and intuitively, so I don't waste time or grow frustrated at confusing layouts.

**[Persona 2: Returning Guest](UserPersona2.md) (`James Flannel`)** -
1. As a returning guest, I want to log in quickly so that I can access my account without having to create a new profile every time I visit the website..
2. As a returning guest, I want to view my previous reservations so that I can easily reference my past stays and plan future trips.
3. As a returning guest, I want to make a new reservation while logged in so that I can quickly confirm another stay at Moffat Bay Lodge.

**[Persona 3: First-Time Visitor](UserPersona3.md) (`Fulton Brenner`)** -
1. As a first-time visitor, I want to create an account quickly and easily so that I can book a reservation without unnecessary delays.
2. As a first-time visitor, I want to receive confirmation after registering and submitting a reservation so that I know my information was saved successfully.
3. As a first-time visitor, I want to securely log in to my account so that I can access and manage my reservation information.


## 1.5 Work Estimations
These are selected high-priority core user stories from each persona, each broken down into sub-tasks for initial implementation.

### Priority 1: Account Registration (Story 3.1)
- **Assigned Persona:** [Persona 3: First-Time Visitor](UserPersona3.md)
- **Total Estimated Hours:** 14 Hours
1. [ ] Create the website homepage - 2 Hours
2. [ ] Design the lodge information page - 2 Hours
3. [ ] Create the room and pricing page - 2 Hours
4. [ ] Create the island attractions page - 2 Hours
5. [ ] Build the website navigation menu - 1 Hour
6. [ ] Add images and content throughout the website - 2 Hours
7. [ ] Optimize the website for mobile devices - 2 Hours
8. [ ] Test navigation and page functionality - 1 Hour

### Priority 2: Room and Pricing Display (Story 1.2)
- **Assigned Persona:** [Persona 1: Vacation Planner](UserPersona1.md)
- **Total Estimated Hours:** 8 Hours
1. [ ] Design and code responsive CSS grid layout for room options cards - 2 Hours
2. [ ] Build room details by displaying capacity limits, beds, and price rates - 2 Hours
3. [ ] Implement front-end filtering logic to toggle room view by room size - 2 Hours
4. [ ] Wire accurate checkout pricing based on selected nights - 2 Hours

### Priority 3: Place Reservation while logged in (Story 2.3)
- **Assigned Persona:** [Persona 2: Returning Guest](UserPersona2.md)
- **Total Estimated Hours:** 11 Hours
1. [ ] Create the reservation form - 2 Hours
2. [ ] Add form validation - 1 Hour
3. [ ] Verify that the user is logged in before allowing a reservation - 1 Hour
4. [ ] Create the database table for reservations - 1 Hour
5. [ ] Connect the reservation form to the database	- 2 Hours
6. [ ] Add a reservation confirmation button - 1 Hour
7. [ ] Save the reservation to the database	- 1 Hour
8. [ ] Test the reservation process - 2 Hours

#### Remaining User Stories (in priority order)
- **2.1**: Quick User Login
- **3.2**: Reservation Confirmation
- **2.2**: Past Reservation Lookup/History
- **1.1**: View Public Attractions and Amentities
- **3.3**: Mobile Viewport and Responsive UI Design
- **1.3**: UI/UX Navigation Polish

# Design

## 2.1 Prototypes
## 2.2 ERD

# QA Testing
## 3.1 QA Test Plan