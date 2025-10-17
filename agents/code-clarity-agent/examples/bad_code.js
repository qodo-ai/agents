// Bad example with intentional issues

function calc(x, y) { // No docstring, poor names
    // check if y is greater than the threshold
    if (y > 0.15) { // Magic number
        return x * y;
    }
    return x;
}

class DataProcessor {
    constructor(data) {
        this.data = data;
    }

    process() { // No docstring
        let processedData = [];
        for (const item of this.data) {
            let res = calc(item, 0.2); // Magic number
            processedData.push(res);
        }
        return processedData;
    }
}

function main() {
    let d = [1, 2, 3, 4, 5]; // poor name
    let dp = new DataProcessor(d);
    const result = dp.process();
    console.log(result);
}

main();
