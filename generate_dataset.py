"""
generate_dataset.py
--------------------
Generates a synthetic (simulated) student admission dataset for model
training. A real-world admission dataset of this kind is not publicly
available, so realistic value ranges are sampled instead, based on
typical academic score distributions and reservation policies.

Run this once to produce admission_data.csv.
"""

import numpy as np
import pandas as pd

np.random.seed(42)

NUM_STUDENTS = 2000

tenth_percent = np.random.normal(75, 10, NUM_STUDENTS).clip(40, 100)
twelfth_percent = np.random.normal(72, 10, NUM_STUDENTS).clip(40, 100)
entrance_score = np.random.normal(150, 30, NUM_STUDENTS).clip(0, 300)
category = np.random.choice(['General', 'OBC', 'SC', 'ST'], NUM_STUDENTS, p=[0.5, 0.3, 0.15, 0.05])
previous_year_cutoff = np.random.normal(140, 20, NUM_STUDENTS).clip(50, 250)

avg_academic_score = (tenth_percent + twelfth_percent) / 2
score_gap_from_cutoff = entrance_score - previous_year_cutoff

relaxation_map = {'General': 0, 'OBC': 10, 'SC': 20, 'ST': 25}
relaxation_values = np.array([relaxation_map[c] for c in category])
effective_gap = score_gap_from_cutoff + relaxation_values

probability = 1 / (1 + np.exp(-effective_gap / 15))
admitted = (np.random.rand(NUM_STUDENTS) < probability).astype(int)

df = pd.DataFrame({
    'tenth_percent': tenth_percent.round(2),
    'twelfth_percent': twelfth_percent.round(2),
    'entrance_score': entrance_score.round(2),
    'category': category,
    'previous_year_cutoff': previous_year_cutoff.round(2),
    'avg_academic_score': avg_academic_score.round(2),
    'score_gap_from_cutoff': score_gap_from_cutoff.round(2),
    'admitted': admitted
})

df.to_csv('admission_data.csv', index=False)
print(f"Dataset generated: {NUM_STUDENTS} records saved to 'admission_data.csv'.")
print(f"Admitted: {admitted.sum()} | Not admitted: {NUM_STUDENTS - admitted.sum()}")
