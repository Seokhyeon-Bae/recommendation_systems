# The code will calculate the simliarity between the users and the predicted popularity of each movies based on simliar users.
from validate import validator 

def main():
    train_path = "File/train_u.data"
    test_path = "File/test_u.data"

    v = validator(train_path, test_path)
    v.validate()

    exact, off_by_one, off_by_more, mean, std = v.stats()
    print("=== Validation Results ===")
    print(f"Exact match:         {exact}")
    print(f"Off by 1:            {off_by_one}")
    print(f"Off by > 1:          {off_by_more}")
    print(f"Mean absolute error: {mean}")
    print(f"Standard deviation:  {std}")
    
if __name__ == "__main__":
    main()
