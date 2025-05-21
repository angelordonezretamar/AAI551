"""
QUESTION 1:
========================================================================================================
Given a list of numbers, write a function to find the maximum number in the list.
Do Not Use the built-in Python function max.
Note: For the purpose of this problem, we define that an empty list will return None.

NOTE: DO NOT USE THE PYTHON FUNCTION max. WRITE your program using a loop. 

Example 1:
========================================
Input: [10, 5, 20, 15, 25]
Output: 25

Example 2:
========================================
Input:[10,10,10]
Output: 10

Example 3:
========================================
Input: []
Output: None
"""

def find_maximum(numbers):
    """
    Takes a list of numbers and returns the max, without using the built-in Python function max
    """
    if not numbers: #base case: empty list
        return None
    
    Max_Number = numbers[0] #start by assuming the first number is the max
    for num in numbers[1:]: #iterate through the list
        if num > Max_Number: #check if the next number is bigger
            Max_Number = num #if so make it the new max
    return Max_Number
    
    


"""
QUESTION 2: 
========================================================================================================
Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.
Write a function named generateParenthesis that takes an integer as an input and returns a list of strings 
as an output. Note that you can define a function inside a function if necessary.

Example 1:
========================================
Input: 0
Output: ['']

Example 2:
========================================
Input: 1
Output: ['()']

Example 3:
========================================
Input: 2
Output: ['(())', '()()']

Example 4:
========================================
Input: 3
Output: ['((()))', '(()())', '(())()', '()(())', '()()()'])
"""

def generateParenthesis(n):
    """
    generates all combinations of well-formed parenthesis given n pairs of parenthesis
    """
    def backtracking(s, left, right):
        """
        function within the function for recursion,
        checks if there is room for left or right parenthesis and adds them
        backtracks a final time to generate the combos
        """
        if len(s) == 2 * n: #base case
            result.append(s) #add s to result since we used exactly n pairs
            return
        if left < n: #if we can add another (, add it then recursion
            backtracking(s + "(", left + 1, right)
        if right < left: #if we can add another ), do it and recursion
            backtracking(s + ")", left, right + 1)

    result = [] #the list to store the valid combos
    backtracking("", 0, 0) #start backtracking with an empty string and no parentheses
    return result


"""
QUESTION 3: 
========================================================================================================
Given a string, determine if it is a palindrome, considering only alphanumeric characters and ignoring cases.
Note: For the purpose of this problem, we define empty string as valid palindrome. Write a function
named isPalindrome that takes a string as an input and returns a bool as an output.

Hint: refer to the following example on how to reverse a string.

>>> S = "abc"
>>> S[::-1]
'cba'


Example 1:
========================================
Input: "A man, a plan, a canal: Panama"
Output: true

Explanation:
After removing non-alphanumeric charactors and ignoring cases, the input is:  amanaplanacanalPanama
which reads the same as backward and forward, so it is true.

Example 2:
=========================================
Input: "race a car"
Output: false

Explanation:
After removing non-alphanumeric charactors and ignoring cases, the input is:  raceacar
which does not read the same as backward and forward, so it is false.
"""

def isPalindrome(x):
    """
    determines if a given string is a palindrome
    """
    def checker(left, right):
        """
        function within the function for recursion, 
        moves pointers in from left and right, skips non-alphanumeric chars,
        checks if they are a match or not
        """
        if left >= right: #base case: if the left index meets or crosses the right index, its a palindrome
            return True
        while left < right and not x[left].isalnum(): #skip the non-alphanumeric chars from the left
            left += 1
        while left < right and not x[right].isalnum(): #skip the non-alphanumeric chars from the right
            right -= 1
        if x[left].lower() != x[right].lower(): #if the chars at left and right don't match its not a palindrome
            return False
        return checker(left + 1, right - 1) #move the pointers inward and keep checking

    return checker(0, len(x) - 1) #starts checking from the beginning and end of the string

    