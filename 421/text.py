ages = {
    'Matt': 30,
    'Katie': 29,
    'Nik': 31,
    'Jack': 43,
    'Alison': 32,
    'Kevin': 38
}

max_value = max(ages, key=ages.get)
print(max_value)