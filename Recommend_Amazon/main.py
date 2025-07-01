from validate import validator

def main():
    train_path = "File/train_u.data"
    test_path = "File/test_u.data"

    v = validator(train_path, test_path)
    v.validate()

    exact, half, more, mean, std = v.stats()
    print("=== Validation Results ===")
    print(f"Exact match:         {exact}")
    print(f"Off by ≤ 0.5:        {half}")
    print(f"Off by > 0.5:        {more}")
    print(f"Mean absolute error: {mean}")
    print(f"Standard deviation:  {std}")


if __name__ == "__main__":
    main()
