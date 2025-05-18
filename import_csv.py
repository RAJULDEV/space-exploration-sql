import pandas as pd
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="Sid@2004",  # Replace with your password
    database="space_exploration"
)
cursor = conn.cursor()

# Read CSV
df = pd.read_csv(r"C:\Users\swapn\Desktop\space-exploration-sql\Space_Corrected.csv")

# Clean and map data
country_map = {
    "USA": ["Kennedy", "Cape Canaveral", "Vandenberg"],
    "Russia": ["Baikonur", "Plesetsk", "Vostochny"],
    "China": ["Jiuquan", "Xichang", "Taiyuan"],
    "Europe": ["Kourou"],
    "India": ["Sriharikota"],
    "Japan": ["Tanegashima", "Uchinoura"],
    "France": ["Kourou"],
    "Kazakhstan": ["Baikonur"],
    "Israel": ["Palmachim"],
    "Iran": ["Semnan"],
    "New Zealand": ["Mahia"],
    "North Korea": ["Sohae"],
    "South Korea": ["Goheung"],
    "UK": ["Cornwall"],
    "Australia": ["Woomera"],
    "Brazil": ["Alcantara"],
    "Kenya": ["San Marco"],
    "Algeria": ["Reggane"]
}
df["country"] = df["Location"].apply(
    lambda x: next((k for k, v in country_map.items() if any(s in x for s in v)), "Unknown")
)

destination_map = {
    "Moon": ["Moon", "Lunar", "Apollo", "Chang'e", "Luna"],
    "Mars": ["Mars", "Rover", "ExoMars"],
    "Low Earth Orbit": ["Satellite", "Starlink", "ISS", "Vostok", "Shenzhou", "Kosmos"],
    "Deep Space": ["Voyager", "Pioneer"],
    "Asteroid": ["Hayabusa", "OSIRIS-REx"],
    "Venus": ["Venus", "Venera"],
    "Jupiter": ["Galileo", "Juno"],
    "Saturn": ["Cassini"],
    "Mercury": ["Messenger"],
    "Sun": ["Solar", "Helios"]
}
df["destination"] = df["Detail"].apply(
    lambda x: next((k for k, v in destination_map.items() if any(s in x.lower() for s in v)), "Other")
)

df["mission_type"] = df["Detail"].apply(
    lambda x: "Crewed" if any(s in x.lower() for s in ["apollo", "vostok", "shenzhou", "soyuz", "gemini"]) else "Robotic"
)

df["success"] = df["Status Mission"].apply(lambda x: True if x == "Success" else False)

df[" Rocket"] = pd.to_numeric(df[" Rocket"].str.replace(",", "", regex=False), errors="coerce")
df["cost"] = df[" Rocket"].where(df[" Rocket"].notna(), None)

# Insert agencies
agencies = df[["Company Name", "country"]].drop_duplicates().reset_index(drop=True)
for _, row in agencies.iterrows():
    cursor.execute(
        "INSERT INTO agencies (name, country) VALUES (%s, %s)",
        (row["Company Name"], row["country"] if row["country"] != "Unknown" else None)
    )
conn.commit()

# Get agency IDs
cursor.execute("SELECT agency_id, name FROM agencies")
agency_dict = {row[1].strip().lower(): row[0] for row in cursor.fetchall()}

# Insert missions
skipped_rows = 0
for _, row in df.iterrows():
    try:
        launch_date = pd.to_datetime(row["Datum"], errors="coerce", utc=True)
        if pd.isna(launch_date):
            print(f"Skipping row due to invalid date: {row['Detail']}")
            skipped_rows += 1
            continue
        cost_value = None if pd.isna(row["cost"]) else row["cost"]
        company_name = row["Company Name"].strip().lower()
        agency_id = agency_dict.get(company_name)
        if agency_id is None:
            print(f"Skipping row due to missing agency: {row['Company Name']}, Detail: {row['Detail']}")
            skipped_rows += 1
            continue
        cursor.execute(
            """
            INSERT INTO missions (name, launch_date, agency_id, success, destination, mission_type, cost)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                row["Detail"],
                launch_date.strftime("%Y-%m-%d %H:%M:%S"),
                agency_id,
                row["success"],
                row["destination"],
                row["mission_type"],
                cost_value
            )
        )
    except Exception as e:
        print(f"Error inserting row: {row['Detail']}, {e}")
        skipped_rows += 1
conn.commit()

# Verify counts
cursor.execute("SELECT COUNT(*) FROM agencies")
print(f"Agencies inserted: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM missions")
print(f"Missions inserted: {cursor.fetchone()[0]}")
print(f"Rows skipped: {skipped_rows}")

cursor.close()
conn.close()