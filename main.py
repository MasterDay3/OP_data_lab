
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------
# Завантаження даних
# -------------------------
df = pd.read_csv('dataset.csv')
df['gender'] = df['gender'].str.lower()
df['platform'] = df['platform'].str.capitalize()

# -------------------------
# 1. Розподіл по віку та статі
# -------------------------
def age_category(age):
    if age <= 25:
        return '0-25'
    elif 26 <= age <= 50:
        return '26-50'
    else:
        return '51+'

df['age_group'] = df['age'].apply(age_category)
df['gender_group'] = df['gender']

social_metrics = ['social_media_time_min', 'daily_screen_time_min']
mood_metrics = ['mood_level', 'stress_level', 'anxiety_level', 'sleep_hours', 'physical_activity_min']

def create_table(metrics_list):
    table_data = []
    for age_group in ['0-25', '26-50', '51+']:
        for gender_group in ['male', 'female']:
            subset = df[(df['age_group'] == age_group) & (df['gender_group'] == gender_group)]
            row = {'Category': f'{age_group} - {gender_group}'}
            if not subset.empty:
                for metric in metrics_list:
                    row[metric] = round(subset[metric].mean(), 2)
            else:
                for metric in metrics_list:
                    row[metric] = 0
            table_data.append(row)
    return pd.DataFrame(table_data)

# -------------------------
# Таблиці
# -------------------------
social_table = create_table(social_metrics)
print("\033[31m\n" + "="*100)
print("Соцмережі та екран")
print("="*100)
print(social_table.to_string(index=False))
print("="*100)

mood_table = create_table(mood_metrics)
print("\033[32m\n" + "="*100)
print("Настрій та фізичний/ментальний стан")
print("="*100)
print(mood_table.to_string(index=False))
print("="*100)

interaction_metrics = ['negative_interactions_count', 'positive_interactions_count', 'mood_level']
platform_stats = df.groupby('platform')[interaction_metrics].mean().reset_index()
platform_stats['neg_to_mood_ratio'] = platform_stats['negative_interactions_count'] / platform_stats['mood_level']

sorted_by_neg = platform_stats.sort_values(by='neg_to_mood_ratio', ascending=False)
print("\033[33m\n" + "="*100)
print("Платформи від найбільшого до найменшого негативного впливу")
print("="*100)
print(sorted_by_neg[['platform', 'negative_interactions_count', 'mood_level', 'neg_to_mood_ratio']].to_string(index=False))
print("="*100)

# -------------------------
# Графіки
# -------------------------

# 1. Соцмережі та скрінтайм
social_table.plot(x='Category', y=social_metrics, kind='bar', figsize=(10,6), title='Середній час у соцмережах та скрінтайм по категоріях')
plt.ylabel('Хвилини')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Настрій та фізичний стан
mood_table.plot(x='Category', y=mood_metrics, kind='bar', figsize=(12,6), title='Середній настрій та фізичний стан по категоріях')
plt.ylabel('Значення')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 3. Негативний вплив по платформах
sorted_by_neg.plot(x='platform', y=['negative_interactions_count','neg_to_mood_ratio'], kind='bar', figsize=(10,6), title='Негативні взаємодії та вплив на настрій по платформах')
plt.ylabel('Значення')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
