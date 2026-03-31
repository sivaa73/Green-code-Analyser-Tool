def process_data(data):
    results = []
    # This is an O(n^2) loop - very energy inefficient!
    for item in data:
        for other in data:
            if item == other:
                results.append(item)
    return results

def test_logic():
    # A simple test to make sure the function works
    assert process_data([1, 2]) == [1, 2]