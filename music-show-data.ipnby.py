import pandas as pd
import numpy as np

# 1. Initialize dataset seed and records count
np.random.seed(42)
n = 5000

# 2. Map structural metrics for Indian music markets
festival_brands = ['Sunburn Festival', 'NH7 Weekender', 'Lollapalooza India', 'Ziro Festival of Music', 
                   'Mahindra Blues Festival', 'Bangalore Open Air', 'Magnetic Fields Festival', 'Hornbill Rock Contest']
artists = ['A.R. Rahman', 'Diljit Dosanjh', 'Arijit Singh', 'Seedhe Maut', 'Anuv Jain', 
           'Prateek Kuhad', 'Nucleya', 'Hanumankind', 'Divine', 'Shreya Ghoshal']
genres = ['Bollywood/Sufi', 'Punjabi Pop', 'Bollywood Romance', 'Desi Hip-Hop', 'Indie Pop', 
          'Indie Folk', 'EDM/Electronica', 'Global Hip-Hop', 'Gully Rap', 'Indian Classical']
cities = ['Mumbai', 'Delhi-NCR', 'Bengaluru', 'Pune', 'Goa', 'Hyderabad', 'Kolkata', 'Ziro Valley', 'Kohima', 'Jodhpur']
venues = ['Mahalaxmi Racecourse', 'JLN Stadium', 'NICE Grounds', 'Mahalakshmi Lawns', 'Vagator Beach Arena', 
          'Gachibowli Stadium', 'Eco Park', 'Ziro Festival Ground', 'Kisama Heritage Village', 'Mehrangarh Fort']

artist_genre_map = dict(zip(artists, genres))
city_venue_map = dict(zip(cities, venues))

rand_artists = np.random.choice(artists, size=n, p=[0.15, 0.15, 0.15, 0.10, 0.08, 0.07, 0.08, 0.08, 0.08, 0.06])
rand_cities = np.random.choice(cities, size=n, p=[0.18, 0.15, 0.15, 0.10, 0.12, 0.08, 0.07, 0.05, 0.05, 0.05])

# 3. Assemble structural base dataframe
getdata = pd.DataFrame({
    'booking_id': [f"IND-SHOW-{30000 + i}" for i in range(n)],
    'event_name': np.random.choice(festival_brands, size=n) + " Tour Edition",
    'headline_artist': rand_artists,
    'music_genre': [artist_genre_map[a] for a in rand_artists],
    'city': rand_cities,
    'venue': [city_venue_map[c] for c in rand_cities],
    'event_date': np.random.choice(pd.date_range('2018-01-01', '2026-05-01').astype(str), size=n),
    'ticket_capacity': np.random.randint(5000, 45000, size=n),
    'tickets_sold': np.random.randint(4000, 50000, size=n),  # Intentionally includes logical capacity overflow anomalies
    'average_ticket_price_inr': np.round(np.random.uniform(999.0, 12500.0, size=n), 2),
    'customer_satisfaction_score': np.round(np.random.uniform(3.2, 10.0, size=n), 1)
})

# 4. Inject explicit cleaning challenges (Missing arrays, negative numbers, corrupted timestamps)
getdata.loc[np.random.choice(n, 200, replace=False), 'music_genre'] = np.nan
getdata.loc[np.random.choice(n, 120, replace=False), 'average_ticket_price_inr'] = -500.0  
getdata.loc[np.random.choice(n, 150, replace=False), 'customer_satisfaction_score'] = 0.0   

# Inject messy date-strings
corrupted_dates = np.random.choice(n, 250, replace=False)
getdata.loc[corrupted_dates, 'event_date'] = "DATE_MISMATCH_" + getdata.loc[corrupted_dates, 'event_date']

# Add duplicate entries to test deduplication (.drop_duplicates())
duplicates = getdata.sample(n=45, random_state=42)
getdata = pd.concat([getdata, duplicates], ignore_index=True)

# 5. Export dataset locally
getdata.to_csv("india_music_shows_dirty_5000.csv", index=False)
print("File successfully generated and saved as 'india_music_shows_dirty_5000.csv'!")
print(f"Total Rows generated (including duplicates): {getdata.shape[0]}")
