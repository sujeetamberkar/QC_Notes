def MaxSum(N):
    # Create a list to store the maximum score for each node.
    max_score = [0] * (2 * N + 1)
    
    # Iterate through the nodes from -N to N.
    for a in range(-N, N + 1):
        max_score[abs(a)] = abs(a)  # Initialize the score for each node as its absolute value.
        
        # Iterate through possible values of x.
        for x in range(2, N // abs(a) + 1):
            b = a * x  # Calculate the target node 'b'.
            
            # Update the maximum score for 'b' using the current 'a'.
            max_score[abs(b)] = max(max_score[abs(b)], max_score[abs(a)] + abs(x))
    
    # Find the maximum score from all nodes.
    max_sum = max(max_score)
    
    return max_sum

# Input number of test cases.
T = int(input())

# Process each test case.
for _ in range(T):
    N = int(input())
    result = MaxSum(N)
    print(result)
