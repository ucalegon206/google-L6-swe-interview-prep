# Google L6 System Design Protocol: "The Anti-Freeze"

## The Core Philosophy
Google L6 (Staff) interviews are not about "knowing the answer." They are about **NAVIGATING AMBIGUITY**.
If you start drawing immediately, you fail.
If you ask clarifying questions and then draw, you pass.

## Phase 0: The Impulse Control (3 Minutes)
**Trigger:** Recruiter says "Design X."
**Action:** Put the pen down. Do NOT draw a box.
**Script:**
1.  "That's an interesting problem. Before I sketch anything, I want to align on the **functional** and **non-functional** requirements."
2.  **Functional:** "Are we focusing on [Feature A] or [Feature B]?" (e.g., Video Upload vs Video Playback).
3.  **Non-Functional:** "What is the scale? 1M users or 1B users? Is consistency critical (Banking) or is availability critical (Social Media)?"

## Phase 1: The Back-of-Napkin Math (5 Minutes)
**Action:** Write numbers on the whiteboard.
**Script:**
*   "DAU: 100M"
*   "QPS: 100M / 100,000 sec ≈ 1,000 QPS average. Peak is 5x = 5,000 QPS."
*   "Storage: 1KB per write * 100M = 100GB/day = 36TB/year."
*   **Conclusion:** "Okay, 5k QPS is low enough for a standard LB, but 36TB/year means we need sharded storage."

## Phase 2: The "Naive" Diagram (5 Minutes)
**Action:** Draw the simplest *broken* solution.
*   Client -> Load Balancer -> API Service -> Monolithic DB.
*   **Say:** "This is the naive approach. It works for 1k users. It breaks at 1M because [Single Point of Failure / Latency]."

## Phase 3: The "Staff" Optimization (25 Minutes)
**Action:** specific deep dives based on constraints.
*   "Since we need low latency, I'm adding a **Redis Cache** here."
*   "Since we have 40PB of data, I'm sharding the DB by `user_id`."
*   "Since we need global availability, I'm moving the read path to a **CDN**."

## The "Cheat Sheet" for Components
| Constraint | Component to Draw |
|---|---|
| "Too much read traffic" | **Replica DBs + Cache (Redis)** |
| "Too much write traffic" | **Kafka (Buffering) + Cassandra/Dynamo (Write speed)** |
| "Global Latency" | **CDN + Geo-DNS** |
| "Complex Relationships" | **Graph DB (TAO/Neo4j)** |
| "Full Text Search" | **ElasticSearch / Solr** |
| "Analytics/Reporting" | **Data Warehouse (BigQuery/Redshift)** - *Never use Prod DB for analytics!* |

## Practice Prompt
**Design a Rate Limiter.**
*   **Constraints:** 1B requests/hour.
*   **Goal:** Prevent DDoS, protect API.
*   **Twist:** It must be distributed (multiple servers).

*Go.*
