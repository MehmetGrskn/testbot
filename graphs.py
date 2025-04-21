import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import folium
from folium.plugins import MarkerCluster
import os

# Klasör adı
output_folder = 'Bitirme/grafikler'

# Klasörün var olup olmadığını kontrol et, yoksa oluştur
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Excel dosyasını yükleyelim
df = pd.read_excel('datalar\\temizlenmiş-datalar.xlsx')

# Grafik ayarları
sns.set(style="whitegrid")
plt.figure(figsize=(12, 8))


# 'Flag Administrations' sütunundaki ülkelere göre kaç olay olduğuna bakalım
country_counts = df['Flag Administrations'].value_counts().reset_index()
country_counts.columns = ['Country', 'Count']

# Harita çizimi
fig = px.choropleth(
    country_counts,
    locations='Country',
    locationmode='country names',
    color='Count',
    color_continuous_scale='YlOrRd',
    title='Casualties by Flag Administration (Country)'
)

# HTML olarak kaydet
fig.write_html(os.path.join(output_folder, 'casualties_by_flag_administration.html'))
print(f"Harita kaydedildi: {os.path.join(output_folder, 'casualties_by_flag_administration.html')}")


# 6. Casualty Event - Donut chart
casualty_event_count = df['Casualty event'].value_counts()

# Küçük değerleri grupla (isteğe bağlı)
threshold = 0.03  # %3 altındaki değerler "Other" olacak
total = casualty_event_count.sum()
filtered_counts = casualty_event_count[casualty_event_count / total >= threshold]
others_count = total - filtered_counts.sum()
if others_count > 0:
    filtered_counts['Other'] = others_count

plt.figure(figsize=(12, 12  ))
plt.pie(filtered_counts, labels=filtered_counts.index, autopct='%1.1f%%', startangle=90, wedgeprops=dict(width=0.4))
plt.title('Casualty Event Distribution (Donut Style)')
plt.savefig(os.path.join(output_folder, 'casualty_event_distribution_donut.png'))
plt.close()

# 2. Ships involved - Count plot (Ship type)
plt.figure(figsize=(20, 20))
sns.countplot(data=df, x='Ship types', order=df['Ship types'].value_counts().index)
plt.title('Ships Involved Count by Type')
plt.xlabel('Ship Type')
plt.ylabel('Count')
plt.xticks(rotation=90)
plt.savefig(os.path.join(output_folder, 'ships_involved_count_by_type.png'))
plt.close()

# 3. SOLAS status - Pie chart
solas_status_count = df['SOLAS status'].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(solas_status_count, labels=solas_status_count.index, autopct='%1.1f%%', startangle=90)
plt.title('SOLAS Status Distribution')
plt.savefig(os.path.join(output_folder, 'solas_status_distribution.png'))
plt.close()

# 4. Flag Administrations - Bar plot
plt.figure(figsize=(20, 20))
sns.countplot(data=df, x='Flag Administrations', order=df['Flag Administrations'].value_counts().index)
plt.title('Flag Administrations Count')
plt.xlabel('Flag Administration')
plt.ylabel('Count')
plt.xticks(rotation=90)
plt.savefig(os.path.join(output_folder, 'flag_administrations_count.png'))
plt.close()

# 5. Occurrence Date and Time - Time series plot
df['Occurrence date and time'] = pd.to_datetime(df['Occurrence date and time'])
df['Month'] = df['Occurrence date and time'].dt.month
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='Month', palette='viridis')
plt.title('Number of Casualties by Month')
plt.xlabel('Month')
plt.ylabel('Casualty Count')
plt.xticks(ticks=range(12), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.savefig(os.path.join(output_folder, 'casualties_by_month.png'))
plt.close()



# 7. Casualty Severity - Bar plot
plt.figure(figsize=(8, 6))
sns.countplot(data=df, x='Casualty severity', order=df['Casualty severity'].value_counts().index)
plt.title('Casualty Severity Distribution')
plt.xlabel('Casualty Severity')
plt.ylabel('Count')
plt.savefig(os.path.join(output_folder, 'casualty_severity_distribution.png'))
plt.close()

# 8. Coordinates - Map visualization
map_center = [df['Coordinates'].mean(), df['Coordinates'].mean()]  # Ortalama koordinatlar
map = folium.Map(location=map_center, zoom_start=6)
marker_cluster = MarkerCluster().add_to(map)

# Koordinatlar için map işaretçileri ekleyelim (bu kısım verinize göre uyarlanabilir)
for idx, row in df.iterrows():
    coordinates = row['Coordinates']
    if pd.notnull(coordinates):
        lat, lon = map(float, coordinates.split(','))
        folium.Marker([lat, lon]).add_to(marker_cluster)

# Haritayı kaydetme
map.save(os.path.join(output_folder, 'casualties_map.html'))

# 9. Number of Investigation Reports - Bar plot
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='Number of investigation reports')
plt.title('Number of Investigation Reports')
plt.xlabel('Number of Reports')
plt.ylabel('Count')
plt.savefig(os.path.join(output_folder, 'number_of_investigation_reports.png'))
plt.close()

# 10. Administrations Submitting Investigation Reports - Bar plot
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='Administrations submitting investigation reports', order=df['Administrations submitting investigation reports'].value_counts().index)
plt.title('Administrations Submitting Investigation Reports')
plt.xlabel('Administration')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.savefig(os.path.join(output_folder, 'administrations_submitting_investigation_reports.png'))
plt.close()

# 11. Casualties by year - Line plot
plt.figure(figsize=(10, 10))
df['Year'] = df['Occurrence date and time'].dt.year
sns.countplot(data=df, x='Year', order=df['Year'].value_counts().index)
plt.title('Casualties by Year')
plt.xlabel('Year')
plt.ylabel('Count')
plt.xticks(rotation=90)
plt.savefig(os.path.join(output_folder, 'casualties_by_year.png'))
plt.close()


