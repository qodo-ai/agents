# Bad example with intentional issues

def calc(x, y): # No docstring, poor names
    # check if y is greater than the threshold
    if y > 0.15: # Magic number
        return x * y
    return x

class DataProcessor:
    def __init__(self, data):
        self.data = data

    def process(self): # No docstring
        processed_data = []
        for item in self.data:
            res = calc(item, 0.2) # Magic number
            processed_data.append(res)
        return processed_data

def main():
    d = [1, 2, 3, 4, 5] # poor name
    dp = DataProcessor(d)
    result = dp.process()
    print(result)

if __name__ == "__main__":
    main()
