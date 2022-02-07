from BB84 import getRandomNumbersQuantum

def test_getRandomNumbersQuantum():
    for i in range(1, 102, 10):
        data = getRandomNumbersQuantum(i)
        print(f"{len(data)}: {data}")

test_getRandomNumbersQuantum()
