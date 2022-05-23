

L = [1,1,1,2]

def CountFrequency(my_list):

    # Creating an empty dictionary
    freq = {}
    for item in my_list:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1

    max_f = max(freq.values())
    return max_f

print(CountFrequency(L))
