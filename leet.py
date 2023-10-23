
from typing import Optional

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        start = 0
        end = 0
        max_len = 0
        word_set = set()

        while end < len(s):
            if s[end] in word_set:
                word_set.remove(s[start])
                start += 1
            else:
                word_set.add(s[end])
                max_len = max(max_len, end - start + 1)
                end += 1
        
        return max_len
    
    def longestPolindrome(self, s: (str)) -> str:
        start = 0
        index = start
        end = None
        polindrome = ''
        while index < len(s):
            if index == end:
                
            end = index + 1
            if s[index] == s[end]:

                start += 1
                if index == end:

                end -= 1
                



if __name__ == '__main__':
    S = Solution()
    
