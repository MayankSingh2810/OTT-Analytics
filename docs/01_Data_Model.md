# OTT Stream Intelligence Platform

## Enterprise Data Model

### 1. content.csv

Master catalogue of all movies and TV shows available on the platform.

Primary Key:

* content_id

Referenced By:

* watch_history.csv
* ratings.csv

---

### 2. users.csv

Stores customer demographic and account information.

Primary Key:

* user_id

Referenced By:

* subscriptions.csv
* sessions.csv
* watch_history.csv
* ratings.csv
* search_history.csv

---

### 3. subscription_plans.csv

Defines available subscription plans.

Primary Key:

* plan_id

Referenced By:

* subscriptions.csv

---

### 4. subscriptions.csv

Stores each customer's subscription details.

Foreign Keys:

* user_id
* plan_id

---

### 5. watch_history.csv

Stores every viewing event.

Foreign Keys:

* user_id
* content_id

---

### 6. ratings.csv

Stores movie ratings.

Foreign Keys:

* user_id
* content_id

---

### 7. sessions.csv

Stores application login sessions.

Foreign Key:

* user_id

---

### 8. search_history.csv

Stores every search performed.

Foreign Key:

* user_id
