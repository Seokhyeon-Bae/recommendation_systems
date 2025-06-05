from validate import validator
import matplotlib.pyplot as plt

def main():
    train_path = "File/train_u.data"
    test_path = "File/test_u.data"

    # Initialize and run validator
    v = validator(train_path, test_path)
    v.validate()

    # Get and print stats
    exact, half, more, mean, std = v.stats()
    print("=== Validation Results ===")
    print(f"Exact match:         {exact}")
    print(f"Off by ≤ 0.5:        {half}")
    print(f"Off by > 0.5:        {more}")
    print(f"Mean absolute error: {mean}")
    print(f"Standard deviation:  {std}")

    # Optional: plot error distribution
    plt.hist(v.prediction, bins=20, edgecolor='black')
    plt.title("Prediction Error Distribution")
    plt.xlabel("Absolute Error")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
