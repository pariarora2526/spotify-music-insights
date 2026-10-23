
from data_utils import load_tracks, get_data_quality_report

df = load_tracks()

print("CLEANED DATASET")
print("=" * 40)

print("Dataset shape:", df.shape)
print("Columns:", df.columns.tolist())
print("\nFirst 5 tracks:")
print(df.head())

print("\nDATA QUALITY REPORT")
print("=" * 40)

report = get_data_quality_report(df)

for key, value in report.items():
    print(f"\n{key}:")
    print(value)
