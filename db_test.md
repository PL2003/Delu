# 📘 Supabase Data Fetching & Verification Master Guide

---

🔰 **Overview**: This guide walks through testing and verifying that your frontend web portal (`web_portal/app.js` or `app_local.js`) properly reads and writes live data to/from your Supabase database.

---

## 📁 Section 1: Pre-Flight Verification Checklist

Before running tests, ensure your Supabase project is seeded and client configuration is active.

### 1. Verification of Required Tables

Ensure these 5 core tables exist in **Supabase Dashboard > Database > Tables**:

* 🔹 `landing_points`
* 🔹 `orders`
* 🔹 `drone_telemetry`
* 🔹 `flight_log`
* 🔹 `drone_commands`

### 2. Confirm Realtime Replication

Navigate to **Database > Replication** and verify that Realtime is explicitly enabled for:

* 📌 `orders`
* 📌 `drone_telemetry`

### 3. Client Configuration (`web_portal/supabase_client.js`)

Confirm your configuration file exports the initialized Supabase client correctly using your Project URL and Anon Key:

```javascript
import { createClient } from '@supabase/supabase-js'

const SUPABASE_URL = 'https://YOUR_PROJECT_ID.supabase.co'
const SUPABASE_ANON_KEY = 'YOUR_ANON_KEY'

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY)

```

---

## 💻 Section 2: Step-by-Step Data Fetching Verification

### Step 1: Seed Initial Landing Points

Your portal needs landing point data to populate maps or drop-down selectors. Run this directly in the **Supabase SQL Editor**:

```sql
-- Seed a test landing point
INSERT INTO landing_points (name, latitude, longitude, aruco_id)
VALUES ('CUET Campus Main Drop', 22.4601, 91.9712, 42)
ON CONFLICT DO NOTHING;

```

🔍 **Syntax Breakdown**:

* `INSERT INTO landing_points`: Specifying target table.
* `VALUES (...)`: Contains coordinates and a unique `aruco_id` used for precision landing.
* `ON CONFLICT DO NOTHING`: Prevents duplicate primary key errors if re-run.

---

### Step 2: Test Direct Browser Querying via Developer Console

Open your web portal in Google Chrome or Firefox, press `F12` to open **Developer Tools**, go to the **Console** tab, and execute:

```javascript
// Test fetching landing points from Supabase client
const { data, error } = await supabase.from('landing_points').select('*');
console.log('Landing Points Data:', data);
console.log('Error Status:', error);

```

🧠 **What Happens Internally**:

* The Supabase JavaScript SDK constructs an HTTPS `GET` request using PostgREST syntax (`/rest/v1/landing_points?select=*`).
* It passes your `SUPABASE_ANON_KEY` in the request header (`apiKey`).
* Supabase checks **Row Level Security (RLS)** policies. If RLS is enabled without read policies, `data` will return empty `[]`.

---

### Step 3: Verify Order Insertion (Write Path)

Test inserting a valid order from the web console to verify schema constraints.

```javascript
// Test order submission
const { data, error } = await supabase
  .from('orders')
  .insert([
    {
      sender_email: 'sender@example.com',
      receiver_email: 'u123@student.cuet.ac.bd',
      receiver_phone: '0100000000',
      pin_code: '1234',
      status: 'PENDING'
    }
  ])
  .select();

console.log('Inserted Order:', data);
console.log('Insertion Error:', error);

```

---

### Step 4: Verify Realtime Telemetry Subscriptions

Since live tracking depends on real-time data streams, verify that client-side websockets are receiving telemetry updates.

Run this script in the browser console to open a WebSocket subscription:

```javascript
// Subscribe to live drone_telemetry table changes
const channel = supabase
  .channel('test-telemetry')
  .on(
    'postgres_changes',
    { event: 'INSERT', schema: 'public', table: 'drone_telemetry' },
    (payload) => {
      console.log('⚡ Realtime Telemetry Received:', payload.new);
    }
  )
  .subscribe((status) => {
    console.log('Subscription Status:', status);
  });

```

To test the stream, execute this dummy insert in the **Supabase SQL Editor**:

```sql
INSERT INTO drone_telemetry (drone_id, latitude, longitude, altitude, battery_voltage)
VALUES ('DRONE-01', 22.4605, 91.9715, 15.4, 12.6);

```

📌 **Expected Outcome**: The browser console immediately logs `⚡ Realtime Telemetry Received:` with the row data.

---

## 🛠️ Section 3: System Testing & Edge Cases

### Schema Constraint Validation (Negative Testing)

Test that invalid status strings are rejected by the database's `valid_status` CHECK constraint.

```javascript
// Should fail due to valid_status CHECK constraint
const { data, error } = await supabase
  .from('orders')
  .insert([
    {
      sender_email: 'test@example.com',
      receiver_email: 'user@example.com',
      receiver_phone: '0100000000',
      pin_code: '1234',
      status: 'NOT_A_REAL_STATUS' // Invalid status
    }
  ]);

console.log('Expected Error:', error);

```

---

## 🧠 Section 4: Architecture Comparison & Cross-References

When making structural database changes, update all system dependencies in parallel:

| Component | File Path | Shared Dependency |
| --- | --- | --- |
| **Database Schema** | `database/schema.sql` | `valid_status` CHECK Constraint |
| **Local Base Station** | `base_station_pc/database/schema_local.sql` | `valid_status` CHECK Constraint |
| **Companion Computer** | `companion_pi/ipc_messages.py` | `MissionStatus` Enum |
| **State Machine** | `companion_pi/process_a_flight.py` | `MissionStateMachine` Transitions |
| **Base Station API** | `base_station_pc/app.py` | `OrderCreate` Pydantic Model |
| **Web Portal UI** | `web_portal/app.js` & `index.html` | Form Payloads & UI Controls |

---

## 📌 Section 5: Diagnostic Pro-Tips

* 💡 **Inspect Network Tab**: Open Browser DevTools > **Network** tab, filter by `Fetch/XHR` or `WS` (WebSocket). Look for requests directed to your Supabase domain to inspect HTTP status codes (e.g., `200 OK`, `401 Unauthorized`, `409 Conflict`).
* 💡 **Check CORS Issues**: If queries fail silently or report network errors, ensure your domain (e.g., `http://localhost:3000`) is listed under **Supabase Dashboard > API Settings > Webhooks / CORS**.
* 💡 **Database Schema Grep**: Whenever modifying column definitions (such as `receiver_phone`), search the repository to keep endpoints and frontend bindings aligned:
```bash
grep -rn "receiver_phone" --include="*.py" --include="*.js" ..

```



---

## 🧠 Memory Hook: The "V-I-S-O-R" Testing Process

Use the **VISOR** acronym to run through database verification steps:

* **V** — **Verify Tables**: Confirm all 5 core tables exist in Supabase.
* **I** — **Insert Seeds**: Populate prerequisite lookup rows like `landing_points`.
* **S** — **Select Query**: Perform client-side `.select()` calls via DevTools console.
* **O** — **Open WebSockets**: Subscribe to Realtime streams for `drone_telemetry`.
* **R** — **Reject Bad Data**: Confirm invalid enum/status inputs trigger database constraints.
