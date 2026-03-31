def process_data(data):
    results = []
    seen = set()
    for item in data:
        if item not in seen:
            results.append(item)
            seen.add(item)
    return results

def test_logic():
    assert process_data([1, 2]) == [1, 2]